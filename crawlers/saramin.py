import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

KEYWORDS = ["AI", "ML", "머신러닝", "딥러닝", "인공지능", "데이터사이언스", "컴퓨터비전", "NLP", "LLM"]

def fetch_jobs():
    jobs = []
    for keyword in KEYWORDS:
        for start in range(0, 300, 40):
            url = (
                f"https://www.saramin.co.kr/zf_user/search/recruit"
                f"?searchType=search&searchword={keyword}&recruitPage={start // 40 + 1}&recruitPageCount=40"
            )
            try:
                res = requests.get(url, headers=HEADERS, timeout=10)
                if res.status_code != 200:
                    break
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(res.text, "html.parser")
                items = soup.select(".item_recruit")
                if not items:
                    break
                for item in items:
                    title_tag = item.select_one(".job_tit a")
                    company_tag = item.select_one(".corp_name a")
                    cond_spans = item.select(".job_condition span")
                    company_size_tag = item.select_one(".company_nm em")
                    if not title_tag:
                        continue
                    job_id = title_tag.get("href", "").split("rec_idx=")[-1].split("&")[0]
                    location = cond_spans[0].get_text(strip=True) if len(cond_spans) > 0 else ""
                    experience = cond_spans[1].get_text(strip=True) if len(cond_spans) > 1 else ""
                    jobs.append({
                        "id": f"saramin_{job_id}",
                        "title": title_tag.get_text(strip=True),
                        "company": company_tag.get_text(strip=True) if company_tag else "",
                        "location": location,
                        "experience": experience,
                        "company_size": company_size_tag.get_text(strip=True) if company_size_tag else "",
                        "url": f"https://www.saramin.co.kr/zf_user/jobs/relay/view?rec_idx={job_id}",
                        "source": "사람인",
                        "keyword": keyword,
                    })
            except Exception as e:
                print(f"[saramin] {keyword} 오류: {e}")
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
    print(f"사람인: {len(jobs)}개")
