# smart_title.py  (drop-in)
from typing import List, Dict, Any

def smart_recenter_title(
    elements: List[Dict[str, Any]],
    *,
    title_tag: str = "title_block",
    target_origin: tuple = (50, 50),
    margin: int = 10
) -> None:
    """
    Moves the title block back to `target_origin` plus a small margin.
    Shifts the *entire drawing* so the title block stays visually
    at the chosen spot but relative positions are preserved.
    """

    # 1. locate the title block
    titles = [e for e in elements if e.get("tag") == title_tag]
    if not titles:
        return  # nothing to do
    title = titles[0]

    # 2. compute shift vector
    dx = target_origin[0] - title["x"]
    dy = target_origin[1] - title["y"]

    # 3. apply shift to *every* element
    for el in elements:
        el["x"] += dx
        el["y"] += dy