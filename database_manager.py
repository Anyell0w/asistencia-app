import sqlite3


class DatabaseManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect("./usuarios.db")
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

    def get_users_by_date_interval(self, start_date, end_date):
        query = "SELECT * FROM usuario WHERE fecha_registro BETWEEN ? AND ?"
        self.cursor.execute(query, (start_date, end_date))
        return self.cursor.fetchall()

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

    def get_users_by_date_range(self, start_date, end_date):
        query = "SELECT * FROM usuario WHERE fecha_registro BETWEEN ? AND ?"
        self.cursor.execute(query, (start_date, end_date))
        return self.cursor.fetchall()

    def get_user_by_dni_and_date(self, dni, date):
        query = "SELECT * FROM usuario WHERE dni = ? AND fecha_registro = ?"
        self.cursor.execute(query, (dni, date))
        return self.cursor.fetchone()

    def get_user_by_date(self, date):
        query = "SELECT * FROM usuario WHERE fecha_registro = ?"
        self.cursor.execute(query, (date,))
        return self.cursor.fetchall()

    def _del_(self):
        self.conn.close()

    def get_column(self):
        query = "PRAGMA table_info(usuario)"
        self.cursor.execute(query)
        return self.cursor.fetchall()
