"""
ParallelLogErrorReader.py
Reads lines containing 'ERROR' from all files in /var/log simultaneously using ThreadPoolExecutor.
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed


LOG_DIR = "/var/log"
KEYWORD = "ERROR"
MAX_WORKERS = 20  # Tune based on I/O capacity


def search_errors_in_file(filepath: str) -> dict:
    """Read a single log file and return lines containing the keyword."""
    matches = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line_num, line in enumerate(f, start=1):
                if KEYWORD in line:
                    matches.append((line_num, line.rstrip()))
    except PermissionError:
        return {"file": filepath, "error": "Permission denied", "matches": []}
    except OSError as e:
        return {"file": filepath, "error": str(e), "matches": []}
    return {"file": filepath, "error": None, "matches": matches}


def collect_log_files(directory: str) -> list[str]:
    """Recursively collect all readable files under the given directory."""
    log_files = []
    for root, _, files in os.walk(directory):
        for name in files:
            log_files.append(os.path.join(root, name))
    return log_files


def read_errors_in_parallel(log_dir: str = LOG_DIR) -> None:
    log_files = collect_log_files(log_dir)
    print(f"Found {len(log_files)} file(s) in '{log_dir}'. Scanning for '{KEYWORD}'...\n")

    total_matches = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_file = {executor.submit(search_errors_in_file, fp): fp for fp in log_files}

        for future in as_completed(future_to_file):
            result = future.result()
            filepath = result["file"]

            if result["error"]:
                print(f"[SKIP] {filepath} — {result['error']}")
                continue

            if result["matches"]:
                print(f"\n[{filepath}] — {len(result['matches'])} match(es):")
                for line_num, line in result["matches"]:
                    print(f"  Line {line_num}: {line}")
                total_matches += len(result["matches"])

    print(f"\nDone. Total '{KEYWORD}' lines found: {total_matches}")


if __name__ == "__main__":
    read_errors_in_parallel()
