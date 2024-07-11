import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Style
import tkinter as tk
import tkinter.messagebox as messagebox
import requests
import sqlite3
import os
import datetime


class APIClient:
    def __init__(self, token):
        self.base_url = 'https://dniruc.apisperu.com/api/v1/dni/'
        self.token = token

    def get_user_info(self, dni):
        url = self.base_url + dni + '?token=' + self.token
        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get('success'):
                return response_json
            else:
                print(f"Error en la respuesta de la API: {response_json}")
                return None
        else:
            print(f"Error en la solicitud HTTP: {response.status_code}")
            return None


class DatabaseManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni TEXT NOT NULL,
            nombres TEXT NOT NULL,
            apellido_paterno TEXT NOT NULL,
            apellido_materno TEXT NOT NULL,
            fecha_registro TEXT NOT NULL
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def insert_user(self, dni, nombres, apellido_paterno, apellido_materno, fecha_registro):
        query = """
        INSERT INTO usuario (dni, nombres, apellido_paterno, apellido_materno, fecha_registro)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (dni, nombres, apellido_paterno, apellido_materno, fecha_registro))
        self.conn.commit()

    def update_user(self, user_id, dni, nombres, apellido_paterno, apellido_materno, fecha_registro):
        query = """
        UPDATE usuario
        SET dni = ?, nombres = ?, apellido_paterno = ?, apellido_materno = ?, fecha_registro = ?
        WHERE id = ?
        """
        self.cursor.execute(query, (dni, nombres, apellido_paterno, apellido_materno, fecha_registro, user_id))
        self.conn.commit()

    def delete_user(self, user_id):
        query = "DELETE FROM usuario WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()

    def get_user_by_dni(self, dni):
        query = "SELECT * FROM usuario WHERE dni = ?"
        self.cursor.execute(query, (dni,))
        return self.cursor.fetchone()

    def get_all_users(self):
        query = "SELECT * FROM usuario"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_users_by_date(self, date):
        query = "SELECT * FROM usuario WHERE fecha_registro = ?"
        self.cursor.execute(query, (date,))
        return self.cursor.fetchall()

    def get_users_by_name(self, name):
        query = "SELECT * FROM usuario WHERE nombres LIKE ?"
        self.cursor.execute(query, ('%' + name + '%',))
        return self.cursor.fetchall()


class AttendanceApp:
    def __init__(self, root, db_path, api_token):
        self.root = root
        self.root.title("Registro de Asistencia")
        self.style = Style(theme='morph')
        self.db_manager = DatabaseManager(db_path)
        self.api_client = APIClient(api_token)

        self.create_main_window()

    def create_main_window(self):
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(pady=10)

        self.label_dni = ttk.Label(self.main_frame, text="DNI:")
        self.label_dni.pack(side=LEFT, padx=(0, 10))

        self.entry_dni = ttk.Entry(self.main_frame)
        self.entry_dni.pack(side=LEFT, padx=(0, 10))

        self.btn_registrar = ttk.Button(self.main_frame, text="Registrar", command=self.registrar_asistencia, bootstyle=PRIMARY)
        self.btn_registrar.pack(side=LEFT, padx=(0, 10))

        self.btn_administrar = ttk.Button(self.root, text="Administrar Registros", command=self.open_admin_window, bootstyle=SUCCESS)
        self.btn_administrar.pack(pady=20)

    def registrar_asistencia(self):
        dni = self.entry_dni.get()
        user_info = self.api_client.get_user_info(dni)

        if user_info:
            nombres = user_info['nombres']
            apellido_paterno = user_info['apellidoPaterno']
            apellido_materno = user_info['apellidoMaterno']
            fecha_registro = datetime.datetime.now().strftime('%Y-%m-%d')

            self.db_manager.insert_user(dni, nombres, apellido_paterno, apellido_materno, fecha_registro)
            messagebox.showinfo("Éxito", "Asistencia registrada correctamente")
        else:
            messagebox.showerror("Error", "No se pudo registrar la asistencia")
            nuevo_usuario = messagebox.askyesno("Nuevo Usuario", "¿Desea registrar un nuevo usuario?")
            if nuevo_usuario:
                self.registrar_usuario()

    def registrar_usuario(self):
        self.registro_window = ttk.Toplevel(self.root)
        self.registro_window.title("Registrar Nuevo Usuario")
        self.registro_window.geometry("1500x100")
        self.create_registro_widgets()

    def create_registro_widgets(self):
        self.frame_registro = ttk.Frame(self.registro_window, padding=10)
        self.frame_registro.pack(pady=10)

        self.label_dni = ttk.Label(self.frame_registro, text="DNI:")
        self.label_dni.pack(side=LEFT, padx=(0, 10))
        self.entry_dni = ttk.Entry(self.frame_registro)
        self.entry_dni.pack(side=LEFT, padx=(0, 10))

        self.label_nombres = ttk.Label(self.frame_registro, text="Nombres:")
        self.label_nombres.pack(side=LEFT, padx=(0, 10))
        self.entry_nombres = ttk.Entry(self.frame_registro)
        self.entry_nombres.pack(side=LEFT, padx=(0, 10))

        self.label_apellido_paterno = ttk.Label(self.frame_registro, text="Apellido Paterno:")
        self.label_apellido_paterno.pack(side=LEFT, padx=(0, 10))
        self.entry_apellido_paterno = ttk.Entry(self.frame_registro)
        self.entry_apellido_paterno.pack(side=LEFT, padx=(0, 10))

        self.label_apellido_materno = ttk.Label(self.frame_registro, text="Apellido Materno:")
        self.label_apellido_materno.pack(side=LEFT, padx=(0, 10))
        self.entry_apellido_materno = ttk.Entry(self.frame_registro)
        self.entry_apellido_materno.pack(side=LEFT, padx=(0, 10))

        self.btn_guardar = ttk.Button(self.frame_registro, text="Guardar", command=self.guardar_usuario, bootstyle=SECONDARY)
        self.btn_guardar.pack(side=LEFT, padx=(0, 10))

    def guardar_usuario(self):
        dni = self.entry_dni.get()
        nombres = self.entry_nombres.get()
        apellido_paterno = self.entry_apellido_paterno.get()
        apellido_materno = self.entry_apellido_materno.get()
        fecha_registro = datetime.datetime.now().strftime('%Y-%m-%d')
        self.db_manager.insert_user(dni, nombres, apellido_paterno, apellido_materno, fecha_registro)
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        self.registro_window.destroy()

    def open_admin_window(self):
        self.admin_window = ttk.Toplevel(self.root)
        self.admin_window.title("Administrar Registros")
        self.admin_window.geometry("600x600")

        self.create_admin_widgets()

    def create_admin_widgets(self):
        self.frame_buscar = ttk.Frame(self.admin_window, padding=10)
        self.frame_buscar.pack(pady=10)

        self.label_buscar = ttk.Label(self.frame_buscar, text="Buscar por:")
        self.label_buscar.pack(side=LEFT, padx=5)

        self.option = ttk.StringVar(value="DNI")
        self.option_menu = ttk.OptionMenu(self.frame_buscar, self.option, "DNI", "Fecha", "Nombre")
        self.option_menu.pack(side=LEFT, padx=5)

        self.entry_buscar = ttk.Entry(self.frame_buscar)
        self.entry_buscar.pack(side=LEFT, padx=5)

        self.btn_buscar = ttk.Button(self.frame_buscar, text="Buscar", command=self.buscar_registros, bootstyle=PRIMARY)
        self.btn_buscar.pack(side=LEFT, padx=5)

        self.frame_resultados = ttk.Frame(self.admin_window, padding=10)
        self.frame_resultados.pack(pady=10)

        self.resultados_text = tk.Text(self.frame_resultados, width=80, height=20)
        self.resultados_text.pack(side=LEFT)

        self.scrollbar = ttk.Scrollbar(self.frame_resultados, command=self.resultados_text.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.resultados_text.config(yscrollcommand=self.scrollbar.set)

        # mostrar todos los dnis registrados
        self.btn_ver_dnis = ttk.Button(self.admin_window, text="Ver DNIs Registrados", command=self.ver_dnis_registrados, bootstyle=SECONDARY)
        self.btn_ver_dnis.pack(pady=10)

    def ver_dnis_registrados(self):
        usuarios = self.db_manager.get_all_users()
        self.resultados_text.delete(1.0, tk.END)
        for usuario in usuarios:
            self.resultados_text.insert(tk.END, f"DNI: {usuario[1]}, Nombres: {usuario[2]}, Apellidos: {usuario[3]} {usuario[4]}, Fecha de Registro: {usuario[5]}\n")

    def buscar_registros(self):
        criterio=self.option.get()
        valor=self.entry_buscar.get()

        if criterio == "Fecha":
            resultados=self.db_manager.get_users_by_date(valor)
        elif criterio == "DNI":
            resultados=[self.db_manager.get_user_by_dni(valor)]
        elif criterio == "Nombre":
            resultados=self.db_manager.get_users_by_name(valor)
        else:
            resultados=[]

        self.resultados_text.delete(1.0, tk.END)
        for resultado in resultados:
            self.resultados_text.insert(tk.END, f"{resultado}\n")

    def ver_dnis_registrados(self):
        usuarios=self.db_manager.get_all_users()
        self.resultados_text.delete(1.0, tk.END)
        for usuario in usuarios:
            self.resultados_text.insert(tk.END, f"DNI: {usuario[1]}, Nombres: {usuario[2]}, Apellidos: {usuario[3]} {usuario[4]}, Fecha de Registro: {usuario[5]}\n")


if __name__ == "__main__":
    root=ttk.Window(themename='litera')
    api_token="tu_api_token_aqui"
    app=AttendanceApp(root, './usuarios.db', api_token)
    root.mainloop()
