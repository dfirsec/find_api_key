"""API key finder module."""

import multiprocessing
import sys
from functools import partial
from pathlib import Path
from re import Pattern

from modules.file_checker import check_file


def find_api_key_references(
    dirpath: str,
    exclude_keywords: list[str],
    patterns: dict[str, list[tuple[Pattern[str], str]]],
) -> list[tuple[Path, list[int], list[str], list[str]]]:
    """Find API key references in the given directory."""
    # Exclude the current Python script file
    current_script_path = Path(sys.argv[0]).resolve()

    all_results = []
    pool = multiprocessing.Pool()
    try:
        files = list(Path(dirpath).rglob("*"))
        check_func = partial(check_file, api_key_regexes=patterns, exclude_keywords=exclude_keywords)
        all_results = pool.map(check_func, files)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Terminating workers...")
        pool.terminate()
        pool.join()
        sys.exit(0)
    else:
        pool.close()
        pool.join()

    return [result for result in all_results if result and result[0] != current_script_path]
