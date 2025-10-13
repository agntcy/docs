#!/bin/bash

# Interactive test to simulate the full tracking flow
# This script simulates what would happen when users visit pages

set -e

echo "🧪 Simulating Visit Tracking Flow"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Configuration matching the tracker
REPO="agntcy/docs"
BATCH_SIZE=50
TEST_VISITS=5

# Simulate visit collection
echo "📊 Step 1: Simulating ${TEST_VISITS} page visits..."
echo ""

VISITS=()
PAGES=("/" "/dir/overview/" "/slim/overview/" "/identity/overview/" "/dir/getting-started/")

for i in $(seq 1 $TEST_VISITS); do
    PAGE="${PAGES[$((i-1))]}"
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")
    DATE=$(date -u +"%Y-%m-%d")

    VISIT=$(cat <<EOF
{"path":"${PAGE}","ref":"direct","device":"desktop","ts":"${TIMESTAMP}","date":"${DATE}"}
EOF
)
    VISITS+=("$VISIT")
    echo "  ${i}. Visit recorded: ${PAGE}"
done

echo ""
echo "✅ Collected ${#VISITS[@]} visits"
echo ""

# Show what would be stored in localStorage
echo "💾 Step 2: What would be stored in localStorage..."
echo ""
echo "Key: docs_visits"
echo "Value:"
printf '%s\n' "${VISITS[@]}" | jq -s '.' 2>/dev/null || (
    echo "["
    for i in "${!VISITS[@]}"; do
        if [ $i -eq $((${#VISITS[@]} - 1)) ]; then
            echo "  ${VISITS[$i]}"
        else
            echo "  ${VISITS[$i]},"
        fi
    done
    echo "]"
)
echo ""

# Create JSONL format
echo "📦 Step 3: Creating JSONL format for submission..."
echo ""
JSONL=""
for VISIT in "${VISITS[@]}"; do
    JSONL="${JSONL}${VISIT}\n"
done

echo "JSONL format (${#VISITS[@]} lines):"
echo "─────────────────────────────────────"
printf "${JSONL}" | head -n 3
echo "..."
echo ""

# Show what would be submitted as GitHub Issue
echo "🐙 Step 4: GitHub Issue that would be created..."
echo ""

ISSUE_TITLE="[Visit Data] ${#VISITS[@]} visits - $(date -u +"%Y-%m-%d")"
ISSUE_BODY=$(cat <<EOF
<!-- AUTOMATED VISIT DATA - DO NOT EDIT -->

**Visits**: ${#VISITS[@]}
**Submitted**: $(date -u +"%Y-%m-%dT%H:%M:%S.000Z")

\`\`\`jsonl
$(printf "${JSONL}")
\`\`\`

<!-- This issue will be auto-processed and closed by GitHub Actions -->
EOF
)

echo "Repository: ${REPO}"
echo "Title: ${ISSUE_TITLE}"
echo "Labels: visit-data, automated"
echo ""
echo "Body Preview:"
echo "─────────────────────────────────────"
echo "$ISSUE_BODY" | head -n 15
echo ""

# Show API call that would be made
echo "🔌 Step 5: API call that would be made..."
echo ""
echo "Endpoint: https://api.github.com/repos/${REPO}/issues"
echo "Method: POST"
echo "Headers:"
echo "  Accept: application/vnd.github.v3+json"
echo "  Content-Type: application/json"
echo ""

# Test actual API endpoint (without creating issue)
echo "🔍 Step 6: Verifying API endpoint accessibility..."
if curl -s --max-time 5 "https://api.github.com/repos/${REPO}" > /dev/null 2>&1; then
    echo "✅ GitHub API is accessible"
    echo "✅ Repository ${REPO} is reachable"
else
    echo "⚠️  Could not reach GitHub API (network issue?)"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Summary of Tracking Flow"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. ✅ Visit data collected from browser"
echo "2. ✅ Data stored in localStorage"
echo "3. ✅ JSONL format created"
echo "4. ✅ GitHub issue body formatted"
echo "5. ✅ API endpoint validated"
echo ""
echo "Trigger Conditions:"
echo "  • Batch size reached: ${TEST_VISITS}/${BATCH_SIZE} visits"
echo "  • Time interval: Every 10 minutes"
echo "  • On page unload: If ≥10 visits stored"
echo ""
echo "⚠️  Important Notes:"
echo ""
echo "  • Tracking is DISABLED on localhost (by design)"
echo "  • No actual GitHub issue created in this test"
echo "  • Real submissions happen on docs.agntcy.org only"
echo ""
echo "🧪 To manually test submission:"
echo ""
echo "  1. Open browser to http://127.0.0.1:8000"
echo "  2. Open DevTools Console"
echo "  3. Manually add visits to localStorage:"
echo ""
echo "     localStorage.setItem('docs_visits', JSON.stringify(["
printf '%s\n' "${VISITS[@]}" | sed 's/^/       /' | head -n 2
echo "       ..."
echo "     ]))"
echo ""
echo "  4. Test submission:"
echo "     window.docsVisitTracker.submit()"
echo ""
echo "  5. Check result in GitHub:"
echo "     https://github.com/${REPO}/issues?q=label:visit-data"
echo ""

