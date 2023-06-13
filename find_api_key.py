"""Find 'api_key' references in files."""

import contextlib
import multiprocessing
import re
import sys
from functools import partial
from pathlib import Path


def check_file(file_path: Path, api_key_regexes: dict) -> tuple[Path, list[int], list[str]] | None:
    """Check if a file contains 'api_key'."""
    file_ext = file_path.suffix
    if file_ext in api_key_regexes:
        line_numbers = []
        api_keys = []
        with contextlib.suppress(OSError):
            with file_path.open(encoding="utf-8", errors="ignore") as file:
                for line_no, line in enumerate(file, start=1):
                    match = api_key_regexes[file_ext].search(line)
                    if match:
                        # Only extract alphanumeric characters and underscore from the matched key
                        matched_key = re.sub(r"\W", "", match.group(1).lower())
                        if "key" not in matched_key and "api" not in matched_key:
                            line_numbers.append(line_no)
                            api_keys.append(matched_key)
            if line_numbers and api_keys:
                return file_path, line_numbers, api_keys
    return None


def find_api_key_references(root_dir: str) -> list[tuple[Path, list[int], list[str]]]:
    """Find api_key references in files."""
    patterns = {
        ".bashrc": re.compile(r"export\s+API_KEY\s*=\s*(.+)", re.IGNORECASE),
        ".cfg": re.compile(r"api_key\s*=\s*(.+)", re.IGNORECASE),
        ".conf": re.compile(r"api_key\s*=\s*(.+)", re.IGNORECASE),
        ".config": re.compile(r"\bapi_key\s*=\s*(\w+)", re.IGNORECASE),
        ".dockerfile": re.compile(r"ENV\s+API_KEY\s*=\s*(.+)", re.IGNORECASE),
        ".ini": re.compile(r"api_key\s*=\s*(.+)", re.IGNORECASE),
        ".json": re.compile(r"\"api_key\"\s*:\s*\"(.+)\"", re.IGNORECASE),
        ".php": re.compile(r"\$api_key\s*=\s*\'(\w+)\'", re.IGNORECASE),
        ".properties": re.compile(r"api_key\s*=\s*(.+)", re.IGNORECASE),
        ".py": re.compile(r'\bapi_key\s*=\s*["\'](\w+)["\']', re.IGNORECASE),
        ".toml": re.compile(r"api_key\s*=\s*(.+)", re.IGNORECASE),
        ".xml": re.compile(r"<api_key>\s*(.*)\s*</api_key>", re.IGNORECASE),
        ".yaml": re.compile(r"\bapi_key\s*:\s*(\w+)", re.IGNORECASE),
        ".yml": re.compile(r"\bapi_key\s*:\s*(\w+)", re.IGNORECASE),
    }

    with multiprocessing.Pool() as pool:
        files = list(Path(root_dir).rglob("*"))
        all_results = pool.map(partial(check_file, api_key_regexes=patterns), files)

    return [result for result in all_results if result]


def main() -> None:
    """Main function."""
    root_dir = input("Enter the root directory to search for 'api_key': ")
    try:
        print("Searching for 'api_key' in files...")
        files_with_api_key = find_api_key_references(root_dir)
        if files_with_api_key:
            print("\nFiles containing 'api_key':\n---------------------------")
            for file_path, line_numbers, api_keys in files_with_api_key:
                print(f"{file_path} (lines: {', '.join(map(str, line_numbers))}), {', '.join(api_keys)}")
        else:
            print("No files found containing 'api_key'.")
    except KeyboardInterrupt:
        print("\nExecution interrupted by user!")
        sys.exit(0)


if __name__ == "__main__":
    main()
