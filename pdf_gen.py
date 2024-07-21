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

        hoy = datetime.datetime.now().strftime("%Y-%m-%d")


        for usuario in data:
            usuario_id, dni, nombres, apellido_paterno, apellido_materno, fecha_registro, asistio = usuario
            if fecha_registro == hoy:
                asistencia = "Si"
            else:
                asistencia = "No"
            self.c.drawString(1 * inch, y, str(usuario_id))
            self.c.drawString(2 * inch, y, str(dni))
            self.c.drawString(3 * inch, y, nombres)
            self.c.drawString(4 * inch, y, asistencia)
            y -= 0.5 * inch

        self.c.save()

    
    def generar_pdf_personalizado(self, fecha_inicio, fecha_fin, data):
        self.c.drawString(1 * inch, 10.5 * inch, "Asistencia del {} al {}".format(fecha_inicio, fecha_fin))
        
        # Convertir fechas a objetos datetime.date si no lo son
        if isinstance(fecha_inicio, str):
            fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        if isinstance(fecha_fin, str):
            fecha_fin = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        
        # Generar la lista de fechas en el rango especificado
        delta = fecha_fin - fecha_inicio
        fechas = [fecha_inicio + datetime.timedelta(days=i) for i in range(delta.days + 1)]
        
        # Dibujar encabezados de columnas
        self.c.drawString(1 * inch, 10 * inch, "ID")
        self.c.drawString(2 * inch, 10 * inch, "DNI")
        self.c.drawString(3 * inch, 10 * inch, "Nombre")
        
        x = 4 * inch
        for fecha in fechas:
            self.c.drawString(x, 10 * inch, fecha.strftime("%Y-%m-%d"))
            x += 1.5 * inch  # Ajustar según el ancho deseado de cada columna
        
        y = 9.5 * inch
        
        # Dibujar datos de asistencia
        for usuario in data:
            usuario_id, dni, nombres, apellido_paterno, apellido_materno, fecha_registro, asistio = usuario
            
            self.c.drawString(1 * inch, y, str(dni))
            self.c.drawString(2 * inch, y, nombres)
            
            x = 4 * inch
            for fecha in fechas:
                fecha_str = fecha.strftime("%Y-%m-%d")
                asistencia = "No"
                if fecha_str == fecha_registro:
                    asistencia = "Si"
                self.c.drawString(x, y, asistencia)
                x += 1.5 * inch
            
            y -= 0.5 * inch

        self.c.save()