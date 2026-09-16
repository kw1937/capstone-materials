import streamlit as st
from datetime import datetime, timezone, timedelta
from uuid import uuid4

st.set_page_config(
    page_title="정비 자재 검색 및 신청",
    page_icon="🔧",
    layout="wide",
)

st.title("🔧 정비 자재 검색 및 일괄 신청")
st.caption(
    "가상 작업·자재 데이터로 구성한 시연입니다. "
    "실제 적용 규격·정비 이력·창고와 연결되어 있지 않습니다."
)

# 각 자재의 순서: 자재명, 기본 수량, 단위
sample_jobs = [
    ("A", "A모터 분해수리", [
        ("구동측 베어링", 1, "개"),
        ("반구동측 베어링", 1, "개"),
        ("오일씰", 2, "개"),
        ("가스켓", 1, "개"),
        ("그리스", 1, "통"),
        ("고정 볼트", 8, "개"),
    ]),
    ("B", "B펌프 분해수리", [
        ("메커니컬 씰", 1, "개"),
        ("베어링", 2, "개"),
        ("오링", 2, "개"),
        ("가스켓", 2, "개"),
        ("임펠러", 1, "개"),
        ("고정 볼트", 8, "개"),
    ]),
    ("C", "C감속기 정비", [
        ("베어링", 2, "개"),
        ("오일씰", 2, "개"),
        ("가스켓", 1, "개"),
        ("기어오일", 1, "통"),
        ("커플링 고무", 1, "세트"),
        ("체결 볼트", 6, "개"),
    ]),
    ("D", "D밸브 정비", [
        ("패킹", 1, "세트"),
        ("가스켓", 2, "개"),
        ("오링", 2, "개"),
        ("시트", 1, "개"),
        ("스템 너트", 1, "개"),
        ("체결 볼트", 8, "개"),
    ]),
    ("E", "E컨베이어 정비", [
        ("롤러", 2, "개"),
        ("베어링", 4, "개"),
        ("벨트", 1, "개"),
        ("체인", 1, "세트"),
        ("스프로킷", 2, "개"),
        ("체결 볼트", 12, "개"),
    ]),
    ("F", "F전동기 전원 케이블 교체", [
        ("전력 케이블", 20, "m"),
        ("압착 단자", 6, "개"),
        ("케이블 글랜드", 2, "개"),
        ("열수축 튜브", 6, "개"),
        ("케이블타이", 20, "개"),
        ("절연테이프", 2, "롤"),
    ]),
    ("G", "G제어반 부품 교체", [
        ("전자접촉기", 1, "개"),
        ("보조 릴레이", 2, "개"),
        ("퓨즈", 3, "개"),
        ("단자대", 1, "세트"),
        ("표시등", 2, "개"),
        ("제어선", 10, "m"),
    ]),
    ("H", "H수위계 교체", [
        ("수위계", 1, "개"),
        ("신호 케이블", 15, "m"),
        ("케이블 글랜드", 2, "개"),
        ("설치 브래킷", 1, "개"),
        ("체결 볼트", 4, "개"),
        ("단자대", 1, "세트"),
    ]),
    ("I", "I배관 누수 보수", [
        ("보수용 배관", 2, "m"),
        ("엘보", 2, "개"),
        ("플랜지", 2, "개"),
        ("가스켓", 2, "개"),
        ("볼트", 8, "개"),
        ("너트", 8, "개"),
    ]),
    ("J", "J조명설비 교체", [
        ("LED 등기구", 2, "개"),
        ("전원 케이블", 10, "m"),
        ("접속 커넥터", 4, "개"),
        ("설치 브래킷", 2, "개"),
        ("체결 볼트", 8, "개"),
        ("케이블타이", 10, "개"),
    ]),
]

# 시연용 자재 코드를 생성
# 같은 이름이어도 작업별 별도 샘플 규격으로 취급
jobs = {}

for job_id, job_title, items in sample_jobs:
    materials = []

    for index, (name, quantity, unit) in enumerate(items, start=1):
        materials.append({
            "자재 코드": f"DEMO-{job_id}-{index:03d}",
            "자재명": name,
            "기본 수량": quantity,
            "단위": unit,
        })

    jobs[job_id] = {
        "작업명": f"{job_id}작업 | {job_title}",
        "자재 목록": materials,
    }

# 현재 접속 중에만 보관할 신청 초안
if "sample_requests" not in st.session_state:
    st.session_state.sample_requests = []

if "last_request_signature" not in st.session_state:
    st.session_state.last_request_signature = None


def normalize(text):
    return "".join(text.split()).lower()


def select_all(job_id, checked):
    """현재 작업의 체크박스를 한 번에 변경"""
    for material in jobs[job_id]["자재 목록"]:
        code = material["자재 코드"]
        st.session_state[f"pick_{code}"] = checked


# 검색 안내
with st.expander("등록된 샘플 작업 10개 보기"):
    st.table([
        {
            "작업 구분": f"{job_id}작업",
            "작업명": job_title,
            "자재 종류": 6,
        }
        for job_id, job_title, _ in sample_jobs
    ])

st.subheader("1. 작업 검색")

keyword = st.text_input(
    "작업 구분 또는 작업명",
    placeholder="예: A작업, A모터, 분해수리, 케이블",
)

query = normalize(keyword)

if query:
    matches = [
        job_id
        for job_id, job in jobs.items()
        if query in normalize(job["작업명"])
    ]

    if matches:
        selected_id = st.selectbox(
            "신청할 작업을 선택하세요",
            options=matches,
            format_func=lambda job_id: jobs[job_id]["작업명"],
        )

        job = jobs[selected_id]

        st.subheader(job["작업명"])
        st.caption("해당 작업의 과거 사용 목록을 가정한 샘플 자재 6종입니다.")

        st.subheader("2. 자재 선택 및 수량 입력")

        requester = st.text_input(
            "신청자 이름",
            key="sample_requester",
            placeholder="연습할 때는 '테스트'로 입력하세요",
        )

        left, right = st.columns(2)

        with left:
            st.button(
                "전체 선택",
                on_click=select_all,
                args=(selected_id, True),
            )

        with right:
            st.button(
                "전체 해제",
                on_click=select_all,
                args=(selected_id, False),
            )

        selected_items = []

        for material in job["자재 목록"]:
            code = material["자재 코드"]

            col1, col2, col3 = st.columns([4, 2, 1])

            with col1:
                checked = st.checkbox(
                    f"{material['자재명']} · {code}",
                    key=f"pick_{code}",
                )

            with col2:
                quantity = st.number_input(
                    "신청 수량",
                    min_value=1,
                    value=material["기본 수량"],
                    step=1,
                    key=f"amount_{code}",
                )

            with col3:
                st.write("단위")
                st.write(material["단위"])

            if checked:
                selected_items.append({
                    "자재 코드": code,
                    "자재명": material["자재명"],
                    "신청 수량": int(quantity),
                    "단위": material["단위"],
                })

        st.info(f"현재 선택한 자재: {len(selected_items)}종")

        if selected_items:
            st.write("**일괄 신청할 목록**")
            st.table(selected_items)

        if st.button("선택 자재 일괄 신청 — 시연", type="primary"):
            if not requester.strip():
                st.warning("신청자 이름을 입력해주세요.")

            elif not selected_items:
                st.warning("신청할 자재를 하나 이상 선택해주세요.")

            else:
                # 같은 내용을 연속 클릭하여 중복 생성하는 것을 방지
                signature = (
                    requester.strip(),
                    selected_id,
                    tuple(
                        (item["자재 코드"], item["신청 수량"])
                        for item in selected_items
                    ),
                )

                if signature == st.session_state.last_request_signature:
                    st.warning(
                        "방금 같은 내용으로 초안을 만들었습니다. "
                        "아래 신청 초안을 확인해주세요."
                    )

                else:
                    korea_time = timezone(timedelta(hours=9))
                    now = datetime.now(korea_time)

                    request_id = (
                        f"DEMO-{now:%Y%m%d}-"
                        f"{uuid4().hex[:8].upper()}"
                    )

                    st.session_state.sample_requests.append({
                        "신청번호": request_id,
                        "신청자": requester.strip(),
                        "작업명": job["작업명"],
                        "신청일시": now.strftime("%Y-%m-%d %H:%M:%S"),
                        "자재 목록": selected_items,
                    })

                    st.session_state.last_request_signature = signature

                    st.success(
                        f"자재 {len(selected_items)}종을 "
                        f"초안 한 건으로 묶었습니다. 신청번호: {request_id}"
                    )

    else:
        st.warning("일치하는 작업이 없습니다. A작업 또는 B작업으로 검색해보세요.")

else:
    st.info("작업명을 입력하고 Enter를 눌러주세요.")

# 신청 초안 확인
st.divider()
st.subheader("3. 이번 접속에서 만든 신청 초안")
st.caption(
    "시연용 임시 기록입니다. 새로고침하거나 접속이 끊기면 사라질 수 있습니다. "
    "다른 컴퓨터와 공유되지 않으며 실제 창고로 전달되지 않습니다."
)

requests = st.session_state.sample_requests

if requests:
    for request in reversed(requests):
        title = (
            f"{request['신청번호']} · "
            f"{request['작업명']} · "
            f"{len(request['자재 목록'])}종"
        )

        with st.expander(title):
            st.write("신청자:", request["신청자"])
            st.write("신청일시(한국시간):", request["신청일시"])
            st.write("상태: 시연용 초안")
            st.table(request["자재 목록"])

else:
    st.write("아직 생성된 신청 초안이 없습니다.")
