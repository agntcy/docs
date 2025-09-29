
import requests
import csv
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "agntcy_pypi_stats_full.csv")

agntcy_pkgs = [
    "agntcy-app-sdk",
    "metrics-computation-engine",
    "ioa-observe-sdk",
    "agntcy-dir",
    "slim-mcp",
    "slima2a",
    "slimrpc",
    "slim-bindings",
    "mce-metrics-plugin",
    "mce-ragas-adapter",
    "mce-opik-adapter",
    "mce-deepeval-adapter",
    "agntcy-identity-sdk",
    "agntcy-dir-sdk",
    "ioa-metrics-computation-engine",
    "agntcy-dir-client-sdk",
    "agntcy-acp",
    "agp-mcp",
    "agp-bindings",
    "agntcy-iomapper",
    "agntcy-pypi-sample"
]

rows = []
for pkg in agntcy_pkgs:
    meta_url = f"https://pypi.org/pypi/{pkg}/json"
    r = requests.get(meta_url)
    version = ""
    if r.status_code == 200:
        info = r.json().get("info", {})
        version = info.get("version", "")
    # Get downloads
    stats_url = f"https://pypistats.org/api/packages/{pkg}/recent"
    s = requests.get(stats_url)
    last_day = last_week = last_month = ""
    if s.status_code == 200:
        stats = s.json().get("data", {})
        last_day = stats.get("last_day", 0)
        last_week = stats.get("last_week", 0)
        last_month = stats.get("last_month", 0)
    rows.append({
        "name": pkg,
        "version": version,
        "last_day_downloads": last_day,
        "last_week_downloads": last_week,
        "last_month_downloads": last_month
    })

with open(CSV_PATH, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["name", "version", "last_day_downloads", "last_week_downloads", "last_month_downloads"])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
print(f"Wrote {len(rows)} agntcy-maintained PyPI packages to {CSV_PATH}")

# Write markdown report
MD_PATH = os.path.join(os.path.dirname(__file__), "agntcy_pypi_stats_report.md")
with open(MD_PATH, "w") as mdfile:
    mdfile.write("# AGNTCY PyPI Package Download Stats\n\n")
    mdfile.write("| Package | Version | Last Day | Last Week | Last Month |\n")
    mdfile.write("|---------|---------|----------|-----------|------------|\n")
    for row in rows:
        mdfile.write(f"| {row['name']} | {row['version']} | {row['last_day_downloads']} | {row['last_week_downloads']} | {row['last_month_downloads']} |\n")
print(f"Wrote markdown report to {MD_PATH}")
