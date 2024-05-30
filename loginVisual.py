import flet as ft

body = ft.Container(
    ft.Row([
        ft.Container(
            ft.Column(controls=[
                # Contenedor con el logo
                ft.Container(
                    ft.Image(src='logo.png', width=350, ),
                    padding=ft.padding.only(180, 1)
                ),
                ft.Container(
                    ft.Image(src='logoName.png', width=350, ),
                    padding=ft.padding.only(180, -10)
                ),
                # Texto Bienvenida
                ft.Container(
                    ft.Text('Bienvenido', width=360, size=20, weight='w900', text_align='center', color='#3F4450'),
                    padding=ft.padding.only(170, -20)
                ),
                # Contenedor con el nombre de usuario y contraseña
                ft.Container(
                    ft.TextField(width=340, height=40, label="Correo Electronico", border_color='#3F4450',
                                 border_radius=20, color='#3F4450', label_style=ft.TextStyle(color='#3F4450')),
                    padding=ft.padding.only(200, 15)
                ),
                ft.Container(
                    ft.TextField(width=340, height=40, label="Contraseña", password=True, can_reveal_password=True,
                                 border_color='#3F4450', border_radius=20, color='#3F4450',
                                 label_style=ft.TextStyle(color='#3F4450')),
                    padding=ft.padding.only(200, 15)
                ),
                ft.Container(
                    ft.Row([
                        ft.Text(
                            '¿Problemas para iniciar?', color='#3F4450'
                        ),
                        ft.TextButton(
                            'Recuperar Cuenta', style=ft.ButtonStyle(color='#3EC99D')
                        ),
                    ], spacing=4),
                    padding=ft.padding.only(225)
                ),
                # Contenedor del Botón
                ft.Container(
                    ft.ElevatedButton(
                        content=ft.Text(
                            'Iniciar Sesión',
                            color='white',
                            weight='w400',
                        ),
                        width=250,
                        height=35,
                        bgcolor='#3F4450',
                    ),
                    padding=ft.padding.only(240, 10)
                ),
            ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
            width=700,
            height=600,
        ),
    ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    ),
)


def main(page: ft.Page):
    # Crear un contenedor para el footer
    footer = ft.Container(
        height=100,
        alignment=ft.alignment.center,
        bgcolor='#3F4450',
    )

    page.window_width = 1400
    page.window_height = 780
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.bgcolor = ft.colors.WHITE
    # Agregar el cuerpo y el footer a una columna
    page.add(
        ft.Column(
            [body, footer],
            expand=True,
            alignment=ft.MainAxisAlignment.END,
        )
    )


ft.app(target=main)
