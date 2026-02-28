# 🧠 AI Research CLI Agent

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

---

## 🔑 API Key

Get your API key from:
https://ollama.com/

---

## ▶️ Usage

Run the program:

python main.py  

Then:

1. Enter a topic to research  
2. Choose target language  
3. Choose output format  

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

- PDF generation requires `DejaVuSans.ttf` in the project root directory.
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

This project is licensed under the MIT License. See the LICENSE file for details.
