from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime

def generar_pdf(data, filename, fecha_inicio=None, fecha_fin=None):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    text = c.beginText(50, height - 50)
    text.setFont("Helvetica", 12)

    text.textLine("Reporte de Asistencia")
    text.textLine(f"Generado el: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    text.textLine("")

    if fecha_inicio and fecha_fin:
        text.textLine(f"Intervalo de fechas: {fecha_inicio.strftime('%Y-%m-%d')} - {fecha_fin.strftime('%Y-%m-%d')}")
        text.textLine("")

    for row in data:
        text.textLine(f"DNI: {row[1]}, Nombres: {row[2]}, Apellidos: {row[3]} {row[4]}, Fecha de Registro: {row[5]}")

    c.drawText(text)
    c.showPage()
    c.save()
