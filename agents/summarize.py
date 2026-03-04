# agents/summarize.py
import time
import httpx

def summarize_agent(client, Summarizer_MODEL, text, retries=3, delay=2):
    """
    Summarize text using Ollama API client.
    Args:
        client: Ollama Client instance
        Summarizer_MODEL: model name for summarization
        text: text to summarize
        retries: number of retries
        delay: delay between retries
    Returns:
        Summarized text
    """
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