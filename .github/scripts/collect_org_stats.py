import re
# Scrape all package URLs from the agntcy org packages page
def get_all_package_urls(org):
    urls = []
    # Helper to extract package name and type from URL
    def parse_package_info(url):
        # Example: https://github.com/orgs/agntcy/packages/container/package/dir-apiserver
        m = re.match(r"https://github.com/orgs/[^/]+/packages/(?P<type>[^/]+)/package/(?P<name>.+)", url)
        if m:
            return m.group("name"), m.group("type")
        return url, "unknown"
    page = 1
    while True:
        url = f"https://github.com/orgs/{org}/packages?page={page}"
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        from bs4 import Tag
        links = soup.find_all("a", href=True)
        found = False
        for link in links:
            if isinstance(link, Tag):
                href = link.get("href")
                if isinstance(href, str) and href.startswith(f"/orgs/{org}/packages/container/package/"):
                    urls.append(f"https://github.com{href}")
                    found = True
        # If no package links found, break
        if not found:
            break
        page += 1
    return urls, parse_package_info
    urls = []
    page = 1
    while True:
        url = f"https://github.com/orgs/{org}/packages?page={page}"
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        from bs4 import Tag
        links = soup.find_all("a", href=True)
        found = False
        for link in links:
            if isinstance(link, Tag):
                href = link.get("href")
                if isinstance(href, str) and href.startswith(f"/orgs/{org}/packages/container/package/"):
                    urls.append(f"https://github.com{href}")
                    found = True
        # If no package links found, break
        if not found:
            break
        page += 1
    return urls
import os
import requests
import csv
from bs4 import BeautifulSoup

ORG = "agntcy"
GITHUB_API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}

CSV_PATH = os.path.join(os.path.dirname(__file__), "agntcy_org_stats.csv")

fields = [
    "name", "full_name", "description", "html_url", "created_at", "updated_at", "pushed_at",
    "stargazers_count", "forks_count", "open_issues_count", "archived", "disabled",
    "unique_views"
]

def get_all_repos(org):
    repos = []
    page = 1
    while True:
        url = f"{GITHUB_API}/orgs/{org}/repos?per_page=100&page={page}"
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def get_repo_views(owner, repo):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/traffic/views"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        return data.get("uniques", 0)
    return ""

def get_artifact_downloads(owner, repo):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/actions/artifacts"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        total = 0
        for artifact in data.get("artifacts", []):
            total += artifact.get("download_count", 0)
        return total
    return ""

# Scrape GitHub Packages download count for a given package URL
def scrape_package_downloads(package_url):
    # Instead of scraping the individual package page, scrape the org packages list page for all counts at once
    # This function will be replaced by scrape_all_package_downloads
    return None

# Scrape all package download counts from the org packages list page
def scrape_all_package_downloads(org):
    url = f"https://github.com/orgs/{org}/packages"
    resp = requests.get(url)
    resp.raise_for_status()
    html = resp.text
    # Regex to match: [name](url) ... <number>k
    # Example: [dir-apiserver](...) ... 9.49k
    pattern = re.compile(r"\[(?P<name>[^\]]+)\]\(https://github.com/orgs/[^/]+/packages/container/package/(?P<id>[^)]+)\)[^\n]*?(?P<count>[\d\.]+k|[\d,]+)")
    results = {}
    for match in pattern.finditer(html):
        name = match.group("name")
        count = match.group("count")
        # Convert k to integer
        if "k" in count:
            count = int(float(count.replace("k", "")) * 1000)
        else:
            count = int(count.replace(",", ""))
        results[name] = count
    return results

def main():
    repos = get_all_repos(ORG)
    # Scrape all package URLs and their download counts
    package_urls, parse_package_info = get_all_package_urls(ORG)
    # Scrape all package download counts from the org packages list page
    package_counts = scrape_all_package_downloads(ORG)
    package_info_list = []
    for url in package_urls:
        name, ptype = parse_package_info(url)
        count = package_counts.get(name, "")
        package_info_list.append({"name": name, "type": ptype, "download_count": count})

    # Write package stats to a separate CSV file
    package_csv_path = os.path.join(os.path.dirname(__file__), "agntcy_packages_stats.csv")
    with open(package_csv_path, "w", newline="") as pkgfile:
        pkg_writer = csv.DictWriter(pkgfile, fieldnames=["name", "type", "download_count"])
        pkg_writer.writeheader()
        for pkg in package_info_list:
            pkg_writer.writerow(pkg)

    # Write markdown report for package stats
    package_md_path = os.path.join(os.path.dirname(__file__), "agntcy_packages_stats_report.md")
    with open(package_md_path, "w") as md:
        md.write("# AGNTCY GitHub Packages Download Stats\n\n")
        md.write("| Package Name | Type | Downloads |\n")
        md.write("|--------------|------|-----------|\n")
        for pkg in package_info_list:
            md.write(f"| {pkg['name']} | {pkg['type']} | {pkg['download_count']} |\n")
    print(f"Wrote markdown report to {package_md_path}")

    with open(CSV_PATH, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for repo in repos:
            row = {key: repo.get(key, "") for key in fields}
            owner = repo.get("owner", {}).get("login", ORG)
            repo_name = repo.get("name", "")
            row["unique_views"] = get_repo_views(owner, repo_name)
            writer.writerow(row)
    print(f"Wrote {len(repos)} repos to {CSV_PATH}")
    print(f"Wrote {len(package_info_list)} packages to {package_csv_path}")

if __name__ == "__main__":
    main()
