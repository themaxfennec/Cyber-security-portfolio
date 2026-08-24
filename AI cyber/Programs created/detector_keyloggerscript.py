import ast
import os
from pathlib import Path


# Things commonly associated with keyboard monitoring
SUSPICIOUS_IMPORTS = {
    "pynput",
    "keyboard",
    "pyHook",
    "pyWinhook",
}

SUSPICIOUS_NAMES = {
    "Listener",
    "on_press",
    "on_release",
    "hook",
    "hook_key",
    "record",
    "GetAsyncKeyState",
    "GetKeyState",
    "GetKeyboardState",
}

SUSPICIOUS_STRINGS = {
    "GetAsyncKeyState",
    "GetKeyboardState",
    "SetWindowsHookEx",
    "WH_KEYBOARD_LL",
    "pynput.keyboard.Listener",
    "keyboard.Listener",
    "keyboard.on_press",
    "keyboard.on_release",
}


def scan_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()

        tree = ast.parse(source, filename=str(filepath))

    except (OSError, SyntaxError):
        return 0, []

    score = 0
    findings = []

    # Check imports
    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for alias in node.names:
                if (
                    alias.name in SUSPICIOUS_IMPORTS
                    or alias.name.startswith("pynput.")
                ):
                    score += 2
                    findings.append(
                        (node.lineno, f"Suspicious import: {alias.name}")
                    )

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""

            if (
                module in SUSPICIOUS_IMPORTS
                or module.startswith("pynput.")
            ):
                score += 2
                findings.append(
                    (node.lineno, f"Suspicious import from: {module}")
                )

            for alias in node.names:
                if alias.name in SUSPICIOUS_NAMES:
                    score += 3
                    findings.append(
                        (node.lineno, f"Suspicious API: {alias.name}")
                    )

        # Function calls
        elif isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):
                name = node.func.id

                if name in SUSPICIOUS_NAMES:
                    score += 3
                    findings.append(
                        (node.lineno, f"Suspicious call: {name}()")
                    )

            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr

                if name in SUSPICIOUS_NAMES:
                    score += 3
                    findings.append(
                        (node.lineno, f"Suspicious call: {name}()")
                    )

    # Look for suspicious strings
    for line_number, line in enumerate(source.splitlines(), 1):
        for suspicious in SUSPICIOUS_STRINGS:
            if suspicious in line:
                findings.append(
                    (line_number, f"Suspicious string/API: {suspicious}")
                )

    # Remove duplicate findings
    findings = list(dict.fromkeys(findings))

    return score, findings


def get_scan_directories():
    home = Path.home()

    directories = [
        home / "Downloads",
        home / "Desktop",
        home / "Documents",
        Path(os.environ.get("TEMP", "")),
        Path(os.environ.get("APPDATA", "")),
        Path(os.environ.get("LOCALAPPDATA", "")),
    ]

    # Remove nonexistent directories
    return [
        path for path in directories
        if path and path.exists() and path.is_dir()
    ]


def should_skip(path):
    parts = {p.lower() for p in path.parts}

    excluded = {
        "__pycache__",
        ".git",
        "node_modules",
        ".venv",
        "venv",
        "env",
        ".tox",
    }

    return bool(parts.intersection(excluded))


def scan_directories():
    directories = get_scan_directories()

    total = 0
    suspicious = 0

    print("Python suspicious-file scanner")
    print("=" * 60)

    print("\nDirectories being scanned:")

    for directory in directories:
        print(f"  {directory}")

    print("\nStarting scan...\n")

    for directory in directories:

        for root, dirs, files in os.walk(directory):

            # Don't descend into excluded directories
            dirs[:] = [
                d for d in dirs
                if d.lower() not in {
                    "__pycache__",
                    ".git",
                    "node_modules",
                    ".venv",
                    "venv",
                    "env",
                    ".tox",
                }
            ]

            for filename in files:

                if not filename.lower().endswith(".py"):
                    continue

                filepath = Path(root) / filename

                if should_skip(filepath):
                    continue

                total += 1

                score, findings = scan_file(filepath)

                # Only report files that have multiple/suspicious indicators
                if score >= 5:
                    suspicious += 1

                    print("=" * 70)
                    print("POSSIBLY SUSPICIOUS FILE")
                    print(f"File: {filepath}")
                    print(f"Risk score: {score}")

                    for line, reason in findings:
                        print(f"  Line {line}: {reason}")

                    print()

    print("=" * 60)
    print("SCAN COMPLETE")
    print(f"Python files examined: {total}")
    print(f"Potentially suspicious files: {suspicious}")


if __name__ == "__main__":
    scan_directories()