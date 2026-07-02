import sqlite3
import os

class GestorBaseDatos:
    def __init__(self, ruta_db="hoku_save.db"):
        self.ruta_db = ruta_db
        self.conectar_y_crear_tablas()
        self.cine_inicial_vista = False

    def obtener_conexion(self):
        return sqlite3.connect(self.ruta_db)

    def conectar_y_crear_tablas(self):
        """Crea las tablas necesarias para el juego si no existen."""
        with self.obtener_conexion() as conn:
            cursor = conn.cursor()
            
            # Tabla para guardar el estado del personaje y progreso general
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS partida (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    escenario_id INTEGER NOT NULL,
                    pos_x REAL NOT NULL,
                    pos_y REAL NOT NULL,
                    vida_actual INTEGER NOT NULL
                )
            ''')
            
            # Tabla para registrar qué JEFES matamos (así no reviven al rezar)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jefes_derrotados (
                    jefe_nombre TEXT PRIMARY KEY
                )
            ''')
            conn.commit()

    def guardar_partida(self, escenario_id, pos_x, pos_y, vida_maxima):
        """Guarda o actualiza la partida de Hoku (curado al máximo)."""
        with self.obtener_conexion() as conn:
            cursor = conn.cursor()
            
            # Limpiamos guardados viejos para tener solo un slot automático
            cursor.execute("DELETE FROM partida")
            
            # Insertamos el nuevo punto de control con la vida al máximo
            cursor.execute('''
                INSERT INTO partida (escenario_id, pos_x, pos_y, vida_actual)
                VALUES (?, ?, ?, ?)
            ''', (escenario_id, pos_x, pos_y, vida_maxima))
            
            conn.commit()
            print("¡Partida guardada en la Base de Datos exitosamente!")

    def registrar_jefe_derrotado(self, nombre_jefe):
        """Guarda en la BD que un jefe murió."""
        with self.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO jefes_derrotados (jefe_nombre) VALUES (?)", (nombre_jefe,))
            conn.commit()

    def obtener_jefes_derrotados(self):
        """Devuelve una lista con los nombres de jefes muertos."""
        with self.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT jefe_nombre FROM jefes_derrotados")
            return [fila[0] for fila in cursor.fetchall()]

    def cargar_partida(self):
        """Devuelve los datos de la partida si existen, o None."""
        with self.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT escenario_id, pos_x, pos_y, vida_actual FROM partida LIMIT 1")
            fila = cursor.fetchone()
            if fila:
                return {
                    "escenario_id": fila[0],
                    "pos_x": fila[1],
                    "pos_y": fila[2],
                    "vida_actual": fila[3]
                }
            return None