from pathlib import Path
from ollama import Client
from dotenv import load_dotenv, set_key
from ddgs import DDGS
import os
import logging
import time
import httpx
from contextlib import redirect_stdout
from datetime import datetime
import traceback
import questionary

logging.getLogger("ddgs").setLevel(logging.ERROR)
logging.getLogger("curl_cffi").setLevel(logging.ERROR)


# -------------------- Ensure .env Exists --------------------
ENV_PATH = ".env"

def ensure_env():
    if not os.path.exists(ENV_PATH):
        print("⚠️ .env not found. Creating with default values...")
        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.write(
                "OLLAMA_API_KEY=\n"
                "OLLAMA_MINIMAX_MODEL=minimax-m2.5:cloud\n"
                "OLLAMA_GPT_MODEL=gpt-oss:20b-cloud\n"
            )


# -------------------- Validate API --------------------
def validate_api_key(api_key: str) -> bool:
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
    ensure_env()          # اطمینان از وجود .env
    load_dotenv()

    while True:
        api_key = os.getenv("OLLAMA_API_KEY")

        if api_key:
            print("🔎 Validating existing API key...")
            if validate_api_key(api_key):
                break
            else:
                print("⚠️ Stored API key invalid.\n")
                # پاک کردن کلید اشتباه از ENV
                set_key(ENV_PATH, "OLLAMA_API_KEY", "")

        # اگر key وجود نداشت یا invalid بود
        print("Enter your Ollama API Key (https://ollama.com/)\n")
        api_key_input = input("OLLAMA_API_KEY: ").strip()

        if not api_key_input:
            print("❌ No API key provided. Exiting.")
            exit()

        # ذخیره در .env و در env فعلی
        set_key(ENV_PATH, "OLLAMA_API_KEY", api_key_input)
        os.environ["OLLAMA_API_KEY"] = api_key_input

        # دوباره validate کنیم
        if validate_api_key(api_key_input):
            print("✅ API key saved and verified.\n")
            break
        else:
            print("⚠️ Invalid API key. Try again.\n")
            # پاک کردن کلید اشتباه و loop ادامه پیدا کنه
            set_key(ENV_PATH, "OLLAMA_API_KEY", "")

# -------------------- Interactive Menus --------------------

def choose_language():
    languages = [
        "English",
        "Persian",
        "French",
        "German",
        "Arabic",
        "Spanish",
        "Italian",
        "Turkish"
    ]

    choice = questionary.select(
        "Choose target language:",
        choices=languages
    ).ask()

    if not choice:
        print("❌ No language selected.")
        exit()

    return choice.lower()


def choose_format():
    formats = ["TXT", "MD", "DOCX", "PDF"]

    choice = questionary.select(
        "Choose output format:",
        choices=formats
    ).ask()

    if not choice:
        print("❌ No format selected.")
        exit()

    return choice.lower()


# -------------------- Logging --------------------

def log_agent(topic, language, filetype, status, output, error=None):
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now().strftime("%H:%M:%S")
    date_str = datetime.now().strftime("%Y-%m-%d")

    safe_topic = "".join(c if c.isalnum() or c in " _-" else "_" for c in topic)
    log_file = os.path.join("logs", f"{safe_topic}.log")

    error_details = ""
    if error:
        error_details = (
            f"\nError Type: {type(error).__name__}"
            f"\nError Message: {error}"
            f"\nTraceback:\n{traceback.format_exc()}"
        )

    content = (
        "\n" + "="*60 +
        f"\nTime: {timestamp}"
        f"\nDate: {date_str}"
        f"\nTopic: {topic}"
        f"\nLanguage: {language}"
        f"\nFormat: {filetype}"
        f"\nStatus: {status}"
        f"\nOutput: {output}"
        f"{error_details}\n"
    )

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(content)


# -------------------- Agents --------------------

def search_agent(topic, num_results=3, retries=3, delay=2):
    print(f"🔍 Searching for {topic}")
    results = []

    for attempt in range(retries):
        try:
            with open(os.devnull, "w") as fnull:
                with redirect_stdout(fnull):
                    with DDGS() as ddgs:
                        for r in ddgs.text(topic, max_results=num_results):
                            results.append(
                                f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n"
                            )
            print("✅ Search completed")
            return "\n\n".join(results)

        except Exception:
            print(f"⚠️ Retry {attempt+1}/{retries}")
            time.sleep(delay)

    raise Exception("Search failed after multiple retries.")


def summarize_agent(text, retries=3, delay=2):
    print("🧩 Summarizing results...")

    for attempt in range(retries):
        try:
            response = client.chat(
                model=Summarizer_MODEL,
                messages=[
                    {"role": "system", "content": "Summarize clearly as continuous prose."},
                    {"role": "user", "content": text}
                ]
            )
            print("✅ Summarization completed")
            return response["message"]["content"]

        except httpx.ReadError:
            print(f"⚠️ Retry {attempt+1}/{retries}")
            time.sleep(delay)

    raise Exception("Summarization failed.")


def translator_agent(text, target_language, retries=3, delay=2):
    language_display = target_language.capitalize()
    print(f"🌐 Translating to {language_display}")
    if target_language == "english":
        return text

    for attempt in range(retries):
        try:
            response = client.chat(
                model=Translator_MODEL,
                messages=[
                    {"role": "system", "content": f"Translate to fluent {target_language.capitalize()}."},
                    {"role": "user", "content": text}
                ]
            )
            print("✅ Translation completed")
            return response["message"]["content"]

        except httpx.ReadError:
            print(f"⚠️ Retry {attempt+1}/{retries}")
            time.sleep(delay)

    raise Exception("Translation failed.")


def writer_agent(text, filename, topic, language, filetype):
    filename = str(filename)
    content = f"{topic}\n\n{text}"

    if filetype in ("txt", "md"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    elif filetype == "docx":
        from docx import Document
        doc = Document()
        doc.add_paragraph(content)
        doc.save(filename)

    elif filetype == "pdf":
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfbase import pdfmetrics
        from bidi.algorithm import get_display
        import arabic_reshaper

        font_path = "DejaVuSans.ttf"
        if not os.path.exists(font_path):
            raise Exception("DejaVuSans.ttf required.")

        pdfmetrics.registerFont(TTFont("DejaVu", font_path))

        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []

        style = ParagraphStyle(
            "Custom",
            parent=getSampleStyleSheet()["Normal"],
            fontName="DejaVu",
            fontSize=12
        )

        lines = content.split("\n")

        for line in lines:
            if language in ("persian", "arabic", "turkish"):
                line = get_display(arabic_reshaper.reshape(line))
            elements.append(Paragraph(line, style))
            elements.append(Spacer(1, 8))

        doc.build(elements)

    else:
        raise ValueError("Unsupported format.")

    print("✅ File written successfully")


# -------------------- Main --------------------

def main():
    check_api_key()
    load_dotenv()

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

    try:
        search_results = search_agent(topic)
        summary = summarize_agent(search_results)
        translated = translator_agent(summary, target_language)

        RESEARCH_DIR = Path("/storage/emulated/0/Download/research")
        RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
        filename = RESEARCH_DIR / f"{topic} {language_display}.{output_format}"
        writer_agent(translated, filename, topic, target_language, output_format)

        log_agent(topic, language_display, output_format, "Success", filename)
        print(f"\n🎉 Done! Saved as {filename}")

    except Exception as e:
        log_agent(topic, language_display, output_format, "Failed", "", e)
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()