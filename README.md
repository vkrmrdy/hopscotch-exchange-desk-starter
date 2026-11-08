# Hopscotch Exchange Desk

Reads a customer's exchange request, checks the facts with tools, and picks **Approve**, **Decline** or **Escalate**.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env          # macOS/Linux: cp .env.example .env
```

Edit `.env` and set `OPENROUTER_API_KEY` to your OpenRouter API key.

## Run

```bash
python main.py                  # all test messages
streamlit run app.py            # UI
```

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub. Do not commit `.env` or any API key.
2. Create an app at [share.streamlit.io](https://share.streamlit.io).
3. Select this repository, its branch, and `app.py` as the main file.
4. In the app settings, open **Secrets** and add:

   ```toml
   OPENROUTER_API_KEY = "your-key"
   ```

   Optionally add `OPENROUTER_BASE_URL`, `APP_URL`, or `APP_NAME` if you need to
   override their defaults. The app reads Streamlit secrets in the cloud and
   `.env` values locally.
