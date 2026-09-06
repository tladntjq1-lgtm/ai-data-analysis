"""검증 함수 모음.

책 Chapter 01의 "세 단계 검증 게이트"를 코드로 옮긴 것.
    1. 실행 검증  - 코드가 도는가 (여기서는 다루지 않음, 실행 자체로 확인)
    2. 데이터 검증 - 컬럼 / 행 수 / 결측 / 중복 / 병합 후 행 증가 / 키 연결
    3. 해석 검증  - 사람이 판단 (자동화 대상 아님)

이 모듈은 주로 2번(데이터 검증)을 돕는다.
"""

from __future__ import annotations

import pandas as pd


def require_columns(df: pd.DataFrame, columns: list[str], name: str = "dataframe") -> None:
    """필요한 컬럼이 모두 있는지 확인한다. 없으면 KeyError."""
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise KeyError(f"[{name}] 없는 컬럼: {missing} / 실제 컬럼: {df.columns.tolist()}")


def summarize(df: pd.DataFrame, name: str = "dataframe") -> pd.DataFrame:
    """행 수, 결측값 개수, 중복 행 수, 자료형을 한 표로 요약한다."""
    print(f"[{name}] shape={df.shape}, 중복 행={df.duplicated().sum()}")
    return pd.DataFrame(
        {
            "dtype": df.dtypes.astype(str),
            "n_missing": df.isna().sum(),
            "n_unique": df.nunique(),
        }
    )


def check_merge_rows(left: pd.DataFrame, right: pd.DataFrame, merged: pd.DataFrame) -> None:
    """병합 후 행이 예상치 못하게 늘었는지 확인한다."""
    print(f"left={left.shape[0]}  right={right.shape[0]}  merged={merged.shape[0]}")
    if merged.shape[0] > left.shape[0]:
        print(
            "  주의: 병합 후 행 수가 left 보다 늘었습니다. "
            "키 중복(일대다/다대다) 여부를 확인하세요."
        )


def check_keys(child: pd.DataFrame, parent: pd.DataFrame, key: str) -> pd.Series:
    """child 의 key 값 중 parent 에 없는 값(연결되지 않는 키)을 돌려준다."""
    orphan_mask = ~child[key].isin(parent[key])
    n = int(orphan_mask.sum())
    if n:
        print(f"  연결 안 되는 {key}: {n}건 -> {child.loc[orphan_mask, key].unique()[:10]}")
    else:
        print(f"  {key}: 모든 값이 부모 테이블에 연결됨")
    return child.loc[orphan_mask, key]


def order_count(order_items: pd.DataFrame) -> int:
    """주문 수는 order_items 의 행 수가 아니라 고유 order_id 개수로 센다."""
    return int(order_items["order_id"].nunique())
