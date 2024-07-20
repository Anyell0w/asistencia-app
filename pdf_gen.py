from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from api_client import APIClient
import datetime


class PDFGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.c = canvas.Canvas(self.filename, pagesize=letter)
        self.width, self.height = letter


    def generar_pdf_del_dia(self, dia, data):
        # generar una matriz con los datos de cada usuario, marcando check en el día en el que
        # se registró la asistencia
        # generar el pdf con la matriz
        # el pdf debe tener un título con la fecha del día

        self.c.drawString(1 * inch, 10.5 * inch, "Asistencia del día {}".format(dia))
        self.c.drawString(1 * inch, 10 * inch, "ID")
        self.c.drawString(2 * inch, 10 * inch, "DNI")
        self.c.drawString(3 * inch, 10 * inch, "Nombre")
        self.c.drawString(4 * inch, 10 * inch, "Asistió")
        y = 9.5 * inch


        
        # verificar segun la fecha si asisitión o no, si no hay fecha, no asistió

        
        
        for usuario in data:
            usuario_id, dni, nombres, apellido_paterno, apellido_materno, asistio = usuario
            asistencia = "✓"
            self.c.drawString(1 * inch, y, str(usuario_id))
            self.c.drawString(2 * inch, y, str(dni))
            self.c.drawString(3 * inch, y, nombres)
            self.c.drawString(4 * inch, y, asistencia)
            y -= 0.5 * inch

        self.c.save()


    def generar_pdf_del_mes(self, mes):
        pass


    def generar_pdf_personalizado(self, fecha_inicio, fecha_fin):
        pass
