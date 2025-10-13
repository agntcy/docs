/**
 * Secure Visit Tracker for docs.agntcy.org
 *
 * Security: No tokens exposed! Uses GitHub Issues as secure submission endpoint.
 *
 * Flow:
 * 1. Collect visits in localStorage
 * 2. Create GitHub Issue with visit data (no auth needed for public repos)
 * 3. GitHub Actions processes issue and stores in Gist (server-side, secure)
 * 4. Issue auto-closes after processing
 */

(function() {
  'use strict';

  // Configuration - NO TOKENS NEEDED!
  const CONFIG = {
    repo: 'agntcy/docs',               // Your repository
    batchSize: 50,                      // Submit after 50 visits
    submitInterval: 10 * 60 * 1000,    // Or every 10 minutes
    issueLabel: 'visit-data',          // Label for auto-processing
  };

  const STORAGE_KEY = 'docs_visits';
  const LAST_SUBMIT_KEY = 'docs_last_submit';

  // Privacy checks
  function shouldTrack() {
    // Don't track on localhost
    if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
      return false;
    }

    // Respect Do Not Track
    if (navigator.doNotTrack === '1' || window.doNotTrack === '1') {
      return false;
    }

    // Skip bots
    if (/bot|crawler|spider|headless/i.test(navigator.userAgent)) {
      return false;
    }

    return true;
  }

  // Collect visit data
  function collectVisit() {
    const now = new Date();
    return {
      path: location.pathname,
      ref: document.referrer ? new URL(document.referrer).hostname : 'direct',
      device: window.innerWidth < 768 ? 'mobile' : window.innerWidth < 1024 ? 'tablet' : 'desktop',
      ts: now.toISOString(),
      date: now.toISOString().split('T')[0]
    };
  }

  // Store in localStorage
  function storeVisit(visit) {
    try {
      const visits = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
      visits.push(visit);

      // Keep only last 200 visits
      if (visits.length > 200) {
        visits.splice(0, visits.length - 200);
      }

      localStorage.setItem(STORAGE_KEY, JSON.stringify(visits));
      return visits;
    } catch (e) {
      console.debug('Storage failed:', e);
      return [];
    }
  }

  // Get stored visits
  function getVisits() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    } catch (e) {
      return [];
    }
  }

  // Clear stored visits
  function clearVisits() {
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (e) {}
  }

  // Submit visits via GitHub Issue (NO TOKEN REQUIRED!)
  async function submitViaIssue(visits) {
    if (!visits || visits.length === 0) return false;

    try {
      // Format as JSONL
      const jsonl = visits.map(v => JSON.stringify(v)).join('\n');

      // Create issue body
      const body = `<!-- AUTOMATED VISIT DATA - DO NOT EDIT -->

**Visits**: ${visits.length}
**Submitted**: ${new Date().toISOString()}

\`\`\`jsonl
${jsonl}
\`\`\`

<!-- This issue will be auto-processed and closed by GitHub Actions -->`;

      const title = `[Visit Data] ${visits.length} visits - ${new Date().toISOString().split('T')[0]}`;

      // Create issue using GitHub API (no authentication needed for public repos!)
      const response = await fetch(`https://api.github.com/repos/${CONFIG.repo}/issues`, {
        method: 'POST',
        headers: {
          'Accept': 'application/vnd.github.v3+json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: title,
          body: body,
          labels: [CONFIG.issueLabel, 'automated']
        })
      });

      if (response.status === 201) {
        console.debug(`Submitted ${visits.length} visits via issue`);
        clearVisits();
        localStorage.setItem(LAST_SUBMIT_KEY, Date.now().toString());
        return true;
      } else {
        const error = await response.text();
        console.debug('Issue creation failed:', response.status, error);
        return false;
      }
    } catch (e) {
      console.debug('Submit error:', e);
      return false;
    }
  }

  // Check if should submit
  function shouldSubmit(visits) {
    // Submit if batch size reached
    if (visits.length >= CONFIG.batchSize) {
      return true;
    }

    // Submit if interval passed and have data
    try {
      const lastSubmit = parseInt(localStorage.getItem(LAST_SUBMIT_KEY) || '0');
      if (Date.now() - lastSubmit > CONFIG.submitInterval) {
        return visits.length > 0;
      }
    } catch (e) {}

    return false;
  }

  // Track page visit
  function trackVisit() {
    if (!shouldTrack()) return;

    const visit = collectVisit();
    const visits = storeVisit(visit);

    // Auto-submit if conditions met
    if (shouldSubmit(visits)) {
      submitViaIssue(visits);
    }
  }

  // Initialize
  function init() {
    // Track initial page view
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
      trackVisit();
    } else {
      document.addEventListener('DOMContentLoaded', trackVisit);
    }

    // Track SPA navigation
    let lastPath = location.pathname;
    const observer = new MutationObserver(() => {
      if (location.pathname !== lastPath) {
        lastPath = location.pathname;
        trackVisit();
      }
    });

    if (document.body) {
      observer.observe(document.body, { childList: true, subtree: false });
    }

    // Submit on page unload
    window.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden') {
        const visits = getVisits();
        if (visits.length >= 10) { // Only submit if reasonable batch
          submitViaIssue(visits);
        }
      }
    });

    // Periodic check
    setInterval(() => {
      const visits = getVisits();
      if (shouldSubmit(visits)) {
        submitViaIssue(visits);
      }
    }, 60000); // Every minute
  }

  // Public API
  window.docsVisitTracker = {
    getVisits,
    clearVisits,
    submit: () => submitViaIssue(getVisits()),
    config: CONFIG
  };

  // Start
  init();

})();

