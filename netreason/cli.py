"""
net-reason CLI — main entry point.

Usage:
  netreason diagnose
  netreason diagnose "could not resolve host example.com"
  netreason diagnose dns
  netreason list
  netreason --help
"""

import sys
import json
import argparse
from pathlib import Path

from .matcher import pick_category, match_category
from .engine import run_diagnosis
from .ui import (
    print_header, print_info, print_success, print_warning,
    print_error, print_diagnosis, print_no_match, prompt_category_manual,
    ask_yn, divider, c, C
)


def load_knowledge_base() -> dict:
    data_path = Path(__file__).parent.parent / "data" / "errors.json"
    if not data_path.exists():
        print_error(f"Knowledge base not found at {data_path}")
        sys.exit(1)
    with open(data_path) as f:
        return json.load(f)


def cmd_diagnose(args):
    kb = load_knowledge_base()
    categories = kb["categories"]

    print_header(
        "Error Diagnosis",
        "Answer a few questions to identify the root cause and fix"
    )

    error_text = " ".join(args.error) if args.error else None

    # If no error text given, prompt for it
    if not error_text:
        print(c(C.DIM, "  Paste the error message, or type a keyword (dns, ssh, apt, connectivity, systemd, firewall)"))
        print(c(C.DIM, "  Leave blank to browse categories manually.\n"))
        try:
            error_text = input(c(C.BOLD, "  Error → ")).strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return

    category = None

    if error_text:
        # Try to auto-match
        category = pick_category(error_text, categories)

    if not category:
        # Fall back to manual selection
        if error_text:
            print_no_match()
        category = prompt_category_manual(categories)

    if not category:
        print_warning("No category selected. Exiting.")
        return

    print()
    print_info(f"Category: {c(C.BOLD, category['name'])} — {category['description']}")
    print(c(C.DIM, "  Answer each question with y (yes), n (no), or q to quit.\n"))
    divider()

    diagnosis = run_diagnosis(category)

    if diagnosis is None:
        print()
        print_warning("Diagnosis cancelled.")
        return

    print_diagnosis(diagnosis)

    # Offer to run another diagnosis
    print(c(C.DIM, "  Need to diagnose another error? Run: ") + c(C.BOLD, "netreason diagnose"))
    print()


def cmd_list(args):
    kb = load_knowledge_base()
    print_header("Error Categories", "Supported error types in the knowledge base")

    for cat in kb["categories"]:
        print(c(C.BOLD + C.CYAN, f"  {cat['name']}"))
        print(c(C.DIM, f"    {cat['description']}"))
        kw_preview = ", ".join(cat["keywords"][:4])
        if len(cat["keywords"]) > 4:
            kw_preview += f", +{len(cat['keywords']) - 4} more"
        print(c(C.DIM, f"    keywords: {kw_preview}"))
        print()


def main():
    parser = argparse.ArgumentParser(
        prog="netreason",
        description="net-reason — Network & Linux error diagnosis CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  netreason diagnose
  netreason diagnose "temporary failure in name resolution"
  netreason diagnose ssh
  netreason diagnose "could not get lock /var/lib/dpkg/lock"
  netreason list
        """
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    # diagnose
    diag_parser = subparsers.add_parser(
        "diagnose",
        help="Diagnose an error interactively",
        description="Diagnose a Linux/network error with guided Y/N questions."
    )
    diag_parser.add_argument(
        "error",
        nargs="*",
        metavar="ERROR",
        help="Error message or keyword (optional — will prompt if omitted)"
    )

    # list
    subparsers.add_parser(
        "list",
        help="List all supported error categories"
    )

    if len(sys.argv) == 1:
        parser.print_help()
        print()
        print(c(C.DIM, "  Quick start: netreason diagnose"))
        print()
        sys.exit(0)

    args = parser.parse_args()

    if args.command == "diagnose":
        cmd_diagnose(args)
    elif args.command == "list":
        cmd_list(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
