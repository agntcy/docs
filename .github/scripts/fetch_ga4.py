import os
import csv
import json
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from google.oauth2 import service_account

def fetch_analytics_data():
    property_id = os.environ.get("GA4_PROPERTY_ID")
    service_account_json = os.environ.get("GA4_SERVICE_ACCOUNT_JSON")

    if not property_id:
        raise ValueError("Environment variable GA4_PROPERTY_ID must be set.")

    if not service_account_json:
        raise ValueError("Environment variable GA4_SERVICE_ACCOUNT_JSON must be set.")

    # Authenticate using the JSON string directly
    try:
        info = json.loads(service_account_json)
        credentials = service_account.Credentials.from_service_account_info(info)
        client = BetaAnalyticsDataClient(credentials=credentials)
    except json.JSONDecodeError:
        raise ValueError("GA4_SERVICE_ACCOUNT_JSON is not valid JSON.")

    print(f"Fetching data for property: {property_id}")

    # Define request - getting data for yesterday
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="date")],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="sessions"),
            Metric(name="screenPageViews"),
            Metric(name="eventCount")
        ],
        date_ranges=[DateRange(start_date="yesterday", end_date="yesterday")],
    )

    try:
        response = client.run_report(request)
    except Exception as e:
        print(f"Error fetching report: {e}")
        exit(1)

    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    csv_file = os.path.join(output_dir, "ga4_stats.csv")

    file_exists = os.path.isfile(csv_file)

    # Check if we already have data for these dates to avoid duplicates
    existing_dates = set()
    if file_exists:
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            try:
                next(reader) # Skip header
                for row in reader:
                    if row:
                        existing_dates.add(row[0])
            except StopIteration:
                pass

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write header if new file
        if not file_exists:
            headers = ['date', 'activeUsers', 'sessions', 'screenPageViews', 'eventCount']
            writer.writerow(headers)

        rows_added = 0
        for row in response.rows:
            date_str = row.dimension_values[0].value
            formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

            if formatted_date in existing_dates:
                print(f"Skipping {formatted_date} - already exists in file.")
                continue

            data_row = [
                formatted_date,
                row.metric_values[0].value, # activeUsers
                row.metric_values[1].value, # sessions
                row.metric_values[2].value, # screenPageViews
                row.metric_values[3].value  # eventCount
            ]
            writer.writerow(data_row)
            rows_added += 1
            print(f"Appended data for {formatted_date}")

        if rows_added == 0 and not response.rows:
             print("No data found for yesterday.")

if __name__ == "__main__":
    fetch_analytics_data()
