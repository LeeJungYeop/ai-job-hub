from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

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

                    items = soup.select(".dlua7o0")
                    if not items:
                        break

                    for item in items:
                        links = item.find_all("a", href=True)
                        job_link = None
                        for a in links:
                            if "GI_Read" in a.get("href", ""):
                                job_link = a
                                break

                        if not job_link:
                            continue

                        href = job_link["href"]
                        if href.startswith("/"):
                            href = f"https://www.jobkorea.co.kr{href}"

                        gi_match = re.search(r"GI_Read/(\d+)", href)
                        job_id = gi_match.group(1) if gi_match else href

                        # sentry component로 각 필드 추출
                        comps = {c.get("data-sentry-component"): c for c in item.find_all(attrs={"data-sentry-component": True})}

                        chips = item.find_all(attrs={"data-sentry-component": "GrayChip"})
                        chip_texts = [c.get_text(strip=True) for c in chips]

                        # GI_Read 링크: 빈텍스트(이미지) → 제목 → 회사명 순서
                        gi_links = [a for a in links if "GI_Read" in a.get("href", "")]
                        title = gi_links[1].get_text(strip=True) if len(gi_links) > 1 else ""
                        company = gi_links[2].get_text(strip=True) if len(gi_links) > 2 else ""

                        jobs.append({
                            "id": f"jobkorea_{job_id}",
                            "title": title,
                            "company": company,
                            "location": chip_texts[0] if len(chip_texts) > 0 else "",
                            "experience": chip_texts[1] if len(chip_texts) > 1 else "",
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
        if job["id"] not in seen and job["title"]:
            seen.add(job["id"])
            unique.append(job)
    return unique


if __name__ == "__main__":
    jobs = fetch_jobs()
    print(f"잡코리아: {len(jobs)}개")
    for j in jobs[:3]:
        print(j)
