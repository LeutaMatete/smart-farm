"""Download daily historical weather for one site from Open-Meteo (no API key)."""
import csv
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SITE = {
    "name": "qachas_nek",
    "latitude": -30.12,
    "longitude": 28.68,
    "timezone": "Africa/Maseru",
}
START, END = "2016-01-01", "2025-12-31"
DAILY = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "precipitation_sum",
    "et0_fao_evapotranspiration",
]
URL = "https://archive-api.open-meteo.com/v1/archive"


def fetch(site, start, end):
    params = {
        "latitude": site["latitude"],
        "longitude": site["longitude"],
        "start_date": start,
        "end_date": end,
        "daily": ",".join(DAILY),
        "timezone": site["timezone"],
    }
    url = URL + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:500]}")


def save(data, path):
    d = data["daily"]
    rows = zip(
        d["time"],
        d["temperature_2m_max"],
        d["temperature_2m_min"],
        d["temperature_2m_mean"],
        d["precipitation_sum"],
        d["et0_fao_evapotranspiration"],
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "tmax_c", "tmin_c", "tmean_c", "precip_mm", "et0_mm"])
        w.writerows(rows)
    return len(d["time"])


if __name__ == "__main__":
    data = fetch(SITE, START, END)
    out = Path("simulator/climates") / f"{SITE['name']}_daily.csv"
    n = save(data, out)
    print(f"Saved {n} days to {out}")
    print("Grid cell elevation (m):", data.get("elevation"))
    print("Grid cell lat/lon:", data.get("latitude"), data.get("longitude"))