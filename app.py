import streamlit as st
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from html import escape

st.set_page_config(page_title="정비 자재 관리 포털", page_icon="🔧", layout="wide")

# 외부 이미지·폰트 없이 작동하는 대학 포털 스타일
st.markdown("""
<style>
:root { --green:#14804a; --ink:#21392f; --line:#dce5df; }
.stApp { background:#f3f6f4; color:#21392f; }
[data-testid="stHeader"] { background:#f3f6f4; }
.block-container { max-width:1360px; padding-top:3.5rem; padding-bottom:2rem; }
h1,h2,h3 { color:#203d30 !important; }
h3 { font-size:1.15rem !important; letter-spacing:-.035em; }
p,label,button,input { font-family: "Malgun Gothic", "Apple SD Gothic Neo", sans-serif; }
.portal-strip {background:#168849;color:white;padding:10px 22px;font-size:13px;
 display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;border-radius:8px 8px 0 0;}
.portal-brand {background:white;border-bottom:3px solid #168849;padding:24px;
 display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-bottom:20px;}
.brand-left {display:flex;align-items:center;gap:14px;}
.brand-icon {background:#14804a;color:white;border-radius:12px;padding:13px;font-size:20px;font-weight:800;}
.brand-title {font-size:29px;font-weight:800;letter-spacing:-1px;color:#243c30;}
.brand-title span {color:#168849;}
.brand-small {font-size:11px;letter-spacing:1.6px;color:#7c8c82;margin-top:3px;}
.brand-note {font-size:13px;color:#6c7e72;}
.hero {border-radius:10px;padding:27px 30px;background:linear-gradient(110deg,#134631,#187d4c);
 color:white;margin-bottom:8px;position:relative;overflow:hidden;}
.hero::after {content:"";position:absolute;right:-45px;top:-80px;width:290px;height:290px;
 border:45px solid rgba(255,255,255,.06);border-radius:50%;pointer-events:none;}
.hero-label {font-size:11px;letter-spacing:2px;color:#a9d7bb;font-weight:700;}
.hero-title {font-size:29px;line-height:1.5;letter-spacing:-1px;font-weight:750;margin:8px 0;}
.hero-copy {font-size:14px;color:#d4e9dc;line-height:1.8;}
.notice {background:#fff;border:1px solid #dce5df;border-left:4px solid #b79959;
 padding:12px 17px;margin:16px 0 22px;font-size:13px;color:#56685d;}
.notice strong {color:#876e3e;margin-right:12px;}
.st-key-search-panel,.st-key-material-panel,.st-key-summary-panel,.st-key-guide-panel,.st-key-history-panel {
 background:white;border:1px solid #dce5df;border-radius:10px;padding:20px; }
.st-key-summary-panel {border-top:4px solid #168849;}
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input {color:#21392f;background:#f5f8f6;}
[data-baseweb="select"] > div {background:#f5f8f6;color:#21392f;}
[data-testid="stWidgetLabel"] p {color:#344c3e;}
[data-testid="stCaptionContainer"] {color:#687e70;}
[data-testid="stButton"] button {border:1px solid #cdded2;border-radius:6px;color:#215b3b;background:white;}
[data-testid="stButton"] button:hover {border-color:#168849;color:#168849;background:#f0f8f2;}
[data-testid="stButton"] button[kind="primary"] {background:#14804a;border-color:#14804a;color:white;}
[data-testid="stButton"] button[kind="primary"]:hover {background:#096332;color:white;}
.material-name {font-size:15px;font-weight:650;color:#293f32;margin-bottom:5px;}
.material-code {font-size:12px;color:#77877d;}
.row-label {font-size:12px;color:#7a8b80;border-bottom:1px solid #e7eee9;padding-bottom:9px;}
.summary-job {background:#eff6f0;border-radius:7px;padding:14px;font-weight:700;color:#245a39;font-size:14px;}
.count {font-size:40px;color:#168849;line-height:1.2;font-weight:800;}
.count-label {color:#6d8072;font-size:12px;margin-bottom:5px;}
.empty {padding:28px 12px;background:#f6f9f7;border:1px dashed #d2dfd6;
 text-align:center;color:#6c8071;border-radius:8px;line-height:1.9;font-size:14px;}
.summary-line {display:flex;justify-content:space-between;gap:12px;padding:8px 0;
 border-bottom:1px solid #edf1ee;font-size:13px;color:#415848;}
.guide-step {display:flex;gap:12px;margin:12px 0;color:#516b5a;font-size:13px;line-height:1.8;}
.guide-number {color:#17834b;font-weight:800;}
.footer {border-top:1px solid #dce5df;margin-top:26px;padding-top:18px;
 color:#76877d;font-size:12px;line-height:1.9;}
@media(max-width:700px){.block-container{padding-left:1rem;padding-right:1rem;}
 .brand-title{font-size:22px;}.hero-title{font-size:23px;}.portal-brand{padding:18px;}}
</style>
""", unsafe_allow_html=True)

# 샘플 목록: (이름, 기본 수량, 단위). 실제 부품 사양이 아닙니다.
sample_jobs = [
    ("A", "A모터 분해수리", [("구동측 베어링",1,"개"),("반구동측 베어링",1,"개"),("오일씰",2,"개"),("가스켓",1,"개"),("그리스",1,"통"),("고정 볼트",8,"개")]),
    ("B", "B펌프 분해수리", [("메커니컬 씰",1,"개"),("베어링",2,"개"),("오링",2,"개"),("가스켓",2,"개"),("임펠러",1,"개"),("고정 볼트",8,"개")]),
    ("C", "C감속기 정비", [("베어링",2,"개"),("오일씰",2,"개"),("가스켓",1,"개"),("기어오일",1,"통"),("커플링 고무",1,"세트"),("체결 볼트",6,"개")]),
    ("D", "D밸브 정비", [("패킹",1,"세트"),("가스켓",2,"개"),("오링",2,"개"),("시트",1,"개"),("스템 너트",1,"개"),("체결 볼트",8,"개")]),
    ("E", "E컨베이어 정비", [("롤러",2,"개"),("베어링",4,"개"),("벨트",1,"개"),("체인",1,"세트"),("스프로킷",2,"개"),("체결 볼트",12,"개")]),
    ("F", "F전동기 전원 케이블 교체", [("전력 케이블",20,"m"),("압착 단자",6,"개"),("케이블 글랜드",2,"개"),("열수축 튜브",6,"개"),("케이블타이",20,"개"),("절연테이프",2,"롤")]),
    ("G", "G제어반 부품 교체", [("전자접촉기",1,"개"),("보조 릴레이",2,"개"),("퓨즈",3,"개"),("단자대",1,"세트"),("표시등",2,"개"),("제어선",10,"m")]),
    ("H", "H수위계 교체", [("수위계",1,"개"),("신호 케이블",15,"m"),("케이블 글랜드",2,"개"),("설치 브래킷",1,"개"),("체결 볼트",4,"개"),("단자대",1,"세트")]),
    ("I", "I배관 누수 보수", [("보수용 배관",2,"m"),("엘보",2,"개"),("플랜지",2,"개"),("가스켓",2,"개"),("볼트",8,"개"),("너트",8,"개")]),
    ("J", "J조명설비 교체", [("LED 등기구",2,"개"),("전원 케이블",10,"m"),("접속 커넥터",4,"개"),("설치 브래킷",2,"개"),("체결 볼트",8,"개"),("케이블타이",10,"개")]),
]
jobs = {}
for job_id, title, items in sample_jobs:
    jobs[job_id] = {
        "작업명": f"{job_id}작업 | {title}",
        "자재 목록": [
            {"자재 코드":f"DEMO-{job_id}-{i:03d}","자재명":name,"기본 수량":qty,"단위":unit}
            for i,(name,qty,unit) in enumerate(items,1)
        ],
    }

if "sample_requests" not in st.session_state:
    st.session_state.sample_requests = []
if "last_request_signature" not in st.session_state:
    st.session_state.last_request_signature = None
# 화면 전환 시에도 입력을 유지하는 별도 데이터
if "portal_choices" not in st.session_state:
    st.session_state.portal_choices = {}
if "portal_amounts" not in st.session_state:
    st.session_state.portal_amounts = {}


def normalize(value):
    return "".join(value.split()).lower()


def change_all(job_id, value):
    for material in jobs[job_id]["자재 목록"]:
        code = material["자재 코드"]
        st.session_state.portal_choices[code] = value
        st.session_state[f"portal_pick_{code}"] = value


def remember_choice(code):
    st.session_state.portal_choices[code] = st.session_state[f"portal_pick_{code}"]


def remember_amount(code):
    st.session_state.portal_amounts[code] = st.session_state[f"portal_qty_{code}"]


st.markdown("""
<div class="portal-strip"><span>전남대학교 캡스톤 디자인 · 불꽃스파크 2조</span><span>CAPSTONE DEMO · 가상 데이터</span></div>
<div class="portal-brand"><div class="brand-left"><div class="brand-icon">M</div><div>
<div class="brand-title">정비 자재 <span>관리 포털</span></div>
<div class="brand-small">MAINTENANCE MATERIALS PORTAL</div></div></div>
<div class="brand-note">작업 검색 &nbsp; / &nbsp; 자재 선택 &nbsp; / &nbsp; 신청 초안</div></div>
<div class="hero"><div class="hero-label">SMART MAINTENANCE · MATERIAL REQUEST</div>
<div class="hero-title">작업은 쉽게 찾고,<br>필요한 자재는 한 번에.</div>
<div class="hero-copy">작업별 사용 자재를 확인하고 필요한 품목과 수량을 선택하세요.<br>
샘플 작업 10개로 검색부터 일괄 신청까지 경험할 수 있습니다.</div></div>
<div class="notice"><strong>이용 안내</strong>본 사이트는 캡스톤 시연용입니다. 신청 초안은 실제 접수·출고로 연결되지 않습니다.</div>
""", unsafe_allow_html=True)

main, side = st.columns([2.15, 1], gap="large")
selected_id = None
selected_items = []
with main:
    with st.container(key="search-panel"):
        st.subheader("01  작업 검색")
        keyword = st.text_input("설비명 또는 작업명", placeholder="A작업, A모터, 분해수리, 케이블 등으로 검색", key="portal_query")
        query = normalize(keyword)
        matches = [j for j in jobs if not query or query in normalize(jobs[j]["작업명"])]
        if matches:
            st.caption(f"검색 결과 {len(matches)}개 · 작업을 선택하면 자재 6종이 표시됩니다.")
            selected_id = st.selectbox("신청할 작업", matches, format_func=lambda j:jobs[j]["작업명"], index=None, placeholder="작업을 선택해주세요", key="portal_job")
        else:
            st.info("일치하는 작업이 없습니다. A작업 또는 모터로 검색해보세요.")
        with st.expander("등록된 작업 전체 보기"):
            st.table([{"작업":f"{j}작업","작업명":title,"자재 종류":"6종"} for j,title,_ in sample_jobs])

    with st.container(key="material-panel"):
        st.subheader("02  자재 목록 및 수량")
        if selected_id is None:
            st.markdown('<div class="empty">위에서 작업을 선택해주세요.<br>선택한 작업의 자재 목록이 여기에 표시됩니다.</div>', unsafe_allow_html=True)
        else:
            st.caption("과거 사용 목록을 가정한 샘플입니다. 필요한 자재에 체크하고 수량을 조정하세요.")
            b1,b2=st.columns(2)
            b1.button("전체 선택",on_click=change_all,args=(selected_id,True),width="stretch")
            b2.button("전체 해제",on_click=change_all,args=(selected_id,False),width="stretch")
            st.markdown('<div class="row-label">선택 / 자재명 · 자재 코드　　　　　　　　　신청 수량</div>',unsafe_allow_html=True)
            for material in jobs[selected_id]["자재 목록"]:
                code=material["자재 코드"]
                ck=f"portal_pick_{code}"
                qk=f"portal_qty_{code}"
                if ck not in st.session_state:
                    st.session_state[ck]=st.session_state.portal_choices.get(code,False)
                if qk not in st.session_state:
                    st.session_state[qk]=st.session_state.portal_amounts.get(code,material["기본 수량"])
                c1,c2,c3=st.columns([.55,3.2,1.6],vertical_alignment="center")
                with c1:
                    checked=st.checkbox(f"{material['자재명']} 선택",key=ck,label_visibility="collapsed",on_change=remember_choice,args=(code,))
                with c2:
                    st.markdown(f'<div class="material-name">{escape(material["자재명"])}</div><div class="material-code">{escape(code)} · 기본 {material["기본 수량"]}{escape(material["단위"])}</div>',unsafe_allow_html=True)
                with c3:
                    qty=st.number_input(f"{material['자재명']} 수량 ({material['단위']})",min_value=1,step=1,key=qk,on_change=remember_amount,args=(code,))
                if checked:
                    selected_items.append({"자재 코드":code,"자재명":material["자재명"],"신청 수량":int(qty),"단위":material["단위"]})

with side:
    with st.container(key="summary-panel"):
        st.subheader("03  신청 요약")
        title=jobs[selected_id]["작업명"] if selected_id else "선택한 작업이 없습니다"
        st.markdown(f'<div class="summary-job">{escape(title)}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="count-label">선택한 자재 종류</div><div class="count">{len(selected_items)} <span style="font-size:16px">종</span></div>',unsafe_allow_html=True)
        if selected_items:
            for item in selected_items:
                st.markdown(f'<div class="summary-line"><span>{escape(item["자재명"])}</span><strong>{item["신청 수량"]} {escape(item["단위"])}</strong></div>',unsafe_allow_html=True)
        else:
            st.caption("목록의 체크박스로 자재를 선택해주세요.")
        requester=st.text_input("신청자 이름",placeholder="시연할 때는 ‘테스트’ 입력",key="sample_requester")
        if st.button("선택 자재 일괄 신청 · 시연",type="primary",width="stretch",disabled=selected_id is None):
            if not requester.strip():
                st.warning("신청자 이름을 입력해주세요.")
            elif not selected_items:
                st.warning("자재를 하나 이상 선택해주세요.")
            else:
                signature=(requester.strip(),selected_id,tuple((r["자재 코드"],r["신청 수량"]) for r in selected_items))
                if signature==st.session_state.last_request_signature:
                    st.info("방금 같은 내용으로 만든 초안이 있습니다. 아래 신청 초안을 확인해주세요.")
                else:
                    now=datetime.now(timezone(timedelta(hours=9)))
                    number=f"DEMO-{now:%Y%m%d}-{uuid4().hex[:8].upper()}"
                    st.session_state.sample_requests.append({"신청번호":number,"신청자":requester.strip(),"작업명":title,"신청일시":now.strftime("%Y-%m-%d %H:%M:%S"),"자재 목록":selected_items})
                    st.session_state.last_request_signature=signature
                    st.success(f"{len(selected_items)}종의 신청 초안을 만들었습니다. 아래에서 확인하세요.")
        st.caption("임시 초안 생성 기능입니다. 새로고침 시 기록이 사라질 수 있으며 다른 컴퓨터와 공유되지 않습니다.")
    with st.container(key="guide-panel"):
        st.subheader("이용 순서")
        st.markdown('''<div class="guide-step"><span class="guide-number">01</span><span>작업명 검색 후 대상 작업 선택</span></div>
<div class="guide-step"><span class="guide-number">02</span><span>자재 체크 및 신청 수량 수정</span></div>
<div class="guide-step"><span class="guide-number">03</span><span>신청자 입력 후 일괄 신청</span></div>
<div class="guide-step"><span class="guide-number">04</span><span>아래에서 묶음 신청 초안 확인</span></div>''',unsafe_allow_html=True)

with st.container(key="history-panel"):
    st.subheader("이번 접속의 신청 초안")
    records=st.session_state.sample_requests
    st.caption(f"총 {len(records)}건 · 시연용 임시 기록 · 영구 저장 및 창고 제어 미연결")
    if not records:
        st.markdown('<div class="empty">아직 신청 초안이 없습니다.<br>자재를 선택하고 일괄 신청하면 이곳에서 확인할 수 있습니다.</div>',unsafe_allow_html=True)
    for record in reversed(records):
        with st.expander(f'{record["신청번호"]} | {record["작업명"]} | {len(record["자재 목록"])}종'):
            st.write("신청자:",record["신청자"])
            st.write("신청일시(한국시간):",record["신청일시"])
            st.caption("처리 상태: 시연용 초안")
            st.table(record["자재 목록"])

st.markdown('<div class="footer">전남대학교 캡스톤 디자인 · 불꽃스파크 2조<br>정비 자재 관리 포털 — 학생 프로젝트 시연 화면 · 대학 공식 서비스가 아닙니다.</div>',unsafe_allow_html=True)
