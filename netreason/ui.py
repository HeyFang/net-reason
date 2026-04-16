"""
Terminal UI helpers — colors, prompts, formatting.
No external dependencies, pure ANSI.
"""

import sys
import shutil


# ANSI color codes
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[36m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    RED     = "\033[31m"
    MAGENTA = "\033[35m"
    BLUE    = "\033[34m"
    WHITE   = "\033[97m"
    BG_DARK = "\033[40m"


def supports_color():
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def c(color, text):
    if supports_color():
        return f"{color}{text}{C.RESET}"
    return text


def terminal_width():
    return shutil.get_terminal_size((80, 20)).columns


def divider(char="─", color=C.DIM):
    w = min(terminal_width(), 72)
    print(c(color, char * w))


def print_header(title: str, subtitle: str = ""):
    print()
    divider("━", C.CYAN)
    print(c(C.BOLD + C.CYAN, f"  net-reason  ") + c(C.DIM, "| AI Knowledge Reasoning for Linux Errors"))
    divider("━", C.CYAN)
    if title:
        print(c(C.BOLD + C.WHITE, f"\n  {title}"))
    if subtitle:
        print(c(C.DIM, f"  {subtitle}"))
    print()


def print_section(label: str):
    print()
    print(c(C.BOLD + C.CYAN, f"  {label}"))
    print(c(C.DIM, "  " + "─" * (len(label) + 2)))


def print_info(msg: str):
    print(c(C.CYAN, "  ℹ ") + msg)


def print_success(msg: str):
    print(c(C.GREEN, "  ✔ ") + msg)


def print_warning(msg: str):
    print(c(C.YELLOW, "  ⚠ ") + msg)


def print_error(msg: str):
    print(c(C.RED, "  ✖ ") + msg)


def print_question(msg: str):
    print()
    print(c(C.BOLD + C.YELLOW, "  ? ") + c(C.BOLD, msg))


def print_diagnosis(diagnosis: dict):
    """Pretty-print the final diagnosis and fix suggestions."""
    divider("━", C.GREEN)
    print(c(C.BOLD + C.GREEN, "\n  DIAGNOSIS\n"))

    print(c(C.BOLD, "  Root cause: ") + c(C.YELLOW, diagnosis.get("diagnosis", "Unknown")))
    print()
    print(c(C.DIM, "  ") + diagnosis.get("cause", ""))

    print_section("Suggested fixes")
    fixes = diagnosis.get("fixes", [])
    for i, fix in enumerate(fixes, 1):
        prefix = c(C.CYAN, f"  {i}. ")
        # Highlight commands in backticks or after colons
        print(prefix + _highlight_commands(fix))

    if diagnosis.get("docs"):
        print()
        print(c(C.DIM, "  📖 Docs: ") + c(C.BLUE, diagnosis["docs"]))

    print()
    divider("━", C.GREEN)
    print()


def _highlight_commands(text: str) -> str:
    """Highlight text that looks like shell commands."""
    if not supports_color():
        return text
    import re
    # Highlight content after colons that looks like a command
    result = re.sub(
        r'(sudo [^\n,]+|[a-z]+-[a-z]+ [^\n,]+|`[^`]+`)',
        lambda m: c(C.BOLD + C.GREEN, m.group(0)),
        text
    )
    return result


def ask_yn(question: str) -> bool | None:
    """
    Ask a Y/N question. Returns True for yes, False for no, None for quit.
    """
    print_question(question)
    while True:
        try:
            raw = input(c(C.DIM, "  [y/n/q] ") + c(C.BOLD, "→ ")).strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            return None
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        if raw in ("q", "quit", "exit"):
            return None
        print(c(C.DIM, "  Please enter y, n, or q to quit."))


def prompt_choice(options: list[tuple[str, str]]) -> int | None:
    """
    Present a numbered list of (name, description) options.
    Returns selected index, or None on quit.
    """
    for i, (name, desc) in enumerate(options, 1):
        print(c(C.CYAN, f"  {i}. ") + c(C.BOLD, name) + c(C.DIM, f"  — {desc}"))
    print(c(C.DIM, "  q. Quit"))
    print()

    while True:
        try:
            raw = input(c(C.DIM, "  Choose [1-") + c(C.DIM, str(len(options))) + c(C.DIM, "/q] ") + c(C.BOLD, "→ ")).strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            return None
        if raw in ("q", "quit", "exit"):
            return None
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return idx
        print(c(C.DIM, f"  Enter a number between 1 and {len(options)}, or q."))


def prompt_category_manual(categories: list) -> dict | None:
    """Let user pick a category from the full list."""
    print(c(C.DIM, "\n  Available error categories:\n"))
    options = [(cat["name"], cat["description"]) for cat in categories]
    idx = prompt_choice(options)
    if idx is None:
        return None
    return categories[idx]


def print_no_match():
    print()
    print_warning("No matching error category found for that input.")
    print(c(C.DIM, "  Tip: try pasting the exact error message, or use a keyword like:"))
    print(c(C.DIM, "       dns  |  ssh  |  apt  |  connectivity  |  systemd  |  firewall"))
    print()
