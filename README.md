# 🔍 Secret Message Decoder

A Python tool that takes a Google Doc URL and reveals a hidden image made from Unicode characters.

---

## Overview

This tool fetches a specially formatted Google Doc, reads a table of character positions, and prints them as a 2D grid. When rendered in a fixed-width font, the characters form a visual pattern or secret message.

---

## How It Works

### 1. Fetch the Document
The program converts the Google Doc link into a public HTML version and downloads it — no authentication required.

### 2. Parse the Table
The document contains a table with three columns:

| Column | Description |
|--------|-------------|
| `x` | Horizontal position (left → right) |
| `Character` | A Unicode block symbol (e.g. `█`, `▀`) |
| `y` | Vertical position (top → bottom) |

Each row represents one character and its location on the grid.

### 3. Build the Grid
A blank 2D grid is created and filled with spaces. Each character is placed at its `(x, y)` coordinate — like plotting points on a board.

### 4. Render Output
The grid is printed row by row. The aligned block characters reveal the hidden image or message.

---

## Installation

```bash
pip install requests beautifulsoup4
```

---

## Usage

**From the command line:**
```bash
python decode_secret.py "https://docs.google.com/document/d/e/<DOC_ID>/pub"
```

**From Python:**
```python
from decode_secret import decode_secret_message

decode_secret_message("https://docs.google.com/document/d/e/<DOC_ID>/pub")
```

---

## Example Output

Given a doc with the right coordinates, the output might look like:

```
█▀▀▀
█▀▀
█
```

Which spells out the letter **F**.

---

## Requirements

- Python 3.10+
- `requests`
- `beautifulsoup4`
