"""전처리 함수 모음.

원본 테이블을 분석 목적에 맞게 정리한다.
- 날짜 문자열 -> datetime 변환
- 결제 완료 주문만 필터링
- 주문상세 기준 매출(item_revenue) 파생 변수 생성
- 주문 / 고객 / 상품 정보 병합

책 Chapter 01의 기준을 따른다:
- status(order_status) 가 "completed" 인 주문만 포함
- 상품 매출 = quantity * unit_price
"""

from __future__ import annotations

import pandas as pd

COMPLETED_STATUS = "completed"


def parse_dates(orders: pd.DataFrame, customers: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """order_date, signup_date 를 datetime 으로 변환한다."""
    orders = orders.copy()
    customers = customers.copy()
    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    customers["signup_date"] = pd.to_datetime(customers["signup_date"], errors="coerce")
    return orders, customers


def filter_completed(orders: pd.DataFrame) -> pd.DataFrame:
    """결제 완료 주문만 남긴다."""
    return orders.loc[orders["order_status"] == COMPLETED_STATUS].copy()


def add_item_revenue(order_items: pd.DataFrame) -> pd.DataFrame:
    """주문상세 한 행의 매출 컬럼을 추가한다. (매출 = 수량 x 단가)"""
    order_items = order_items.copy()
    order_items["item_revenue"] = order_items["quantity"] * order_items["unit_price"]
    return order_items


def build_sales_table(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame,
    completed_only: bool = True,
) -> pd.DataFrame:
    """분석용 통합 매출 테이블을 만든다. 한 행 = 주문상세 한 항목.

    병합 순서:
        order_items -> orders (order_id)
                    -> products (product_id)
                    -> customers (customer_id)
    """
    orders, customers = parse_dates(orders, customers)
    if completed_only:
        orders = filter_completed(orders)

    items = add_item_revenue(order_items)

    merged = (
        items
        .merge(orders, on="order_id", how="inner", validate="many_to_one")
        .merge(products, on="product_id", how="left", validate="many_to_one")
        .merge(customers, on="customer_id", how="left", validate="many_to_one")
    )

    merged["order_month"] = merged["order_date"].dt.to_period("M").astype(str)
    return merged


if __name__ == "__main__":
    from load_data import load_all

    frames = load_all()
    sales = build_sales_table(
        frames["orders"], frames["order_items"], frames["customers"], frames["products"]
    )
    print(f"통합 매출 테이블 shape={sales.shape}")
    print(sales.head(3).to_string(index=False))
