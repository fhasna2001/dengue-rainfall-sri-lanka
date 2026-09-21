"""Offline, calendar-aligned analysis of the project's local CSV files."""
import csv
import math
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def correlation(pairs):
    if len(pairs) < 3:
        return None
    xs, ys = zip(*pairs)
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    denominator = math.sqrt(sum((x-mx)**2 for x in xs) * sum((y-my)**2 for y in ys))
    return sum((x-mx)*(y-my) for x, y in pairs) / denominator if denominator else None


def build_data():
    latest = {}
    revisions = 0
    with (ROOT / 'data/processed/dengue_weekly_by_district_raw.csv').open(newline='') as f:
        source = sorted(csv.DictReader(f), key=lambda r: (int(r['report_year']), int(r['report_week'])))
    for row in source:
        key = (row['district'], int(row['year']), int(row['week']))
        if key in latest and latest[key]['cases'] != row['cases']:
            revisions += 1
        latest[key] = row
    weather = defaultdict(dict)
    with (ROOT / 'data/raw/nasa_power_colombo_daily.csv').open(newline='') as f:
        for row in csv.DictReader(f):
            day = datetime.strptime(row['date'], '%Y%m%d').date()
            monday = day - timedelta(days=day.weekday())
            values = [float(row[k]) for k in ('PRECTOTCORR', 'T2M', 'RH2M')]
            if all(math.isfinite(v) and v != -999 for v in values):
                weather[monday][day] = values
    weekly = {day: {'rainfall': round(sum(v[0] for v in days.values()), 2),
                    'temperature': round(sum(v[1] for v in days.values()) / 7, 2),
                    'humidity': round(sum(v[2] for v in days.values()) / 7, 2)}
              for day, days in weather.items() if len(days) == 7}
    rows = []
    for (district, year, week), raw in sorted(latest.items()):
        day = date.fromisocalendar(year, week, 1)
        rows.append(dict(district=district, year=year, week=week, date=day.isoformat(),
                         cases=float(raw['cases']), report=f"{raw['report_year']} W{int(raw['report_week']):02}",
                         **(weekly.get(day, dict(rainfall=None, temperature=None, humidity=None))
                            if district == 'Colombo' else dict(rainfall=None, temperature=None, humidity=None))))
    lags = []
    colombo = [r for r in rows if r['district'] == 'Colombo']
    for lag in range(13):
        entry = {'lag': lag}
        for variable in ('rainfall', 'temperature', 'humidity'):
            pairs = [(weekly[day][variable], r['cases']) for r in colombo
                     if (day := date.fromisoformat(r['date']) - timedelta(weeks=lag)) in weekly]
            entry[variable] = correlation(pairs)
            entry['n'] = len(pairs)
        lags.append(entry)
    return {'rows': rows, 'lags': lags, 'revisions': revisions,
            'weather_weeks': len(weekly), 'report_count': len({(r['report_year'], r['report_week']) for r in source})}
