import streamlit as st
import pandas as pd
import altair as alt

# 📥 CSV 데이터 로드 (캐싱)
@st.cache_data
def load_data():
    df = countriesMBTI_16types.csv
    return df

df = load_data()

# MBTI 유형 리스트
mbti_types = [
    "INFJ", "INFP", "INTJ", "INTP",
    "ISFJ", "ISFP", "ISTJ", "ISTP",
    "ENFJ", "ENFP", "ENTJ", "ENTP",
    "ESFJ", "ESFP", "ESTJ", "ESTP"
]

# MBTI별 간단한 진로 추천
mbti_career_map = {
    "INFJ": ["상담가", "심리학자", "교육자"],
    "INFP": ["작가", "예술가", "사회운동가"],
    "INTJ": ["전략가", "과학자", "정책분석가"],
    "INTP": ["연구자", "데이터 분석가", "프로그래머"],
    "ISFJ": ["간호사", "사서", "행정직"],
    "ISFP": ["디자이너", "음악가", "수의사"],
    "ISTJ": ["회계사", "판사", "기록관리자"],
    "ISTP": ["엔지니어", "정비사", "수사관"],
    "ENFJ": ["교사", "상담가", "인사담당자"],
    "ENFP": ["창작자", "광고기획자", "사회복지사"],
    "ENTJ": ["경영자", "변호사", "정치인"],
    "ENTP": ["벤처 창업가", "기획자", "마케팅 전문가"],
    "ESFJ": ["간호사", "영업직", "이벤트 기획자"],
    "ESFP": ["연예인", "유튜버", "관광가이드"],
    "ESTJ": ["경영관리자", "군인", "현장감독"],
    "ESTP": ["영업사원", "스포츠 코치", "응급구조사"]
}

# 🌍 사이드바: 사용자 입력
st.sidebar.title("🌍 국가 및 MBTI 선택")
country = st.sidebar.selectbox("국가를 선택하세요", df["Country"].unique())
mbti = st.sidebar.selectbox("MBTI 유형을 선택하세요", mbti_types)

# 선택된 국가의 MBTI 데이터
row = df[df["Country"] == country].iloc[0]
mbti_value = row[mbti]

# 🔍 본문 표시
st.title("🎓 국가별 MBTI 기반 진로 추천기")
st.markdown(f"### 📌 선택한 국가: **{country}**")
st.markdown(f"### 🧬 MBTI 유형: **{mbti}**")
st.markdown(f"- 이 국가의 {mbti} 유형 비율은 **{mbti_value:.2%}** 입니다.")

st.markdown("### 💼 추천 진로:")
for job in mbti_career_map[mbti]:
    st.markdown(f"- {job}")

# 📊 Altair 그래프
st.markdown("### 📈 이 국가의 전체 MBTI 유형 분포")

# 데이터프레임 변환: long format
mbti_data = row[mbti_types].reset_index()
mbti_data.columns = ["MBTI", "비율"]

chart = alt.Chart(mbti_data).mark_bar().encode(
    x=alt.X('MBTI', sort=mbti_types),
    y=alt.Y('비율', axis=alt.Axis(format='%')),
    tooltip=['MBTI', alt.Tooltip('비율', format='.2%')],
    color=alt.condition(
        alt.datum.MBTI == mbti,
        alt.value("orange"),  # 선택한 MBTI 강조
        alt.value("steelblue")
    )
).properties(
    width=600,
    height=400,
    title=f"{country}의 MBTI 분포"
)

st.altair_chart(chart, use_container_width=True)

st.info("💡 Altair로 시각화된 MBTI 분포입니다. 선택한 MBTI는 주황색으로 표시됩니다.")
