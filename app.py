import streamlit as st

st.title("정비 자재 검색 및 신청 시스템")
st.caption("가상 데이터 기반 시연입니다. 실제 자재 출고와 연결되지 않습니다.")

# 작업별 과거 사용 자재 예시
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

# 현재 접속 중에 신청 초안을 보관
if "request_draft" not in st.session_state:
    st.session_state.request_draft = None

keyword = st.text_input(
    "설비명 또는 작업명을 입력하세요",
    placeholder="예: A모터, B펌프, 분해수리",
)

search_text = "".join(keyword.split()).lower()

if search_text:
    matching_jobs = [
        name
        for name in work_history
        if search_text in "".join(name.split()).lower()
    ]

    if matching_jobs:
        selected_job = st.selectbox(
            "자재를 신청할 작업을 선택하세요",
            matching_jobs,
        )

        st.subheader("이전 사용 자재")
        st.table(work_history[selected_job])

        st.subheader("신청할 자재 선택")
        st.write("체크한 자재만 신청 목록에 포함됩니다.")

        # 신청 버튼을 누르면 입력 내용을 한 번에 처리
        with st.form(key=f"request_form_{selected_job}"):
            requester = st.text_input("신청자 이름")

            selected_materials = []

            for material in work_history[selected_job]:
                code = material["자재 코드"]
                name = material["자재명"]
                unit = material["단위"]

                left, right = st.columns([3, 1])

                with left:
                    checked = st.checkbox(
                        f"{name} · {code}",
                        value=True,
                        key=f"check_{selected_job}_{code}",
                    )

                with right:
                    quantity = st.number_input(
                        f"신청 수량 ({unit})",
                        min_value=1,
                        value=material["수량"],
                        step=1,
                        key=f"qty_{selected_job}_{code}",
                    )

                if checked:
                    selected_materials.append({
                        "자재 코드": code,
                        "자재명": name,
                        "신청 수량": int(quantity),
                        "단위": unit,
                    })

            submitted = st.form_submit_button("자재 신청 — 시연")

            if submitted:
                if not requester.strip():
                    st.warning("신청자 이름을 입력해주세요.")
                elif not selected_materials:
                    st.warning("신청할 자재를 하나 이상 선택해주세요.")
                else:
                    st.session_state.request_draft = {
                        "신청자": requester.strip(),
                        "작업명": selected_job,
                        "자재 목록": selected_materials,
                    }
                    st.success("신청 초안이 생성됐습니다. 아래 내용을 확인해주세요.")

    else:
        st.warning("일치하는 작업이 없습니다.")
else:
    st.info("검색어를 입력하고 Enter를 눌러주세요.")

# 가장 최근에 만든 신청 초안 표시
draft = st.session_state.request_draft

if draft is not None:
    st.divider()
    st.subheader("최근 신청 초안")
    st.write("신청자:", draft["신청자"])
    st.write("작업명:", draft["작업명"])
    st.table(draft["자재 목록"])
    st.caption(
        "이 초안은 현재 접속 중에만 유지됩니다. "
        "새로고침하거나 접속이 끊기면 사라질 수 있습니다. "
        "실제 신청 접수·영구 저장·창고 제어는 아직 연결되지 않았습니다."
    )
