# Data Sources

## NASA POWER (weather)
- **Source:** NASA Prediction Of Worldwide Energy Resources (POWER), https://power.larc.nasa.gov
- **Access:** Daily point API, downloaded with `src/download_weather.py`
- **Location:** Colombo (6.9271 N, 79.8612 E)
- **Period:** 2019-01-01 to 2024-12-31
- **Variables:** PRECTOTCORR (rainfall, mm/day), T2M (temperature at 2 m, °C), RH2M (relative humidity at 2 m, %)
- **Downloaded:** 21 September 2026
- **Note:** Satellite and model-based grid data, not a weather station reading