"""Download the 2026 Weekly Dengue Update PDFs from the NDCU website."""
import time
from pathlib import Path

import requests

BASE = "https://www.dengue.health.gov.lk/wp-content/uploads/2026/"
OUT_DIR = Path("data/raw/dengue")

# week number -> path on the website (copied from the site's Weekly Report page)
REPORTS = {
    37: "09/Weekly-Dengue-Update-2026-Week-37.pdf",
    36: "09/Weekly-Dengue-Update-2026-Week-36.pdf",
    35: "09/Weekly-Dengue-Update-2026-Week-35.pdf",
    34: "08/Weekly-Dengue-Update-2026-Week-34.pdf",
    33: "08/Weekly-Dengue-Update-2026-Week-33.pdf",
    32: "08/Weekly-Dengue-Update-2026-Week-32.pdf",
    31: "08/Weekly-Dengue-Update-2026-Week-31-1.pdf",
    30: "08/Weekly-Dengue-Update-2026-Week-30.pdf",
    29: "07/Weekly-Dengue-Update-2026-Week-29.pdf",
    28: "07/Weekly-Dengue-Update-2026-Week-28.pdf",
    27: "07/Weekly-Dengue-Update-2026-Week-27.pdf",
    26: "07/Weekly-Dengue-Update-2026-Week-26.pdf",
    25: "06/Weekly-Dengue-Update-2026-Week-25.pdf",
    24: "06/Weekly-Dengue-Update-2026-Week-24.pdf",
    23: "06/weekly-dengue-update-2026-week-23.pdf",
    22: "06/weekly-dengue-update-2026-week-22.pdf",
    21: "06/Weekly-Dengue-Update-2026-Week-21.pdf",
    20: "08/Weekly-Dengue-Update-2026-Week-20.pdf",
    19: "06/Weekly-Dengue-Update-2026-Week-19.pdf",
    18: "08/Weekly-Dengue-Update-2026-Week-18.pdf",
    17: "06/Weekly-Dengue-Update-2026-Week-17.pdf",
    16: "06/Weekly-Dengue-Update-2026-Week-16.pdf",
}
# Weeks 1-12 are all in the 06 folder
for w in range(1, 13):
    REPORTS[w] = f"06/Weekly-Dengue-Update-2026-Week-{w:02d}.pdf"

OUT_DIR.mkdir(parents=True, exist_ok=True)
failed = []

for week in sorted(REPORTS):
    target = OUT_DIR / f"2026_Week_{week:02d}.pdf"
    if target.exists():
        print("Already have", target.name)
        continue
    url = BASE + REPORTS[week]
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        if not r.content.startswith(b"%PDF"):
            raise ValueError("not a PDF file")
        target.write_bytes(r.content)
        print("Downloaded", target.name)
    except Exception as e:
        print("FAILED week", week, "-", e)
        failed.append(week)
    time.sleep(1)  # be polite to the website

print("Failed weeks:", failed if failed else "none")