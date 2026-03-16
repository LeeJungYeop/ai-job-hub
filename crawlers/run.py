import json
import os
from datetime import datetime, timezone, timedelta

from wanted import fetch_jobs as fetch_wanted
from saramin import fetch_jobs as fetch_saramin
from jobkorea import fetch_jobs as fetch_jobkorea

KST = timezone(timedelta(hours=9))

def main():
    print("크롤링 시작...")

    all_jobs = []

    print("원티드 크롤링...")
    all_jobs.extend(fetch_wanted())
    print(f"  → {len(all_jobs)}개")

    print("사람인 크롤링...")
    all_jobs.extend(fetch_saramin())
    print(f"  → {len(all_jobs)}개")

    print("잡코리아 크롤링...")
    all_jobs.extend(fetch_jobkorea())
    print(f"  → {len(all_jobs)}개")

    updated_at = datetime.now(KST).strftime("%Y-%m-%d %H:%M")

    output = {
        "updated_at": updated_at,
        "total": len(all_jobs),
        "jobs": all_jobs,
    }

    os.makedirs("../docs", exist_ok=True)
    with open("../docs/jobs.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n완료: 총 {len(all_jobs)}개 → docs/jobs.json 저장")


if __name__ == "__main__":
    main()
