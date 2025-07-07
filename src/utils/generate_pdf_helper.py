from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf_from_text(text: str) -> BytesIO:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    lines = text.split("\n")
    y = height - 40 

    for line in lines:
        if y < 40:
            pdf.showPage()
            y = height - 40
        pdf.drawString(40, y, line[:110]) 
        y -= 20

    pdf.save()
    buffer.seek(0)
    return buffer
