import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def _settings() -> dict:
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")

    try:
        secrets = st.secrets
    except FileNotFoundError:
        secrets = {}

    def setting(name: str, default: str | None = None) -> str | None:
        return os.getenv(name) or secrets.get(name, default)

    return {
        "api_key": setting("OPENROUTER_API_KEY"),
        "base_url": setting("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        "app_url": setting("APP_URL", "http://localhost"),
        "app_name": setting("APP_NAME", "hopscotch-exchange-desk"),
    }


def create_llm() -> ChatOpenAI:
    settings = _settings()
    if not settings["api_key"]:
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Set it in the project-root .env file "
            "for local use or in Streamlit Cloud app secrets."
        )

    return ChatOpenAI(
        api_key=settings["api_key"],
        base_url=settings["base_url"],
        model="openai/gpt-4o-mini-2024-07-18",
        default_headers={
            "HTTP-Referer": settings["app_url"],
            "X-Title": settings["app_name"],
        },
    )


RETURN_WINDOW_DAYS = 10
HIGH_VALUE = 5000  # INR
VENDOR_SPIKE = 15  # %
MAX_TRIPS = 4

PINCODE_API = "https://api.postalpincode.in/pincode/"
