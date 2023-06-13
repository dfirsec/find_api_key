"""Find API key references in files."""

import argparse
import contextlib
import multiprocessing
import re
import sys
from functools import partial
from pathlib import Path


def check_file(file_path: Path, api_key_regexes: dict) -> tuple[Path, list[int], list[str]] | None:
    """Checks files in a given directory for API key references.

    Args:
        file_path (Path): Path to the file to check.
        api_key_regexes (dict): Dictionary of file extensions and their regex patterns.

    Returns:
        Tuple containing the file path, line numbers, and API key values found.
    """
    file_ext = file_path.suffix
    if file_ext in api_key_regexes:
        line_numbers = []
        api_keys = []
        with contextlib.suppress(OSError):
            with file_path.open(encoding="utf-8", errors="ignore") as file:
                for line_no, line in enumerate(file, start=1):
                    match = api_key_regexes[file_ext].search(line)
                    if match:
                        # only extract alphanumeric characters and underscore from the matched key
                        matched_key = re.sub(r"\W", "", match.group(1).lower())
                        if "key" not in matched_key and "api" not in matched_key:
                            line_numbers.append(line_no)
                            api_keys.append(matched_key)
            if line_numbers and api_keys:
                return file_path, line_numbers, api_keys
    return None


def find_api_key_references(root_dir: str, api: str) -> list[tuple[Path, list[int], list[str]]]:
    """Searches for API key references in files using regex and multiprocessing.

    Args:
        root_dir (str): Directory to search for files containing API key references.
        api (str): API key to search for.


    Returns:
        List of tuples containing the file path, line numbers, and API key values found.
    """
    patterns = {
        ".bashrc": re.compile(rf"export\s+{api}\s*=\s*(.+)", re.IGNORECASE),
        ".cfg": re.compile(rf"{api}\s*=\s*(.+)", re.IGNORECASE),
        ".conf": re.compile(rf"{api}\s*=\s*(.+)", re.IGNORECASE),
        ".config": re.compile(rf"\b{api}\s*=\s*(\w+)", re.IGNORECASE),
        ".dockerfile": re.compile(rf"ENV\s+{api}\s*=\s*(.+)", re.IGNORECASE),
        ".ini": re.compile(rf"{api}\s*=\s*(.+)", re.IGNORECASE),
        ".json": re.compile(rf"\"{api}\"\s*:\s*\"(.+)\"", re.IGNORECASE),
        ".php": re.compile(rf"\${api}\s*=\s*\'(\w+)\'", re.IGNORECASE),
        ".properties": re.compile(rf"{api}\s*=\s*(.+)", re.IGNORECASE),
        ".py": re.compile(rf'\b{api}\s*=\s*["\'](\w+)["\']', re.IGNORECASE),
        ".toml": re.compile(rf"{api}\s*=\s*(.+)", re.IGNORECASE),
        ".xml": re.compile(rf"<{api}>\s*(.*)\s*</{api}>", re.IGNORECASE),
        ".yaml": re.compile(rf"\b{api}\s*:\s*(\w+)", re.IGNORECASE),
        ".yml": re.compile(rf"\b{api}\s*:\s*(\w+)", re.IGNORECASE),
    }

    with multiprocessing.Pool() as pool:
        files = list(Path(root_dir).rglob("*"))
        all_results = pool.map(partial(check_file, api_key_regexes=patterns), files)

    return [result for result in all_results if result]


def main(root_dir: str, api: str) -> None:
    """Main function."""
    api_ref = f"\033[96m{api}\033[0m"
    try:
        print(f"Searching for {api_ref} references in files...")
        files_with_api_key = find_api_key_references(root_dir, api)
        if files_with_api_key:
            print(f"\nFiles containing {api_ref} references:\n{'-' * 35}")
            for file_path, line_numbers, api_keys in files_with_api_key:
                print(f"{file_path} (lines: {', '.join(map(str, line_numbers))}), \033[93m{', '.join(api_keys)}\033[0m")
        else:
            print(f"No files found containing {api_ref} references.")
    except KeyboardInterrupt:
        print("\nExecution interrupted by user!")
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find API key references in files.")
    parser.add_argument("root_dir", help="Directory to search for files containing API key references.")
    parser.add_argument(
        "-a", "--api", help="Key to search for. Default is 'api_key'.", default="api_key", required=False
    )
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()
    main(args.root_dir, args.api)
