# Dengue and weather in Sri Lanka

Run the offline dashboard from this folder with Python 3.10 or later:

```powershell
python app.py
```

Open **http://localhost:8000**. Stop with Ctrl+C. For another port, run
`python app.py --port 8001`. No extra packages or internet connection are needed
for the dashboard.

The dashboard includes reporting-area/year filters, case and rainfall charts,
Colombo weather correlations at calendar lags of 0–12 weeks, a weekly table,
and CSV download. JSON is available at `/api/data`.

## Data and limitations

The current dengue CSV contains four 2023 reports (weeks 1–4), including their
historical comparisons. It is sparse and is not updated through today.
Weather covers 2019–2024. Weather is matched to Colombo only; other areas
show cases with no weather values. Kalmunai is a reporting area within Ampara.

Duplicate area/year/week values use the latest report. Missing weeks are not
zero-filled. Weather uses Monday–Sunday ISO weeks: rainfall is summed and
temperature/humidity averaged, using only complete seven-day weeks. Lags match
calendar dates rather than row offsets. Correlations use all available Colombo
observations, independently of table filters. They do not establish causation.
The sample is too sparse for a reliable forecast; none is generated.

## Optional data preparation

The original scripts need requests, pandas and pdfplumber. `requirements.txt`
records the original full analysis environment. To use just the preparation scripts:

```powershell
python -m pip install requests pandas pdfplumber
python src/extract_dengue.py
```

Run these from the project root. The extractor reads `data/raw/dengue` and
writes `data/processed/dengue_weekly_by_district_raw.csv`. It assumes a specific
PDF table layout; check extraction and week labels for new report layouts.
The weather downloader is configured for 2019–2024. The dengue downloader uses
a manual 2026 URL list, not automatic discovery. Downloads require internet.
Refresh the dashboard after updating CSVs.

Run checks with `python -m unittest discover -s tests`.
