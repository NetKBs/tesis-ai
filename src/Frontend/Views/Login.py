import flet as ft
from backend.models.user import User 
from Frontend.Views.Home import Home


def Login(page: ft.Page):
    page.title = "Iniciar Sesión - ANGLAI"
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLUE_700 
    page.window_width = 800
    page.window_height = 700
    page.window_resizable = False 

    logo = ft.Image(src="src/assets/logo.png", width=120, height=120) 

    title = ft.Text(
        "Inicia Sesión en ANGLAI",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE 
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
        value="",
        color=ft.Colors.RED_ACCENT_400,
        size=14,
        visible=False 
    )

    def on_login_click(e):
        username = username_field.value
        password = password_field.value
        print(f"Usuario: {username}, Contraseña: {password}")

        user = User()
        if user.login(username, password):
            print("Inicio de sesión exitoso")
            user_id = user.get_user_id(username)
            page.clean()
            Home(page, user_id=user_id)
            page.update()
        else:
            print("Usuario o contraseña incorrectos")
            error_text.value = "Usuario o contraseña incorrectos."
            error_text.visible = True
            page.update()

    login_button = ft.ElevatedButton(
        text="Ingresar",
        icon=ft.Icons.LOGIN, 
        color=ft.Colors.BLUE_GREY_900,
        bgcolor=ft.Colors.CYAN_ACCENT_400, 
        width=250, 
        height=50,
        on_click=on_login_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )


    login_form_content = ft.Column(
        [
            logo,
            title,
            ft.Container(height=20),
            username_field,
            password_field,
            error_text, 
            ft.Container(height=30), 
            login_button,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15, 
    )


    login_container = ft.Container(
        content=login_form_content,
        width=450, 
        height=550, 
        padding=40,
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
            [login_container],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
    )
    page.update()