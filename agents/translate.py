# agents/translate.py
import time
import httpx

def translator_agent(client, Translator_MODEL, text, target_language, retries=3, delay=2):
    """
    Translate text to target_language using Ollama API.
    """
    language_display = target_language.capitalize()
    print(f"🌐 Translating to {language_display}")

    if target_language == "english":
        return text

    for attempt in range(retries):
        try:
            response = client.chat(
                model=Translator_MODEL,
                messages=[
                    {"role": "system", "content": f"Translate to fluent {language_display}."},
                    {"role": "user", "content": text}
                ]
            )
            print("✅ Translation completed")
            return response["message"]["content"]

        except httpx.ReadError:
            print(f"⚠️ Retry {attempt+1}/{retries}")
            time.sleep(delay)

    raise Exception("Translation failed.")