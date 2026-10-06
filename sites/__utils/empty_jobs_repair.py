#
#  Auto-repair for scrapers that return an empty jobs list.
#  ... verifies the company source website before declaring a scraper "done"
#
import calendar
import inspect
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path


HELPER_DIR = Path(__file__).resolve().parent
SITES_DIR = HELPER_DIR.parent
REPO_ROOT = SITES_DIR.parent

STATE_PATH = REPO_ROOT / ".cache" / "empty_jobs_repair_state.json"
BUDGET_PATH = REPO_ROOT / ".cache" / "repair_daily_budget.json"
NO_JOBS_MARKER = "[NO JOBS]"

MAX_LOG_LENGTH = 4000
REPAIR_TIMEOUT_SECONDS = int(os.getenv("OPENCODE_REPAIR_TIMEOUT", "900"))
COOLDOWN_DAYS = int(os.getenv("OPENCODE_EMPTY_JOBS_REPAIR_COOLDOWN_DAYS", "7"))

# cel mult BASE_DAILY_BUDGET reparari pe zi; daca nu incap toate scraperele
# intr-o luna la acest ritm, bugetul creste automat la total / zile_in_luna
BASE_DAILY_BUDGET = int(os.getenv("OPENCODE_EMPTY_JOBS_REPAIR_DAILY_BUDGET", "10"))

ATTEMPT_ENV = "OPENCODE_EMPTY_JOBS_REPAIR_ATTEMPTED"
DEPTH_ENV = "OPENCODE_EMPTY_JOBS_REPAIR_DEPTH"
DISABLED_ENV = "OPENCODE_EMPTY_JOBS_REPAIR_DISABLED"
MAX_REPAIR_DEPTH = 1

RUNNER_NAMES = {"__main_RunnerFile.py", "main.py"}


def utc_now():
    return datetime.now(timezone.utc)


def format_timestamp(value):
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_timestamp(value):
    if not value:
        return None

    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def truncate_output(content, limit=MAX_LOG_LENGTH):
    if not content:
        return "No output captured."

    content = content.strip()
    if len(content) <= limit:
        return content

    return content[:limit] + "\n...[truncated]"


def count_scrapers():
    """
    ... totalul de scrapere care ruleaza prin runner (*_scraper.py)
    """
    return len([path for path in SITES_DIR.glob("*.py") if path.name.endswith("_scraper.py")])


def get_daily_budget():
    """
    ... cate reparari pot fi facute intr-o zi.

    De regula BASE_DAILY_BUDGET. Daca toate scraperele nu incap in luna curenta la
    acest ritm (total > buget * zile_in_luna), bugetul creste automat ca sa fie
    acoperite intr-o singura luna.
    """
    total = count_scrapers()
    today = utc_now()
    days_in_month = calendar.monthrange(today.year, today.month)[1]

    if total <= BASE_DAILY_BUDGET * days_in_month:
        return BASE_DAILY_BUDGET

    return math.ceil(total / days_in_month)


def load_daily_budget():
    """
    ... bugetul zilei curente; se reseteaza automat la schimbarea datei (UTC)
    """
    today_key = utc_now().strftime("%Y-%m-%d")

    if not BUDGET_PATH.exists():
        return {"date": today_key, "used": 0}

    try:
        with BUDGET_PATH.open("r", encoding="utf-8") as budget_file:
            budget = json.load(budget_file)
    except (OSError, json.JSONDecodeError):
        budget = {}

    if not isinstance(budget, dict) or budget.get("date") != today_key:
        return {"date": today_key, "used": 0}

    try:
        used = int(budget.get("used", 0))
    except (TypeError, ValueError):
        used = 0

    return {"date": today_key, "used": max(used, 0)}


def save_daily_budget(budget):
    BUDGET_PATH.parent.mkdir(parents=True, exist_ok=True)
    with BUDGET_PATH.open("w", encoding="utf-8") as budget_file:
        json.dump(budget, budget_file, indent=2, sort_keys=True)


def consume_daily_budget():
    """
    ... rezerva un loc in bugetul zilei; False daca bugetul s-a epuizat
    """
    budget = load_daily_budget()
    daily_limit = get_daily_budget()

    if budget["used"] >= daily_limit:
        return False

    budget["used"] += 1
    save_daily_budget(budget)
    return True


def get_remaining_daily_budget():
    budget = load_daily_budget()
    return max(get_daily_budget() - budget["used"], 0)


def get_state_key(script_path):
    try:
        return str(script_path.relative_to(REPO_ROOT))
    except ValueError:
        return str(script_path)


def load_state():
    if not STATE_PATH.exists():
        return {}

    try:
        with STATE_PATH.open("r", encoding="utf-8") as state_file:
            data = json.load(state_file)
            return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with STATE_PATH.open("w", encoding="utf-8") as state_file:
        json.dump(state, state_file, indent=2, sort_keys=True)


def update_state(script_path, company, **fields):
    state = load_state()
    key = get_state_key(script_path)
    entry = state.get(key, {})
    entry["company"] = company

    for field_name, value in fields.items():
        if value is not None:
            entry[field_name] = value

    state[key] = entry
    save_state(state)


def clear_state(script_path):
    state = load_state()
    key = get_state_key(script_path)

    if key not in state:
        return

    state.pop(key, None)
    if state:
        save_state(state)
    else:
        STATE_PATH.unlink(missing_ok=True)


def get_cooldown_until(script_path):
    state = load_state()
    entry = state.get(get_state_key(script_path))

    if not isinstance(entry, dict):
        return None

    confirmed_empty_at = parse_timestamp(entry.get("last_confirmed_empty_at"))
    if confirmed_empty_at is None:
        return None

    return confirmed_empty_at + timedelta(days=COOLDOWN_DAYS)


def is_cooldown_active(script_path):
    cooldown_until = get_cooldown_until(script_path)
    return bool(cooldown_until and utc_now() < cooldown_until)


def get_repair_backlog(limit=None):
    """
    ... scraperele din cache care asteapta reparare: au returnat lista goala si
    cooldown-ul lor a expirat (sau nu au apucat sa fie reparate deloc).

    Ordine: cele mai vechi primele, ca sa nu ramana vreuna uitata.
    """
    state = load_state()
    due = []

    for state_key, entry in sorted(state.items()):
        if not isinstance(entry, dict):
            continue

        script_path = REPO_ROOT / state_key
        if not script_path.is_file() or is_cooldown_active(script_path):
            continue

        due.append((state_key, entry, script_path))

    due.sort(key=lambda item: str(item[1].get("last_empty_at") or ""))

    if limit is not None:
        due = due[:limit]

    return [(state_key, entry.get("company") or state_key, script_path)
            for state_key, entry, script_path in due]


def infer_company_name(module_globals, script_path):
    for key in ("company_name", "company", "COMPANY"):
        value = module_globals.get(key)
        if isinstance(value, dict):
            value = value.get("company")
        if isinstance(value, str) and value.strip():
            return value.strip()

    return script_path.stem.replace("_scraper", "")


def _is_internal_frame(frame_path):
    return frame_path.parent == HELPER_DIR or frame_path.name in RUNNER_NAMES


def get_calling_scraper_context():
    current_file = Path(__file__).resolve()
    main_module = sys.modules.get("__main__")
    main_file = getattr(main_module, "__file__", None)

    if main_file:
        main_path = Path(main_file).resolve()
        if (
            main_path != current_file
            and main_path.suffix == ".py"
            and not _is_internal_frame(main_path)
        ):
            return main_path, infer_company_name(main_module.__dict__, main_path)

    frame = inspect.currentframe()
    if frame is None:
        return None, None

    selected_context = None

    try:
        caller = frame.f_back
        while caller:
            caller_path = Path(caller.f_code.co_filename).resolve()
            if caller_path != current_file and caller_path.suffix == ".py":
                if _is_internal_frame(caller_path):
                    caller = caller.f_back
                    continue

                company = infer_company_name(caller.f_globals, caller_path)
                if caller.f_globals.get("__name__") == "__main__":
                    return caller_path, company

                if selected_context is None:
                    selected_context = (caller_path, company)
            caller = caller.f_back
    finally:
        del frame

    if selected_context is not None:
        return selected_context

    return None, None


def repair_scraper_with_opencode(script_path, company):
    if shutil.which("opencode") is None:
        print(f"OpenCode is not installed. Cannot auto-repair {script_path.name}.")
        return False

    prompt = (
        f"Fix the scraper `{get_state_key(script_path)}`. "
        f"It exits successfully but returns an empty jobs list for company `{company}`. "
        "Check the company's source website, repair the scraper if jobs still exist there, "
        "and rerun the scraper until it no longer returns an empty list unless the company "
        "truly has no jobs left on the source website."
    )
    repair_context = f"""
Scraper: {get_state_key(script_path)}
Run command: {sys.executable} {get_state_key(script_path)}

Requirements:
- Fix only what is needed for this scraper to return the real jobs.
- Preserve the existing scraper behavior and output schema.
- Scraper files live in `sites/` and import shared helpers from the `__utils` package.
- The company name is passed to `UpdateAPI().update_jobs(company_name, jobs)`.
- Re-run the scraper after your fix and stop only when it exits successfully.
- Do not leave any extra files next to the scraper.

Observed behavior:
- The scraper returned an empty jobs list and printed `{NO_JOBS_MARKER} {company}`.
- Company detected from scraper: {company}
- You must verify the source website directly, not peviitor search results.
""".strip()
    context_file_path = None

    try:
        print(f"Starting OpenCode empty-jobs repair for {script_path.name}...")

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix="_opencode_empty_jobs_context.md",
            delete=False,
            encoding="utf-8",
        ) as context_file:
            context_file.write(repair_context)
            context_file_path = context_file.name

        # agentul ruleaza el insusi scraperul ca sa-si verifice repararea; fara
        # guard, acel run ar porni inca un opencode run, la infinit
        repair_env = os.environ.copy()
        repair_env[ATTEMPT_ENV] = "1"
        repair_env[DEPTH_ENV] = str(int(os.getenv(DEPTH_ENV, "0")) + 1)

        action = subprocess.run(
            [
                "opencode",
                "run",
                "--dir",
                str(REPO_ROOT),
                "-f",
                str(script_path),
                "-f",
                context_file_path,
                "--",
                prompt,
            ],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            env=repair_env,
            timeout=REPAIR_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(f"OpenCode empty-jobs repair timed out for {script_path.name}.")
        return False
    finally:
        if context_file_path and os.path.exists(context_file_path):
            os.unlink(context_file_path)

    if action.returncode != 0:
        print(f"OpenCode could not repair {script_path.name}.")
        print(truncate_output(action.stderr or action.stdout))
        return False

    print(f"OpenCode empty-jobs repair finished for {script_path.name}.")
    return True


def snapshot_sibling_files(script_path):
    return {
        path.name
        for path in script_path.parent.iterdir()
        if path.is_file() or path.is_symlink()
    }


def cleanup_created_sibling_files(script_path, existing_files):
    for file_name in sorted(snapshot_sibling_files(script_path) - existing_files):
        created_file = script_path.parent / file_name
        if created_file == script_path:
            continue

        created_file.unlink(missing_ok=True)
        print(f"Deleted extra file {created_file.name}")


def rerun_repaired_scraper(script_path):
    env = os.environ.copy()
    env[ATTEMPT_ENV] = "1"

    print(f"Re-running repaired scraper {script_path.name}...")
    action = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env=env,
    )

    if action.stdout:
        print(action.stdout, end="" if action.stdout.endswith("\n") else "\n")
    if action.stderr:
        print(action.stderr, end="" if action.stderr.endswith("\n") else "\n")

    if action.returncode != 0:
        raise Exception(
            "Auto-repair rerun failed:\n" + truncate_output(action.stderr or action.stdout)
        )

    return NO_JOBS_MARKER in (action.stdout or "") or NO_JOBS_MARKER in (action.stderr or "")


def clear_cooldown_for_calling_scraper():
    script_path, _ = get_calling_scraper_context()
    if script_path:
        clear_state(script_path)


def maybe_repair_empty_jobs_output(company_name):
    if os.getenv(ATTEMPT_ENV) == "1":
        print("Empty-jobs auto-repair already attempted for this run.", flush=True)
        return False

    depth = int(os.getenv(DEPTH_ENV, "0"))
    if depth >= MAX_REPAIR_DEPTH:
        print(
            f"Empty-jobs auto-repair skipped at nesting depth {depth} "
            f"(max {MAX_REPAIR_DEPTH}) to avoid an opencode/scraper loop.",
            flush=True,
        )
        return False

    script_path, detected_company = get_calling_scraper_context()
    if not script_path:
        print("Could not detect scraper context for empty-jobs verification.", flush=True)
        return False

    company = company_name or detected_company

    # modul detectie: rularea principala doar depisteaza si scrie scraperul in
    # cache, fara sa consume din bugetul zilnic de reparatii (10/zi) rezervat
    # rularii repair_empty_jobs.yml
    if os.getenv(DISABLED_ENV) == "1":
        update_state(script_path, company, last_empty_at=format_timestamp(utc_now()))
        print(
            f"No jobs returned for {company}. {script_path.name} recorded in the "
            f"empty-jobs cache; repair is disabled for this run.",
            flush=True,
        )
        return False

    if is_cooldown_active(script_path):
        update_state(script_path, company, last_empty_at=format_timestamp(utc_now()))
        print(
            f"No jobs returned for {company}. Empty-jobs auto-repair is on cooldown for "
            f"{script_path.name} until {format_timestamp(get_cooldown_until(script_path))}.",
            flush=True,
        )
        return False

    if not consume_daily_budget():
        update_state(script_path, company, last_empty_at=format_timestamp(utc_now()))
        print(
            f"No jobs returned for {company}. Daily repair budget reached "
            f"({get_daily_budget()}/day); {script_path.name} is queued for a later day "
            f"({get_remaining_daily_budget()} repair(s) left today).",
            flush=True,
        )
        return False

    print(
        f"No jobs returned for {company}. Starting direct source verification and repair for "
        f"{script_path.name}...",
        flush=True,
    )

    attempted_at = format_timestamp(utc_now())
    update_state(
        script_path,
        company,
        last_empty_at=attempted_at,
        last_repair_attempt_at=attempted_at,
    )

    existing_files = snapshot_sibling_files(script_path)
    repaired = repair_scraper_with_opencode(script_path, company)
    cleanup_created_sibling_files(script_path, existing_files)

    if not repaired:
        # SystemExit mosteneste din BaseException, deci nu este prins de
        # 'except Exception' din main() si runnerul vad esecul
        raise SystemExit(
            f"Auto-repair failed for empty jobs result in {script_path.name}."
        )

    existing_files = snapshot_sibling_files(script_path)
    try:
        rerun_was_empty = rerun_repaired_scraper(script_path)
    finally:
        cleanup_created_sibling_files(script_path, existing_files)

    if rerun_was_empty:
        now = format_timestamp(utc_now())
        update_state(
            script_path,
            company,
            last_empty_at=now,
            last_confirmed_empty_at=now,
            last_repair_attempt_at=attempted_at,
        )
    else:
        clear_state(script_path)

    # iesim cu succes: rerularea a rezolvat problema sau a confirmat ca
    # lista vida e corecta. SystemExit nu e prins de 'except Exception'.
    raise SystemExit(0)
