import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

KEYWORDS = ["AI", "ML", "머신러닝", "딥러닝", "인공지능", "데이터사이언스", "컴퓨터비전", "NLP", "LLM"]

def fetch_jobs():
    jobs = []
    for keyword in KEYWORDS:
        offset = 0
        while True:
            url = f"https://www.wanted.co.kr/api/v4/jobs?query={keyword}&offset={offset}&limit=100"
            try:
                res = requests.get(url, headers=HEADERS, timeout=10)
                if res.status_code != 200:
                    break
                data = res.json()
                items = data.get("data", [])
                if not items:
                    break
                for item in items:
                    jobs.append({
                        "id": f"wanted_{item['id']}",
                        "title": item.get("position", ""),
                        "company": item.get("company", {}).get("name", ""),
                        "location": item.get("address", {}).get("location", ""),
                        "experience": item.get("experience_level", {}).get("name", ""),
                        "url": f"https://www.wanted.co.kr/wd/{item['id']}",
                        "source": "원티드",
                        "keyword": keyword,
                    })
                offset += 100
                if offset >= data.get("total", 0):
                    break
            except Exception as e:
                print(f"[wanted] {keyword} 오류: {e}")
                break
    # 중복 제거
    seen = set()
    unique = []
    for job in jobs:
        if job["id"] not in seen:
            seen.add(job["id"])
            unique.append(job)
    return unique


if __name__ == "__main__":
    jobs = fetch_jobs()
    print(f"원티드: {len(jobs)}개")
