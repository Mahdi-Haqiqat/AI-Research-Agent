# helpers/output_settings.py
import questionary

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