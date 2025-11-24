#!/usr/bin/env python3
"""
Secure validation and extraction of visit data from GitHub issue body.

This script implements security measures:
1. Input validation and sanitization
2. JSON schema validation
3. Size limits
4. Field whitelisting
5. Path traversal prevention
"""

import sys
import json
import re
from datetime import datetime
from pathlib import Path

# Security Configuration
MAX_ISSUE_SIZE = 1_000_000  # 1MB max
MAX_VISITS_PER_ISSUE = 100  # Max 100 visits per issue
MAX_PATH_LENGTH = 500
MAX_REFERRER_LENGTH = 200
MAX_TIMESTAMP_LENGTH = 30
ALLOWED_DEVICES = {'mobile', 'tablet', 'desktop'}

# Expected fields with types
VISIT_SCHEMA = {
    'path': str,
    'ref': str,
    'device': str,
    'ts': str,
    'date': str
}


def validate_path(path: str) -> bool:
    """Validate URL path to prevent path traversal and injection."""
    if not path or not isinstance(path, str):
        return False

    if len(path) > MAX_PATH_LENGTH:
        return False

    # Must start with /
    if not path.startswith('/'):
        return False

    # Check for path traversal attempts
    if '..' in path or '~' in path:
        return False

    # Only allow safe characters
    if not re.match(r'^/[a-zA-Z0-9/_\-\.]*$', path):
        return False

    return True


def validate_referrer(ref: str) -> bool:
    """Validate referrer string."""
    if not ref or not isinstance(ref, str):
        return False

    if len(ref) > MAX_REFERRER_LENGTH:
        return False

    # Allow 'direct' or domain names
    if ref == 'direct':
        return True

    # Simple domain validation
    if not re.match(r'^[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}$', ref):
        return False

    return True


def validate_device(device: str) -> bool:
    """Validate device type."""
    if not isinstance(device, str):
        return False

    return device.lower() in ALLOWED_DEVICES


def validate_timestamp(ts: str) -> bool:
    """Validate ISO timestamp."""
    if not ts or not isinstance(ts, str):
        return False

    if len(ts) > MAX_TIMESTAMP_LENGTH:
        return False

    try:
        # Must be valid ISO format
        datetime.fromisoformat(ts.replace('Z', '+00:00'))
        return True
    except (ValueError, AttributeError):
        return False


def validate_date(date: str) -> bool:
    """Validate date string (YYYY-MM-DD)."""
    if not date or not isinstance(date, str):
        return False

    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        return False

    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_visit_record(visit: dict) -> tuple[bool, str]:
    """
    Validate a single visit record.

    Returns:
        (is_valid, error_message)
    """
    # Check all required fields present
    for field in VISIT_SCHEMA:
        if field not in visit:
            return False, f"Missing required field: {field}"

    # No extra fields allowed
    for field in visit:
        if field not in VISIT_SCHEMA:
            return False, f"Unexpected field: {field}"

    # Validate field types
    for field, expected_type in VISIT_SCHEMA.items():
        if not isinstance(visit[field], expected_type):
            return False, f"Invalid type for {field}: expected {expected_type.__name__}"

    # Validate path
    if not validate_path(visit['path']):
        return False, f"Invalid path: {visit['path']}"

    # Validate referrer
    if not validate_referrer(visit['ref']):
        return False, f"Invalid referrer: {visit['ref']}"

    # Validate device
    if not validate_device(visit['device']):
        return False, f"Invalid device: {visit['device']}"

    # Validate timestamp
    if not validate_timestamp(visit['ts']):
        return False, f"Invalid timestamp: {visit['ts']}"

    # Validate date
    if not validate_date(visit['date']):
        return False, f"Invalid date: {visit['date']}"

    return True, ""


def extract_jsonl_block(issue_body: str) -> str:
    """
    Safely extract JSONL block from issue body.

    Args:
        issue_body: The full issue body text

    Returns:
        Extracted JSONL content (may be empty)
    """
    if not issue_body or not isinstance(issue_body, str):
        return ""

    # Size check
    if len(issue_body) > MAX_ISSUE_SIZE:
        print(f"ERROR: Issue body too large: {len(issue_body)} bytes (max: {MAX_ISSUE_SIZE})",
              file=sys.stderr)
        return ""

    # Find JSONL code block
    pattern = r'```jsonl\s*\n(.*?)\n```'
    match = re.search(pattern, issue_body, re.DOTALL)

    if not match:
        print("ERROR: No JSONL code block found", file=sys.stderr)
        return ""

    return match.group(1).strip()


def parse_and_validate_visits(jsonl_content: str) -> list[dict]:
    """
    Parse and validate JSONL visit data.

    Args:
        jsonl_content: JSONL formatted visit data

    Returns:
        List of validated visit records
    """
    if not jsonl_content:
        return []

    visits = []
    lines = jsonl_content.strip().split('\n')

    # Check count limit
    if len(lines) > MAX_VISITS_PER_ISSUE:
        print(f"ERROR: Too many visits: {len(lines)} (max: {MAX_VISITS_PER_ISSUE})",
              file=sys.stderr)
        return []

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        # Parse JSON
        try:
            visit = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"ERROR: Line {line_num}: Invalid JSON: {e}", file=sys.stderr)
            continue

        # Validate record
        is_valid, error = validate_visit_record(visit)
        if not is_valid:
            print(f"ERROR: Line {line_num}: {error}", file=sys.stderr)
            continue

        visits.append(visit)

    return visits


def main():
    """Main execution."""
    # Read issue body from stdin
    issue_body = sys.stdin.read()

    # Extract JSONL block
    jsonl_content = extract_jsonl_block(issue_body)

    if not jsonl_content:
        print("ERROR: No valid JSONL content found", file=sys.stderr)
        sys.exit(1)

    # Parse and validate
    visits = parse_and_validate_visits(jsonl_content)

    if not visits:
        print("ERROR: No valid visits found", file=sys.stderr)
        sys.exit(1)

    # Output validated JSONL to stdout
    for visit in visits:
        print(json.dumps(visit, separators=(',', ':')))

    # Log success to stderr
    print(f"✓ Validated {len(visits)} visits", file=sys.stderr)


if __name__ == '__main__':
    main()

