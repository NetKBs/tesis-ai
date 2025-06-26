import flet as ft
from backend.models.user import User
from Frontend.Views.Login import Login


def Register(page: ft.Page):
    page.title = "Registrarse - ANGLAI"
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLUE_700
    page.window_width = 800
    page.window_height = 700
    page.window_resizable = False

    logo = ft.Image(src="src/assets/logo.png", width=120, height=120)

    title = ft.Text(
        "Únete a la Aventura ANGLAI",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    username_field = ft.TextField(
        label="Nombre de usuario",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_100),
        border_color=ft.Colors.CYAN_ACCENT_400,
        focused_border_color=ft.Colors.CYAN_ACCENT_200,
        color=ft.Colors.WHITE,
        cursor_color=ft.Colors.CYAN_ACCENT_100,
        width=300,
        border_radius=10,
        autocorrect=False,
        enable_suggestions=False,
    )
    name_field = ft.TextField(
        label="Nombre real",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_100),
        border_color=ft.Colors.CYAN_ACCENT_400,
        focused_border_color=ft.Colors.CYAN_ACCENT_200,
        color=ft.Colors.WHITE,
        cursor_color=ft.Colors.CYAN_ACCENT_100,
        width=300,
        border_radius=10,
        autocorrect=False,
        enable_suggestions=False,
    )
    email_field = ft.TextField(
        label="Correo electrónico",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_100),
        border_color=ft.Colors.CYAN_ACCENT_400,
        focused_border_color=ft.Colors.CYAN_ACCENT_200,
        color=ft.Colors.WHITE,
        cursor_color=ft.Colors.CYAN_ACCENT_100,
        keyboard_type=ft.KeyboardType.EMAIL,
        width=300,
        border_radius=10,
    )
    password_field = ft.TextField(
        label="Contraseña",
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_100),
        password=True,
        can_reveal_password=True,
        border_color=ft.Colors.CYAN_ACCENT_400,
        focused_border_color=ft.Colors.CYAN_ACCENT_200,
        color=ft.Colors.WHITE,
        cursor_color=ft.Colors.CYAN_ACCENT_100,
        width=300,
        border_radius=10,
    )

    error_text = ft.Text(
        value="", color=ft.Colors.RED_ACCENT_400, size=14, visible=False
    )

    def handle_register(e):
        user = User()
        # El orden correcto es: correo, password, nombre, usuario
        if user.register(email_field.value, password_field.value, name_field.value, username_field.value):
            print("Registro exitoso")
            page.clean()
            Login(page)
            page.update()
        else:
            print("Error en el registro")
            error_text.value = "Error al registrar. Intenta de nuevo."
            error_text.visible = True
            page.update()

        print(
            f"Registrando: {username_field.value}, {email_field.value}, {password_field.value}, {name_field.value}"
        )
        page.clean()
        Login(page)
        page.update()

    register_button = ft.ElevatedButton(
        text="Registrarse",
        icon=ft.Icons.PERSON_ADD,
        color=ft.Colors.BLUE_GREY_900,
        bgcolor=ft.Colors.CYAN_ACCENT_400,
        width=250,
        height=50,
        on_click=handle_register,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )

    def navigate_to_login_from_register(e):
        page.clean()
        Login(page)
        page.update()

    login_link = ft.TextButton(
        text="¿Ya tienes una cuenta? Inicia sesión.",
        style=ft.ButtonStyle(color=ft.Colors.BLUE_ACCENT_100),
        on_click=navigate_to_login_from_register,
    )

    register_form_content = ft.Column(
        [
            logo,
            title,
            ft.Container(height=20),
            username_field,
            name_field,
            email_field,
            password_field,
            error_text,
            ft.Container(height=30),
            register_button,
            login_link,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
    )

    register_container = ft.Container(
        content=register_form_content,
        width=450,
        height=650,
        padding=40,
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.BLACK54,
        border_radius=ft.border_radius.all(20),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=ft.Colors.BLACK38,
            offset=ft.Offset(0, 8),
        ),
    )

    page.add(
        ft.Column(
            [register_container],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
    )
    page.update()
