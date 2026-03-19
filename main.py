import os
import logging
import argparse
from ollama import Client
from datetime import datetime

from agents.search import search_agent
from agents.summarize import summarize_agent
from agents.translate import translator_agent
from agents.writer import writer_agent

from helpers.log import log_agent
from helpers.api import validate_api_key, check_api_key
from helpers.env import ensure_env
from helpers.output_settings import choose_language, choose_format

__version__ = "1.0.1"

logging.getLogger("ddgs").setLevel(logging.ERROR)
logging.getLogger("curl_cffi").setLevel(logging.ERROR)

CONFIG_FILE = "config_output_path.txt"  # مسیر ذخیره مسیر خروجی


def save_output_path(path):
    """Save output path to file"""
    with open(CONFIG_FILE, "w") as f:
        f.write(path)
    print(f"✅ New Output Saved: {path}")


def load_output_path(default_path):
    """Load saved output path if exists"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            saved_path = f.read().strip()
            if saved_path:
                return saved_path
    return default_path


# -------------------- Main --------------------
def main():

    parser = argparse.ArgumentParser(description="AI Research Agent")

    parser.add_argument(
        "topic",
        nargs="*",
        help="Topic to research"
    )

    parser.add_argument(
        "-l",
        "--language",
        help="Output language"
    )

    parser.add_argument(
        "-f",
        "--format",
        help="Output format"
    )

    # -------- Change output path ----------
    parser.add_argument(
        "-c",
        "--change",
        help="Change output directory",
        metavar="OUTPUT_PATH"
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"AI-Research-Agent {__version__}"
    )

    args = parser.parse_args()

    # --------- اگر change زده شد، فقط مسیر ذخیره شود و برنامه ادامه نده ---------
    if args.change:
        output_dir = args.change
        os.makedirs(output_dir, exist_ok=True)
        save_output_path(output_dir)
        return  # برنامه اصلی اجرا نمیشه

    ensure_env()
    check_api_key()

    global Summarizer_MODEL, Translator_MODEL, client

    Summarizer_MODEL = os.getenv("OLLAMA_GPT_MODEL", "")
    Translator_MODEL = os.getenv("OLLAMA_MINIMAX_MODEL", "")

    client = Client(
        host="https://ollama.com",
        headers={"Authorization": f"Bearer {os.getenv('OLLAMA_API_KEY')}"}
    )

    # -------- topic --------
    if args.topic:
        topic = " ".join(args.topic)
    else:
        topic = input("Enter a topic to research: ").strip()

    # -------- language --------
    target_language = args.language or choose_language()
    language_display = target_language.capitalize()

    # -------- format --------
    output_format = args.format or choose_format()

    # -------- output path --------
    if "com.termux" in os.environ.get("PREFIX", ""):
        default_output_dir = "/storage/emulated/0/Download/Research"
    else:
        default_output_dir = os.path.join("Research")

    # load previous saved path
    output_dir = load_output_path(default_output_dir)
    os.makedirs(output_dir, exist_ok=True)

    try:

        search_results = search_agent(topic)

        summary = summarize_agent(client, Summarizer_MODEL, search_results)

        translated = translator_agent(client, Translator_MODEL, summary, target_language)

        filename = os.path.join(output_dir, f"{topic} {language_display}.{output_format}")

        writer_agent(translated, filename, topic, target_language, output_format)

        log_agent(topic, language_display, output_format, "Success", filename)

        print(f"\n🎉 Done! Saved as {filename}")

    except Exception as e:

        log_agent(topic, language_display, output_format, "Failed", "", e)

        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()