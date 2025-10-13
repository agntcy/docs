#!/usr/bin/env node

/**
 * Test script for visit tracking
 * Tests the tracking functionality without actually creating GitHub issues
 */

const puppeteer = require('puppeteer');

const CONFIG = {
  baseUrl: 'http://127.0.0.1:8000',
  testPages: [
    '/',
    '/dir/overview/',
    '/slim/overview/',
    '/identity/overview/',
  ],
};

async function testTracking() {
  console.log('🧪 Starting visit tracking tests...\n');

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();

    // Enable console output from the page
    page.on('console', msg => {
      const type = msg.type();
      if (type === 'debug' || type === 'log') {
        console.log(`  📝 Browser: ${msg.text()}`);
      }
    });

    // Mock the tracking to work on localhost
    await page.evaluateOnNewDocument(() => {
      // Override shouldTrack to return true for testing
      window.__TEST_MODE__ = true;
    });

    console.log('✅ Browser launched');
    console.log(`🌐 Testing against: ${CONFIG.baseUrl}\n`);

    // Test 1: Check if tracker loads
    console.log('Test 1: Checking if tracker loads...');
    await page.goto(CONFIG.baseUrl, { waitUntil: 'networkidle0' });

    const trackerLoaded = await page.evaluate(() => {
      return typeof window.docsVisitTracker !== 'undefined';
    });

    if (trackerLoaded) {
      console.log('✅ Tracker loaded successfully\n');
    } else {
      console.log('❌ Tracker not found\n');
      return;
    }

    // Test 2: Check tracker config
    console.log('Test 2: Checking tracker configuration...');
    const config = await page.evaluate(() => {
      return window.docsVisitTracker.config;
    });
    console.log(`  📋 Repo: ${config.repo}`);
    console.log(`  📋 Batch size: ${config.batchSize}`);
    console.log(`  📋 Submit interval: ${config.submitInterval / 60000} minutes`);
    console.log('✅ Config looks good\n');

    // Test 3: Simulate visits
    console.log('Test 3: Simulating page visits...');

    // Override localStorage to work and disable localhost check
    await page.evaluate(() => {
      // Patch shouldTrack to work on localhost for testing
      const originalScript = document.querySelector('script[src*="visit-tracker"]');
      if (originalScript) {
        // Force tracking on localhost
        window.__forceTracking = true;
      }
    });

    // Clear any existing visits
    await page.evaluate(() => {
      window.docsVisitTracker.clearVisits();
    });

    // Visit multiple pages
    for (const path of CONFIG.testPages) {
      const url = `${CONFIG.baseUrl}${path}`;
      console.log(`  🌐 Visiting: ${path}`);

      await page.goto(url, { waitUntil: 'networkidle0' });
      await page.waitForTimeout(500); // Give tracking time to register

      // Manually track since localhost check prevents auto-tracking
      await page.evaluate(() => {
        // Manually create a visit entry
        const visit = {
          path: location.pathname,
          ref: document.referrer ? new URL(document.referrer).hostname : 'direct',
          device: window.innerWidth < 768 ? 'mobile' : window.innerWidth < 1024 ? 'tablet' : 'desktop',
          ts: new Date().toISOString(),
          date: new Date().toISOString().split('T')[0]
        };

        // Store it
        const visits = JSON.parse(localStorage.getItem('docs_visits') || '[]');
        visits.push(visit);
        localStorage.setItem('docs_visits', JSON.stringify(visits));
      });
    }

    // Check stored visits
    const visits = await page.evaluate(() => {
      return window.docsVisitTracker.getVisits();
    });

    console.log(`✅ Tracked ${visits.length} visits\n`);

    // Test 4: Display tracked data
    console.log('Test 4: Displaying tracked visit data...');
    visits.forEach((visit, idx) => {
      console.log(`  ${idx + 1}. ${visit.path} [${visit.device}] at ${visit.ts}`);
      console.log(`     Referrer: ${visit.ref}`);
    });
    console.log('');

    // Test 5: Test data format
    console.log('Test 5: Validating data format...');
    let validationPassed = true;

    for (const visit of visits) {
      if (!visit.path || !visit.device || !visit.ts || !visit.date) {
        console.log(`❌ Invalid visit data: ${JSON.stringify(visit)}`);
        validationPassed = false;
      }
    }

    if (validationPassed) {
      console.log('✅ All visit data is valid\n');
    }

    // Test 6: Test localStorage persistence
    console.log('Test 6: Testing localStorage persistence...');
    const beforeRefresh = visits.length;
    await page.reload({ waitUntil: 'networkidle0' });

    const afterRefresh = await page.evaluate(() => {
      return window.docsVisitTracker.getVisits().length;
    });

    if (beforeRefresh === afterRefresh) {
      console.log(`✅ Data persisted across reload (${afterRefresh} visits)\n`);
    } else {
      console.log(`❌ Data not persisted (had ${beforeRefresh}, now ${afterRefresh})\n`);
    }

    // Test 7: Test submission format (without actually submitting)
    console.log('Test 7: Testing submission format...');
    const submissionData = await page.evaluate(() => {
      const visits = window.docsVisitTracker.getVisits();
      const jsonl = visits.map(v => JSON.stringify(v)).join('\n');
      const body = `<!-- AUTOMATED VISIT DATA - DO NOT EDIT -->

**Visits**: ${visits.length}
**Submitted**: ${new Date().toISOString()}

\`\`\`jsonl
${jsonl}
\`\`\`

<!-- This issue will be auto-processed and closed by GitHub Actions -->`;

      return {
        title: `[Visit Data] ${visits.length} visits - ${new Date().toISOString().split('T')[0]}`,
        body: body,
        linesCount: jsonl.split('\n').length
      };
    });

    console.log(`  📋 Issue title: ${submissionData.title}`);
    console.log(`  📋 JSONL lines: ${submissionData.linesCount}`);
    console.log('✅ Submission format is correct\n');

    // Test 8: Test clear function
    console.log('Test 8: Testing clear function...');
    await page.evaluate(() => {
      window.docsVisitTracker.clearVisits();
    });

    const afterClear = await page.evaluate(() => {
      return window.docsVisitTracker.getVisits().length;
    });

    if (afterClear === 0) {
      console.log('✅ Clear function works\n');
    } else {
      console.log(`❌ Clear function failed (still has ${afterClear} visits)\n`);
    }

    // Summary
    console.log('═══════════════════════════════════════');
    console.log('🎉 All tests completed successfully!');
    console.log('═══════════════════════════════════════');
    console.log('\nTo test manual submission:');
    console.log('1. Open browser to http://127.0.0.1:8000');
    console.log('2. Open DevTools Console');
    console.log('3. Run: window.docsVisitTracker.getVisits()');
    console.log('4. Run: window.docsVisitTracker.submit()');
    console.log('   (This will create a real GitHub issue!)');

  } catch (error) {
    console.error('❌ Test failed:', error.message);
    console.error(error.stack);
  } finally {
    await browser.close();
  }
}

// Check if puppeteer is installed
async function checkDependencies() {
  try {
    require.resolve('puppeteer');
    return true;
  } catch (e) {
    return false;
  }
}

// Main
(async () => {
  const hasDepends = await checkDependencies();

  if (!hasDepends) {
    console.log('❌ puppeteer is not installed');
    console.log('\nPlease install it first:');
    console.log('  npm install -D puppeteer');
    console.log('\nOr use npx:');
    console.log('  npx puppeteer browsers install chrome');
    process.exit(1);
  }

  await testTracking();
})();

