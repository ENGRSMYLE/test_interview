import requests
from bs4 import BeautifulSoup


def decode_secret_message(url: str) -> None:
    export_url = _to_export_url(url)
    response = requests.get(export_url, timeout=15)
    response.raise_for_status()

    # ── 2. Parse the HTML table ───────────────────────────────────────────────
    soup = BeautifulSoup(response.text, "html.parser")
    entries = _parse_table(soup)          # list of (char, x, y)

    # ── 3. Build the grid ─────────────────────────────────────────────────────
    if not entries:
        print("(no data found)")
        return

    max_x = max(x for _, x, _ in entries)
    max_y = max(y for _, _, y in entries)

    # Fill with spaces; address as grid[row][col] → grid[y][x]
    grid = [[" "] * (max_x + 1) for _ in range(max_y + 1)]
    for char, x, y in entries:
        grid[y][x] = char

    # ── 4. Print ──────────────────────────────────────────────────────────────
    for row in grid:
        print("".join(row))


# ── Helpers ───────────────────────────────────────────────────────────────────

def _to_export_url(url: str) -> str:
    import re

    # Handle /e/ published URLs: /document/d/e/<ID>/pub
    match = re.search(r"/document/d/e/([^/]+)", url)
    if match:
        published_id = match.group(1)
        return f"https://docs.google.com/document/d/e/{published_id}/pub?output=html"

    # Handle regular /d/<ID> URLs
    match = re.search(r"/document/d/([^/]+)", url)
    if match:
        doc_id = match.group(1)
        return f"https://docs.google.com/document/d/{doc_id}/export?format=html"

    # Assume the caller already passed a usable URL
    return url


def _parse_table(soup: BeautifulSoup) -> list[tuple[str, int, int]]:
    table = soup.find("table")
    if table is None:
        return []

    rows = table.find_all("tr")
    entries: list[tuple[str, int, int]] = []

    for row in rows[1:]:          
        cells = row.find_all(["td", "th"])
        if len(cells) < 3:
            continue

        texts = [c.get_text(strip=True) for c in cells]

        try:
            x    = int(texts[0])
            char = texts[1]       
            y    = int(texts[2])
        except (ValueError, IndexError):
            continue              

        if char:                  
            entries.append((char, x, y))

    return entries


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python decode_secret.py <google-doc-url>")
        sys.exit(1)

    decode_secret_message(sys.argv[1])


# Engr Smyle  
