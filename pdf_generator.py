from reportlab import pdfgen
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime as date

class PDFGenerator:
    def generate(filename, data):
        width, height = letter
        c = canvas.Canvas(filename, pagesize=letter)
        text = c.beginText(50, height - 50)
        text.setFont("Helvetica", 12)
        
        text.textLine("Reporte de Asistencia")
        text.textLine(f"Generado el: {date.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        text.textLine("")
        
        for row in data:
            text.textLine(f"DNI: {row[1]}, Nombres: {row[2]}, Apellidos: {row[3]} {row[4]}, Fecha de Registro: {row[5]}")

        c.drawText(text)
        c.save()
        
        
        
        
        
        
        
        
        
        
        