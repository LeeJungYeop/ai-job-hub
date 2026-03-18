import json
import os
from datetime import datetime, timezone, timedelta

from wanted import fetch_jobs as fetch_wanted
from saramin import fetch_jobs as fetch_saramin
from jobkorea import fetch_jobs as fetch_jobkorea

KST = timezone(timedelta(hours=9))

# 제목에 아래 키워드 중 하나라도 포함되어야 AI/ML 관련 공고로 인정
AI_TITLE_KEYWORDS = [
    # 영문 약어
    "AI", "ML", "LLM", "NLP", "GPT", "RAG", "SLAM", "MLOps",
    # 영문 전체 표기
    "Machine Learning", "Deep Learning", "Artificial Intelligence",
    "Natural Language", "Computer Vision", "Machine Vision",
    "Data Science", "Data Scientist",
    "Reinforcement Learning", "Foundation Model", "Fine-tun",
    "Recommendation System",
    # 한글
    "머신러닝", "딥러닝", "인공지능", "자연어처리",
    "컴퓨터비전", "컴퓨터 비전",
    "데이터사이언스", "데이터 사이언스",
    "데이터사이언티스트", "데이터 사이언티스트",
    "생성형 AI", "생성형AI",
    "파운데이션 모델", "파운데이션모델",
    "파인튜닝", "파인 튜닝",
    "추천시스템", "추천 시스템",
    "강화학습", "강화 학습",
    "자율주행", "자율 주행",
    "모델 개발", "모델개발",
    "데이터 엔지니어", "데이터엔지니어",
]

def is_ai_job(title: str) -> bool:
    t = title.upper()
    return any(kw.upper() in t for kw in AI_TITLE_KEYWORDS)

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

    before = len(all_jobs)
    all_jobs = [job for job in all_jobs if is_ai_job(job["title"])]
    print(f"\n노이즈 필터링: {before}개 → {len(all_jobs)}개 ({before - len(all_jobs)}개 제거)")

    updated_at = datetime.now(KST).strftime("%Y-%m-%d %H:%M")

    output = {
        "updated_at": updated_at,
        "total": len(all_jobs),
        "jobs": all_jobs,
    }

    os.makedirs("../docs", exist_ok=True)
    with open("../docs/jobs.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"완료: 총 {len(all_jobs)}개 → docs/jobs.json 저장")


if __name__ == "__main__":
    main()
