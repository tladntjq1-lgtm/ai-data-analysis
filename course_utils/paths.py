"""프로젝트 경로 탐색 유틸리티.

이 모듈의 파일 위치(``__file__``)를 기준으로 위로 올라가며 ``data`` 폴더가 있는
디렉터리를 프로젝트 루트로 판단한다. 노트북의 현재 작업 폴더(``Path.cwd()``)와
무관하게 항상 같은 결과를 돌려주는 것이 핵심이다.
"""

from pathlib import Path

# course_utils/paths.py -> course_utils -> <프로젝트 루트>
_THIS_DIR = Path(__file__).resolve().parent


def get_project_root() -> Path:
    """``data`` 폴더를 가진 상위 디렉터리를 프로젝트 루트로 반환한다."""
    current = _THIS_DIR
    while current != current.parent:
        if (current / "data").is_dir():
            return current
        current = current.parent
    raise FileNotFoundError("프로젝트 루트를 찾을 수 없습니다. (data 폴더가 있는 상위 폴더 없음)")


def get_data_dir() -> Path:
    """``<프로젝트 루트>/data`` 경로를 반환한다."""
    return get_project_root() / "data"


def get_raw_dir() -> Path:
    """``<프로젝트 루트>/data/raw`` 경로를 반환한다."""
    return get_data_dir() / "raw"
