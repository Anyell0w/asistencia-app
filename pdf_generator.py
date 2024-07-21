from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import datetime

class PDFGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.c = canvas.Canvas(self.filename, pagesize=letter)
        self.width, self.height = letter

    def generar_pdf_del_dia(self, dia, data):
        self.c.drawString(1 * inch, 10.5 * inch, "Asistencia del día {}".format(dia))
        self.c.drawString(1 * inch, 10 * inch, "ID")
        self.c.drawString(2 * inch, 10 * inch, "DNI")
        self.c.drawString(3 * inch, 10 * inch, "Nombre")
        self.c.drawString(4 * inch, 10 * inch, "Asistió")
        y = 9.5 * inch

        for usuario in data:
            usuario_id, dni, nombres, apellido_paterno, apellido_materno, fecha_registro = usuario
            if fecha_registro == dia:
                asistencia = "Si"
            else:
                asistencia = "No"
            self.c.drawString(1 * inch, y, str(usuario_id))
            self.c.drawString(2 * inch, y, str(dni))
            self.c.drawString(3 * inch, y, nombres)
            self.c.drawString(4 * inch, y, asistencia)
            y -= 0.5 * inch

        self.c.save()

    def generar_pdf_de_la_semana(self, fecha_inicio, fecha_fin, data):
        self.c.drawString(1 * inch, 10.5 * inch, "Asistencia de la semana {} a {}".format(fecha_inicio, fecha_fin))
        self.c.drawString(1 * inch, 10 * inch, "ID")
        self.c.drawString(2 * inch, 10 * inch, "DNI")
        self.c.drawString(3 * inch, 10 * inch, "Nombre")
        self.c.drawString(4 * inch, 10 * inch, "Fechas de Asistencia")
        y = 9.5 * inch

        for usuario in data:
            usuario_id, dni, nombres, apellido_paterno, apellido_materno, fechas_asistencia = usuario
            fechas_asistencia = fechas_asistencia.split(",")
            asistencia = ", ".join([fecha for fecha in fechas_asistencia if fecha_inicio <= fecha <= fecha_fin])
            self.c.drawString(1 * inch, y, str(usuario_id))
            self.c.drawString(2 * inch, y, str(dni))
            self.c.drawString(3 * inch, y, nombres)
            self.c.drawString(4 * inch, y, asistencia)
            y -= 0.5 * inch

        self.c.save()

    def generar_pdf_del_mes(self, mes, data):
        self.c.drawString(1 * inch, 10.5 * inch, "Asistencia del mes {}".format(mes))
        self.c.drawString(1 * inch, 10 * inch, "ID")
        self.c.drawString(2 * inch, 10 * inch, "DNI")
        self.c.drawString(3 * inch, 10 * inch, "Nombre")
        self.c.drawString(4 * inch, 10 * inch, "Fechas de Asistencia")
        y = 9.5 * inch

        for usuario in data:
            usuario_id, dni, nombres, apellido_paterno, apellido_materno, fechas_asistencia = usuario
            fechas_asistencia = fechas_asistencia.split(",")
            asistencia = ", ".join([fecha for fecha in fechas_asistencia if fecha.startswith(mes)])
            self.c.drawString(1 * inch, y, str(usuario_id))
            self.c.drawString(2 * inch, y, str(dni))
            self.c.drawString(3 * inch, y, nombres)
            self.c.drawString(4 * inch, y, asistencia)
            y -= 0.5 * inch

        self.c.save()

    def generar_pdf_personalizado(self, fecha_inicio, fecha_fin, data):
        self.c.drawString(1 * inch, 10.5 * inch, "Asistencia desde {} hasta {}".format(fecha_inicio, fecha_fin))
        self.c.drawString(1 * inch, 10 * inch, "ID")
        self.c.drawString(2 * inch, 10 * inch, "DNI")
        self.c.drawString(3 * inch, 10 * inch, "Nombre")
        self.c.drawString(4 * inch, 10 * inch, "Fechas de Asistencia")
        y = 9.5 * inch

        for usuario in data:
            usuario_id, dni, nombres, apellido_paterno, apellido_materno, fechas_asistencia = usuario
            fechas_asistencia = fechas_asistencia.split(",")
            asistencia = ", ".join([fecha for fecha in fechas_asistencia if fecha_inicio <= fecha <= fecha_fin])
            self.c.drawString(1 * inch, y, str(usuario_id))
            self.c.drawString(2 * inch, y, str(dni))
            self.c.drawString(3 * inch, y, nombres)
            self.c.drawString(4 * inch, y, asistencia)
            y -= 0.5 * inch

        self.c.save()
