# helpers/api.py
import os
from dotenv import load_dotenv, set_key
from ollama import Client
import httpx
from helpers.env import ensure_env

def validate_api_key(api_key: str) -> bool:
    """
    Validate the Ollama API key by pinging both models.
    """
    summarizer_model = os.getenv("OLLAMA_GPT_MODEL", "")
    translator_model = os.getenv("OLLAMA_MINIMAX_MODEL", "")

    if not summarizer_model or not translator_model:
        print("\n⚠️ Model configuration missing in .env")
        print("Set OLLAMA_GPT_MODEL and OLLAMA_MINIMAX_MODEL\n")
        return False

    try:
        test_client = Client(
            host="https://ollama.com",
            headers={"Authorization": f"Bearer {api_key}"}
        )

        print("🔎 Verifying API access...")

        test_client.chat(
            model=summarizer_model,
            messages=[{"role": "user", "content": "ping"}]
        )

        test_client.chat(
            model=translator_model,
            messages=[{"role": "user", "content": "ping"}]
        )

        print("✅ API verified successfully.\n")
        return True

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            print("\n❌ Authentication failed. API key invalid or revoked.\n")
        elif e.response.status_code == 404:
            print("\n❌ Model not found. Check model names in .env\n")
        else:
            print("\n❌ Server error. Try again later.\n")
        return False

    except httpx.ConnectError:
        print("\n❌ Cannot connect to Ollama servers. Check internet.\n")
        return False

    except httpx.ReadTimeout:
        print("\n⏳ Server timeout. Try again.\n")
        return False

    except Exception:
        print("\n❌ Unexpected validation error.\n")
        return False


def check_api_key():
    """
    Ensure API key exists and is valid. If not, ask user to input.
    """
    ensure_env()  # Make sure .env exists
    load_dotenv()

    ENV_PATH = ".env"

    while True:
        api_key = os.getenv("OLLAMA_API_KEY")

        if api_key:
            print("🔎 Validating existing API key...")
            if validate_api_key(api_key):
                break
            else:
                print("⚠️ Stored API key invalid.\n")
                set_key(ENV_PATH, "OLLAMA_API_KEY", "")

        print("Enter your Ollama API Key (https://ollama.com/)\n")
        api_key_input = input("OLLAMA_API_KEY: ").strip()

        if not api_key_input:
            print("❌ No API key provided. Exiting.")
            exit()

        set_key(ENV_PATH, "OLLAMA_API_KEY", api_key_input)
        os.environ["OLLAMA_API_KEY"] = api_key_input

        if validate_api_key(api_key_input):
            print("✅ API key saved and verified.\n")
            break
        else:
            print("⚠️ Invalid API key. Try again.\n")
            set_key(ENV_PATH, "OLLAMA_API_KEY", "")