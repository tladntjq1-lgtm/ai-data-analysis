"""Titanic 생존 예측 Streamlit 앱.

사용자 입력 -> FamilySize/IsAlone 파생 -> 결측치 처리 -> One-Hot Encoding
-> StandardScaler -> 숫자형/범주형 결합 -> 저장된 모델 예측
"""

import numpy as np
import pandas as pd
import joblib
import streamlit as st

from course_utils import get_project_root

NUMERIC_FEATURES = ["Age", "SibSp", "Parch", "Fare", "FamilySize"]
CATEGORICAL_FEATURES = ["Pclass", "Sex", "Embarked", "IsAlone"]

BUNDLE_PATH = get_project_root() / "models" / "titanic_model_bundle.joblib"


@st.cache_resource
def load_bundle():
    return joblib.load(BUNDLE_PATH)


def build_features(pclass, sex, age, sibsp, parch, fare, embarked) -> pd.DataFrame:
    family_size = sibsp + parch + 1
    is_alone = int(family_size == 1)
    return pd.DataFrame([{
        "Pclass": pclass,
        "Sex": sex,
        "Age": age,
        "SibSp": sibsp,
        "Parch": parch,
        "Fare": fare,
        "Embarked": embarked,
        "FamilySize": family_size,
        "IsAlone": is_alone,
    }])


def predict(bundle: dict, passenger: pd.DataFrame):
    num_imputed = bundle["numeric_imputer"].transform(passenger[NUMERIC_FEATURES])
    num_scaled = bundle["scaler"].transform(num_imputed)

    cat_imputed = bundle["categorical_imputer"].transform(passenger[CATEGORICAL_FEATURES])
    cat_encoded = bundle["encoder"].transform(cat_imputed)

    ready = np.hstack([num_scaled, cat_encoded])

    model = bundle["model"]
    prediction = int(model.predict(ready)[0])
    positive_index = list(model.classes_).index(1)
    probability = float(model.predict_proba(ready)[0][positive_index])
    return prediction, probability


def main():
    st.set_page_config(page_title="Titanic 생존 예측", page_icon="🚢")

    title_col, ship_col = st.columns([0.85, 0.15])
    with title_col:
        st.title("Titanic 생존 예측")
    with ship_col:
        st.markdown(
            "<div style='font-size:64px; line-height:1; margin-top:20px'>🚢</div>",
            unsafe_allow_html=True,
        )
    st.caption("입력한 승객 정보로 저장된 모델이 생존 여부를 예측합니다.")

    bundle = load_bundle()

    with st.form("passenger_form"):
        col1, col2 = st.columns(2)
        with col1:
            pclass = st.selectbox("Pclass (객실 등급)", [1, 2, 3], index=2)
            sex = st.selectbox("Sex (성별)", ["male", "female"])
            age = st.number_input("Age (나이)", min_value=0.0, max_value=100.0, value=30.0, step=1.0)
            fare = st.number_input("Fare (운임)", min_value=0.0, value=10.0, step=1.0)
        with col2:
            sibsp = st.number_input("SibSp (형제/배우자 수)", min_value=0, max_value=10, value=0, step=1)
            parch = st.number_input("Parch (부모/자녀 수)", min_value=0, max_value=10, value=0, step=1)
            embarked = st.selectbox("Embarked (승선 항구)", ["S", "C", "Q"])

        submitted = st.form_submit_button("예측하기")

    if submitted:
        passenger = build_features(pclass, sex, age, sibsp, parch, fare, embarked)
        st.subheader("입력된 승객 정보")
        st.json(passenger.iloc[0].to_dict())

        prediction, probability = predict(bundle, passenger)

        st.subheader("예측 결과")
        if prediction == 1:
            st.success(f"생존 예측 (생존 확률 {probability:.1%})")
        else:
            st.error(f"사망 예측 (생존 확률 {probability:.1%})")


if __name__ == "__main__":
    main()
