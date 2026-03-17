# 🔬 AI Research CLI Agent

[![PyPI](https://img.shields.io/pypi/v/ai-research-agent?logo=pypi&style=for-the-badge)](https://pypi.org/project/ai-research-agent)
[![Python](https://img.shields.io/pypi/pyversions/ai-research-agent?logo=python&style=for-the-badge)](https://pypi.org/project/ai-research-agent)
[![Downloads](https://img.shields.io/pypi/dm/ai-research-agent?logo=pypi&style=for-the-badge)](https://pypi.org/project/ai-research-agent)
[![License](https://img.shields.io/github/license/Mahdi-Haqiqat/AI-Research-Agent?style=for-the-badge)](https://github.com/Mahdi-Haqiqat/AI-Research-Agent/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Mahdi-Haqiqat/AI-Research-Agent?logo=github&style=for-the-badge)](https://github.com/Mahdi-Haqiqat/AI-Research-Agent)

A powerful command-line research assistant built with Ollama Cloud API.  
It searches the web, summarizes results using AI, translates the content, and exports it into multiple file formats.

---

## 🚀 Features

- 🔍 Web search via DuckDuckGo (DDGS)
- 🧩 AI-powered summarization using Ollama Cloud models
- 🌐 Multi-language translation
- 📄 Export to: TXT, MD, DOCX, PDF (RTL supported)
- 🔐 Secure API key validation
- 🗂 Automatic logging system
- 🎯 Interactive CLI menus

---

## 🛠 Tech Stack

Python 3.10+  
ollama  
ddgs  
questionary  
python-dotenv  
httpx  
python-docx  
reportlab  
arabic-reshaper  
python-bidi  

---

## 📦 Installation

Clone the repository:

git clone https://github.com/Mahdi-Haqiqat/AI-Research-Agent.git  
cd AI-Research-Agent

Install dependencies:

pip install -r requirements.txt  

Or install manually:

pip install ollama ddgs questionary python-dotenv httpx python-docx reportlab arabic-reshaper python-bidi  

Note: If you want to install on mobile read [Mobile Installation](https://docs.google.com/document/d/1bDfO-2dRdam6HHqPnYnGtFQyHfOT8r6YC0CY-pFJDJc/edit?usp=sharing)

---

## 🔑 API Key

Get your API key from:
[Ollama](https://ollama.com/)

---

## ▶️ Usage

Run the program:

python main.py  

Then:

1. Enter an API
2. Enter a topic to research  
3. Choose target language  
4. Choose output format  

Or:

Interactive mode (prompts for topic, language, and format)

- Provide topic only:

python main.py ChatGPT

- Provide topic + language:

python main.py ChatGPT --language persian

- Provide topic + language + format:

python main.py ChatGPT --language persian --format docx

- Check version:

python main.py --version

The tool will:

- Search the web  
- Summarize the results  
- Translate (if needed)  
- Generate the output file  
- Log execution details  

---

## 📝 Logging System

All executions are logged inside the `/logs/` directory.

Each topic generates its own log file containing:

- Date & Time  
- Topic  
- Language  
- Output format  
- Execution status  
- Error details (with full traceback if failure occurs)  

---

## 🌍 Supported Languages

English  
Persian  
French  
German  
Arabic  
Spanish  
Italian  
Turkish  

PDF output supports RTL languages (Persian, Arabic, Turkish).

---

## ⚠️ Important Notes

- PDF generation requires [`DejaVuSans.ttf`](https://github.com/Mahdi-Haqiqat/AI-Research-Agent/blob/main/DejaVuSans.ttf) in the project root directory.
- Internet connection is required.
- Ollama Cloud models must be accessible in your account.
- Ensure model names in `.env` are correct.

---

## 🧠 Project Architecture

search_agent() → Web search  
summarize_agent() → AI summarization  
translator_agent() → AI translation  
writer_agent() → File export  
log_agent() → Execution logging  

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Mahdi-Haqiqat/AI-Research-Agent/tree/main?tab=MIT-1-ov-file) file for details.
