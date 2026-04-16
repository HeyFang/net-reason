"""
Matches an error string to a category in the knowledge base.
"""

import re


def match_category(error_text: str, categories: list) -> list:
    """
    Returns a ranked list of (score, category) tuples for the given error text.
    Higher score = better match.
    """
    error_lower = error_text.lower()
    scores = []

    for cat in categories:
        score = 0
        for keyword in cat["keywords"]:
            if keyword.lower() in error_lower:
                # Longer/more specific keywords score higher
                score += len(keyword.split())
        if score > 0:
            scores.append((score, cat))

    # Sort descending by score
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores


def pick_category(error_text: str, categories: list, auto: bool = False):
    """
    Returns the best matching category dict, or prompts the user to choose.
    Returns None if user exits.
    """
    from .ui import print_header, print_info, print_warning, prompt_choice

    matches = match_category(error_text, categories)

    if not matches:
        return None

    # Single strong match — use it directly
    if len(matches) == 1 or (matches[0][0] >= 3 and (len(matches) < 2 or matches[0][0] > matches[1][0] * 1.5)):
        if not auto:
            print_info(f"Matched category: {matches[0][1]['name']}")
        return matches[0][1]

    # Multiple possible matches — let the user pick
    if not auto:
        print_warning("Multiple possible categories found. Which best describes your issue?\n")
        options = [(cat["name"], cat["description"]) for _, cat in matches[:5]]
        idx = prompt_choice(options)
        if idx is None:
            return None
        return matches[idx][1]

    return matches[0][1]
