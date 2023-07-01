"""Module that checks files for API keys."""


import re
from pathlib import Path
from re import Pattern

# Maximum file size in bytes
MAX_FILE_SIZE = 100000  # 100 KB

# Skip non-text files
NON_TEXT_FILES = {
    ".3ds",
    ".3gp",
    ".7z",
    ".aac",
    ".accdb",
    ".ai",
    ".aiff",
    ".apk",
    ".app",
    ".avi",
    ".bin",
    ".blend",
    ".bmp",
    ".csv",
    ".dbf",
    ".dll",
    ".dmg",
    ".dwg",
    ".dxf",
    ".exe",
    ".fbx",
    ".flac",
    ".flv",
    ".gif",
    ".gz",
    ".hex",
    ".img",
    ".ini",
    ".iso",
    ".jpeg",
    ".json",
    ".key",
    ".kml",
    ".log",
    ".mdb",
    ".mkv",
    ".mov",
    ".mp3",
    ".mp4",
    ".mpeg",
    ".msi",
    ".nds",
    ".obj",
    ".odp",
    ".ods",
    ".ogg",
    ".otf",
    ".ovf",
    ".png",
    ".ppt",
    ".pptx",
    ".proj",
    ".psd",
    ".rar",
    ".rom",
    ".shp",
    ".sln",
    ".sql",
    ".stl",
    ".svg",
    ".sys",
    ".tar",
    ".tgz",
    ".tiff",
    ".ttf",
    ".vcxproj",
    ".vdi",
    ".vmdk",
    ".vmx",
    ".wav",
    ".wma",
    ".wmv",
    ".xcodeproj",
    ".xls",
    ".xlsx",
    ".xml",
    ".yaml",
    ".zip",
}


def has_base64(line: str, match: str) -> bool:
    """Check if the matched key is part of a base64 encoded string."""
    end = line.find(match) + len(match)
    return "=" in line[end:]


def check_file(
    file_path: Path,
    api_key_regexes: dict[str, list[tuple[Pattern[str], str]]],
    exclude_keywords: list[str],
) -> tuple[Path, list[int], list[str], list[str]] | None:
    """Checks if the file contains API keys."""
    # Skip if not regular file or exceeds maximum size
    if not file_path.is_file() or file_path.stat().st_size > MAX_FILE_SIZE:
        return None

    # Skips the program file
    if file_path.name == Path(__file__).name:
        return None

    # Get the file extension
    extension = file_path.suffix

    # Skip non-text files or files without any associated regexes
    if extension in NON_TEXT_FILES or extension not in api_key_regexes:
        return None

    # Get the patterns to use
    patterns = api_key_regexes[extension]

    # Initialize lists to store the results
    line_numbers = []
    api_keys = []
    descriptions = []

    # Create a set of exclude keywords
    exclude_keywords_set = {keyword.lower() for keyword in exclude_keywords}

    # Open the file and check each line
    with open(file_path, encoding="utf-8", errors="ignore") as file:
        for line_no, line in enumerate(file, start=1):
            for pattern, description in patterns:
                match = pattern.search(line)
                if match:
                    api_key = match.group()
                    # Split at declarator (= or :) and take the part after the declarator.
                    api_value = re.split(r"=|:", api_key, 1, flags=re.IGNORECASE)[-1].strip()
                    if (
                        api_value
                        and api_value not in ('""', '"', "''", "'")  # Exclude empty strings and empty quotes
                        and all(keyword.lower() not in api_value.lower() for keyword in exclude_keywords_set)
                        and not has_base64(line, api_key)  # Exclude base64 encoded strings
                    ):
                        line_numbers.append(line_no)
                        api_keys.append(api_key)
                        descriptions.append(description)

    if line_numbers and api_keys and descriptions:
        return file_path, line_numbers, api_keys, descriptions

    return None
