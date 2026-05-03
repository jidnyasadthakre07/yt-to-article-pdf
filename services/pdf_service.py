from fpdf import FPDF

def clean_for_pdf(text):
    replacements = {
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "•": "-",
        "…": "...",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


def create_pdf(text, output_path="output/article.pdf"):
    pdf = FPDF()
    pdf.add_page()

    try:
        # Try Unicode font (BEST)
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", size=12)
    except:
        # Fallback if font missing
        pdf.set_font("Arial", size=12)
        text = clean_for_pdf(text)

    pdf.multi_cell(0, 8, text)
    pdf.output(output_path, dest="F")