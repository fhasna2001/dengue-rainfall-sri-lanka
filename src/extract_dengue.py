"""Extract Table 1 (cases per district per week) from NDCU Weekly Dengue Update PDFs.

Run from the project root:  python src/extract_dengue.py
"""
import re
from datetime import date
from pathlib import Path

import pandas as pd
import pdfplumber

RAW_DIR = Path("data/raw/dengue")
OUT_FILE = Path("data/processed/dengue_weekly_by_district_raw.csv")

# A number, a number with a * (e.g. 71*), a decimal (64.00) or the word Nil
NUM = r"(?:\d+(?:\.\d+)?\*?|Nil)"
# A table row = district name followed by exactly 6 values
ROW = re.compile(rf"^([A-Za-z][A-Za-z ]*?)\*?\s+({NUM}(?:\s+{NUM}){{5}})\s*$")

# The same district is spelled differently in different years
NAME_FIX = {"Rathnapura": "Ratnapura"}


def year_week_from_filename(path):
    """'2023_Week_04.pdf' -> (2023, 4).  Returns None if it is not a weekly report."""
    m = re.search(r"(20\d{2}).*?week[_\- ]?(\d{1,2})", path.name, re.I)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def last_week_of(year):
    """Number of the last ISO week of a year (52 or 53)."""
    return date(year, 12, 28).isocalendar()[1]


def column_labels(year, week):
    """What (year, week) each of the first 4 numeric columns of Table 1 holds."""
    if week > 1:
        return [(year - 1, week - 1), (year - 1, week), (year, week - 1), (year, week)]
    # Week 1 reports look back across the New Year
    return [
        (year - 2, last_week_of(year - 2)), (year - 1, 1),
        (year - 1, last_week_of(year - 1)), (year, 1),
    ]


def to_number(token):
    token = token.replace("*", "")
    return 0.0 if token == "Nil" else float(token)


def read_table1(pdf_path):
    """Return the district rows of Table 1 as a list of (district, [6 numbers])."""
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        # The table is in the right-hand column; crop so the left text column
        # is not mixed into the same lines.
        right = page.crop((page.width * 0.53, 0, page.width, page.height))
        text = right.extract_text()
    rows = []
    for line in text.split("\n"):
        m = ROW.match(line.strip())
        if m:
            name = NAME_FIX.get(m.group(1).strip(), m.group(1).strip())
            rows.append((name, [to_number(t) for t in m.group(2).split()]))
    return rows


records = []
for pdf_path in sorted(RAW_DIR.glob("*.pdf")):
    yw = year_week_from_filename(pdf_path)
    if yw is None:
        print("Skipped (not a weekly report):", pdf_path.name)
        continue
    year, week = yw
    labels = column_labels(year, week)
    rows = read_table1(pdf_path)

    # --- Check 1: 26 districts + Total found
    districts = [r for r in rows if r[0] != "Total"]
    total = [r for r in rows if r[0] == "Total"]
    print(f"{pdf_path.name}: {len(districts)} districts, total row found: {bool(total)}")

    # --- Check 2: districts add up to the Total row (weekly columns)
    if total:
        for i in range(4):
            s = sum(r[1][i] for r in districts)
            if s != total[0][1][i]:
                print(f"   WARNING column {i}: districts sum to {s}, Total says {total[0][1][i]}")

    for name, values in rows:
        for (y, w), cases in zip(labels, values[:4]):
            records.append({
                "report_year": year, "report_week": week,
                "district": name, "year": y, "week": w, "cases": cases,
            })

df = pd.DataFrame(records)
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_FILE, index=False)
print("Saved", len(df), "rows to", OUT_FILE)