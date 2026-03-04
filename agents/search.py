# agents/search.py
import time
from contextlib import redirect_stdout
import os
import sys
from ddgs import DDGS

def search_agent(topic, num_results=3, retries=3, delay=2):
    """
    Perform a DuckDuckGo search using DDGS and return formatted results.
    This version suppresses all stdout and stderr to hide warnings like
    "Impersonate 'firefox_117' does not exist".
    """
    print(f"🔍 Searching for {topic}")
    results = []

    for attempt in range(retries):
        try:
            with open(os.devnull, "w") as fnull:
                old_stderr = sys.stderr
                sys.stderr = fnull  # redirect stderr
                try:
                    with redirect_stdout(fnull):  # redirect stdout
                        with DDGS() as ddgs:
                            for r in ddgs.text(topic, max_results=num_results):
                                results.append(
                                    f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n"
                                )
                finally:
                    sys.stderr = old_stderr  # restore stderr

            print("✅ Search completed")
            return "\n\n".join(results)

        except Exception:
            print(f"⚠️ Retry {attempt+1}/{retries}")
            time.sleep(delay)

    raise Exception("Search failed after multiple retries.")