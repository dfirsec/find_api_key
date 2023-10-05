"""Find API keys in a directory."""

import argparse
import sys
import textwrap

from modules.api_key_finder import find_api_key_references
from modules.pattern_seeker import get_other_patterns
from modules.pattern_seeker import get_patterns
from rich.console import Console

console = Console(highlight=False)


def check_python_version() -> bool:
    """Check if the Python version is 3.8 or higher."""
    major, minor = sys.version_info[:2]
    return major > 3 or (major == 3 and minor >= 8)


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

    api_reference = "hardcoded api key" if other else "api key"
    with console.status(f"Searching for [green]{api_reference}[/green] references in files..."):
        # Get the patterns to use
        patterns = get_other_patterns() if other else get_patterns([api])

        results = find_api_key_references(dirpath, exclude_keywords, patterns)

        if results:
            for file_path, line_numbers, api_keys, descriptions in results:
                console.print(f"\n[cyan]{file_path}[/cyan]:")
                for line_no, api_key, description in zip(line_numbers, api_keys, descriptions, strict=True):
                    # wrap the API key to 100 characters
                    wrapped_api_key = textwrap.fill(api_key, width=100)
                    console.print(
                        f"  [green]Line {line_no}[/green]: [yellow]{wrapped_api_key}[/yellow] ({description})",
                    )
        else:
            console.print("No API keys found.", style="bright_white")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath", help="Directory to search for files containing API key references.")
    parser.add_argument(
        "--api",
        type=str,
        default="api[_ -]*key",
        required=False,
        help="API key to search for. Default is match either 'api key', 'apikey', 'api_key', or 'api-key'.",
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
        console.print("Python version is less than 3.8", style="red")
        sys.exit(1)

    main(args.dirpath, args.api, args.other, args.exclude)
