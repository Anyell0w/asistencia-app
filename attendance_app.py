import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from api_client import APIClient
from database_manager import DatabaseManager
from pdf_generator import PDFGenerator
from Login import Login
import datetime
from datetime import date, timedelta
from tkcalendar import DateEntry


class AttendanceApp:
    def __init__(self, root, db_path, api_token):
        self.root = root
        self.db_manager = DatabaseManager(db_path)
        self.api_client = APIClient(api_token)
        self.excel_data = None
        self.root.title("Registro de Asistencia")

        # Frame para ingresar DNI
        self.frame_dni = tk.Frame(self.root)
        self.frame_dni.pack(pady=10)

        self.lbl_dni = tk.Label(self.frame_dni, text="DNI:")
        self.lbl_dni.pack(side=tk.LEFT, padx=5)
        self.entry_dni = tk.Entry(self.frame_dni)
        self.entry_dni.pack(side=tk.LEFT, padx=5)
        self.btn_registrar = tk.Button(self.frame_dni, text="Registrar", command=self.registrar_asistencia)
        self.btn_registrar.pack(side=tk.LEFT, padx=5)
        self.btn_admin = tk.Button(self.frame_dni, text="Admin", command=self.admin_window)
        self.btn_admin.pack(side=tk.LEFT, padx=5)

    def admin_window(self):
        # Ingresar Credenciales de admin
        self.root_login = tk.Toplevel(self.root)
        self.root_login.title("Login")
        self.login = Login(self.root_login)
        self.login.button.config(command=self.login_admin)

    def login_admin(self):
        username = self.login.entry1.get()
        password = self.login.entry2.get()
        if username == "admin" and password == "admin":
            self.root_login.destroy()
            self.admin_interface()
        else:
            messagebox.showerror("Login", "Usuario o contraseña incorrectos")

    def admin_interface(self):
        self.frame_dni.destroy()
        self.btn_admin.destroy()
        # Frame para la interfaz de administrador
        self.frame_admin = tk.Frame(self.root)
        self.frame_admin.pack(pady=10)

        self.lbl_buscar = tk.Label(self.frame_admin, text="Buscar por:")
        self.lbl_buscar.pack(side=tk.LEFT, padx=5)

        self.option = tk.StringVar(self.frame_admin)
        self.option.set("Fecha")
        self.option_menu = tk.OptionMenu(self.frame_admin, self.option, "Fecha", "DNI", "Nombre")
        self.option_menu.pack(side=tk.LEFT, padx=5)

        self.entry_buscar = tk.Entry(self.frame_admin)
        self.entry_buscar.pack(side=tk.LEFT, padx=5)

        self.btn_buscar = tk.Button(self.frame_admin, text="Buscar", command=self.buscar_registros)
        self.btn_buscar.pack(side=tk.LEFT, padx=5)

        self.btn_ver_dnis = tk.Button(self.frame_admin, text="Ver DNIs Registrados", command=self.ver_dnis_registrados)
        self.btn_ver_dnis.pack(side=tk.LEFT, padx=5)

        self.btn_cargar_excel = tk.Button(self.frame_admin, text="Cargar Archivo Excel", command=self.cargar_excel)
        self.btn_cargar_excel.pack(side=tk.LEFT, padx=5)

        self.btn_generar_pdf = tk.Button(self.frame_admin, text="Generar PDF", command=self.generar_pdf_opciones)
        self.btn_generar_pdf.pack(side=tk.LEFT, padx=5)

        # Frame para mostrar resultados de búsqueda
        self.frame_resultados = tk.Frame(self.root)
        self.frame_resultados.pack(pady=10)

        self.resultados_text = tk.Text(self.frame_resultados, height=10, width=80)
        self.resultados_text.pack()

        # boton para volver al menu principal
        self.btn_volver = tk.Button(self.frame_admin, text="Volver", command=self.volver)
        self.btn_volver.pack(side=tk.RIGHT, padx=5)

    def volver(self):
        # para volver al registro de asistencia
        self.frame_admin.destroy()
        self.frame_resultados.destroy()
        self.__init__(self.root, "attendance.db", "API_TOKEN")

    def cargar_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.excel_data = pd.read_excel(file_path)
            # subir datos a la base de datos
            for index, row in self.excel_data.iterrows():
                dni = row['DNI']
                nombres = row['Nombres']
                apellido_paterno = row['Apellido Paterno']
                apellido_materno = row['Apellido Materno']
                fecha_registro = datetime.datetime.now().strftime('%Y-%m-%d')
                self.db_manager.insert_user(dni, nombres, apellido_paterno, apellido_materno, fecha_registro)
            messagebox.showinfo("Éxito", "Archivo Excel cargado correctamente")

    def registrar_asistencia(self):
        dni = self.entry_dni.get()
        if not dni:
            messagebox.showerror("Error", "Debe ingresar un DNI")
            return

        existing_user = self.db_manager.get_user_by_dni(dni)
        existing_user_by_date = self.db_manager.get_user_by_date(datetime.datetime.now().strftime('%Y-%m-%d'))
        if existing_user_by_date:
            messagebox.showwarning("Advertencia", "Este usuario ya ha sido registrado.")
            return

        user_info = self.api_client.get_user_info(dni)
        if not user_info or user_info.get('success') == False:
            messagebox.showerror("Error", "No se encontró información para el DNI ingresado")
            nuevo_usuario = messagebox.askyesno("Nuevo Usuario", "¿Desea registrar un nuevo usuario?")
            if nuevo_usuario:
                self.nuevo_usuario()
            return

        nombres = user_info['nombres']
        apellido_paterno = user_info['apellidoPaterno']
        apellido_materno = user_info['apellidoMaterno']
        fecha_registro = "2024-07-05"  # Se puede cambiar por la fecha actual

        self.db_manager.insert_user(dni, nombres, apellido_paterno, apellido_materno, fecha_registro)
        messagebox.showinfo("Éxito", "Asistencia registrada correctamente")

    def nuevo_usuario(self):
        self.root_nuevo_usuario = tk.Toplevel(self.root)
        self.root_nuevo_usuario.title("Nuevo Usuario")

        self.lbl_dni_nuevo = tk.Label(self.root_nuevo_usuario, text="DNI:")
        self.lbl_dni_nuevo.pack(side=tk.LEFT, padx=5)
        self.entry_dni_nuevo = tk.Entry(self.root_nuevo_usuario)
        self.entry_dni_nuevo.pack(side=tk.LEFT, padx=5)

        self.lbl_nombres = tk.Label(self.root_nuevo_usuario, text="Nombres:")
        self.lbl_nombres.pack(side=tk.LEFT, padx=5)
        self.entry_nombres = tk.Entry(self.root_nuevo_usuario)
        self.entry_nombres.pack(side=tk.LEFT, padx=5)

        self.lbl_apellido_paterno = tk.Label(self.root_nuevo_usuario, text="Apellido Paterno:")
        self.lbl_apellido_paterno.pack(side=tk.LEFT, padx=5)
        self.entry_apellido_paterno = tk.Entry(self.root_nuevo_usuario)
        self.entry_apellido_paterno.pack(side=tk.LEFT, padx=5)

        self.lbl_apellido_materno = tk.Label(self.root_nuevo_usuario, text="Apellido Materno:")
        self.lbl_apellido_materno.pack(side=tk.LEFT, padx=5)
        self.entry_apellido_materno = tk.Entry(self.root_nuevo_usuario)
        self.entry_apellido_materno.pack(side=tk.LEFT, padx=5)

        fecha = datetime.datetime.now().strftime('%Y-%m-%d')

        self.lbl_fecha_registro = tk.Label(self.root_nuevo_usuario, text=f"Fecha de Registro: {fecha}")
        self.lbl_fecha_registro.pack(side=tk.LEFT, padx=5)

        self.btn_guardar = tk.Button(self.root_nuevo_usuario, text="Guardar", command=self.guardar_usuario)
        self.btn_guardar.pack()

    def guardar_usuario(self):
        dni = self.entry_dni_nuevo.get()
        nombres = self.entry_nombres.get()
        apellido_paterno = self.entry_apellido_paterno.get()
        apellido_materno = self.entry_apellido_materno.get()
        fecha_registro = datetime.datetime.now().strftime('%Y-%m-%d')

        self.db_manager.insert_user(dni, nombres, apellido_paterno, apellido_materno, fecha_registro)
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        self.root_nuevo_usuario.destroy()

    def buscar_registros(self):
        criterio = self.option.get()
        valor = self.entry_buscar.get()

        if criterio == "Fecha":
            resultados = self.db_manager.get_users_by_date(valor)
        elif criterio == "DNI":
            resultados = [self.db_manager.get_user_by_dni(valor)]
            if not resultados[0] and self.excel_data is not None:
                resultados = self.excel_data[self.excel_data['DNI'] == int(valor)].to_dict(orient='records')
        elif criterio == "Nombre":
            resultados = self.db_manager.get_users_by_name(valor)
        else:
            resultados = []

        self.resultados_text.delete(1.0, tk.END)
        for resultado in resultados:
            self.resultados_text.insert(tk.END, f"{resultado}\n")

    def ver_dnis_registrados(self):
        usuarios = self.db_manager.get_all_users()
        self.resultados_text.delete(1.0, tk.END)
        for usuario in usuarios:
            self.resultados_text.insert(tk.END, f"DNI: {usuario[1]}, Nombres: {usuario[2]}, Apellidos: {usuario[3]} {usuario[4]}, Fecha de Registro: {usuario[5]}\n")

    def generar_pdf_opciones(self):
        opciones_window = tk.Toplevel(self.root)
        opciones_window.title("Generar PDF")

        tk.Label(opciones_window, text="Seleccione el rango de fechas:").pack(pady=5)

        self.fecha_inicio = DateEntry(opciones_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.fecha_inicio.pack(pady=5)

        self.fecha_fin = DateEntry(opciones_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.fecha_fin.pack(pady=5)

        self.btn_generar_pdf = tk.Button(opciones_window, text="Generar PDF", command=self.generar_pdf)
        self.btn_generar_pdf.pack(pady=5)

    def generar_pdf(self):
        fecha_inicio = self.fecha_inicio.get_date().strftime('%Y-%m-%d')
        fecha_fin = self.fecha_fin.get_date().strftime('%Y-%m-%d')
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        data = self.db_manager.get_users_by_date_range(fecha_inicio, fecha_fin)
        PDFGenerator.generate(filename, data)
