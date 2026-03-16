from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

KEYWORDS = ["AI", "ML", "머신러닝", "딥러닝", "인공지능", "데이터사이언스", "컴퓨터비전", "NLP", "LLM"]

def fetch_jobs():
    jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for keyword in KEYWORDS:
            for page_no in range(1, 6):
                url = f"https://www.jobkorea.co.kr/Search/?stext={keyword}&tabType=recruit&Page_No={page_no}"
                try:
                    page.goto(url, timeout=30000, wait_until="networkidle")
                    soup = BeautifulSoup(page.content(), "html.parser")

                    items = soup.select(".list-post .post-list-recruitment")
                    if not items:
                        items = soup.select("[class*='recruit'] li")
                    if not items:
                        break

                    for item in items:
                        title_tag = item.select_one("a.title, .title a, a[class*='title']")
                        company_tag = item.select_one(".company, .corp, [class*='company']")
                        location_tag = item.select_one(".location, .loc, [class*='location']")
                        exp_tag = item.select_one(".exp, .experience, [class*='exp']")

                        if not title_tag:
                            continue

                        href = title_tag.get("href", "")
                        if href.startswith("/"):
                            href = f"https://www.jobkorea.co.kr{href}"

                        job_id = href.split("GI_No=")[-1].split("&")[0] if "GI_No=" in href else href.split("/")[-1]

                        jobs.append({
                            "id": f"jobkorea_{job_id}",
                            "title": title_tag.get_text(strip=True),
                            "company": company_tag.get_text(strip=True) if company_tag else "",
                            "location": location_tag.get_text(strip=True) if location_tag else "",
                            "experience": exp_tag.get_text(strip=True) if exp_tag else "",
                            "company_size": "",
                            "url": href,
                            "source": "잡코리아",
                            "keyword": keyword,
                        })
                except Exception as e:
                    print(f"[jobkorea] {keyword} p{page_no} 오류: {e}")
                    break

        browser.close()

    seen = set()
    unique = []
    for job in jobs:
        if job["id"] not in seen:
            seen.add(job["id"])
            unique.append(job)
    return unique


if __name__ == "__main__":
    jobs = fetch_jobs()
    print(f"잡코리아: {len(jobs)}개")
