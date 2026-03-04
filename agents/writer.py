# agents/writer.py
import os
from bidi.algorithm import get_display
import arabic_reshaper

def writer_agent(text, filename, topic="", language="english", filetype="txt"):
    """
    Write text to a file in the specified format.
    Supported formats: txt, md, docx, pdf
    """
    content = f"{topic}\n\n{text}" if topic else text

    filetype = filetype.lower()

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

        font_path = "DejaVuSans.ttf"
        if not os.path.exists(font_path):
            raise Exception("DejaVuSans.ttf required in working directory.")

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
        raise ValueError(f"Unsupported format: {filetype}")

    print("✅ File written successfully")