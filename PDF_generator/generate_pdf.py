from fpdf import FPDF
import os
import re
from datetime import datetime

def sanitize_text(text):
    if not text:
        return ""
    
    # Replace common problematic Unicode characters
    replacements = {
        "’": "'",     # curly to straight apostrophe
        "‘": "'",     # left single quote
        "“": '"',     # left double quote
        "”": '"',     # right double quote
        "–": "-",     # en-dash
        "—": "-",     # em-dash
        "≤": "<=",    # less than or equal
        "≥": ">=",    # greater than or equal
        "•": "-",     # bullet point
        "→": "->",    # arrow
        "←": "<-",    # left arrow
        "\u00a0": " " # non-breaking space
    }

    for orig, repl in replacements.items():
        text = text.replace(orig, repl)

    # Remove emojis and any other unsupported characters
    emoji_pattern = re.compile(
        "[" u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub("", text)

    return text.encode("latin-1", "ignore").decode("latin-1")  # Strip any remaining unsupported chars

def generate_pdf(row):
    try:
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Blood Test Report Summary", ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.ln(10)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Report Details", ln=True)
        pdf.set_font("Arial", "", 11)

        pdf.multi_cell(0, 8, f"Filename: {sanitize_text(row.get('filename'))}")
        pdf.multi_cell(0, 8, f"Query: {sanitize_text(row.get('query'))}")
        pdf.ln(5)

        sections = [
            ("Medical Result", row.get("medical_result")),
            ("Nutrition Result", row.get("nutrition_result")),
            ("Exercise Result", row.get("exercise_result")),
            ("Verification Result", row.get("verification_result")),
        ]

        for title, content in sections:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, sanitize_text(title), ln=True)

            pdf.set_font("Arial", "", 11)
            clean_content = sanitize_text(content)
            if clean_content.strip():
                pdf.multi_cell(0, 8, clean_content)
            else:
                pdf.multi_cell(0, 8, "No result found.")

            pdf.ln(3)

        output_dir = "output/pdf_reports"
        os.makedirs(output_dir, exist_ok=True)

        filename_safe = sanitize_text(row.get("filename", "report")).replace(" ", "_").replace(".", "_")
        output_path = os.path.join(output_dir, f"{filename_safe}.pdf")

        pdf.output(output_path)
        return output_path

    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        return None
