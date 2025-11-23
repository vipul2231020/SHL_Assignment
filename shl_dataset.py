import time
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_CATALOG_URL = "https://www.shl.com/products/product-catalog/"
BASE_DOMAIN = "https://www.shl.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def fetch_url(url, params=None, sleep_sec=1.0):
    """Fetch a URL safely with retry + polite delay."""
    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                
                time.sleep(sleep_sec)
                return resp.text
            else:
                print(f"[WARN] {url} -> status {resp.status_code}")
        except Exception as e:
            print(f"[ERROR] Fetch failed ({url}): {e}")
        time.sleep(2)
    return None


def extract_individual_links_from_page(html):
    """
    From one catalog page (Individual Test Solutions view),
    collect all product detail URLs + display names.
    """
    soup = BeautifulSoup(html, "html.parser")
    links = []

    
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/products/product-catalog/view/" in href:
            full_url = urljoin(BASE_DOMAIN, href)
            name = a.get_text(strip=True)
            if name and full_url:
                links.append((name, full_url))

    
    unique = {}
    for name, url in links:
        unique[url] = name
    return [(name, url) for url, name in unique.items()]


def crawl_all_individual_links(max_pages=50):
    """
    Crawl all Individual Test Solutions using ?type=1 & ?start=offset.
    It will stop automatically when no new links are found.
    """
    all_links = {}
    offset = 0
    page_index = 0
    page_size = 12  

    while page_index < max_pages:
        params = {"type": "1"}
        if offset > 0:
            params["start"] = str(offset)

        print(f"\n[INFO] Fetching catalog page index={page_index}, offset={offset}, params={params}")
        html = fetch_url(BASE_CATALOG_URL, params=params)
        if not html:
            print("[WARN] No HTML, breaking.")
            break

        page_links = extract_individual_links_from_page(html)
        print(f"[INFO] Found {len(page_links)} detail links on this page.")

        
        new_count = 0
        for name, url in page_links:
            if url not in all_links:
                all_links[url] = name
                new_count += 1

        print(f"[INFO] New links added from this page: {new_count}")

        
        if new_count == 0:
            print("[INFO] No new links on this page. Stopping crawl.")
            break

        offset += page_size
        page_index += 1

    print(f"\n[SUMMARY] Total unique Individual Test Solutions URLs collected: {len(all_links)}")
    return all_links  


def parse_assessment_detail(url):
    """
    Visit each product detail page and extract:
    name, description, job levels, languages, length, test type
    """
    html = fetch_url(url, sleep_sec=0.8)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    
    name_tag = soup.find("h1")
    name = name_tag.get_text(strip=True) if name_tag else ""

    
    description = ""
    desc_header = soup.find(lambda tag: tag.name in ["h3", "h4"] and "Description" in tag.get_text())
    if desc_header:
        
        next_p = desc_header.find_next("p")
        if next_p:
            description = next_p.get_text(" ", strip=True)

    
    job_levels = ""
    job_header = soup.find(lambda tag: tag.name in ["h3", "h4"] and "Job levels" in tag.get_text())
    if job_header:
        job_p = job_header.find_next("p")
        if job_p:
            job_levels = job_p.get_text(" ", strip=True)

    
    languages = ""
    lang_header = soup.find(lambda tag: tag.name in ["h3", "h4"] and "Languages" in tag.get_text())
    if lang_header:
        lang_p = lang_header.find_next("p")
        if lang_p:
            languages = lang_p.get_text(" ", strip=True)

    
    assessment_length_minutes = None
    length_text_node = soup.find(string=lambda t: t and "Approximate Completion Time in minutes" in t)
    if length_text_node:
        
        m = re.search(r"(\d+)", length_text_node)
        if m:
            assessment_length_minutes = int(m.group(1))

    
    test_type = ""
    test_type_node = soup.find(string=lambda t: t and "Test Type:" in t)
    if test_type_node:
        
        after = test_type_node.split("Test Type:")[-1]
        test_type = after.strip().strip(":").strip()

   

    return {
        "name": name,
        "url": url,
        "description": description,
        "job_levels": job_levels,
        "languages": languages,
        "assessment_length_minutes": assessment_length_minutes,
        "test_type": test_type,
    }


def main():
    
    all_links = crawl_all_individual_links()

    print("\n[INFO] Starting detail scraping for each assessment...")
    records = []
    total = len(all_links)
    for i, (url, name_from_list) in enumerate(all_links.items(), start=1):
        print(f"[{i}/{total}] Scraping detail: {name_from_list} -> {url}")
        data = parse_assessment_detail(url)
        if data is None:
            print(f"[WARN] Failed to parse detail for {url}")
            continue

        
        if not data["name"]:
            data["name"] = name_from_list

        records.append(data)

   
    df = pd.DataFrame(records)
    print("\n[SUMMARY] Final rows:", len(df))

    
    df = df.drop_duplicates(subset=["url"])
    print("[SUMMARY] After drop_duplicates by url:", len(df))

    output_file = "shl_individual_tests.csv"
    df.to_csv(output_file, index=False)
    print(f"\n DONE: Saved scraped data to {output_file}")


if __name__ == "__main__":
    main()
