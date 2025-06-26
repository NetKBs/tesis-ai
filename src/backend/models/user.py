import sqlite3

class User:
    def __init__(self, db_path="tesisIA.db"):
        self.db_path = db_path

    def login(self, username: str, password: str) -> bool:
        """Verifica si el usuario y password existe en la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM User WHERE usuario = ? AND password = ?",
            (username, password))
        
        result = cursor.fetchone()

        conn.close()
        return result is not None

    def register(self, correo: str, password: str, nombre: str, usuario: str) -> bool:
        """Inserta un nuevo usuario en la tabla User. Devuelve True si lo logró, False si hubo error (e.g. correo duplicado)."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO User (correo, password, nombre, usuario) VALUES (?, ?, ?, ?)",
                (correo, password, nombre, usuario)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Si tienes restricciones de unicidad y se viola alguna
            return False
        except Exception as e:
            print("Error al registrar usuario:", e)
            return False

    def get_user_id(self, username: str) -> int:
        """Obtiene el id del usuario dado su nombre de usuario."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM User WHERE usuario = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
        return None