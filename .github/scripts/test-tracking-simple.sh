#!/bin/bash

# Simple CLI test for visit tracking
# Tests that the tracking script is loaded and validates its presence

set -e

BASE_URL="http://127.0.0.1:8000"
TRACKER_PATH="/javascripts/visit-tracker-secure.js"

echo "🧪 Testing visit tracking setup..."
echo ""

# Test 1: Check if server is running
echo "Test 1: Checking if docs server is running..."
if curl -s --max-time 5 "${BASE_URL}" > /dev/null 2>&1; then
    echo "✅ Server is running at ${BASE_URL}"
else
    echo "❌ Server is not responding at ${BASE_URL}"
    echo "   Please run: task run"
    exit 1
fi
echo ""

# Test 2: Check if tracking script exists
echo "Test 2: Checking if tracking script is available..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}${TRACKER_PATH}")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Tracking script found at ${TRACKER_PATH}"
else
    echo "❌ Tracking script not found (HTTP ${HTTP_CODE})"
    exit 1
fi
echo ""

# Test 3: Check if script is included in pages
echo "Test 3: Checking if tracking script is included in pages..."
if curl -s "${BASE_URL}" | grep -q "visit-tracker-secure.js"; then
    echo "✅ Tracking script is included in the HTML"
else
    echo "❌ Tracking script not found in HTML"
    exit 1
fi
echo ""

# Test 4: Validate script content
echo "Test 4: Validating script content..."
SCRIPT_CONTENT=$(curl -s "${BASE_URL}${TRACKER_PATH}")

# Check for key components
if echo "$SCRIPT_CONTENT" | grep -q "docsVisitTracker"; then
    echo "  ✅ Found window.docsVisitTracker API"
else
    echo "  ❌ Missing window.docsVisitTracker API"
    exit 1
fi

if echo "$SCRIPT_CONTENT" | grep -q "shouldTrack"; then
    echo "  ✅ Found shouldTrack function"
else
    echo "  ❌ Missing shouldTrack function"
    exit 1
fi

if echo "$SCRIPT_CONTENT" | grep -q "submitViaIssue"; then
    echo "  ✅ Found submitViaIssue function"
else
    echo "  ❌ Missing submitViaIssue function"
    exit 1
fi

if echo "$SCRIPT_CONTENT" | grep -q "agntcy/docs"; then
    echo "  ✅ Found correct repo configuration"
else
    echo "  ❌ Missing or incorrect repo configuration"
    exit 1
fi

echo ""

# Test 5: Check localhost protection
echo "Test 5: Verifying localhost protection..."
if echo "$SCRIPT_CONTENT" | grep -q "localhost.*127.0.0.1"; then
    echo "✅ Localhost protection is enabled (won't track on local dev)"
else
    echo "⚠️  Warning: Localhost protection might be disabled"
fi
echo ""

# Summary
echo "═══════════════════════════════════════════════"
echo "🎉 Basic tracking setup validated successfully!"
echo "═══════════════════════════════════════════════"
echo ""
echo "📋 Tracking Configuration:"
curl -s "${BASE_URL}${TRACKER_PATH}" | grep -A 5 "const CONFIG = {" | head -n 6
echo ""
echo "🔍 To test in browser:"
echo "  1. Open: ${BASE_URL}"
echo "  2. Open DevTools Console (F12)"
echo "  3. Type: window.docsVisitTracker"
echo "  4. Check storage: window.docsVisitTracker.getVisits()"
echo ""
echo "⚠️  Note: Tracking is disabled on localhost by design."
echo "   Use browser console commands to test manually."
echo ""
echo "Available browser commands:"
echo "  • window.docsVisitTracker.getVisits()  - View stored visits"
echo "  • window.docsVisitTracker.clearVisits() - Clear storage"
echo "  • window.docsVisitTracker.submit()     - Submit to GitHub"
echo "  • window.docsVisitTracker.config       - View configuration"

