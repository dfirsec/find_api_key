"""Module for generating patterns for the user-specified API key."""

import re
from pathlib import Path
from re import Pattern

import tomllib

PATTERNS_FILEPATH = str(Path(__file__).parent.parent / "patterns.toml")

# Read the TOML file
with open(PATTERNS_FILEPATH, "rb") as tome_file:
    patterns_data = tomllib.load(tome_file)

# Get patterns from the loaded patterns data
PATTERNS = patterns_data["pattern"]


def get_patterns(api: str) -> dict[str, list[tuple[Pattern[str], str]]]:
    """Get the patterns for the user-specified API key."""
    common_patterns: list[tuple[Pattern[str], str]] = [
        (re.compile(rf"\b{api}\s*=\s*(.+)", re.IGNORECASE), "User API Key"),
    ]

    return {
        ".bashrc": common_patterns,
        ".cfg": common_patterns,
        ".conf": common_patterns,
        ".config": common_patterns,
        ".cs": common_patterns,
        ".dockerfile": [(re.compile(rf"ENV\s+{api}\s*=\s*(.+)", re.IGNORECASE), "User API Key")],
        ".env": common_patterns,
        ".gemspec": common_patterns,
        ".go": common_patterns,
        ".ini": common_patterns,
        ".java": common_patterns,
        ".js": common_patterns,
        ".json": [(re.compile(rf"\"{api}\"\s*:\s*\"(.+)\"", re.IGNORECASE), "User API Key")],
        ".php": common_patterns,
        ".properties": common_patterns,
        ".ps1": common_patterns,
        ".py": common_patterns,
        ".rb": common_patterns,
        ".sh": common_patterns,
        ".swift": common_patterns,
        ".toml": common_patterns,
        ".txt": common_patterns,
        ".xml": [(re.compile(rf"<{api}>\s*(.*)\s*</{api}>", re.IGNORECASE), "User API Key")],
        ".yaml": common_patterns,
        ".yml": common_patterns,
    }


def get_other_patterns() -> dict[str, list[tuple[Pattern[str], str]]]:
    """Get the other hardcoded patterns."""
    return {
        ext: [(re.compile(pattern["regex"], re.IGNORECASE), pattern["name"]) for pattern in PATTERNS]
        for ext in [
            ".bashrc",
            ".cfg",
            ".conf",
            ".config",
            ".cs",
            ".dockerfile",
            ".env",
            ".go",
            ".ini",
            ".java",
            ".js",
            ".json",
            ".log",
            ".php",
            ".properties",
            ".ps1",
            ".py",
            ".rb",
            ".sh",
            ".swift",
            ".toml",
            ".txt",
            ".xml",
            ".yaml",
            ".yml",
        ]
    }
