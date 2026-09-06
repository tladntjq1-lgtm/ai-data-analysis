# 데이터 사전 (Data Dictionary)

실습용 가상 온라인 쇼핑몰 데이터. `scripts/generate_sample_data.py` 로 생성한다
(SEED=42 고정, 인코딩 `utf-8-sig`). 원본은 `data/raw/` 에 둔다.

> 책 Chapter 01 예시는 `status`, `unit_price`, `region` 같은 이름을 쓰지만
> 이 저장소의 실제 컬럼명은 아래 표를 기준으로 한다.

## 테이블 관계

```
customers.customer_id  ──<  orders.customer_id
orders.order_id        ──<  order_items.order_id
products.product_id    ──<  order_items.product_id
```

- 고객 1명 → 주문 여러 건
- 주문 1건 → 주문상세 여러 항목
- 상품 1개 → 여러 주문상세에서 판매

주문 수는 `order_items` 의 행 수가 아니라 고유 `order_id` 개수로 센다.

---

## customers.csv — 고객 (150행)

한 행 = 고객 1명. 기본 키: `customer_id`.

| 컬럼 | 자료형 | 설명 | 예시 / 값 |
|---|---|---|---|
| customer_id | int | 고객 번호 (PK) | 1 ~ 150 |
| name | str | 고객 이름 (가상, ko_KR) | "김수민" |
| gender | str | 성별 | F, M |
| age | int | 나이 | 18 ~ 69 |
| city | str | 거주 도시 | 서울, 부산, 대구, 인천, 광주, 대전, 울산, 수원, 성남, 고양 |
| signup_date | date(str) | 가입일 (YYYY-MM-DD), 최근 3년 | "2024-07-15" |

## products.csv — 상품 (100행)

한 행 = 상품 1개. 기본 키: `product_id`.

| 컬럼 | 자료형 | 설명 | 예시 / 값 |
|---|---|---|---|
| product_id | int | 상품 번호 (PK) | 1 ~ 100 |
| product_name | str | 상품명 | "전자기기 상품 001" |
| category | str | 카테고리 | 식품, 생활용품, 패션, 전자기기, 도서, 스포츠, 뷰티 |
| price | int | 정가(원), 1,000원 단위 | 5,000 ~ 200,000 |

## orders.csv — 주문 (300행)

한 행 = 주문 1건. 기본 키: `order_id`. 외래 키: `customer_id → customers`.

| 컬럼 | 자료형 | 설명 | 예시 / 값 |
|---|---|---|---|
| order_id | int | 주문 번호 (PK) | 1 ~ 300 |
| customer_id | int | 주문 고객 (FK) | customers.customer_id |
| order_date | date(str) | 주문일 (YYYY-MM-DD), 최근 1년 | "2026-06-02" |
| payment_method | str | 결제 수단 | card, bank_transfer, kakao_pay, naver_pay |
| order_status | str | 주문 상태 | completed, cancelled, refunded |

- 매출/판매량 분석은 기본적으로 `order_status == "completed"` 만 포함한다.

## order_items.csv — 주문상세 (765행)

한 행 = 주문 1건에 포함된 상품 1항목. 기본 키: `order_item_id`.
외래 키: `order_id → orders`, `product_id → products`.

| 컬럼 | 자료형 | 설명 | 예시 / 값 |
|---|---|---|---|
| order_item_id | int | 주문상세 번호 (PK) | 1 ~ 765 |
| order_id | int | 소속 주문 (FK) | orders.order_id |
| product_id | int | 상품 (FK) | products.product_id |
| quantity | int | 주문 수량 | 1 ~ 5 |
| unit_price | int | 판매 단가(원). 생성 시 products.price 와 동일 | 102000 |

### 파생 지표

| 이름 | 계산식 | 비고 |
|---|---|---|
| item_revenue | quantity × unit_price | 주문상세 한 항목의 매출 |
| 상품별 매출 | Σ item_revenue (product_id 그룹) | |
| 상품별 판매량 | Σ quantity (product_id 그룹) | 매출 순위와 다를 수 있음 |
| 주문 수 | order_id 고유값 개수 | 행 수 아님 |
| 객단가 | 매출 합계 / 주문 수 | |
