"""
TalentScout Hiring Assistant
A conversational AI chatbot for initial candidate screening.
"""

import streamlit as st
import json
from datetime import datetime

from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="TalentScout | Hiring Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>

/* ── GOOGLE FONTS ── */
@import url('https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,400;0,600;0,700;0,800;0,900;1,700;1,800&display=swap');

/* ── ROOT PALETTE ── */
:root {
    --bg:         #FAF8F5;
    --card:       #FFFFFF;
    --ink:        #1E1B2E;
    --ink-soft:   #484466;
    --ink-muted:  #9B97B2;

    --peach:      #FFD4BE;
    --mint:       #C2EDDA;
    --sky:        #BDD8FF;
    --lav:        #DDD4FF;
    --butter:     #FFECB3;
    --blush:      #FFCFE8;

    --peach-dk:   #7A2E0E;
    --mint-dk:    #145235;
    --sky-dk:     #0F3470;
    --lav-dk:     #3A1F8A;

    --border:     #ECEAF2;
    --sh-sm:      0 2px 8px rgba(30,27,46,0.07);
    --sh-md:      0 6px 28px rgba(30,27,46,0.09);
}

/* ── WHOLE APP ── */
.stApp {
    background-color: var(--bg);
    font-family: 'Nunito', sans-serif;
    color: var(--ink);
}

.block-container {
    max-width: 860px;
    padding-top: 2.6rem;
    padding-bottom: 2rem;
}

/* ═══════════════════════════════════════
   HEADER — big, bubbly, hierarchical
═══════════════════════════════════════ */
.header-wrap { text-align: center; margin-bottom: 2.4rem; }

.live-chip {
    display: inline-flex; align-items: center; gap: 7px;
    background: var(--card); border: 2px solid var(--border);
    color: var(--ink-muted); font-family: 'Nunito', sans-serif;
    font-weight: 800; font-size: 0.63rem; letter-spacing: 0.16em;
    text-transform: uppercase; padding: 6px 16px 6px 12px;
    border-radius: 999px; margin-bottom: 18px; box-shadow: var(--sh-sm);
}
.live-dot {
    width: 7px; height: 7px; background: #4ADE80;
    border-radius: 50%; display: inline-block;
    box-shadow: 0 0 0 3px rgba(74,222,128,0.25);
}

/* Giant title — Nunito Black */
.hero-title {
    font-family: 'Nunito', sans-serif;
    font-size: 5.2rem; font-weight: 900;
    color: var(--ink); line-height: 1.0;
    letter-spacing: 3px; margin: 0;
}
/* "Scout" — peach bubble block */
.hero-title .word-scout {
    display: inline-block;
    background: var(--peach); color: var(--peach-dk);
    border-radius: 20px; padding: 2px 20px 6px;
    margin-left: 8px; font-style: italic;
}

/* Tagline hierarchy — two sizes, clear distinction */
.hero-tagline-big {
    display: block; font-family: 'Nunito', sans-serif;
    font-size: 1.35rem; font-weight: 800; color: var(--ink);
    margin: 16px 0 5px; letter-spacing: -0.3px;
}
.hero-tagline-small {
    display: block; font-family: 'Nunito', sans-serif;
    font-size: 0.84rem; font-weight: 500; color: var(--ink-muted);
}

/* Pills */
.pills-row {
    display: flex; justify-content: center;
    flex-wrap: wrap; gap: 8px; margin-top: 18px;
}
.fp {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 8px 16px; border-radius: 999px;
    font-family: 'Nunito', sans-serif; font-size: 0.74rem;
    font-weight: 800; border: 2px solid transparent;
}
.fp-peach { background: var(--peach); color: var(--peach-dk); border-color: #F0B99A; }
.fp-mint  { background: var(--mint);  color: var(--mint-dk);  border-color: #96D9BB; }
.fp-sky   { background: var(--sky);   color: var(--sky-dk);   border-color: #94BFFF; }
.fp-lav   { background: var(--lav);   color: var(--lav-dk);   border-color: #BBAEFF; }

/* ═══════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: var(--card);
    border-right: 2px solid var(--border);
}

/* Sidebar top banner */
.sb-banner {
    background: linear-gradient(135deg, var(--peach) 0%, var(--blush) 55%, var(--lav) 100%);
    border-radius: 18px; padding: 16px 14px 14px;
    margin-bottom: 14px; text-align: center;
}
.sb-banner-emoji { font-size: 1.8rem; display: block; margin-bottom: 4px; }
.sb-banner-title {
    font-family: 'Nunito', sans-serif; font-size: 1.05rem !important;
    font-weight: 900 !important; color: var(--ink) !important;
    letter-spacing: -0.3px; margin: 0 0 2px !important; display: block;
}
.sb-banner-sub {
    font-family: 'Nunito', sans-serif; font-size: 0.66rem !important;
    font-weight: 600 !important; color: var(--ink-soft) !important; display: block;
}

/* Section labels */
.sb-section-label {
    font-family: 'Nunito', sans-serif; font-size: 0.58rem !important;
    font-weight: 900 !important; color: var(--ink-muted) !important;
    text-transform: uppercase; letter-spacing: 0.16em;
    margin: 14px 0 7px !important; display: block;
}

/* Status badge */
.status-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: var(--mint); color: var(--mint-dk);
    padding: 5px 14px; border-radius: 999px;
    font-family: 'Nunito', sans-serif; font-size: 0.63rem;
    font-weight: 900; letter-spacing: 0.12em; text-transform: uppercase;
    border: 2px solid #96D9BB;
}

/* Profile cards */
.candidate-info {
    background: var(--bg); padding: 10px 12px;
    border-radius: 14px; margin: 6px 0;
    border: 2px solid var(--border); border-left: 5px solid var(--peach);
}
.candidate-info:nth-child(2n) { border-left-color: var(--mint); }
.candidate-info:nth-child(3n) { border-left-color: var(--sky);  }
.candidate-info:nth-child(4n) { border-left-color: var(--lav);  }
.candidate-info:nth-child(5n) { border-left-color: var(--butter); }
.candidate-info p {
    font-family: 'Nunito', sans-serif !important; color: var(--ink-muted) !important;
    font-size: 0.58rem !important; text-transform: uppercase !important;
    font-weight: 900 !important; letter-spacing: 0.14em; margin-bottom: 2px;
}
.candidate-info strong {
    font-family: 'Nunito', sans-serif; color: var(--ink) !important;
    font-size: 0.83rem; font-weight: 700;
}

/* Interview progress tracker */
.sb-progress-wrap {
    background: var(--bg); border-radius: 16px;
    border: 2px solid var(--border); padding: 12px 13px; margin-bottom: 10px;
}
.sb-progress-title {
    font-family: 'Nunito', sans-serif; font-size: 0.70rem !important;
    font-weight: 900 !important; color: var(--ink) !important;
    margin-bottom: 10px !important; display: block;
}
.sb-step { display: flex; align-items: center; gap: 9px; margin-bottom: 7px; }
.sb-step-dot {
    width: 22px; height: 22px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.60rem; font-weight: 900; flex-shrink: 0;
}
.sb-step-dot.done   { background: var(--mint);   color: var(--mint-dk); border: 2px solid #96D9BB; }
.sb-step-dot.active { background: var(--sky);    color: var(--sky-dk);  border: 2px solid #94BFFF; }
.sb-step-dot.todo   { background: var(--border); color: var(--ink-muted); border: 2px solid #DCDCDC; }
.sb-step-label { font-family: 'Nunito', sans-serif; font-size: 0.72rem !important; font-weight: 700 !important; }
.sb-step-label.done   { color: var(--mint-dk) !important; }
.sb-step-label.active { color: var(--sky-dk) !important; font-weight: 800 !important; }
.sb-step-label.todo   { color: var(--ink-muted) !important; }

/* Tips card */
.sb-tip {
    background: linear-gradient(135deg, var(--butter) 0%, #FFFAEA 100%);
    border: 2px solid #F0D87A; border-radius: 16px;
    padding: 11px 13px; margin-bottom: 10px;
}
.sb-tip-title {
    font-family: 'Nunito', sans-serif; font-size: 0.68rem !important;
    font-weight: 900 !important; color: #7A5C00 !important;
    margin-bottom: 5px !important; display: block;
}
.sb-tip-body {
    font-family: 'Nunito', sans-serif; font-size: 0.68rem !important;
    font-weight: 600 !important; color: #7A5C00 !important; line-height: 1.65 !important;
}

/* Privacy note */
.sb-privacy {
    background: var(--bg); border: 2px solid var(--border);
    border-radius: 14px; padding: 10px 12px; margin-top: 6px;
}
.sb-privacy-text {
    font-family: 'Nunito', sans-serif; font-size: 0.64rem !important;
    font-weight: 600 !important; color: var(--ink-muted) !important; line-height: 1.65 !important;
}

/* ═══════════════════════════════════════
   CHAT BUBBLES
═══════════════════════════════════════ */
.bot-bubble {
    background: var(--card); border-radius: 22px 22px 22px 6px;
    padding: 18px 22px; margin: 12px 65px 12px 0;
    font-family: 'Nunito', sans-serif; font-size: 0.88rem;
    font-weight: 500; line-height: 1.9; color: var(--ink-soft);
    box-shadow: var(--sh-md); border: 2px solid var(--border);
}
.user-bubble {
    background: var(--lav); color: var(--lav-dk) !important;
    border-radius: 22px 22px 6px 22px; padding: 16px 20px;
    margin: 12px 0 12px 65px; font-family: 'Nunito', sans-serif;
    font-size: 0.88rem; font-weight: 700; line-height: 1.8;
    border: 2px solid #BBAEFF;
}

/* ═══════════════════════════════════════
   INPUT FORM
═══════════════════════════════════════ */
.stForm {
    background: var(--card); border-radius: 22px; padding: 14px 18px;
    border: 2px solid var(--border); box-shadow: var(--sh-md);
}
.stTextInput input {
    background: var(--bg) !important; border: 2px solid var(--border) !important;
    border-radius: 14px !important; color: var(--ink) !important;
    padding: 13px 16px !important; font-family: 'Nunito', sans-serif !important;
    font-size: 0.88rem !important; font-weight: 600 !important;
}
.stTextInput input:focus {
    border: 2px solid #94BFFF !important;
    box-shadow: 0 0 0 4px rgba(148,191,255,0.25) !important;
    background: #FFFFFF !important;
}
.stTextInput input::placeholder {
    color: var(--ink-muted) !important; font-weight: 500 !important;
}

/* ── BUTTONS — dark bg, pure white text, -webkit-text-fill-color override ── */
.stButton button,
.stFormSubmitButton button {
    background: var(--ink) !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: none !important; border-radius: 14px !important;
    padding: 13px 22px !important; font-family: 'Nunito', sans-serif !important;
    font-size: 0.88rem !important; font-weight: 900 !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 4px 14px rgba(30,27,46,0.22) !important;
}
.stButton button:hover,
.stFormSubmitButton button:hover {
    background: #352F60 !important; transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(30,27,46,0.28) !important;
    color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important;
}
/* Force white on any inner span Streamlit wraps around button text */
.stButton button p,
.stFormSubmitButton button p,
.stButton button span,
.stFormSubmitButton button span {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 900 !important;
}

/* ── GLOBAL TEXT ── */
p, label, span {
    font-family: 'Nunito', sans-serif !important;
    color: var(--ink-soft) !important;
    font-size: 0.82rem !important;
}

/* ── DONE CARD ── */
.done-card {
    background: var(--mint); border: 2px solid #96D9BB;
    border-radius: 20px; padding: 22px 24px;
    text-align: center; margin-top: 16px;
}
.done-card .done-main {
    font-family: 'Nunito', sans-serif; color: var(--mint-dk) !important;
    font-size: 0.94rem !important; font-weight: 800 !important; margin-bottom: 5px;
}
.done-card .done-sub {
    font-family: 'Nunito', sans-serif; color: #1F6B47 !important;
    font-size: 0.76rem !important; font-weight: 600 !important;
}

/* ── HIDE DEFAULTS ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

/* ── FORCE SIDEBAR ALWAYS OPEN ── */
section[data-testid="stSidebar"] {
    min-width: 260px !important;
    max-width: 300px !important;
    transform: none !important;
    visibility: visible !important;
    display: block !important;
}

/* Hide the collapse/expand arrow button */
button[data-testid="collapsedControl"],
button[kind="header"] {
    display: none !important;
}

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# System Prompt
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are TalentScout, a professional and friendly AI hiring assistant for a tech recruitment agency. Your sole purpose is to conduct initial candidate screening interviews.

## Your Conversation Flow
Follow these stages internally but NEVER mention stage names or labels in your responses:
**STAGE 1 - GREETING**: Greet the candidate warmly, introduce yourself, and briefly mention data privacy.

**STAGE 2 - INFO GATHERING**: Collect the following details ONE AT A TIME (never ask multiple things at once):
1. Full Name
2. Email Address
3. Phone Number
4. Years of Experience
5. Desired Position(s)
6. Current Location
7. Tech Stack (programming languages, frameworks, databases, tools)
8. Work preference: Full-time or Internship?
9. Work mode preference: Remote, On-site, or Hybrid?
10. Availability / Notice period

**STAGE 3 - TECHNICAL ASSESSMENT**: Based ONLY on their declared tech stack, ask exactly 3 targeted technical questions, ONE AT A TIME. Wait for their full answer before asking the next. Tailor difficulty to years of experience. After asking all 3, acknowledge their answers with a brief encouraging remark.

**STAGE 4 - WRAP UP**: Thank them warmly by name, give a short summary of their profile (name, position, stack, preferences), and inform them the TalentScout team will review and reach out within 3-5 business days.

## Rules
- Stay strictly on topic. If asked anything unrelated, politely redirect.
- Be warm, encouraging, and professional at all times.
- Keep questions short and answerable in 2-3 sentences. Never ask someone to write out functions or code.
- Good question style: "Can you explain how X works?" or "What's the difference between X and Y?" or "When would you use X over Y?"
- Bad question style: "Write a function that does X" or "Implement Y"
- Tailor difficulty to years of experience but keep it chat-friendly.
- Never ask generic questions like "what is OOP".
- After collecting tech stack, say: "Great! I'll now ask you 3 technical questions based on your stack."
- Never ask for sensitive info beyond what's listed above.
- Keep responses concise and conversational — one question or thought at a time.
- If the candidate says bye, exit, quit, done, or end — gracefully conclude.

## Data Privacy
Inform the candidate at the start that data is collected solely for recruitment and handled per GDPR standards.
"""
GROQ_MODEL = "llama-3.1-8b-instant"
# ─────────────────────────────────────────────
# Session state init
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = {}
if "conversation_ended" not in st.session_state:
    st.session_state.conversation_ended = False
if "greeted" not in st.session_state:
    st.session_state.greeted = False

# Keep sidebar always expanded
st.session_state["sidebar_state"] = "expanded"

# ─────────────────────────────────────────────
# Ollama model
# ─────────────────────────────────────────────
MODEL = "llama3.2"

EXIT_KEYWORDS = {"bye", "goodbye", "exit", "quit", "done", "end", "stop", "farewell"}

def is_exit_message(text: str) -> bool:
    return any(kw in text.lower().split() for kw in EXIT_KEYWORDS)

def build_gemini_history(messages: list) -> list:
    history = []
    for msg in messages:
        if msg["role"] == "user" and msg["content"] == "START_CONVERSATION":
            continue
        role = "model" if msg["role"] == "assistant" else "user"
        history.append({"role": role, "parts": [{"text": msg["content"]}]})
    return history

import re

def extract_candidate_info(messages: list) -> dict:
    info = st.session_state.candidate_info.copy()
    # Only scan assistant messages for confirmed info
    convo = " ".join(m["content"] for m in messages if m["role"] == "assistant")
    user_msgs = [m["content"] for m in messages if m["role"] == "user" and m["content"] != "START_CONVERSATION"]

    for msg in user_msgs:
        # Email
        email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', msg)
        if email:
            info["email"] = email.group()
        # Phone
        phone = re.search(r'[\+\d][\d\s\-\(\)]{7,}', msg)
        if phone:
            info["phone"] = phone.group().strip()
        # Years of experience
        exp = re.search(r'(\d+)\s*(?:years?|yrs?)', msg, re.IGNORECASE)
        if exp:
            info["experience_years"] = exp.group(1)

    # Name: first user message after greeting that looks like a name (2-4 words, no special chars)
    if not info.get("name") or info.get("name") == "null":
        for msg in user_msgs[:4]:
            if re.match(r'^[A-Za-z]{2,}\s[A-Za-z]{2,}[\sA-Za-z]*$', msg.strip()):
                info["name"] = msg.strip()
                break

    # Scrape assistant-confirmed lines for location, position, tech stack
    for msg in user_msgs:
        # Tech stack keywords
        tech_keywords = ["python","javascript","typescript","react","node","django","fastapi",
                        "flask","vue","angular","sql","postgresql","mongodb","redis","docker",
                        "kubernetes","aws","gcp","azure","java","kotlin","swift","go","rust",
                        "c++","c#","php","ruby","rails","spring","nextjs","express"]
        found_tech = [t for t in tech_keywords if t in msg.lower()]
        if len(found_tech) >= 1:
            info["tech_stack"] = msg.strip()

        # Work preference
        if re.search(r'\bfull.?time\b', msg, re.IGNORECASE):
            info["work_preference"] = "Full-time"
        elif re.search(r'\binternship\b', msg, re.IGNORECASE):
            info["work_preference"] = "Internship"

        # Work mode
        if re.search(r'\bremote\b', msg, re.IGNORECASE):
            info["work_mode"] = "Remote"
        elif re.search(r'\bon.?site\b', msg, re.IGNORECASE):
            info["work_mode"] = "On-site"
        elif re.search(r'\bhybrid\b', msg, re.IGNORECASE):
            info["work_mode"] = "Hybrid"

    return info

def chat(user_message: str) -> str:
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
        if m["content"] != "START_CONVERSATION"
    ]
    
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
            max_tokens=1024
        )
        assistant_message = response.choices[0].message.content
    except Exception as e:
        assistant_message = f"Error: {str(e)}"
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    return assistant_message

def get_greeting() -> str:
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "START_CONVERSATION"}
            ],
            max_tokens=1024
        )
        msg = response.choices[0].message.content
    except Exception as e:
        msg = f"Error: {str(e)}"
    
    st.session_state.messages.append({"role": "user", "content": "START_CONVERSATION"})
    st.session_state.messages.append({"role": "assistant", "content": msg})
    return msg

# ─────────────────────────────────────────────
# Header — redesigned
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-wrap">
    <div class="live-chip"><span class="live-dot"></span> AI-Powered Screening</div>
    <h1 class="hero-title">Talent Scout</h1>
    <span class="hero-tagline-big">Your friendly hiring companion ✦</span>
    <span class="hero-tagline-small">Let's find the right fit — one conversation at a time.</span>
    <div class="pills-row">
        <span class="fp fp-peach">-> Smart Screening</span>
        <span class="fp fp-mint">-> Tech Assessment</span>
        <span class="fp fp-sky">-> GDPR Safe</span>
        <span class="fp fp-lav">-> AI-Powered</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Sidebar — rich candidate panel
# ─────────────────────────────────────────────
with st.sidebar:

    # Top banner
    st.markdown("""
    <div class="sb-banner">
        <span class="sb-banner-emoji">🤖</span>
        <span class="sb-banner-title">TalentScout</span>
        <span class="sb-banner-sub">AI Hiring Assistant · Tech Recruitment</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="status-badge">● LIVE SESSION</span>', unsafe_allow_html=True)

    # Interview progress tracker
    info = st.session_state.candidate_info
    has_basics = bool(info.get("name") and info.get("name") != "null")
    has_tech   = bool(info.get("tech_stack") and info.get("tech_stack") != "null")
    is_done    = st.session_state.conversation_ended

    def _dot(done, active):
        if done:   return "done",   "done",   "✓"
        if active: return "active", "active", "→"
        return "todo", "todo", "·"

    s1d, s1l, s1i = _dot(has_basics, not has_basics)
    s2d, s2l, s2i = _dot(has_tech,   has_basics and not has_tech)
    s3d, s3l, s3i = _dot(is_done,    has_tech and not is_done)

    st.markdown(f"""
    <span class="sb-section-label">📍 Interview Progress</span>
    <div class="sb-progress-wrap">
        <div class="sb-step">
            <div class="sb-step-dot {s1d}">{s1i}</div>
            <span class="sb-step-label {s1l}">Personal Info</span>
        </div>
        <div class="sb-step">
            <div class="sb-step-dot {s2d}">{s2i}</div>
            <span class="sb-step-label {s2l}">Tech Stack</span>
        </div>
        <div class="sb-step">
            <div class="sb-step-dot {s3d}">{s3i}</div>
            <span class="sb-step-label {s3l}">Technical Q&A</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Candidate profile cards
    fields = [
        ("👤 Name", "name"),
        ("📧 Email", "email"),
        ("📱 Phone", "phone"),
        ("💼 Experience", "experience_years"),
        ("🎯 Position", "desired_position"),
        ("📍 Location", "location"),
        ("🛠️ Tech Stack", "tech_stack"),
        ("🏢 Work Type", "work_preference"),
        ("🌐 Work Mode", "work_mode"),
    ]
    any_info = False
    for label, key in fields:
        val = info.get(key)
        if val and val != "null":
            any_info = True
            display = f"{val} years" if key == "experience_years" else str(val)
            st.markdown(f"""
            <div class="candidate-info">
                <p>{label}</p>
                <strong>{display}</strong>
            </div>
            """, unsafe_allow_html=True)

    if not any_info:
        st.markdown("""
        <span class="sb-section-label">👤 Candidate Profile</span>
        <div style="background:#F5F3FF;border:2px dashed #BBAEFF;border-radius:14px;padding:14px 12px;text-align:center;">
            <span style="font-size:1.4rem;display:block;margin-bottom:6px;">💬</span>
            <span style="font-family:Nunito,sans-serif;font-size:0.72rem;font-weight:700;color:#9B97B2;">Profile fills in as you chat!</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<span class="sb-section-label">👤 Candidate Profile</span>', unsafe_allow_html=True)

    # Tips card
    st.markdown("""
    <span class="sb-section-label" style="margin-top:14px;">💡 Quick Tips</span>
    <div class="sb-tip">
        <span class="sb-tip-title">✦ How to stand out</span>
        <span class="sb-tip-body">Be specific about your stack · Mention real projects · It's okay to say you're still learning!</span>
    </div>
    """, unsafe_allow_html=True)

    # New session button
    if st.button("🔄 Start New Session", use_container_width=True):
        st.session_state.messages = []
        st.session_state.candidate_info = {}
        st.session_state.conversation_ended = False
        st.session_state.greeted = False
        st.rerun()

    # Privacy note
    st.markdown("""
    <div class="sb-privacy" style="margin-top:8px;">
        <span class="sb-privacy-text">🔒 Your data is handled per GDPR standards and used solely for recruitment.</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Auto-greet on first load
# ─────────────────────────────────────────────
if not st.session_state.greeted:
    with st.spinner("TalentScout is waking up..."):
        greeting = get_greeting()
    st.session_state.greeted = True
    st.rerun()

# ─────────────────────────────────────────────
# Render chat history
# ─────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user" and msg["content"] == "START_CONVERSATION":
        continue
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('<div id="chat-bottom"></div>', unsafe_allow_html=True)
st.markdown("""
<script>
    const el = document.getElementById('chat-bottom');
    if (el) el.scrollIntoView({behavior: 'smooth'});
</script>
""", unsafe_allow_html=True)
# ─────────────────────────────────────────────
# Input
# ─────────────────────────────────────────────
if not st.session_state.conversation_ended:
    with st.form(key="chat_form", clear_on_submit=True, enter_to_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(
                "Your message",
                placeholder="Type your response here...",
                label_visibility="collapsed"
            )
        with col2:
            submitted = st.form_submit_button("Send ➤")

    if submitted and user_input.strip():
        if is_exit_message(user_input):
            st.session_state.conversation_ended = True
            st.rerun()
        else:
            with st.spinner("Thinking..."):
                response = chat(user_input)
            st.session_state.candidate_info = extract_candidate_info(st.session_state.messages)
            conclusion_phrases = ["next steps", "reach out", "review your profile", "thank you for your time", "best of luck"]
            if any(phrase in response.lower() for phrase in conclusion_phrases):
                st.session_state.conversation_ended = True
                st.session_state.candidate_info = extract_candidate_info(st.session_state.messages)
            st.rerun()
else:
    st.markdown("""
    <div class="done-card">
        <p class="done-main">✅ Session complete! The TalentScout team will review your profile shortly.</p>
        <p class="done-sub">Click <strong>New Session</strong> in the sidebar to start over.</p>
    </div>
    """, unsafe_allow_html=True)
    if not st.session_state.candidate_info:
        st.session_state.candidate_info = extract_candidate_info(st.session_state.messages)
        st.rerun()
