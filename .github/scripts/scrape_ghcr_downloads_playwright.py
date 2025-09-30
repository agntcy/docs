import asyncio
from playwright.async_api import async_playwright
import csv

ORG_URL = "https://github.com/orgs/agntcy/packages?type=container"

async def scrape_ghcr_downloads():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        containers = []
        # Get total number of pages
        page = await browser.new_page()
        await page.goto(ORG_URL, timeout=60000)
        await page.wait_for_selector("#org-packages", timeout=60000)
        pagination = await page.query_selector(".pagination")
        total_pages = 1
        if pagination:
            current = await pagination.query_selector("em.current")
            if current:
                total_pages = int(await current.get_attribute("data-total-pages") or "1")
        await page.close()
        # Scrape all pages
        for i in range(1, total_pages+1):
            url = f"https://github.com/orgs/agntcy/packages?page={i}&type=container"
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            await page.wait_for_selector("#org-packages", timeout=60000)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(2)
            for row in await page.query_selector_all("#org-packages ul li.Box-row"):
                name_tag = await row.query_selector('a.Link--primary')
                downloads_tag = await row.query_selector('span.color-fg-muted')
                if name_tag and downloads_tag:
                    name = (await name_tag.text_content()).strip()
                    downloads = (await downloads_tag.text_content()).strip()
                    containers.append({"name": name, "downloads": downloads})
            await page.close()
        await browser.close()
        import os
        output_path = os.path.join(os.path.dirname(__file__), "agntcy_ghcr_downloads.csv")
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "downloads"])
            writer.writeheader()
            writer.writerows(containers)
        print(f"Wrote {len(containers)} container download stats to {output_path}")

        # Write markdown report
        md_path = os.path.join(os.path.dirname(__file__), "agntcy_ghcr_downloads_report.md")
        with open(md_path, "w") as md:
            md.write(f"# AGNTCY GHCR Container Download Stats\n\n")
            md.write("| Container Name | Downloads |\n")
            md.write("|---------------|----------|\n")
            for c in containers:
                md.write(f"| {c['name']} | {c['downloads']} |\n")
        print(f"Wrote markdown report to {md_path}")

if __name__ == "__main__":
    asyncio.run(scrape_ghcr_downloads())
