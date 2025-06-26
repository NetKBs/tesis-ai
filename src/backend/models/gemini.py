import os
from dotenv import load_dotenv
# import google.generativeai as genai
# from google.generativeai import types
from google import genai
from google.genai import types
import pathlib
import sqlite3
from typing import List, Dict, Optional
from datetime import datetime
import sys
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'database'))
from database.setup_database import setup_database


load_dotenv()
API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

if not API_KEY:
    raise ValueError("No se encontró la variable de entorno 'GOOGLE_GENAI_API_KEY'")


class Gemini:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)
        self.current_chat_id = None
        self._system_prompt_text = """Actúa como Anglai, un asistente experto y riguroso en lineamientos de trabajos especiales de grado, especializado en normativas académicas, específicamente las normas APA 7ma edición. 
            Tu objetivo principal es guiar a los estudiantes en la formulación y desarrollo de sus tesis con precisión y estructura. "
            "Para cada sección, considera las siguientes directrices estrictas:"
            "1. Título:"
            "   - No debe exceder las 18 palabras."
            "   - Debe iniciar con una palabra de accion (ej. 'Analisis', 'Implementacion', 'creacion')."
            "2. Planteamiento del Problema:"
            "   - Desarrolla el problema de forma descriptiva y argumentativa."
            "   - Inicia desde una perspectiva internacional, luego aterriza a nivel nacional (Venezuela), y finalmente enfócate en el contexto regional (Bolívar)."
            "   - Obligatoriamente, incluye citas de autores relevantes para respaldar cada nivel (internacional, nacional, regional), aplicando el formato APA 7ma edición."
            "3. Antecedentes:"
            "   - Presenta tres antecedentes de investigación:"
            "     - Uno internacional."
            "     - Uno nacional (Venezuela)."
            "     - Uno regional (Bolívar)."
            "   - Para cada antecedente, resume su propósito, metodología, resultados y cómo se relaciona con la investigación actual del estudiante, siempre citando según APA 7ma edición."
            "4. Objetivos de la Investigación:"
            "   - Objetivo General: Debe ser único, iniciar con el verbo en infinitivo del título (manteniendo la misma idea principal) y expresar el propósito global del estudio."
            "   - Objetivos Específicos: Deben ser tres, cada uno iniciando con un verbo en infinitivo, ser medibles, alcanzables y detallar los pasos para lograr el objetivo general."
            "5. Justificación:"
            "   - Explica la relevancia, utilidad y viabilidad del estudio desde perspectivas teóricas, prácticas, metodológicas, sociales y personales, según aplique."
            "6. Marco Teórico:"
            "   - Proporciona las bases teóricas y conceptuales que sustentan la investigación, definiendo términos clave y teorías relevantes, con citas APA 7ma edición."
            "7. Marco Metodológico:"
            "   - Detalla el tipo de investigación, diseño, población, muestra, técnicas e instrumentos de recolección de datos, y el plan de análisis, todo conforme a las normas académicas."
            "Además de estas directrices, puedes ayudar a generar ideas para mapas mentales sobre los temas de tesis, facilitando la organización de ideas y conceptos complejos. "
            "Siempre que proporciones información, asegúrate de que esté redactada bajo los principios de las normas APA 7ma edición, ademas de que no respondas con asteriscos, solo vinetas."""
        
        
    def _get_db_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect('tesisIA.db')
        setup_database(conn) 
        return conn

    def _crear_nuevo_chat(self, user_id: int, titulo: str = "Nuevo chat") -> int:
        conn = self._get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Chat (user_id, titulo) VALUES (?, ?)",
                (user_id, titulo)
            )
            conn.commit()
            chat_id = cursor.lastrowid
            self._guardar_mensaje(chat_id, "user", self._system_prompt_text)
            return chat_id
        finally:
            conn.close()
    
    def _guardar_mensaje(self, chat_id: int, role: str, contenido: str) -> int:
        conn = self._get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT COALESCE(MAX(orden), 0) + 1 FROM Historial WHERE chat_id = ?",
                (chat_id,)
            )
            orden = cursor.fetchone()[0]
            
            cursor.execute(
                "INSERT INTO Historial (chat_id, orden, role, contenido) VALUES (?, ?, ?, ?)",
                (chat_id, orden, role, contenido)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close() 
    
    def _cargar_historial(self, chat_id: int, filtrar_system_prompt: bool = True) -> List[Dict[str, str]]:
        """
        Si filtrar_system_prompt=True (por defecto), el system prompt no se incluye en el historial devuelto.
        Si filtrar_system_prompt=False, se incluye (solo para el modelo Gemini).
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT role, contenido FROM Historial WHERE chat_id = ? ORDER BY orden",
                (chat_id,)
            )
            mensajes = []
            for i, row in enumerate(cursor.fetchall()):
                if filtrar_system_prompt and i == 0 and row[0] == "user" and row[1].strip().startswith("Actúa como Anglai"):
                    continue
                mensajes.append({"role": row[0], "content": row[1]})
            return mensajes
        finally:
            conn.close() 

    def generar_respuesta(self, prompt: str, chat_id: Optional[int] = None, user_id: Optional[int] = None) -> str:
        if chat_id is None:
            if user_id is None:
                raise ValueError("Se requiere user_id para crear un nuevo chat si chat_id es None.")
            chat_id = self._crear_nuevo_chat(user_id)
            self.current_chat_id = chat_id 
        else:
            self.current_chat_id = chat_id 

        self._guardar_mensaje(chat_id, "user", prompt)
        # No filtrar el system prompt para el modelo
        historial = self._cargar_historial(chat_id, filtrar_system_prompt=False)
        contents = [types.Content(role=msg["role"], parts=[types.Part(text=msg["content"])]) 
                    for msg in historial]
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents
        )
        # Eliminar asteriscos con regex
        clean_text = re.sub(r"\*+", "", response.text)
        self._guardar_mensaje(chat_id, "model", clean_text)
        return clean_text
    
    def evaluar_pdf(self, pdf_path: pathlib.Path, prompt: str, chat_id: Optional[int] = None, 
                     user_id: Optional[int] = None) -> str:
        if not pdf_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {pdf_path}")
            
        if chat_id is None:
            if user_id is None:
                raise ValueError("Se requiere user_id para crear un nuevo chat si chat_id es None.")
            chat_id = self._crear_nuevo_chat(user_id)
            self.current_chat_id = chat_id
        else:
            self.current_chat_id = chat_id

        self._guardar_mensaje(chat_id, "user", prompt)
        
        historial = self._cargar_historial(chat_id)[:-1] 
        
        contents = [types.Content(role=msg["role"], parts=[types.Part(text=msg["content"])]) 
                    for msg in historial]
        
        contents.append(types.Blob(
            mime_type='application/pdf',
            data=pdf_path.read_bytes()
        ))
        contents.append(types.Content(role="user", parts=[types.Part(text=prompt)]))
        
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents
        )
        
        self._guardar_mensaje(chat_id, "model", response.text)
        
        return response.text
    
    def obtener_chats_usuario(self, user_id: int) -> List[Dict]:
        conn = self._get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id, titulo, fecha_creacion FROM Chat WHERE user_id = ? ORDER BY fecha_creacion DESC",
                (user_id,)
            )
            return [{"id": row[0], "titulo": row[1], "fecha_creacion": row[2]} 
                    for row in cursor.fetchall()]
        finally:
            conn.close() 
    
    def obtener_historial_chat(self, chat_id: int) -> List[Dict]:
        conn = self._get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT role, contenido, fecha FROM Historial WHERE chat_id = ? ORDER BY orden",
                (chat_id,)
            )
            mensajes = []
            for i, row in enumerate(cursor.fetchall()):
                if i == 0 and row[0] == "user" and row[1].strip().startswith("Actúa como Anglai"):
                    continue
                mensajes.append({"role": row[0], "content": row[1], "fecha": row[2]})
            return mensajes
        finally:
            conn.close()
    
    def limpiar_historial(self, chat_id: int):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Historial WHERE chat_id = ?", (chat_id,))
            cursor.execute("DELETE FROM Chat WHERE id = ?", (chat_id,))
            conn.commit()
            print(f"Historial y chat {chat_id} limpiados y eliminados.")
        finally:
            conn.close() 


if __name__ == "__main__":
    print("Iniciando pruebas de la clase Gemini...")

    initial_conn = sqlite3.connect('tesisIA.db')
    setup_database(initial_conn)
    initial_conn.close() 
    print("Base de datos configurada.")

    gemini_instance = Gemini()
    test_user_id = 1 

    print("\n--- Ejemplo: Nuevo chat y primera pregunta ---")
    pregunta_inicial = "Necesito ayuda con el planteamiento del problema de mi tesis."
    print(f"Usuario ({test_user_id}): {pregunta_inicial}")
    respuesta_inicial = gemini_instance.generar_respuesta(pregunta_inicial, user_id=test_user_id)
    print(f"Gemini: {respuesta_inicial}")
    current_test_chat_id = gemini_instance.current_chat_id
    print(f"ID del chat actual: {current_test_chat_id}")

    print("\n--- Ejemplo: Continuar el mismo chat ---")
    pregunta_seguimiento = "¿Y qué hay de los agujeros negros?"
    print(f"Usuario ({test_user_id}): {pregunta_seguimiento}")
    respuesta_seguimiento = gemini_instance.generar_respuesta(pregunta_seguimiento, chat_id=current_test_chat_id)
    print(f"Gemini: {respuesta_seguimiento}")

    print("\n--- Ejemplo: Chats del usuario ---")
    chats_del_usuario = gemini_instance.obtener_chats_usuario(test_user_id)
    if chats_del_usuario:
        for chat in chats_del_usuario:
            print(f"Chat ID: {chat['id']}, Título: '{chat['titulo']}', Creado: {chat['fecha_creacion']}")
    else:
        print("No se encontraron chats para este usuario.")

    if current_test_chat_id:
        print(f"\n--- Ejemplo: Historial del chat {current_test_chat_id} ---")
        historial_completo = gemini_instance.obtener_historial_chat(current_test_chat_id)
        for msg in historial_completo:
            print(f"[{msg['fecha']}] {msg['role'].capitalize()}: {msg['content']}")


    print("\nPruebas de Gemini finalizadas.")