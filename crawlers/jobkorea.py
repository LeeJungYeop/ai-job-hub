import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

KEYWORDS = ["AI", "ML", "머신러닝", "딥러닝", "인공지능", "데이터사이언스", "컴퓨터비전", "NLP", "LLM"]

def fetch_jobs():
    jobs = []
    for keyword in KEYWORDS:
        for page in range(1, 6):
            url = f"https://www.jobkorea.co.kr/Search/?stext={keyword}&tabType=recruit&Page_No={page}"
            try:
                res = requests.get(url, headers=HEADERS, timeout=10)
                if res.status_code != 200:
                    break
                soup = BeautifulSoup(res.text, "html.parser")
                items = soup.select(".list-default li.recruit-list")
                if not items:
                    break
                for item in items:
                    title_tag = item.select_one(".title")
                    company_tag = item.select_one(".name")
                    location_tag = item.select_one(".loc")
                    exp_tag = item.select_one(".exp")
                    link_tag = item.select_one("a.title")
                    if not title_tag or not link_tag:
                        continue
                    href = link_tag.get("href", "")
                    job_id = href.split("GI_No=")[-1].split("&")[0] if "GI_No=" in href else href
                    jobs.append({
                        "id": f"jobkorea_{job_id}",
                        "title": title_tag.get_text(strip=True),
                        "company": company_tag.get_text(strip=True) if company_tag else "",
                        "location": location_tag.get_text(strip=True) if location_tag else "",
                        "experience": exp_tag.get_text(strip=True) if exp_tag else "",
                        "url": f"https://www.jobkorea.co.kr{href}" if href.startswith("/") else href,
                        "source": "잡코리아",
                        "keyword": keyword,
                    })
            except Exception as e:
                print(f"[jobkorea] {keyword} 오류: {e}")
                break
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
