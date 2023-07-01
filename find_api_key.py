"""Find API keys in a directory."""

import argparse
import sys
import textwrap

from modules.api_key_finder import find_api_key_references
from modules.pattern_seeker import get_other_patterns
from modules.pattern_seeker import get_patterns

# ANSI escape sequences for colored output
C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_END = "\033[0m"


def check_python_version() -> bool:
    """Check if the Python version is 3.11 or higher."""
    major, minor = sys.version_info[:2]
    return major > 3 or (major == 3 and minor >= 11)


def main(dirpath: str, api: str, other: bool, exclude_keywords: list[str]) -> None:
    """Outputs all API keys found.

    Args:
        dirpath (str): Path to the directory to search in.
        api (str): API key to search for.
        other (bool): Whether to use the other hardcoded patterns.
        exclude_keywords (list[str]): List of keywords to exclude.
    """
    if exclude_keywords is None:
        exclude_keywords = [
            "api_key",
            "apikey",
            "api key",
            "api",
            "key",
            "none",
            "null",
            "test",
            "username",
            "password",
            "passwd",
        ]
    else:
        exclude_keywords += [
            "api_key",
            "apikey",
            "api key",
            "api",
            "key",
            "none",
            "null",
            "test",
            "username",
            "password",
            "passwd",
        ]

    api_reference = f"{C_GREEN}other hardcoded api key{C_END}" if other else f"{C_GREEN}{api}{C_END}"
    print(f"Searching for {api_reference} references in files...")

    # Get the patterns to use
    patterns = get_other_patterns() if other else get_patterns(api)

    results = find_api_key_references(dirpath, exclude_keywords, patterns)

    if results:
        for file_path, line_numbers, api_keys, descriptions in results:
            print(f"\n{C_CYAN}{file_path}{C_END}:")
            for line_no, api_key, description in zip(line_numbers, api_keys, descriptions, strict=True):
                # Wrap the API key to 100 characters
                wrapped_api_key = textwrap.fill(api_key, width=100)
                print(f"  {C_GREEN}Line {line_no}{C_END}: {C_YELLOW}{wrapped_api_key}{C_END} ({description})")
    else:
        print("No API keys found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath", help="Directory to search for files containing API key references.")
    parser.add_argument(
        "--api",
        type=str,
        default="api_key",
        required=False,
        help="API key to search for. Default is 'api_key'.",
    )
    parser.add_argument("--other", action="store_true", help="Use other hardcoded patterns.")
    parser.add_argument(
        "--exclude",
        type=str,
        nargs="*",
        default=[],
        help="Space-separated list of additional keywords to exclude.",
    )
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()

    if not check_python_version():
        print("Python version is less than 3.11")
        sys.exit(1)

    main(args.dirpath, args.api, args.other, args.exclude)
