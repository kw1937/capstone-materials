import streamlit as st

st.title("정비 자재 검색 시스템")
st.write("설비명이나 작업명으로 이전 사용 자재를 검색하세요.")
st.caption("현재 자료는 기능 시연을 위한 가상 데이터입니다.")

# 작업별 사용 자재 예시
work_history = {
    "A설비 A모터 분해수리": [
        {"자재 코드": "MAT-001", "자재명": "베어링 A", "수량": 1, "단위": "개"},
        {"자재 코드": "MAT-002", "자재명": "베어링 B", "수량": 1, "단위": "개"},
        {"자재 코드": "MAT-003", "자재명": "오일씰", "수량": 2, "단위": "개"},
    ],
    "B설비 B펌프 분해수리": [
        {"자재 코드": "MAT-004", "자재명": "메커니컬 씰", "수량": 1, "단위": "개"},
        {"자재 코드": "MAT-005", "자재명": "가스켓", "수량": 2, "단위": "개"},
    ],
}

# 검색창
keyword = st.text_input(
    "작업명을 입력하세요",
    placeholder="예: A모터, B펌프, 분해수리",
)

# 띄어쓰기와 영문 대소문자 차이를 무시
search_text = "".join(keyword.split()).lower()

if search_text:
    found = False

    for work_name, materials in work_history.items():
        target_text = "".join(work_name.split()).lower()

        if search_text in target_text:
            found = True
            st.subheader(work_name)
            st.table(materials)

    if not found:
        st.warning("일치하는 작업이 없습니다. 다른 검색어를 입력해주세요.")
else:
    st.info("검색어를 입력하고 Enter를 눌러주세요.")
