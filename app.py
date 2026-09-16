import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================================================
# 1. 기본 설정
# =========================================================

st.set_page_config(
    page_title="CNU Smart Materials",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. CSS 디자인
# =========================================================

st.markdown("""
<style>

/* 전체 배경 */
.stApp {
    background-color: #F5F7FA;
}

/* 기본 콘텐츠 폭 */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* 제목 */
.main-title {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 4px;
    color: #14213D;
}

.main-subtitle {
    font-size: 14px;
    color: #7B8495;
    margin-bottom: 22px;
}

/* KPI 카드 */
.kpi-card {
    background: white;
    padding: 22px 22px 18px 22px;
    border-radius: 16px;
    border: 1px solid #E7EAF0;
    box-shadow: 0 3px 10px rgba(0,0,0,0.035);
    min-height: 125px;
}

.kpi-label {
    color: #7E8797;
    font-size: 14px;
    font-weight: 600;
}

.kpi-number {
    color: #14213D;
    font-size: 31px;
    font-weight: 800;
    margin-top: 8px;
}

.kpi-desc {
    color: #9AA2AF;
    font-size: 12px;
    margin-top: 2px;
}

/* 일반 카드 */
.content-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #E7EAF0;
    box-shadow: 0 3px 10px rgba(0,0,0,0.03);
    margin-bottom: 14px;
}

/* 검색 영역 */
.search-box {
    background: linear-gradient(120deg, #173B63, #275D8C);
    border-radius: 20px;
    padding: 30px 32px;
    margin-bottom: 24px;
}

.search-title {
    font-size: 24px;
    color: white;
    font-weight: 800;
}

.search-desc {
    font-size: 14px;
    color: #DAE7F4;
    margin-top: 6px;
    margin-bottom: 12px;
}

/* 섹션 제목 */
.section-title {
    color: #17213A;
    font-size: 20px;
    font-weight: 800;
    margin-top: 5px;
    margin-bottom: 13px;
}

/* 작업 상태 Badge */
.badge-green {
    background: #E8F8F0;
    color: #168657;
    border-radius: 20px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 700;
}

.badge-orange {
    background: #FFF3DE;
    color: #C77700;
    border-radius: 20px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 700;
}

.badge-red {
    background: #FFE8E8;
    color: #D33B3B;
    border-radius: 20px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 700;
}

/* Streamlit 버튼 */
.stButton > button {
    border-radius: 10px;
    border: none;
    font-weight: 700;
    min-height: 40px;
}

/* 입력창 */
div[data-baseweb="input"] > div {
    border-radius: 10px;
}

/* 탭 */
button[data-baseweb="tab"] {
    font-weight: 700;
    font-size: 15px;
}

/* 사이드바 */
section[data-testid="stSidebar"] {
    background-color: #101C2E;
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* hr */
hr {
    border: none;
    height: 1px;
    background-color: #E8EBF0;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. 샘플 데이터
# =========================================================

jobs = pd.DataFrame([
    {
        "작업코드": "JOB-001",
        "작업명": "순환수 펌프 베어링 교체",
        "설비": "순환수 펌프 #1",
        "작업구분": "정비",
        "부서": "기계정비",
        "상태": "작업예정"
    },
    {
        "작업코드": "JOB-002",
        "작업명": "고압 모터 정기점검",
        "설비": "6.6kV Motor #2",
        "작업구분": "예방정비",
        "부서": "전기정비",
        "상태": "진행중"
    },
    {
        "작업코드": "JOB-003",
        "작업명": "배관 누수 보수",
        "설비": "공업용수 배관",
        "작업구분": "긴급정비",
        "부서": "기계정비",
        "상태": "완료"
    },
    {
        "작업코드": "JOB-004",
        "작업명": "수위 센서 교체",
        "설비": "폐수 Tank #3",
        "작업구분": "계장정비",
        "부서": "전기계장",
        "상태": "작업예정"
    },
    {
        "작업코드": "JOB-005",
        "작업명": "컨베이어 감속기 점검",
        "설비": "CV-102",
        "작업구분": "예방정비",
        "부서": "기계정비",
        "상태": "진행중"
    },
    {
        "작업코드": "JOB-006",
        "작업명": "제어반 차단기 교체",
        "설비": "MCC-03",
        "작업구분": "전기정비",
        "부서": "전기정비",
        "상태": "완료"
    },
    {
        "작업코드": "JOB-007",
        "작업명": "펌프 Mechanical Seal 교체",
        "설비": "Drain Pump #2",
        "작업구분": "정비",
        "부서": "기계정비",
        "상태": "작업예정"
    },
    {
        "작업코드": "JOB-008",
        "작업명": "PLC 통신 모듈 점검",
        "설비": "Local PLC-04",
        "작업구분": "계장정비",
        "부서": "전기계장",
        "상태": "완료"
    },
    {
        "작업코드": "JOB-009",
        "작업명": "공업용수 밸브 교체",
        "설비": "WV-103",
        "작업구분": "정비",
        "부서": "기계정비",
        "상태": "진행중"
    },
    {
        "작업코드": "JOB-010",
        "작업명": "모터 절연저항 측정",
        "설비": "Motor M-410",
        "작업구분": "예방정비",
        "부서": "전기정비",
        "상태": "작업예정"
    }
])


materials = pd.DataFrame([
    ["JOB-001", "MAT-001", "베어링 6205", 2, 18, "A-01-01", "EA"],
    ["JOB-001", "MAT-002", "구리스", 1, 8, "A-02-05", "CAN"],
    ["JOB-001", "MAT-003", "오일씰", 2, 3, "A-04-03", "EA"],

    ["JOB-002", "MAT-004", "절연테이프", 3, 32, "B-01-03", "EA"],
    ["JOB-002", "MAT-005", "압착단자", 12, 140, "B-04-01", "EA"],
    ["JOB-002", "MAT-006", "세척제", 1, 11, "B-05-02", "CAN"],

    ["JOB-003", "MAT-007", "스테인리스 용접봉", 6, 21, "C-02-01", "KG"],
    ["JOB-003", "MAT-008", "배관 패치", 2, 5, "C-03-07", "EA"],

    ["JOB-004", "MAT-009", "수위 센서", 1, 4, "D-01-04", "EA"],
    ["JOB-004", "MAT-010", "실드 케이블", 10, 45, "D-04-02", "M"],

    ["JOB-005", "MAT-011", "기어오일", 2, 7, "A-05-02", "CAN"],
    ["JOB-005", "MAT-012", "커플링 고무", 4, 2, "A-06-01", "EA"],

    ["JOB-006", "MAT-013", "MCCB 100AF", 1, 5, "B-06-04", "EA"],
    ["JOB-006", "MAT-014", "터미널 블록", 8, 54, "B-07-02", "EA"],

    ["JOB-007", "MAT-015", "Mechanical Seal", 1, 2, "A-09-01", "EA"],
    ["JOB-007", "MAT-016", "O-Ring", 2, 35, "A-03-03", "EA"],

    ["JOB-008", "MAT-017", "PLC 통신모듈", 1, 1, "D-06-03", "EA"],
    ["JOB-008", "MAT-018", "RJ45 산업용 커넥터", 2, 15, "D-06-05", "EA"],

    ["JOB-009", "MAT-019", "Butterfly Valve", 1, 3, "C-08-03", "EA"],
    ["JOB-009", "MAT-020", "가스켓 100A", 2, 18, "C-04-01", "EA"],

    ["JOB-010", "MAT-021", "절연저항계 리드선", 1, 6, "B-02-01", "EA"],
], columns=[
    "작업코드", "자재코드", "자재명",
    "필요수량", "현재재고", "창고위치", "단위"
])


history = pd.DataFrame({
    "월": ["4월", "5월", "6월", "7월", "8월", "9월"],
    "출고건수": [52, 61, 57, 74, 81, 93],
    "자재사용량": [132, 148, 141, 188, 207, 231],
    "긴급출고": [8, 6, 9, 7, 11, 6]
})


category_usage = pd.DataFrame({
    "분류": ["기계", "전기", "계장", "배관", "소모품"],
    "사용량": [38, 23, 14, 17, 8]
})


# =========================================================
# 4. Session State
# =========================================================

if "requests" not in st.session_state:
    st.session_state.requests = pd.DataFrame([
        {
            "신청번호": "REQ-24001",
            "작업코드": "JOB-001",
            "작업명": "순환수 펌프 베어링 교체",
            "자재명": "베어링 6205",
            "수량": 2,
            "신청자": "홍길동",
            "상태": "승인대기",
            "신청일시": "2026-09-16 09:20"
        },
        {
            "신청번호": "REQ-24002",
            "작업코드": "JOB-004",
            "작업명": "수위 센서 교체",
            "자재명": "수위 센서",
            "수량": 1,
            "신청자": "김정비",
            "상태": "출고완료",
            "신청일시": "2026-09-16 10:35"
        },
        {
            "신청번호": "REQ-24003",
            "작업코드": "JOB-005",
            "작업명": "컨베이어 감속기 점검",
            "자재명": "커플링 고무",
            "수량": 4,
            "신청자": "이기계",
            "상태": "출고대기",
            "신청일시": "2026-09-16 11:12"
        }
    ])


# =========================================================
# 5. 함수
# =========================================================

def kpi_card(label, value, description):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-number">{value}</div>
            <div class="kpi-desc">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def stock_status(row):
    if row["현재재고"] < row["필요수량"]:
        return "재고부족"
    elif row["현재재고"] <= row["필요수량"] * 2:
        return "주의"
    else:
        return "정상"


materials["재고상태"] = materials.apply(stock_status, axis=1)


# =========================================================
# 6. 사이드바
# =========================================================

with st.sidebar:

    st.markdown("""
    <div style="padding:10px 0 25px 0;">
        <div style="font-size:22px;font-weight:800;">
            CNU
        </div>
        <div style="font-size:14px;color:#AAB7C6;">
            Smart Materials
        </div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "MENU",
        [
            "종합현황",
            "작업 검색",
            "자재 신청",
            "출고 · 검수",
            "사용 이력 분석"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.caption("Capstone Design")
    st.caption("전남대학교 산업기술융합공학과")
    st.caption("v1.0 Demo")


# =========================================================
# 7. 헤더
# =========================================================

st.markdown(
    """
    <div class="main-title">
        스마트 작업·자재 관리 시스템
    </div>

    <div class="main-subtitle">
        작업정보를 기반으로 필요한 자재를 검색하고 신청·출고·사용이력을 통합 관리합니다.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 8. 종합현황
# =========================================================

if menu == "종합현황":

    request_df = st.session_state.requests

    shortage = len(
        materials[materials["재고상태"] == "재고부족"]
    )

    waiting = len(
        request_df[
            request_df["상태"].isin(["승인대기", "출고대기"])
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card(
            "등록 작업",
            len(jobs),
            "현재 시스템 등록 작업"
        )

    with c2:
        kpi_card(
            "금일 자재 신청",
            len(request_df),
            "신규 자재 요청"
        )

    with c3:
        kpi_card(
            "처리 대기",
            waiting,
            "승인 또는 출고 대기"
        )

    with c4:
        kpi_card(
            "재고 부족",
            shortage,
            "필요수량 대비 부족 품목"
        )

    st.write("")

    # -----------------------------------------------------
    # 빠른 작업 검색
    # -----------------------------------------------------

    st.markdown("""
    <div class="search-box">
        <div class="search-title">
            🔎 어떤 작업을 준비하고 있나요?
        </div>
        <div class="search-desc">
            작업명, 설비명, 작업코드를 입력하면 필요한 자재를 빠르게 확인할 수 있습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    keyword = st.text_input(
        "통합 작업 검색",
        placeholder="예: 펌프 교체 / 모터 점검 / JOB-001",
        label_visibility="collapsed"
    )

    if keyword:

        result = jobs[
            jobs.astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    keyword,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        ]

        if len(result) > 0:

            st.success(
                f"{len(result)}개의 관련 작업을 찾았습니다."
            )

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning("검색 결과가 없습니다.")

    st.write("")

    # -----------------------------------------------------
    # 그래프
    # -----------------------------------------------------

    left, right = st.columns([1.7, 1])

    with left:

        st.markdown(
            '<div class="section-title">월별 자재 출고 추이</div>',
            unsafe_allow_html=True
        )

        fig = px.area(
            history,
            x="월",
            y="출고건수",
            markers=True
        )

        fig.update_layout(
            height=330,
            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title=None,
            yaxis_title="출고 건수"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with right:

        st.markdown(
            '<div class="section-title">분야별 자재 사용 비율</div>',
            unsafe_allow_html=True
        )

        fig2 = px.donut if hasattr(px, "donut") else None

        fig2 = px.pie(
            category_usage,
            names="분류",
            values="사용량",
            hole=0.60
        )

        fig2.update_layout(
            height=330,
            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20
            ),
            legend=dict(
                orientation="h",
                y=-0.15
            )
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    st.write("")

    # -----------------------------------------------------
    # 최근 신청 + 부족재고
    # -----------------------------------------------------

    left, right = st.columns([1.6, 1])

    with left:

        st.markdown(
            '<div class="section-title">최근 자재 신청</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            request_df[
                [
                    "신청번호",
                    "작업명",
                    "자재명",
                    "수량",
                    "상태"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    with right:

        st.markdown(
            '<div class="section-title">재고 주의 품목</div>',
            unsafe_allow_html=True
        )

        warning_material = materials[
            materials["재고상태"] != "정상"
        ][
            [
                "자재명",
                "필요수량",
                "현재재고",
                "재고상태"
            ]
        ]

        st.dataframe(
            warning_material,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 9. 작업 검색
# =========================================================

elif menu == "작업 검색":

    st.markdown(
        '<div class="section-title">작업 기반 자재 검색</div>',
        unsafe_allow_html=True
    )

    keyword = st.text_input(
        "작업 검색",
        placeholder="작업명 / 작업코드 / 설비명을 입력하세요."
    )

    col1, col2 = st.columns([1, 3])

    with col1:

        department = st.selectbox(
            "부서",
            ["전체"] + sorted(
                jobs["부서"].unique().tolist()
            )
        )

    with col2:

        work_type = st.selectbox(
            "작업구분",
            ["전체"] + sorted(
                jobs["작업구분"].unique().tolist()
            )
        )

    filtered = jobs.copy()

    if keyword:

        filtered = filtered[
            filtered.astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    keyword,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        ]

    if department != "전체":
        filtered = filtered[
            filtered["부서"] == department
        ]

    if work_type != "전체":
        filtered = filtered[
            filtered["작업구분"] == work_type
        ]

    st.caption(
        f"검색 결과 {len(filtered)}건"
    )

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    if len(filtered) > 0:

        selected_job = st.selectbox(
            "상세 정보를 확인할 작업",
            filtered["작업명"].tolist()
        )

        job_info = filtered[
            filtered["작업명"] == selected_job
        ].iloc[0]

        job_materials = materials[
            materials["작업코드"]
            == job_info["작업코드"]
        ]

        st.divider()

        st.markdown(
            f"""
            ### {job_info['작업명']}

            **작업코드**
            {job_info['작업코드']}

            **설비**
            {job_info['설비']}

            **담당부서**
            {job_info['부서']}
            """
        )

        tab1, tab2, tab3 = st.tabs(
            [
                "필요 자재",
                "재고 현황",
                "작업 정보"
            ]
        )

        with tab1:

            st.dataframe(
                job_materials[
                    [
                        "자재코드",
                        "자재명",
                        "필요수량",
                        "단위",
                        "창고위치"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        with tab2:

            st.dataframe(
                job_materials[
                    [
                        "자재명",
                        "필요수량",
                        "현재재고",
                        "재고상태"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        with tab3:

            st.write(
                f"작업 종류: {job_info['작업구분']}"
            )

            st.write(
                f"작업 상태: {job_info['상태']}"
            )

            st.write(
                f"관련 설비: {job_info['설비']}"
            )


# =========================================================
# 10. 자재 신청
# =========================================================

elif menu == "자재 신청":

    st.markdown(
        '<div class="section-title">자재 신청</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(
        [1, 1.4],
        gap="large"
    )

    with left:

        selected_job = st.selectbox(
            "작업 선택",
            jobs["작업명"].tolist()
        )

        selected_code = jobs[
            jobs["작업명"]
            == selected_job
        ]["작업코드"].iloc[0]

        related_materials = materials[
            materials["작업코드"]
            == selected_code
        ]

        selected_material = st.selectbox(
            "자재 선택",
            related_materials["자재명"].tolist()
        )

        material_info = related_materials[
            related_materials["자재명"]
            == selected_material
        ].iloc[0]

        c1, c2 = st.columns(2)

        c1.metric(
            "필요 수량",
            material_info["필요수량"]
        )

        c2.metric(
            "현재 재고",
            material_info["현재재고"]
        )

        request_qty = st.number_input(
            "신청 수량",
            min_value=1,
            value=int(
                material_info["필요수량"]
            )
        )

        requester = st.text_input(
            "신청자",
            placeholder="이름을 입력하세요."
        )

        reason = st.text_area(
            "비고",
            placeholder="필요 시 요청사항을 입력하세요."
        )

        if st.button(
            "자재 신청",
            use_container_width=True
        ):

            if requester.strip() == "":

                st.warning(
                    "신청자 이름을 입력해주세요."
                )

            elif request_qty > material_info["현재재고"]:

                st.error(
                    "신청 수량이 현재 재고보다 많습니다."
                )

            else:

                req_id = (
                    "REQ-"
                    + datetime.now().strftime(
                        "%H%M%S"
                    )
                )

                new_row = pd.DataFrame([{
                    "신청번호": req_id,
                    "작업코드": selected_code,
                    "작업명": selected_job,
                    "자재명": selected_material,
                    "수량": request_qty,
                    "신청자": requester,
                    "상태": "승인대기",
                    "신청일시": datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
                }])

                st.session_state.requests = pd.concat(
                    [
                        st.session_state.requests,
                        new_row
                    ],
                    ignore_index=True
                )

                st.success(
                    "자재 신청이 완료되었습니다."
                )

    with right:

        st.markdown("#### 작업 필요 자재")

        st.dataframe(
            related_materials[
                [
                    "자재명",
                    "필요수량",
                    "현재재고",
                    "창고위치",
                    "재고상태"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 11. 출고 / 검수
# =========================================================

elif menu == "출고 · 검수":

    st.markdown(
        '<div class="section-title">출고 및 검수 현황</div>',
        unsafe_allow_html=True
    )

    requests = st.session_state.requests

    status = st.selectbox(
        "상태 필터",
        [
            "전체",
            "승인대기",
            "출고대기",
            "출고완료"
        ]
    )

    if status == "전체":
        display_df = requests

    else:
        display_df = requests[
            requests["상태"] == status
        ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.write("")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "승인 대기",
        len(
            requests[
                requests["상태"]
                == "승인대기"
            ]
        )
    )

    c2.metric(
        "출고 대기",
        len(
            requests[
                requests["상태"]
                == "출고대기"
            ]
        )
    )

    c3.metric(
        "출고 완료",
        len(
            requests[
                requests["상태"]
                == "출고완료"
            ]
        )
    )


# =========================================================
# 12. 사용 이력 분석
# =========================================================

elif menu == "사용 이력 분석":

    st.markdown(
        '<div class="section-title">자재 사용 이력 분석</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "9월 출고 건수",
        "93건",
        "+14.8%"
    )

    c2.metric(
        "9월 자재 사용량",
        "231개",
        "+11.6%"
    )

    c3.metric(
        "긴급 출고",
        "6건",
        "-45.5%"
    )

    st.write("")

    left, right = st.columns(2)

    with left:

        fig = px.line(
            history,
            x="월",
            y="자재사용량",
            markers=True,
            title="월별 자재 사용량"
        )

        fig.update_layout(
            height=380
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig2 = px.bar(
            category_usage,
            x="분류",
            y="사용량",
            title="분야별 자재 사용량"
        )

        fig2.update_layout(
            height=380
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.markdown("### 자재 재고 분석")

    stock_analysis = (
        materials
        .groupby("재고상태")
        .size()
        .reset_index(name="품목수")
    )

    fig3 = px.pie(
        stock_analysis,
        names="재고상태",
        values="품목수",
        hole=0.55
    )

    fig3.update_layout(
        height=350
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


# =========================================================
# Footer
# =========================================================

st.divider()

st.caption(
    "CNU Smart Materials Management System · Capstone Design Prototype"
)
