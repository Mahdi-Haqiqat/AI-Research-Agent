# helpers/log.py
import os
import traceback
from datetime import datetime

def log_agent(topic, language, filetype, status, output, error=None, log_dir="logs"):
    """
    Log agent activity to a file inside logs/ folder.
    """
    os.makedirs(log_dir, exist_ok=True)  # این خط فولدر logs رو میسازه اگر وجود نداشته باشه

    timestamp = datetime.now().strftime("%H:%M:%S")
    date_str = datetime.now().strftime("%Y-%m-%d")

    safe_topic = "".join(c if c.isalnum() or c in " _-" else "_" for c in topic)
    log_file = os.path.join(log_dir, f"{safe_topic}.log")

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