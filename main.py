import os
import logging
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

logging.getLogger("ddgs").setLevel(logging.ERROR)
logging.getLogger("curl_cffi").setLevel(logging.ERROR)

# -------------------- Main --------------------
def main():
    ensure_env()       
    check_api_key()

    global Summarizer_MODEL, Translator_MODEL, client

    Summarizer_MODEL = os.getenv("OLLAMA_GPT_MODEL", "")
    Translator_MODEL = os.getenv("OLLAMA_MINIMAX_MODEL", "")

    client = Client(
        host="https://ollama.com",
        headers={"Authorization": f"Bearer {os.getenv('OLLAMA_API_KEY')}"}
    )

    topic = input("Enter a topic to research: ").strip()

    target_language = choose_language()
    language_display = target_language.capitalize()

    output_format = choose_format()
    
    output_dir = os.path.join("Research")
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