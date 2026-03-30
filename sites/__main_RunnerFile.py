import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXCLUDE = {
    "__init__.py",
    "main.py",
    "__create_scraper.py",
    "__main_RunnerFile.py",
}
SITES_DIR = Path(__file__).resolve().parent
REPO_ROOT = SITES_DIR.parent
REPAIR_TIMEOUT_SECONDS = int(os.getenv("OPENCODE_REPAIR_TIMEOUT", "900"))
MAX_LOG_LENGTH = 4000


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
    return subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
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
    action = run_scraper(script_path)
    cleanup_created_sibling_files(script_path, existing_files)

    if action.returncode == 0:
        print(f"Scraper {script_path.name} already works.")
        return True

    print(f"Error scraping {script_path.name}")
    print(truncate_output(action.stderr))

    if not repair_scraper_with_opencode(script_path, action):
        return False

    existing_files = snapshot_sibling_files(script_path)
    repaired_action = run_scraper(script_path)
    cleanup_created_sibling_files(script_path, existing_files)

    if repaired_action.returncode == 0:
        print(f"Success scraping after auto-repair {script_path.name}")
        return True

    print(f"Auto-repair did not fix {script_path.name}")
    print(truncate_output(repaired_action.stderr))
    return False


def main():
    for site in sorted(os.listdir(SITES_DIR)):
        if not site.endswith(".py") or site in EXCLUDE:
            continue

        script_path = SITES_DIR / site
        existing_files = snapshot_sibling_files(script_path)
        action = run_scraper(script_path)
        cleanup_created_sibling_files(script_path, existing_files)

        if action.returncode == 0:
            print("Success scraping " + site)
            continue

        print("Error scraping " + site)
        print(truncate_output(action.stderr))

        if not repair_scraper_with_opencode(script_path, action):
            continue

        existing_files = snapshot_sibling_files(script_path)
        repaired_action = run_scraper(script_path)
        cleanup_created_sibling_files(script_path, existing_files)

        if repaired_action.returncode == 0:
            print("Success scraping after auto-repair " + site)
        else:
            print("Auto-repair did not fix " + site)
            print(truncate_output(repaired_action.stderr))


class Scraper:
    def __init__(self, exclude=None):
        self.exclude = set(EXCLUDE if exclude is None else exclude)

    def run(self):
        for site in sorted(os.listdir(SITES_DIR)):
            if not site.endswith(".py") or site in self.exclude:
                continue

            script_path = SITES_DIR / site
            existing_files = snapshot_sibling_files(script_path)
            action = run_scraper(script_path)
            cleanup_created_sibling_files(script_path, existing_files)

            if action.returncode == 0:
                print(f"Success scraping {site} with exit code {action.returncode}")
                continue

            print(f"Error scraping {site} with exit code {action.returncode}")
            print(truncate_output(action.stderr))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_scraper_repair(sys.argv[1])
    else:
        main()
