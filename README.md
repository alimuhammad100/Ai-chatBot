# 🤖 Ali AI — Chatbot

A conversational AI assistant built with **Streamlit**, **LangChain**, and **Groq** (`openai/gpt-oss-120b`), with a custom dark UI.

## Live Demo

_Add your deployed Streamlit Cloud link here once deployed._

## Features

- Real-time chat with conversation history
- Fast inference via Groq
- Custom dark theme with distinct typography and accent colors
- "New conversation" reset

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI
- [LangChain](https://www.langchain.com/) — LLM orchestration
- [Groq](https://groq.com/) — LLM inference (`openai/gpt-oss-120b`)

## Project Structure

```
ali-ai-chatbot/
├── app.py                  # Streamlit application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Dark theme config
├── .env.example             # Example env file (local dev only)
├── .gitignore
└── README.md
```

---

## 1. Push this project to GitHub

```bash
cd ali-ai-chatbot
git init
git add .
git commit -m "Initial commit: Ali AI chatbot"
git branch -M main
git remote add origin https://github.com/<your-username>/ali-ai-chatbot.git
git push -u origin main
```

> `.env` is excluded via `.gitignore` — never commit your real API key.

## 2. Run locally

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then edit .env and add your real key
streamlit run app.py
```

Get a free Groq API key at [console.groq.com](https://console.groq.com/).

## 3. Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
2. Click **"New app"** and select this repository, branch `main`, and file path `app.py`.
3. Click **"Advanced settings"** and add your secret in the **Secrets** box (TOML format):
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
4. Click **"Deploy"**.

Streamlit Cloud exposes root-level secrets as environment variables automatically, so `os.getenv("GROQ_API_KEY")` in `app.py` picks it up with no code changes needed.

## Author

Built by **Ali**.
