import flet as ft
from backend.models.user import User

def Login(page: ft.Page):
    page.title = "Login"
    page.bgcolor = ft.Colors.TRANSPARENT

    image_container = ft.Container(
        content=ft.Image(
            src="src/assets/MOCKUP.png",
            fit=ft.ImageFit.COVER,
        ),
        expand=True,
    )

    logo = ft.Image(src="src/assets/logo.png", width=150, height=150)

    title = ft.Text("Iniciar Sesión", size=25, color=ft.Colors.WHITE)

    username_field = ft.TextField(
        label="Nombre de usuario",
        border_color=ft.Colors.BLUE_ACCENT_700,
        color=ft.Colors.WHITE,
    )
    password_field = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        border_color=ft.Colors.BLUE_ACCENT_700,
        color=ft.Colors.WHITE,
    )
    
    def on_login_click(e):
        username = username_field.value
        password = password_field.value
        print(f"Usuario: {username}, Contraseña: {password}")   
        user = User() 
        if user.login(username, password):
            print("Inicio de sesión exitoso")
        else:
            print("Usuario o contraseña incorrectos")
    
    login_button = ft.ElevatedButton(
        text="Ingresar",
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_ACCENT_700,
        width=200,
        on_click=on_login_click  # Añadir el evento al botón
    )

    login_form = ft.Column(
        [logo, title, username_field, password_field, login_button],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    login_container = ft.Container(
        content=login_form,
        padding=30,
        bgcolor=ft.Colors.BLACK,
        expand=True,
        alignment=ft.alignment.center,
        border_radius=20
    )

    row_layout = ft.Row(
        [image_container, login_container],
        expand=True,
    )

    page.add(row_layout)
