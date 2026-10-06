import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from __utils.empty_jobs_repair import (
    ATTEMPT_ENV,
    COOLDOWN_DAYS,
    DEPTH_ENV,
    NO_JOBS_MARKER,
    STATE_PATH,
    count_scrapers,
    format_timestamp,
    get_cooldown_until,
    get_daily_budget,
    get_repair_backlog,
    get_remaining_daily_budget,
    load_state,
    parse_timestamp,
    utc_now,
)

EXCLUDE = {
    "__init__.py",
    "main.py",
    "__create_scraper.py",
    "__main_RunnerFile.py",
}
SITES_DIR = Path(__file__).resolve().parent
REPO_ROOT = SITES_DIR.parent
SCRAPER_TIMEOUT_SECONDS = int(os.getenv("SCRAPER_TIMEOUT_SECONDS", "1800"))
REPAIR_TIMEOUT_SECONDS = int(os.getenv("OPENCODE_REPAIR_TIMEOUT", "900"))
MAX_LOG_LENGTH = 4000

# un scraper care ajunge la lista goala ruleaza repararea cu OpenCode chiar in
# interiorul procesului sau, deci bugetul extern trebuie sa acopere si repair-ul
if 0 < SCRAPER_TIMEOUT_SECONDS < REPAIR_TIMEOUT_SECONDS + 300:
    SCRAPER_TIMEOUT_SECONDS = REPAIR_TIMEOUT_SECONDS + 300
    print(
        f"Warning: SCRAPER_TIMEOUT_SECONDS raised to {SCRAPER_TIMEOUT_SECONDS}s "
        f"so the in-scraper auto-repair (max {REPAIR_TIMEOUT_SECONDS}s) can finish."
    )


def parse_no_jobs(stdout):
    companies = []

    for line in (stdout or "").splitlines():
        line = line.strip()
        if line.startswith(NO_JOBS_MARKER):
            company = line[len(NO_JOBS_MARKER):].strip()
            if company:
                companies.append(company)

    return companies


def format_remaining(delta):
    total_seconds = int(delta.total_seconds())
    if total_seconds <= 0:
        return "expired"

    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes = remainder // 60

    if days:
        return f"{days}d {hours}h left"
    if hours:
        return f"{hours}h {minutes}m left"
    return f"{minutes}m left"


def print_cache_summary():
    state = load_state()

    try:
        cache_display = STATE_PATH.relative_to(REPO_ROOT)
    except ValueError:
        cache_display = STATE_PATH

    if not state:
        print(f"Empty-jobs cache: no entries ({cache_display} missing or empty).")
        print("  Auto-repair will run for every scraper returning 0 jobs, with no cooldown.")
        return

    now = utc_now()
    on_cooldown = []
    cooldown_over = []

    for state_key, entry in sorted(state.items()):
        if not isinstance(entry, dict):
            continue

        company = entry.get("company") or state_key
        cooldown_until = get_cooldown_until(REPO_ROOT / state_key)

        if cooldown_until and now < cooldown_until:
            on_cooldown.append((state_key, company, cooldown_until))
        else:
            cooldown_over.append(
                (state_key, company, parse_timestamp(entry.get("last_confirmed_empty_at")))
            )

    print(f"Empty-jobs cache: {len(state)} scraper(s) known to return 0 jobs ({cache_display}).")
    print(f"  Cooldown lasts {COOLDOWN_DAYS} days after a confirmed empty result.")

    for state_key, company, cooldown_until in on_cooldown:
        print(f"  [on cooldown] {state_key} | {company} | {format_remaining(cooldown_until - now)}")

    for state_key, company, confirmed_at in cooldown_over:
        confirmed = confirmed_at.strftime("%Y-%m-%d %H:%M UTC") if confirmed_at else "unknown"
        print(f"  [cooldown over] {state_key} | {company} | confirmed empty {confirmed}")

    if not on_cooldown:
        print("  No scraper is currently on cooldown.")


def describe_empty_scrapers(all_no_jobs):
    """
    ... maps the company names collected during the run to the cooldown state
    """

    state = load_state()
    if not state:
        return

    by_company = {entry.get("company"): key for key, entry in state.items() if isinstance(entry, dict)}
    now = utc_now()

    for company in sorted(set(all_no_jobs)):
        state_key = by_company.get(company)
        if not state_key:
            print(f"  - {company} | first time seen, no cooldown yet")
            continue

        cooldown_until = get_cooldown_until(REPO_ROOT / state_key)
        if cooldown_until and now < cooldown_until:
            print(f"  - {company} | on cooldown | {format_remaining(cooldown_until - now)}")
        else:
            print(f"  - {company} | OpenCode verification will run")


def print_no_jobs_summary(all_no_jobs):
    print()
    print("=" * 50)
    if all_no_jobs:
        print(f"FIRME FARA JOBURI ({len(all_no_jobs)}):")
        describe_empty_scrapers(all_no_jobs)
    else:
        print("Toate firmele au joburi disponibile.")
    print("=" * 50)


def print_repair_plan(limit=None):
    backlog = get_repair_backlog(limit)
    print_cache_summary()
    print()
    print(
        f"Repair budget: {get_remaining_daily_budget()}/{get_daily_budget()} left today | "
        f"{count_scrapers()} scrapers total | {len(backlog)} queued for repair."
    )
    if not backlog:
        print("  Nothing to repair right now.")
    else:
        for state_key, company, _script_path in backlog:
            print(f"  - {state_key} | {company}")
    print()
    return backlog


def run_repair_backlog(limit=None):
    """
    ... ruleaza doar scraperele din cache care asteapta reparare, cel mult
    cate permite bugetul zilei. Rularea lunara completa ramane separata.
    """
    remaining = get_remaining_daily_budget()
    if limit is None:
        limit = remaining

    if limit <= 0:
        print(f"Daily repair budget already spent today ({get_daily_budget()}/day).")
        return False

    backlog = print_repair_plan(limit)
    if not backlog:
        return False

    all_no_jobs = []
    succeeded = 0

    for _state_key, _company, script_path in backlog:
        existing_files = snapshot_sibling_files(script_path)
        try:
            action = run_scraper(script_path)
        except subprocess.TimeoutExpired:
            cleanup_created_sibling_files(script_path, existing_files)
            log_scraper_timeout(script_path)
            continue

        cleanup_created_sibling_files(script_path, existing_files)
        all_no_jobs.extend(parse_no_jobs(action.stdout))

        if action.returncode == 0:
            succeeded += 1
            print(f"Processed {script_path.name} (exit 0)")
        else:
            print(f"Error scraping {script_path.name}")
            print(truncate_output(action.stderr))

    print_no_jobs_summary(all_no_jobs)
    print()
    print_cache_summary()
    print(f"Repair queue: {succeeded}/{len(backlog)} scraper(s) exited successfully.")
    return True


def snapshot_sibling_files(script_path):
    return {
        path.name
        for path in script_path.parent.iterdir()
        if path.is_file() or path.is_symlink()
    }


def cleanup_created_sibling_files(script_path, existing_files):
    current_files = snapshot_sibling_files(script_path)
    created_files = sorted(current_files - existing_files)

    for file_name in created_files:
        created_file = script_path.parent / file_name
        if created_file == script_path:
            continue

        created_file.unlink(missing_ok=True)
        print(f"Deleted extra file {created_file.name}")


def truncate_output(content, limit=MAX_LOG_LENGTH):
    if not content:
        return "No output captured."

    content = content.strip()
    if len(content) <= limit:
        return content

    return content[:limit] + "\n...[truncated]"


def run_scraper(script_path):
    command = [sys.executable, str(script_path)]

    if SCRAPER_TIMEOUT_SECONDS <= 0:
        return subprocess.run(command, capture_output=True, text=True, cwd=REPO_ROOT)

    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        timeout=SCRAPER_TIMEOUT_SECONDS,
    )


def log_scraper_timeout(script_path, after_repair=False):
    minutes = SCRAPER_TIMEOUT_SECONDS / 60
    stage = "after auto-repair" if after_repair else "while scraping"
    print(
        f"Timeout {stage} {script_path.name} after {minutes:.0f} min. "
        f"Scraper skipped without a verdict. Raise SCRAPER_TIMEOUT_SECONDS "
        f"(current: {SCRAPER_TIMEOUT_SECONDS}) or set it to 0 to disable."
    )


def get_script_path(scraper_name):
    script_name = scraper_name if scraper_name.endswith(".py") else scraper_name + ".py"
    script_path = SITES_DIR / script_name

    if script_name in EXCLUDE:
        raise ValueError(f"{script_name} cannot be tested manually.")

    if not script_path.exists() or not script_path.is_file():
        raise FileNotFoundError(f"Scraper not found: {script_name}")

    return script_path


def repair_scraper_with_opencode(script_path, failed_action):
    if shutil.which("opencode") is None:
        print(f"OpenCode is not installed. Skipping auto-repair for {script_path.name}.")
        return False

    stderr_output = truncate_output(failed_action.stderr)
    stdout_output = truncate_output(failed_action.stdout)
    prompt = (
        f"Fix the failing scraper `{script_path.relative_to(REPO_ROOT)}`. "
        "Use the attached context file for the traceback and rerun the scraper until it exits successfully."
    )
    context_file_path = None

    repair_context = f"""
Scraper: {script_path.relative_to(REPO_ROOT)}
Run command: {sys.executable} {script_path.relative_to(REPO_ROOT)}

Requirements:
- Fix only what is needed for this scraper to run correctly.
- Preserve the existing scraper behavior and output schema.
- Keep changes focused; avoid unrelated edits.
- Re-run the scraper after your fix and stop only when it exits successfully.

Captured stderr:
```
{stderr_output}
```

Captured stdout:
```
{stdout_output}
```
""".strip()

    try:
        print(f"Starting OpenCode repair for {script_path.name}...")

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix="_opencode_repair_context.md",
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
        print(f"OpenCode repair timed out for {script_path.name}.")
        return False
    finally:
        if context_file_path and os.path.exists(context_file_path):
            os.unlink(context_file_path)

    if action.returncode != 0:
        opencode_error = truncate_output(action.stderr or action.stdout)
        print(f"OpenCode could not repair {script_path.name}.")
        print(opencode_error)
        return False

    print(f"OpenCode repair finished for {script_path.name}.")
    return True


def test_scraper_repair(scraper_name):
    try:
        script_path = get_script_path(scraper_name)
    except (FileNotFoundError, ValueError) as error:
        print(error)
        return False

    existing_files = snapshot_sibling_files(script_path)
    try:
        action = run_scraper(script_path)
    except subprocess.TimeoutExpired:
        cleanup_created_sibling_files(script_path, existing_files)
        log_scraper_timeout(script_path)
        return False

    cleanup_created_sibling_files(script_path, existing_files)

    if action.returncode == 0:
        print(f"Scraper {script_path.name} already works.")
        return True

    print(f"Error scraping {script_path.name}")
    print(truncate_output(action.stderr))

    if not repair_scraper_with_opencode(script_path, action):
        return False

    existing_files = snapshot_sibling_files(script_path)
    try:
        repaired_action = run_scraper(script_path)
    except subprocess.TimeoutExpired:
        cleanup_created_sibling_files(script_path, existing_files)
        log_scraper_timeout(script_path, after_repair=True)
        return False

    cleanup_created_sibling_files(script_path, existing_files)

    if repaired_action.returncode == 0:
        print(f"Success scraping after auto-repair {script_path.name}")
        return True

    print(f"Auto-repair did not fix {script_path.name}")
    print(truncate_output(repaired_action.stderr))
    return False


def main():
    print_cache_summary()
    print()

    all_no_jobs = []

    for site in sorted(os.listdir(SITES_DIR)):
        if not site.endswith(".py") or site in EXCLUDE:
            continue

        script_path = SITES_DIR / site
        existing_files = snapshot_sibling_files(script_path)
        try:
            action = run_scraper(script_path)
        except subprocess.TimeoutExpired:
            cleanup_created_sibling_files(script_path, existing_files)
            log_scraper_timeout(script_path)
            continue

        cleanup_created_sibling_files(script_path, existing_files)
        all_no_jobs.extend(parse_no_jobs(action.stdout))

        if action.returncode == 0:
            print("Success scraping " + site)
            continue

        print("Error scraping " + site)
        print(truncate_output(action.stderr))

        if not repair_scraper_with_opencode(script_path, action):
            continue

        existing_files = snapshot_sibling_files(script_path)
        try:
            repaired_action = run_scraper(script_path)
        except subprocess.TimeoutExpired:
            cleanup_created_sibling_files(script_path, existing_files)
            log_scraper_timeout(script_path, after_repair=True)
            continue

        cleanup_created_sibling_files(script_path, existing_files)
        all_no_jobs.extend(parse_no_jobs(repaired_action.stdout))

        if repaired_action.returncode == 0:
            print("Success scraping after auto-repair " + site)
        else:
            print("Auto-repair did not fix " + site)
            print(truncate_output(repaired_action.stderr))

    print_no_jobs_summary(all_no_jobs)


class Scraper:
    def __init__(self, exclude=None):
        self.exclude = set(EXCLUDE if exclude is None else exclude)

    def run(self):
        print_cache_summary()
        print()

        all_no_jobs = []

        for site in sorted(os.listdir(SITES_DIR)):
            if not site.endswith(".py") or site in self.exclude:
                continue

            script_path = SITES_DIR / site
            existing_files = snapshot_sibling_files(script_path)
            try:
                action = run_scraper(script_path)
            except subprocess.TimeoutExpired:
                cleanup_created_sibling_files(script_path, existing_files)
                log_scraper_timeout(script_path)
                continue

            cleanup_created_sibling_files(script_path, existing_files)
            all_no_jobs.extend(parse_no_jobs(action.stdout))

            if action.returncode == 0:
                print(f"Success scraping {site} with exit code {action.returncode}")
                continue

            print(f"Error scraping {site} with exit code {action.returncode}")
            print(truncate_output(action.stderr))

        print_no_jobs_summary(all_no_jobs)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--repair-backlog":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
            run_repair_backlog(limit)
        else:
            test_scraper_repair(sys.argv[1])
    else:
        main()
