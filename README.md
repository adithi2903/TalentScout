<<<<<<< HEAD
# 🤖 TalentScout — AI Hiring Assistant

An intelligent conversational chatbot for initial candidate screening, built with Streamlit and Claude (Anthropic). TalentScout conducts structured interviews, collects candidate information, and generates tailored technical questions based on each candidate's declared tech stack.

---

## 📌 Project Overview

TalentScout is a hiring assistant for "TalentScout," a fictional tech recruitment agency. It automates the first round of candidate screening by:

- Greeting candidates and explaining the process
- Collecting key profile details (name, email, phone, experience, position, location, tech stack)
- Generating 3–5 targeted technical questions based on the declared tech stack
- Maintaining conversation context throughout the session
- Gracefully ending conversations on exit keywords
- Displaying a live candidate profile in the sidebar as info is collected

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- An Anthropic API key ([get one here](https://console.anthropic.com/))

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/talentscout-hiring-assistant
cd talentscout-hiring-assistant

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your Anthropic API key
export ANTHROPIC_API_KEY=your_api_key_here   # Mac/Linux
set ANTHROPIC_API_KEY=your_api_key_here      # Windows

# 5. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🧭 Usage Guide

1. **Launch** the app — TalentScout greets you automatically
2. **Respond naturally** to each question in the chat input
3. **Declare your tech stack** — e.g., "Python, FastAPI, PostgreSQL, Docker"
4. **Answer technical questions** — generated specifically for your stack
5. **End the session** by saying "bye", "exit", "done", or "quit"
6. **View your profile** building live in the left sidebar
7. Click **New Session** to restart

---

## 🏗️ Architecture & Technical Details

### Libraries Used
| Library | Purpose |
|---|---|
| `streamlit` | Frontend UI framework |
| `anthropic` | Claude API client (LLM backbone) |
| `json` | Structured info extraction parsing |

### Model
- **Claude Sonnet** (`claude-sonnet-4-20250514`) — used for both conversation and structured info extraction

### Architecture
```
app.py
├── System Prompt          → Defines TalentScout's persona and conversation stages
├── Chat Function          → Sends full conversation history to Claude each turn
├── Info Extractor         → Secondary Claude call to parse candidate profile as JSON
├── Session State          → Streamlit session state manages conversation memory
└── UI Layer               → Custom CSS dark theme, chat bubbles, sidebar profile
```

---

## 🎯 Prompt Design

### Main System Prompt Strategy
The system prompt is structured into **4 explicit stages**:

1. **Greeting** — Sets tone, mentions data privacy
2. **Info Gathering** — Instructs Claude to collect 7 fields one at a time (prevents overwhelming the candidate)
3. **Technical Assessment** — Instructs Claude to generate 3–5 questions tailored to declared tech stack AND years of experience (senior vs junior framing)
4. **Wrap Up** — Standardized conclusion with next-steps messaging

**Key prompt engineering decisions:**
- Explicit stage labeling keeps the model on track across long conversations
- "ONE AT A TIME" instruction prevents the model from dumping all questions at once
- Exit keyword handling is built into the system prompt as a rule
- Fallback behavior ("stay on topic, redirect if off-topic") prevents jailbreaks

### Info Extraction Prompt
A separate, minimal prompt runs every 6 turns to extract structured JSON from the conversation transcript. This is kept deliberately simple and instructs the model to return null for missing fields rather than hallucinating values.

---

## 🔒 Data Privacy

- No candidate data is persisted to disk or any database
- All data exists only in Streamlit session state (in-memory, cleared on refresh)
- Candidates are informed of data usage at the start of each session
- Compliant with GDPR principles: minimal collection, clear purpose, no retention

---

## ⚠️ Challenges & Solutions

| Challenge | Solution |
|---|---|
| Model asking all questions at once | Added "ONE AT A TIME" instruction explicitly in prompt |
| Conversation going off-topic | Added strict "stay on topic" rule with redirect instruction |
| Extracting structured info from freeform chat | Separate extraction prompt returning JSON with null fallbacks |
| Detecting conversation end | Combined exit keyword detection + bot response phrase matching |
| Showing profile as it builds | Periodic extraction every 6 messages + sidebar live update |

---

## ✨ Features

- ✅ Dark themed, custom-styled Streamlit UI
- ✅ Live candidate profile sidebar that populates during conversation
- ✅ Context-aware multi-turn conversation
- ✅ Tech-stack-specific technical questions
- ✅ Exit keyword detection ("bye", "quit", "exit", "done", etc.)
- ✅ Graceful session conclusion with next-steps messaging
- ✅ New Session button to reset and restart
- ✅ GDPR-compliant in-memory only data handling

---

## 📁 File Structure

```
talentscout/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

*Built with ❤️ using Streamlit + Anthropic Claude*
=======
# TalentScout
>>>>>>> 5b95b95c9d17a63ffd4fbd931c2a20c43165cccf
