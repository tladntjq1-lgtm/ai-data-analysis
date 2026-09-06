"""데이터 로딩 함수 모음.

data/raw 아래의 4개 CSV 파일을 일관된 방식으로 읽어온다.
- CSV 파일에 BOM이 포함되어 있어 encoding="utf-8-sig" 를 사용한다.
- 날짜 컬럼은 여기서 파싱하지 않는다. 전처리 단계(preprocess.py)에서 처리한다.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# 프로젝트 루트 기준 경로 (src/ 의 부모 디렉터리)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

RAW_FILES = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
}


def load_csv(name: str, raw_dir: Path | str = RAW_DIR) -> pd.DataFrame:
    """RAW_FILES 에 등록된 이름으로 단일 CSV 를 읽는다."""
    if name not in RAW_FILES:
        raise KeyError(f"알 수 없는 데이터 이름: {name!r}. 사용 가능: {list(RAW_FILES)}")
    path = Path(raw_dir) / RAW_FILES[name]
    if not path.exists():
        raise FileNotFoundError(f"파일이 없습니다: {path}")
    return pd.read_csv(path, encoding="utf-8-sig")


def load_all(raw_dir: Path | str = RAW_DIR) -> dict[str, pd.DataFrame]:
    """4개 원본 테이블을 한 번에 읽어 딕셔너리로 반환한다."""
    return {name: load_csv(name, raw_dir) for name in RAW_FILES}


if __name__ == "__main__":
    frames = load_all()
    for key, df in frames.items():
        print(f"[{key}] shape={df.shape}")
        print(df.head(3).to_string(index=False))
        print()
