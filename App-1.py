import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
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

    def get_users_by_date(self, date):
        query = "SELECT * FROM usuario WHERE fecha_registro = ?"
        self.cursor.execute(query, (date,))
        return self.cursor.fetchall()

    def get_users_by_name(self, name):
        query = "SELECT * FROM usuario WHERE nombres LIKE ?"
        self.cursor.execute(query, (f'%{name}%',))
        return self.cursor.fetchall()

    def get_all_users(self):
        query = "SELECT * FROM usuario"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()


class AttendanceApp:
    def __init__(self, root, db_path, api_token):
        self.root = root
        self.db_manager = DatabaseManager(db_path)
        self.api_client = APIClient(api_token)
        self.root.title("Registro de Asistencia")

        # imagen
        self.lbl_imagen = tk.PhotoImage(file="./images/finesi.png")
        self.lbl_logo = tk.Label(self.root, image=self.lbl_imagen)
        self.lbl_logo.pack()
        # fecha actual en frame
        self.frame_fecha = tk.Frame(self.root)
        self.frame_fecha.pack(pady=10)
        self.fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        self.lbl_fecha = tk.Label(self.frame_fecha, text=f"Fecha Actual: {self.fecha}")
        self.lbl_fecha.pack()
        # hora actual en frame
        self.hora = datetime.datetime.now().strftime("%H:%M:%S")
        self.frame_hora = tk.Frame(self.root)
        self.frame_hora.pack(pady=10)
        self.lbl_hora = tk.Label(self.frame_hora, text=f"Hora Actual: {self.hora}")
        self.lbl_hora.pack()

        # Frame para ingresar DNI
        self.frame_dni = tk.Frame(self.root)
        self.frame_dni.pack(pady=10)

        self.lbl_dni = tk.Label(self.frame_dni, text="DNI:")
        self.lbl_dni.pack(side=tk.LEFT, padx=5)
        self.entry_dni = tk.Entry(self.frame_dni)
        self.entry_dni.pack(side=tk.LEFT, padx=5)
        self.btn_registrar = tk.Button(self.frame_dni, text="Registrar", command=self.registrar_asistencia)
        self.btn_registrar.pack(side=tk.LEFT, padx=5)

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

        # Frame para mostrar resultados de búsqueda
        self.frame_resultados = tk.Frame(self.root)
        self.frame_resultados.pack(pady=10)

        self.resultados_text = tk.Text(self.frame_resultados, height=10, width=80)
        self.resultados_text.pack()

    def registrar_asistencia(self):
        dni = self.entry_dni.get()
        if not dni:
            messagebox.showerror("Error", "Debe ingresar un DNI")
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

        self.lbl_fecha_registro = tk.Label(self.root_nuevo_usuario, text="Fecha de Registro:")
        self.lbl_fecha_registro.pack(side=tk.LEFT, padx=5)
        self.entry_fecha_registro = tk.Entry(self.root_nuevo_usuario)
        self.fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        self.entry_fecha_registro.pack(side=tk.LEFT, padx=5)
        self.entry_fecha_registro.insert(0, self.fecha)
        self.entry_fecha_registro.config(state='readonly')

        self.btn_guardar = tk.Button(self.root_nuevo_usuario, text="Guardar", command=self.guardar_usuario)
        self.btn_guardar.pack()

    def guardar_usuario(self):
        dni = self.entry_dni_nuevo.get()
        nombres = self.entry_nombres.get()
        apellido_paterno = self.entry_apellido_paterno.get()
        apellido_materno = self.entry_apellido_materno.get()
        fecha_registro = self.entry_fecha_registro.get()

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


if __name__ == "__main__":
    root = tk.Tk()
    api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Ijc2NjA2Mzc1QGVzdC51bmFwLmVkdS5wZSJ9.wr2q4R-W7ymnCmYpJ5khKA3DTQuZ4w098KcVQ1yha88"
    app = AttendanceApp(root, './usuarios.db', api_token)
    root.mainloop()
