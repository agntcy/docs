#!/usr/bin/env python3
"""
Process website visits from GitHub Gist and generate daily report

This script:
1. Fetches visit data from GitHub Gist
2. Aggregates data by day, page, referrer
3. Generates a daily report
4. Archives processed data
"""

import os
import sys
import json
from datetime import datetime, timezone
from collections import defaultdict, Counter
from pathlib import Path

# Configuration
GIST_ID = os.environ.get('GIST_ID', 'YOUR_GIST_ID_HERE')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')

SCRIPT_DIR = Path(__file__).parent
REPORT_FILE = SCRIPT_DIR / 'visit_report.md'
STATS_FILE = SCRIPT_DIR / 'visit_stats.json'
ARCHIVE_DIR = SCRIPT_DIR / 'visit_archive'


def fetch_gist_data():
    """Fetch visit data from GitHub Gist."""
    import urllib.request

    url = f'https://api.github.com/gists/{GIST_ID}'
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }

    if GITHUB_TOKEN:
        headers['Authorization'] = f'Bearer {GITHUB_TOKEN}'

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            gist = json.loads(response.read().decode())

            # Get first file content
            filename = list(gist['files'].keys())[0]
            content = gist['files'][filename]['content']

            return content, filename
    except Exception as e:
        print(f"Error fetching gist: {e}", file=sys.stderr)
        return None, None


def parse_visits(content):
    """Parse JSONL content into visit records."""
    visits = []

    if not content:
        return visits

    for line in content.strip().split('\n'):
        if not line:
            continue
        try:
            visit = json.loads(line)
            visits.append(visit)
        except json.JSONDecodeError as e:
            print(f"Warning: Skipping invalid line: {e}", file=sys.stderr)

    return visits


def aggregate_visits(visits):
    """Aggregate visits by various dimensions."""
    stats = {
        'total_visits': len(visits),
        'by_date': defaultdict(int),
        'by_page': Counter(),
        'by_referrer': Counter(),
        'by_device': Counter(),
        'unique_dates': set(),
        'date_range': {'start': None, 'end': None}
    }

    for visit in visits:
        date = visit.get('date', '')
        path = visit.get('path', '/')
        ref = visit.get('ref', 'direct')
        device = visit.get('device', 'desktop')

        if date:
            stats['by_date'][date] += 1
            stats['unique_dates'].add(date)

        stats['by_page'][path] += 1
        stats['by_referrer'][ref] += 1
        stats['by_device'][device] += 1

    # Calculate date range
    if stats['unique_dates']:
        sorted_dates = sorted(stats['unique_dates'])
        stats['date_range']['start'] = sorted_dates[0]
        stats['date_range']['end'] = sorted_dates[-1]

    # Convert sets to lists for JSON serialization
    stats['unique_dates'] = len(stats['unique_dates'])
    stats['by_date'] = dict(stats['by_date'])
    stats['by_page'] = dict(stats['by_page'].most_common(20))
    stats['by_referrer'] = dict(stats['by_referrer'].most_common(10))
    stats['by_device'] = dict(stats['by_device'])

    return stats


def generate_report(stats):
    """Generate a markdown report."""
    now = datetime.now(timezone.utc)

    report = f"""# Website Visit Report - docs.agntcy.org

**Generated**: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}

## Summary

- **Total Visits**: {stats['total_visits']:,}
- **Unique Days**: {stats['unique_dates']}
- **Date Range**: {stats['date_range']['start']} to {stats['date_range']['end']}

## Top Pages

| Page | Visits |
|------|-------:|
"""

    for page, count in list(stats['by_page'].items())[:15]:
        report += f"| `{page}` | {count:,} |\n"

    report += "\n## Top Referrers\n\n| Referrer | Visits |\n|----------|-------:|\n"

    for ref, count in list(stats['by_referrer'].items())[:10]:
        report += f"| {ref} | {count:,} |\n"

    report += "\n## Device Distribution\n\n| Device | Visits | Percentage |\n|--------|-------:|-----------:|\n"

    total = stats['total_visits']
    for device, count in stats['by_device'].items():
        pct = (count / total * 100) if total > 0 else 0
        report += f"| {device.capitalize()} | {count:,} | {pct:.1f}% |\n"

    report += "\n## Daily Visits (Last 30 Days)\n\n| Date | Visits |\n|------|-------:|\n"

    sorted_dates = sorted(stats['by_date'].keys(), reverse=True)[:30]
    for date in sorted_dates:
        count = stats['by_date'][date]
        report += f"| {date} | {count:,} |\n"

    report += "\n---\n*Data collected from docs.agntcy.org visits*\n"

    return report


def save_report(report):
    """Save report to file."""
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ Report saved to {REPORT_FILE}")


def save_stats(stats):
    """Save statistics as JSON."""
    stats['last_updated'] = datetime.now(timezone.utc).isoformat()

    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    print(f"✓ Statistics saved to {STATS_FILE}")


def archive_data(content, filename):
    """Archive processed data."""
    if not content:
        return

    ARCHIVE_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    archive_file = ARCHIVE_DIR / f"{filename}_{timestamp}.jsonl"

    with open(archive_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Data archived to {archive_file}")


def clear_gist():
    """Clear the gist after processing (optional)."""
    import urllib.request

    if not GITHUB_TOKEN:
        print("No GitHub token, skipping gist clear")
        return

    url = f'https://api.github.com/gists/{GIST_ID}'

    # Get filename
    content, filename = fetch_gist_data()
    if not filename:
        return

    # Clear content
    data = json.dumps({
        'files': {
            filename: {
                'content': '# Processed - waiting for new data\n'
            }
        }
    }).encode()

    req = urllib.request.Request(
        url,
        data=data,
        method='PATCH',
        headers={
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'Bearer {GITHUB_TOKEN}',
            'Content-Type': 'application/json'
        }
    )

    try:
        with urllib.request.urlopen(req) as response:
            print("✓ Gist cleared")
    except Exception as e:
        print(f"Warning: Failed to clear gist: {e}", file=sys.stderr)


def main():
    """Main execution."""
    print("Processing website visits from GitHub Gist...\n")

    # Fetch data
    content, filename = fetch_gist_data()

    if not content:
        print("No data to process")
        return

    print(f"Fetched {len(content)} bytes from Gist")

    # Parse visits
    visits = parse_visits(content)
    print(f"Parsed {len(visits)} visits")

    if len(visits) == 0:
        print("No visits to process")
        return

    # Aggregate
    stats = aggregate_visits(visits)

    # Generate report
    report = generate_report(stats)
    save_report(report)

    # Save stats
    save_stats(stats)

    # Archive data
    archive_data(content, filename.replace('.jsonl', ''))

    # Clear gist (optional - comment out if you want to keep data)
    # clear_gist()

    print(f"\n✓ Processing complete!")
    print(f"  Total visits: {stats['total_visits']:,}")
    print(f"  Date range: {stats['date_range']['start']} to {stats['date_range']['end']}")


if __name__ == '__main__':
    main()


