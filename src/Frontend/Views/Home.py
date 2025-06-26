import flet as ft
from Frontend.Views.Chat import Chat

def Home(page: ft.Page, user_id=None):
    page.title = "ANGLAI - Guía Rápida"
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLUE_700
    page.window_width = 800
    page.window_height = 700
    page.window_resizable = False

    text_animation = ft.Animation(600, ft.AnimationCurve.EASE_OUT_SINE)

    welcome_title = ft.Text(
        "¡Bienvenido a ANGLAI, tu asistente de tesis!",
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER,
        opacity=0,
        animate_opacity=text_animation,
        animate_offset=text_animation,
    )

    intro_text = ft.Text(
        "Estoy aquí para simplificar tu camino en la elaboración de tu trabajo especial de grado.",
        size=22,
        color=ft.Colors.CYAN_200,
        italic=True,
        text_align=ft.TextAlign.CENTER,
        opacity=0,
        animate_opacity=text_animation,
        animate_offset=text_animation,
    )

    instruction_point_1 = ft.Row(
        [
            ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE, color=ft.Colors.WHITE, size=30),
            ft.Text(
                "Pregúntame sobre tu tesis: ¡Soy experto en lineamientos de trabajos de grado! Puedes consultarme sobre:",
                size=18,
                color=ft.Colors.BLUE_GREY_100,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.LEFT,
                expand=True,  
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    instruction_sub_point_1_1 = ft.Text(
        "    •  Título y planteamiento del problema",
        size=16,
        color=ft.Colors.BLUE_GREY_100,
    )
    instruction_sub_point_1_2 = ft.Text(
        "    •  Objetivos y justificación",
        size=16,
        color=ft.Colors.BLUE_GREY_100,
    )
    instruction_sub_point_1_3 = ft.Text(
        "    •  Marco teórico y metodológico",
        size=16,
        color=ft.Colors.BLUE_GREY_100,
    )
    instruction_sub_point_1_4 = ft.Text(
        "¡Y cualquier otra duda que tengas!",
        size=16,
        color=ft.Colors.BLUE_GREY_100,
    )

    instruction_point_2 = ft.Row(
        [
            ft.Icon(ft.Icons.MAP, color=ft.Colors.WHITE, size=30),
            ft.Text(
                "Crea mapas mentales: ¿Necesitas visualizar tus ideas? ¡Juntos podemos construir mapas mentales para organizar y entender mejor tus temas!",
                size=18,
                color=ft.Colors.BLUE_GREY_100,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.LEFT,
                expand=True,  
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    final_prompt = ft.Text(
        "¡Es muy sencillo! Solo escribe tu primera pregunta y empecemos.",
        size=20,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        opacity=0,
        animate_opacity=text_animation,
        animate_offset=text_animation,
    )

    def on_start_chat_click(e):
        page.clean()
        Chat(page, user_id=user_id)
        page.update()

    start_button = ft.ElevatedButton(
        text="¡Entendido! Empezar a Chatear",
        on_click=on_start_chat_click,
        icon=ft.Icons.ARROW_FORWARD,
        color=ft.Colors.BLUE_GREY_900,
        bgcolor=ft.Colors.CYAN_ACCENT_400,
        height=55,
        width=300,
        opacity=0,
        animate_opacity=ft.Animation(800, ft.AnimationCurve.EASE_IN),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    guide_content = ft.Column(
        [
            welcome_title,
            ft.Container(height=15),
            intro_text,
            ft.Container(height=40),
            instruction_point_1,
            instruction_sub_point_1_1,
            instruction_sub_point_1_2,
            instruction_sub_point_1_3,
            instruction_sub_point_1_4,
            ft.Container(height=25),
            instruction_point_2,
            ft.Container(height=40),
            final_prompt,
            ft.Container(height=30),
            start_button,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=0,
    )

    content_container = ft.Container(
        content=guide_content,
        padding=ft.padding.all(40),
        width=750,
        height=650,
        bgcolor=ft.Colors.BLACK,
        border_radius=ft.border_radius.all(15),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=10,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 5),
        ),
    )

    page.add(
        ft.Column(
            [content_container],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
    )
    page.update()

    welcome_title.opacity = 1
    page.update()
    import time

    time.sleep(0.1)

    intro_text.opacity = 1
    page.update()
    time.sleep(0.1)


    instruction_point_1.controls[0].opacity = 0 
    instruction_point_1.controls[1].opacity = 0
    page.update()
    time.sleep(0.1)
    instruction_point_1.controls[0].opacity = 1
    instruction_point_1.controls[1].opacity = 1
    page.update()
    time.sleep(0.1)

    instruction_sub_point_1_1.opacity = 0
    instruction_sub_point_1_2.opacity = 0
    instruction_sub_point_1_3.opacity = 0
    instruction_sub_point_1_4.opacity = 0
    page.update()
    time.sleep(0.1)
    instruction_sub_point_1_1.opacity = 1
    page.update()
    time.sleep(0.05)
    instruction_sub_point_1_2.opacity = 1
    page.update()
    time.sleep(0.05)
    instruction_sub_point_1_3.opacity = 1
    page.update()
    time.sleep(0.05)
    instruction_sub_point_1_4.opacity = 1
    page.update()
    time.sleep(0.1)

    instruction_point_2.controls[0].opacity = 0
    instruction_point_2.controls[1].opacity = 0
    page.update()
    time.sleep(0.1)
    instruction_point_2.controls[0].opacity = 1
    instruction_point_2.controls[1].opacity = 1
    page.update()
    time.sleep(0.1)

    final_prompt.opacity = 1
    page.update()
    time.sleep(0.1)

    start_button.opacity = 1
    page.update()

if __name__ == "__main__":
    ft.app(target=Home)