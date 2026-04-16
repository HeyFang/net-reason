"""
Walks a decision tree for a given category, asking Y/N questions,
and returns the final diagnosis node.
"""

from .ui import ask_yn, print_info, print_warning


def walk_tree(tree: dict, depth: int = 0) -> dict | None:
    """
    Recursively walk the decision tree.
    Each node is either:
      - A question node: { "question": ..., "yes": <node>, "no": <node> }
      - A leaf node:     { "diagnosis": ..., "cause": ..., "fixes": [...], "docs": ... }

    Returns the leaf node dict, or None if user quits.
    """
    # Leaf node — we're done
    if "diagnosis" in tree:
        return tree

    # Question node
    question = tree.get("question")
    if not question:
        print_warning("Malformed knowledge base entry — missing question.")
        return None

    answer = ask_yn(question)

    if answer is None:
        return None  # User quit

    branch = tree.get("yes") if answer else tree.get("no")

    if branch is None:
        print_warning("Knowledge base has no branch for that answer.")
        return None

    return walk_tree(branch, depth + 1)


def run_diagnosis(category: dict) -> dict | None:
    """
    Entry point for the diagnosis engine.
    Takes a category dict from the knowledge base and runs the Q/A flow.
    Returns the diagnosis dict or None.
    """
    tree = category.get("tree")
    if not tree:
        print_warning(f"No decision tree found for category: {category.get('name')}")
        return None

    return walk_tree(tree)
