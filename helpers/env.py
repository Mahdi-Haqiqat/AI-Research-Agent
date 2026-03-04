# env.py
import os

ENV_PATH = ".env"

def ensure_env():
    """
    Make sure .env exists with default keys.
    """
    if not os.path.exists(ENV_PATH):
        print("⚠️ .env not found. Creating with default values...")
        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.write(
                "OLLAMA_API_KEY=\n"
                "OLLAMA_MINIMAX_MODEL=minimax-m2.5:cloud\n"
                "OLLAMA_GPT_MODEL=gpt-oss:20b-cloud\n"
            )