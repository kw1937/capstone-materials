import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import datetime


# =========================================================
# 1. 페이지 기본 설정
# =========================================================

st.set_page_config(
    page_title="CNU Smart Materials",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. 전체 CSS
# =========================================================

st.html("""
<style>

/* ======================================================
   전체 화면
====================================================== */

.stApp {
    background-color: #F4F7FA;
}

.block-container {
    padding-top: 1.7rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Streamlit 기본 UI */
header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.stDeployButton {
    display: none;
}


/* ======================================================
   상단 헤더
====================================================== */

.top-header {
    background: #FFFFFF;
    border: 1px solid #E3E9F0;
    border-radius: 18px;
    padding: 18px 22px;
    margin-bottom: 24px;

    box-shadow:
        0 4px 14px rgba(15, 34, 58, 0.05);
}

.top-header-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
}

.brand-area {
    display: flex;
    align-items: center;
    gap: 16px;
}

.cnu-logo {
    width: 62px;
    height: 62px;

    border-radius: 15px;

    background:
        linear-gradient(
            135deg,
            #12375D,
            #245D91
        );

    color: white;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 18px;
    font-weight: 900;

    box-shadow:
        0 4px 12px rgba(22, 66, 107, 0.25);
}

.brand-text-wrap {
    display: flex;
    flex-direction: column;
}

.brand-small {
    font-size: 11px;
    font-weight: 800;

    color: #8390A1;

    letter-spacing: 0.8px;

    margin-bottom: 2px;
}

.brand-title {
    font-size: 28px;
    font-weight: 900;

    color: #10233D;

    line-height: 1.25;
}

.brand-subtitle {
    font-size: 13px;

    color: #778397;

    margin-top: 5px;
}


/* 사용자 영역 */

.user-area {
    display: flex;
    align-items: center;
    gap: 11px;
}

.notification-box {
    position: relative;

    width: 45px;
    height: 45px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 13px;

    background: #F5F8FB;

    border: 1px solid #E1E7EE;

    font-size: 19px;
}

.notification-badge {
    position: absolute;

    top: -5px;
    right: -5px;

    width: 19px;
    height: 19px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #F05050;

    color: white;

    border: 2px solid white;

    border-radius: 50%;

    font-size: 10px;
    font-weight: 900;
}

.user-card {
    display: flex;
    align-items: center;

    gap: 10px;

    background: #F8FAFC;

    border: 1px solid #E1E7EE;

    border-radius: 14px;

    padding: 7px 12px;
}

.user-avatar {
    width: 39px;
    height: 39px;

    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #143D66;

    color: white;

    font-size: 12px;
    font-weight: 900;
}

.user-name {
    color: #14243B;

    font-size: 13px;
    font-weight: 800;
}

.user-role {
    color: #8A95A5;

    font-size: 10px;

    margin-top: 1px;
}


/* ======================================================
   KPI 카드
====================================================== */

.kpi-card {
    background: #FFFFFF;

    padding: 22px 22px 18px 22px;

    border-radius: 16px;

    border: 1px solid #E2E7ED;

    box-shadow:
        0 3px 10px rgba(20, 40, 65, 0.04);

    min-height: 125px;
}

.kpi-label {
    color: #768399;

    font-size: 14px;

    font-weight: 700;
}

.kpi-number {
    color: #11243E;

    font-size: 32px;

    font-weight: 900;

    margin-top: 7px;
}

.kpi-desc {
    color: #98A2B1;

    font-size: 12px;

    margin-top: 3px;
}


/* ======================================================
   메인 검색 박스
====================================================== */

.search-box {
    background:
        linear-gradient(
            120deg,
            #173E67,
            #286396
        );

    border-radius: 19px;

    padding: 28px 31px;

    margin-bottom: 20px;

    box-shadow:
        0 4px 12px rgba(23, 62, 103, 0.12);
}

.search-title {
    font-size: 23px;

    color: white;

    font-weight: 900;
}

.search-desc {
    font-size: 13px;

    color: #D7E6F3;

    margin-top: 7px;
}


/* ======================================================
   일반 콘텐츠
====================================================== */

.section-title {
    color: #10213A;

    font-size: 21px;

    font-weight: 900;

    margin-top: 5px;

    margin-bottom: 13px;
}

.stButton > button {
    border-radius: 11px;

    font-weight: 800;

    min-height: 42px;
}

div[data-baseweb="input"] > div {
    border-radius: 10px;
}

button[data-baseweb="tab"] {
    font-size: 15px;

    font-weight: 800;
}

[data-testid="stDataFrame"] {
    border-radius: 12px;

    overflow: hidden;
}


/* ======================================================
   사이드바
====================================================== */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #08192D 0%,
            #0C2543 100%
        );

    min-width: 295px !important;
    max-width: 295px !important;

    border-right:
        1px solid rgba(255,255,255,0.06);
}


/* 사이드바 내부 여백 */

section[data-testid="stSidebar"]
div[data-testid="stSidebarUserContent"] {

    padding-left: 17px;
    padding-right: 17px;
}


/* 사이드바 모든 기본 텍스트 */

section[data-testid="stSidebar"] * {
    color: white;
}


/* ======================================================
   사이드바 CNU 브랜드 카드
====================================================== */

.sidebar-brand {

    background:
        rgba(255,255,255,0.045);

    border:
        1px solid rgba(255,255,255,0.08);

    border-radius: 16px;

    padding: 18px 16px;

    margin-top: 8px;
    margin-bottom: 22px;
}

.sidebar-logo {

    font-size: 30px;

    font-weight: 900;

    line-height: 1.0;

    letter-spacing: 0.5px;
}

.sidebar-sub {

    font-size: 14px;

    color: #B9C8D8 !important;

    margin-top: 8px;

    font-weight: 600;
}


/* ======================================================
   사이드바 RADIO 메뉴
====================================================== */

section[data-testid="stSidebar"]
div[role="radiogroup"] {

    gap: 8px;
}


/* 메뉴 한 칸 */

section[data-testid="stSidebar"]
label[data-baseweb="radio"] {

    background:
        rgba(255,255,255,0.045);

    border:
        1px solid rgba(255,255,255,0.08);

    border-radius: 13px;

    padding: 12px 13px !important;

    margin-bottom: 8px;

    min-height: 54px;

    display: flex;

    align-items: center;

    transition:
        background 0.18s ease,
        border 0.18s ease,
        transform 0.18s ease,
        box-shadow 0.18s ease;

    cursor: pointer;
}


/* 마우스를 올렸을 때 */

section[data-testid="stSidebar"]
label[data-baseweb="radio"]:hover {

    background:
        rgba(255,255,255,0.095);

    border-color:
        rgba(255,255,255,0.20);

    transform:
        translateX(3px);
}


/* 선택된 메뉴 */

section[data-testid="stSidebar"]
label[data-baseweb="radio"]:has(input:checked) {

    background:
        linear-gradient(
            135deg,
            #1C4D7D,
            #2E6DA5
        );

    border:
        1px solid #72B7F2;

    box-shadow:
        0 6px 16px rgba(0,0,0,0.22);
}


/* 메뉴 글자 */

section[data-testid="stSidebar"]
label[data-baseweb="radio"] p {

    font-size: 17px !important;

    font-weight: 800 !important;

    line-height: 1.35 !important;

    color: #FFFFFF !important;
}


/* 라디오 원 부분 */

section[data-testid="stSidebar"]
label[data-baseweb="radio"] > div:first-child {

    margin-right: 5px;

    transform: scale(1.05);
}


/* 구분선 */

section[data-testid="stSidebar"] hr {

    border-color:
        rgba(255,255,255,0.09);

    margin-top: 22px;
    margin-bottom: 22px;
}


/* 캡션 */

section[data-testid="stSidebar"] .stCaption {

    color: #B8C5D4 !important;

    font-size: 13px !important;

    line-height: 1.5;
}


/* ======================================================
   모바일 반응형
====================================================== */

@media (max-width: 900px) {

    .top-header-inner {

        flex-direction: column;

        align-items: flex-start;
    }

    .user-area {

        width: 100%;

        justify-content: flex-end;
    }

    .brand-title {

        font-size: 22px;
    }

    .brand-subtitle {

        font-size: 11px;
    }

    .cnu-logo {

        width: 50px;
        height: 50px;
    }
}

</style>
""")


# =========================================================
# 3. 작업 데이터
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


# =========================================================
# 4. 자재 데이터
# =========================================================

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

    ["JOB-010", "MAT-021", "절연저항계 리드선", 1, 6, "B-02-01", "EA"]

], columns=[
    "작업코드",
    "자재코드",
    "자재명",
    "필요수량",
    "현재재고",
    "창고위치",
    "단위"
])


# =========================================================
# 5. 그래프 데이터
# =========================================================

history = pd.DataFrame({

    "월": [
        "4월",
        "5월",
        "6월",
        "7월",
        "8월",
        "9월"
    ],

    "출고건수": [
        52,
        61,
        57,
        74,
        81,
        93
    ],

    "자재사용량": [
        132,
        148,
        141,
        188,
        207,
        231
    ],

    "긴급출고": [
        8,
        6,
        9,
        7,
        11,
        6
    ]

})


category_usage = pd.DataFrame({

    "분류": [
        "기계",
        "전기",
        "계장",
        "배관",
        "소모품"
    ],

    "사용량": [
        38,
        23,
        14,
        17,
        8
    ]

})


# =========================================================
# 6. 신청 데이터
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
# 7. 함수
# =========================================================

def stock_status(row):

    if row["현재재고"] < row["필요수량"]:

        return "재고부족"

    elif row["현재재고"] <= row["필요수량"] * 2:

        return "주의"

    else:

        return "정상"


materials["재고상태"] = materials.apply(
    stock_status,
    axis=1
)


def kpi_card(
    label,
    value,
    description
):

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                {label}
            </div>

            <div class="kpi-number">
                {value}
            </div>

            <div class="kpi-desc">
                {description}
            </div>

        </div>
        """
    )


# =========================================================
# 8. 사이드바
# =========================================================

menu_icons = {

    "종합현황":
        "📊 종합현황",

    "작업 검색":
        "🔎 작업 검색",

    "자재 신청":
        "📝 자재 신청",

    "출고 · 검수":
        "📦 출고 · 검수",

    "사용 이력 분석":
        "📈 사용 이력 분석"

}


with st.sidebar:

    st.html("""
    <div class="sidebar-brand">

        <div class="sidebar-logo">
            CNU
        </div>

        <div class="sidebar-sub">
            Smart Materials
        </div>

    </div>
    """)

    menu = st.radio(

        "MENU",

        [
            "종합현황",
            "작업 검색",
            "자재 신청",
            "출고 · 검수",
            "사용 이력 분석"
        ],

        format_func=lambda x:
            menu_icons[x],

        label_visibility="collapsed"
    )

    st.markdown("---")

    st.caption(
        "CAPSTONE DESIGN"
    )

    st.caption(
        "전남대학교 산업기술융합공학과"
    )

    st.caption(
        "Smart Materials Management"
    )

    st.caption(
        "v1.3 Demo"
    )


# =========================================================
# 9. 상단 헤더
# =========================================================

header_html = """

<div class="top-header">

    <div class="top-header-inner">


        <div class="brand-area">


            <div class="cnu-logo">
                CNU
            </div>


            <div class="brand-text-wrap">


                <div class="brand-small">
                    CHONNAM NATIONAL UNIVERSITY
                </div>


                <div class="brand-title">
                    스마트 작업·자재 관리 시스템
                </div>


                <div class="brand-subtitle">
                    작업정보 기반 자재 검색 · 신청 · 출고 · 재고 · 사용이력 통합관리 플랫폼
                </div>


            </div>


        </div>


        <div class="user-area">


            <div class="notification-box">

                🔔

                <div class="notification-badge">
                    3
                </div>

            </div>


            <div class="user-card">


                <div class="user-avatar">
                    KW
                </div>


                <div>


                    <div class="user-name">
                        관리자
                    </div>


                    <div class="user-role">
                        Capstone Team
                    </div>


                </div>


            </div>


        </div>


    </div>

</div>

"""

st.html(
    header_html
)


# =========================================================
# 10. 종합현황
# =========================================================

if menu == "종합현황":

    request_df = (
        st.session_state.requests
    )

    shortage = len(
        materials[
            materials["재고상태"]
            == "재고부족"
        ]
    )

    waiting = len(
        request_df[
            request_df["상태"].isin(
                [
                    "승인대기",
                    "출고대기"
                ]
            )
        ]
    )


    # -----------------------------------------------------
    # KPI
    # -----------------------------------------------------

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
    # 검색 영역
    # -----------------------------------------------------

    st.html("""
    <div class="search-box">

        <div class="search-title">
            🔎 어떤 작업을 준비하고 있나요?
        </div>

        <div class="search-desc">
            작업명, 설비명, 작업코드를 입력하면
            필요한 자재를 빠르게 확인할 수 있습니다.
        </div>

    </div>
    """)


    keyword = st.text_input(

        "통합 작업 검색",

        placeholder=
        "예: 펌프 교체 / 모터 점검 / JOB-001",

        label_visibility="collapsed"
    )


    if keyword:

        result = jobs[
            jobs.astype(str).apply(

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

            st.warning(
                "검색 결과가 없습니다."
            )


    st.write("")


    # -----------------------------------------------------
    # 그래프
    # -----------------------------------------------------

    left, right = st.columns(
        [1.7, 1]
    )


    with left:

        st.html(
            """
            <div class="section-title">
                월별 자재 출고 추이
            </div>
            """
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
                t=25,
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

            config={
                "displayModeBar":
                    False
            }
        )


    with right:

        st.html(
            """
            <div class="section-title">
                분야별 자재 사용 비율
            </div>
            """
        )


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
                t=25,
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

            config={
                "displayModeBar":
                    False
            }
        )


    # -----------------------------------------------------
    # 최근 신청 / 재고주의
    # -----------------------------------------------------

    left, right = st.columns(
        [1.6, 1]
    )


    with left:

        st.html(
            """
            <div class="section-title">
                최근 자재 신청
            </div>
            """
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

        st.html(
            """
            <div class="section-title">
                재고 주의 품목
            </div>
            """
        )


        warning_material = materials[

            materials[
                "재고상태"
            ] != "정상"

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
# 11. 작업 검색
# =========================================================

elif menu == "작업 검색":

    st.html("""
    <div class="section-title">
        🔎 작업 기반 자재 검색
    </div>
    """)


    keyword = st.text_input(

        "작업 검색",

        placeholder=
        "작업명 / 작업코드 / 설비명을 입력하세요."
    )


    col1, col2 = st.columns(
        [1, 2]
    )


    with col1:

        department = st.selectbox(

            "담당 부서",

            [
                "전체"
            ]
            +
            sorted(
                jobs[
                    "부서"
                ].unique().tolist()
            )
        )


    with col2:

        work_type = st.selectbox(

            "작업 구분",

            [
                "전체"
            ]
            +
            sorted(
                jobs[
                    "작업구분"
                ].unique().tolist()
            )
        )


    filtered = jobs.copy()


    if keyword:

        filtered = filtered[

            filtered
            .astype(str)
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
            filtered["부서"]
            == department
        ]


    if work_type != "전체":

        filtered = filtered[
            filtered["작업구분"]
            == work_type
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

            filtered[
                "작업명"
            ].tolist()
        )


        job_info = filtered[

            filtered["작업명"]
            == selected_job

        ].iloc[0]


        job_materials = materials[

            materials["작업코드"]
            ==
            job_info["작업코드"]

        ]


        st.divider()


        st.subheader(
            job_info["작업명"]
        )


        info1, info2, info3 = st.columns(
            3
        )


        info1.metric(
            "작업 코드",
            job_info["작업코드"]
        )


        info2.metric(
            "설비",
            job_info["설비"]
        )


        info3.metric(
            "현재 상태",
            job_info["상태"]
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
                f"**작업 종류:** {job_info['작업구분']}"
            )

            st.write(
                f"**담당 부서:** {job_info['부서']}"
            )

            st.write(
                f"**관련 설비:** {job_info['설비']}"
            )

            st.write(
                f"**작업 상태:** {job_info['상태']}"
            )


# =========================================================
# 12. 자재 신청
# =========================================================

elif menu == "자재 신청":

    st.html("""
    <div class="section-title">
        📝 자재 신청
    </div>
    """)


    left, right = st.columns(
        [1, 1.4],
        gap="large"
    )


    with left:

        selected_job = st.selectbox(

            "작업 선택",

            jobs[
                "작업명"
            ].tolist()
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

            related_materials[
                "자재명"
            ].tolist()
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
                material_info[
                    "필요수량"
                ]
            )
        )


        requester = st.text_input(

            "신청자",

            placeholder=
            "이름을 입력하세요."
        )


        reason = st.text_area(

            "비고",

            placeholder=
            "필요 시 요청사항을 입력하세요."
        )


        if st.button(
            "자재 신청",
            use_container_width=True,
            type="primary"
        ):

            if requester.strip() == "":

                st.warning(
                    "신청자 이름을 입력해주세요."
                )


            elif (
                request_qty
                >
                material_info["현재재고"]
            ):

                st.error(
                    "신청 수량이 현재 재고보다 많습니다."
                )


            else:

                req_id = (
                    "REQ-"
                    +
                    datetime.now().strftime(
                        "%H%M%S"
                    )
                )


                new_row = pd.DataFrame(
                    [
                        {
                            "신청번호":
                                req_id,

                            "작업코드":
                                selected_code,

                            "작업명":
                                selected_job,

                            "자재명":
                                selected_material,

                            "수량":
                                request_qty,

                            "신청자":
                                requester,

                            "상태":
                                "승인대기",

                            "신청일시":
                                datetime.now().strftime(
                                    "%Y-%m-%d %H:%M"
                                )
                        }
                    ]
                )


                st.session_state.requests = (
                    pd.concat(
                        [
                            st.session_state.requests,
                            new_row
                        ],
                        ignore_index=True
                    )
                )


                st.success(
                    "자재 신청이 완료되었습니다."
                )


    with right:

        st.subheader(
            "작업 필요 자재"
        )


        st.dataframe(

            related_materials[
                [
                    "자재코드",
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
# 13. 출고 / 검수
# =========================================================

elif menu == "출고 · 검수":

    st.html("""
    <div class="section-title">
        📦 출고 및 검수 현황
    </div>
    """)


    requests = (
        st.session_state.requests
    )


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
            requests["상태"]
            == status
        ]


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


    st.write("")


    st.dataframe(

        display_df,

        use_container_width=True,

        hide_index=True
    )


# =========================================================
# 14. 사용 이력 분석
# =========================================================

elif menu == "사용 이력 분석":

    st.html("""
    <div class="section-title">
        📈 자재 사용 이력 분석
    </div>
    """)


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

            title=
            "월별 자재 사용량"
        )


        fig.update_layout(
            height=380
        )


        st.plotly_chart(

            fig,

            use_container_width=True,

            config={
                "displayModeBar":
                    False
            }
        )


    with right:

        fig2 = px.bar(

            category_usage,

            x="분류",

            y="사용량",

            title=
            "분야별 자재 사용량"
        )


        fig2.update_layout(
            height=380
        )


        st.plotly_chart(

            fig2,

            use_container_width=True,

            config={
                "displayModeBar":
                    False
            }
        )


    st.subheader(
        "재고 상태 분석"
    )


    stock_analysis = (

        materials
        .groupby(
            "재고상태"
        )
        .size()
        .reset_index(
            name="품목수"
        )
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

        use_container_width=True,

        config={
            "displayModeBar":
                False
        }
    )


# =========================================================
# 15. Footer
# =========================================================

st.divider()

st.caption(
    "CNU Smart Materials Management System "
    "· Chonnam National University "
    "· Capstone Design Prototype"
)
