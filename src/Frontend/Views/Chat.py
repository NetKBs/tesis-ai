import flet as ft
from backend.models.gemini import Gemini


def Chat(page: ft.Page, user_id=None):
    page.title = "Chat Interface"
    gemini_client = Gemini()
    # Si se pasa el user_id, úsalo, si no, usa 1 por defecto
    current_user_id = user_id if user_id is not None else 1

    current_chat_id = None
    messages = []

    def cargar_historial():
        nonlocal messages, current_chat_id
        # Buscar el último chat_id del usuario
        import sqlite3

        conn = sqlite3.connect("tesisIA.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM Chat WHERE user_id = ? ORDER BY id DESC LIMIT 1",
            (current_user_id,),
        )
        row = cursor.fetchone()
        if row:
            current_chat_id = row[0]
            # Cargar historial real
            cursor.execute(
                "SELECT role, contenido FROM Historial WHERE chat_id = ? ORDER BY orden",
                (current_chat_id,),
            )
            mensajes_db = cursor.fetchall()
            messages = []
            for i, msg in enumerate(mensajes_db):
                if i == 0 and msg[0] == "user" and msg[1].strip().startswith("Actúa como Anglai"):
                    continue
                messages.append((msg[1], msg[0]))
        else:
            current_chat_id = None
            messages = []
        conn.close()

    def update_chat(e=None):
        chat_column.controls.clear()
        screen_width = page.window_width

        if not messages:
            chat_column.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Hola",
                                size=60,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_ACCENT_400,
                            ),
                            ft.Text(
                                "¿Cómo puedo ayudarte?", size=20, color=ft.Colors.WHITE
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                )
            )
        else:
            for msg_content, msg_role in messages:
                is_user = msg_role == "user"

                horizontal_padding_total = 40

                if screen_width < 600:
                    content_width = screen_width * 0.9 - horizontal_padding_total
                    content_width = max(content_width, 100)
                else:
                    content_width = min(600, max(100, len(msg_content) * 9))
                    content_width = max(content_width, 100)

                if is_user:
                    message_control = ft.Container(
                        content=ft.Text(
                            msg_content,
                            color=ft.Colors.WHITE,
                            size=18,
                            selectable=True,
                            width=content_width,
                            max_lines=None,
                        ),
                        padding=ft.padding.symmetric(vertical=10, horizontal=18),
                        bgcolor="#1e2128",
                        border_radius=18,
                        width=content_width + 36,
                        margin=ft.margin.only(top=4, bottom=4),
                        expand=False,
                    )
                else:
                    message_control = ft.Container(
                        content=ft.Text(
                            msg_content,
                            color=ft.Colors.WHITE,
                            size=18,
                            selectable=True,
                            text_align=ft.TextAlign.START,
                            width=content_width,
                            max_lines=None,
                        ),
                        padding=ft.padding.symmetric(vertical=5, horizontal=0),
                        margin=ft.margin.only(top=4, bottom=4, left=20, right=20),
                        width=content_width,
                        expand=False,
                    )

                chat_column.controls.append(
                    ft.Row(
                        [message_control],
                        alignment=(
                            ft.MainAxisAlignment.END
                            if is_user
                            else ft.MainAxisAlignment.START
                        ),
                        expand=True,
                    )
                )

        chat_column.auto_scroll = True
        page.update()

    page.on_resize = update_chat

    chat_column = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def send_message(e):
        nonlocal current_chat_id, messages
        user_msg = input_field.value.strip()
        if user_msg:
            messages.append((user_msg, "user"))
            input_field.value = ""
            update_chat()

            try:
                response_text = gemini_client.generar_respuesta(
                    prompt=user_msg, chat_id=current_chat_id, user_id=current_user_id
                )
                if current_chat_id is None:
                    current_chat_id = gemini_client.current_chat_id

                messages.append((response_text, "model"))
            except Exception as ex:
                messages.append((f"Error al obtener respuesta: {ex}", "model"))
            finally:
                update_chat()

    input_field = ft.TextField(
        hint_text="Pregúntale a...",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_600),
        border_radius=10,
        border_color=ft.Colors.BLUE_ACCENT_700,
        focused_border_color=ft.Colors.BLUE_ACCENT_400,
        filled=True,
        fill_color=ft.Colors.BLUE_GREY_900,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        expand=True,
        content_padding=ft.padding.symmetric(vertical=10, horizontal=15),
        multiline=True,
        min_lines=1,
        max_lines=3,
    )

    input_bar = ft.Container(
        content=ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.ATTACH_FILE, icon_color=ft.Colors.WHITE, icon_size=25
                ),
                input_field,
                ft.IconButton(
                    icon=ft.Icons.SEND,
                    icon_color=ft.Colors.WHITE,
                    icon_size=25,
                    bgcolor=ft.Colors.BLUE_ACCENT_700,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=send_message,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=ft.padding.only(left=15, right=15, top=15, bottom=30),
        height=90,
        alignment=ft.alignment.center,
        bgcolor="#1e2128",
        border_radius=15,
    )

    chat_area = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.PERSON,
                                icon_color=ft.Colors.WHITE,
                                icon_size=30,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        expand=True,
                    ),
                    height=50,
                    padding=ft.padding.only(right=15, top=10),
                ),
                ft.Container(
                    content=chat_column, alignment=ft.alignment.center, expand=True
                ),
                ft.Row(
                    [
                        ft.Column(
                            [input_bar, ft.Container()],
                            expand=True,
                            alignment=ft.CrossAxisAlignment.CENTER,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
        ),
        expand=True,
        bgcolor="#1e1e1e",
    )

    page.add(ft.Container(content=chat_area, expand=True))

    cargar_historial()
    update_chat()


if __name__ == "__main__":
    ft.app(target=Chat)
