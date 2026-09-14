# AI Data Analysis

AI(LLM)와 함께하는 데이터 분석 실습 프로젝트. 가상 온라인 쇼핑몰 데이터를 사용해
좋은 질문 만들기 → 데이터 확인 → 전처리 → EDA → 모델링 → 검증 → 보고서 흐름을 연습한다.

책 *AI Data Analysis* (문길래, 부크크) Chapter 01의 프로젝트 구조를 따른다.

## 폴더 구조

```
ai-data-analysis/
├─ data/
│  ├─ raw/          원본 CSV (customers, products, orders, order_items)
│  ├─ processed/    전처리 완료 데이터 (git 미추적)
│  └─ sample/       LLM 질문·공개 예제용 익명화 소규모 샘플
├─ notebooks/       탐색·실습용 Jupyter Notebook (chNN/chNN_*.ipynb)
├─ scripts/         일회성 스크립트 (샘플 데이터 생성 등)
├─ src/             재사용 함수 (load_data / preprocess / validate)
├─ reports/         표·그래프·보고서 결과물
│  ├─ figures/
│  ├─ tables/
│  └─ chapterNN/
├─ prompts/         LLM 프롬프트·수정 기록 (prompt_log.md)
├─ docs/            데이터 사전, 분석 기준 (data_dictionary.md)
├─ .env.example     환경변수 예시 (복사해서 .env 생성, .env 는 커밋 금지)
├─ .gitignore
└─ requirements.txt
```

## 시작하기

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt

# 샘플 데이터 생성 (data/raw/*.csv)
python scripts/generate_sample_data.py

# 환경변수 준비
cp .env.example .env   # 이후 .env 에 개인 API 키 입력
```

## src 모듈 사용 예

```python
from src.load_data import load_all
from src.preprocess import build_sales_table
from src.validate import summarize, order_count

frames = load_all()
sales = build_sales_table(
    frames["orders"], frames["order_items"], frames["customers"], frames["products"]
)
summarize(sales, "sales")
print("주문 수:", order_count(frames["order_items"]))
```

## 데이터

4개 CSV의 컬럼·관계·파생 지표는 [docs/data_dictionary.md](docs/data_dictionary.md) 참고.

## 보안 원칙

- 실제 개인정보·API 키·`.env`·회사 비공개 데이터는 커밋하지 않는다.
- LLM에는 전체 데이터가 아니라 컬럼명·자료형·익명화 샘플·오류 메시지 등 최소 정보만 제공한다.
- LLM 답변은 최종 결과가 아니라 출발점이다. 실행·데이터·해석 3단계로 검증한다.

## 참고

- https://github.com/GilbertMoon/llm-data-analysis-course
