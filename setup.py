from setuptools import setup, find_packages

setup(
    name="ai-research-agent",
    version="1.0.9",
    summary="Automate & accelerate AI research with Python! Focus on experiments, not setup, with smart topic planning, multi-source retrieval, and automated report generation.",
    author="Mahdi Haqiqat",
    author_email="mahdihaqiqat55@gmail.com",
    maintainer="Mahdi Haqiqat",
    maintainer_email="mahdihaqiqat@outlook.com",
    url="https://pypi.org/project/ai-research-agent/",
    license="MIT",
    
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "ai_research_agent": ["DejaVuSans.ttf", ".env"],
    },
    data_files=[("", ["LICENSE"])],  # تضمین اضافه شدن LICENSE به build
    
    install_requires=[
        "ollama",
        "python-dotenv",
        "ddgs",
        "httpx",
        "questionary",
        "python-docx",
        "reportlab",
        "arabic-reshaper",
        "python-bidi",
        "pathlib",
        "argparse",
    ],
    
    entry_points={
        "console_scripts": [
            "ai-research=ai_research_agent.main:main",
        ],
    },
    
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],

    # ------------------ PyPI long description ------------------
    long_description="""
🔬 **AI-Research-Agent** — A powerful Python toolkit to automate and accelerate AI research workflows. 
Focus on experiments and insights, not repetitive setup, with seamless API integration and smart environment management.

✨ **Key Features:**
- 🧠 Intelligent research planning and topic breakdown
- 🌐 Multi-source retrieval including web and APIs
- 🧾 Automated synthesis of findings into concise reports
- 🔗 API integrations for real-time data
- 📁 Export results in Markdown, text, or structured formats
- 🧩 Modular and extensible design for custom workflows

Perfect for AI developers, data scientists, researchers, and enthusiasts who want:
✔ Repeatable, automated research processes  
✔ High-quality, structured research briefs  
✔ Easy integration with large language models (LLMs) and AI tools  

🚀 **Install**: `pip install AI-Research-Agent`  
📚 **Docs & examples**: [GitHub Repository](https://github.com/Mahdi-Haqiat/AI-Research-Agent)
""",
    long_description_content_type="text/markdown",
)