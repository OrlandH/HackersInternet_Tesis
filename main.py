import flet as ft

body =  ft.Container(
            ft.Row([
                ft.Container(
                    ft.Column(controls= [
                        # Contenedor con el logo
                        ft.Container(
                            ft.Image(src='logo.png', width=150,),
                            padding= ft.padding.only(100,20)
                            ),
                        # Texto Bienvenida
                        ft.Text('Bienvenido', width=360, size=30, weight ='w900', text_align = 'center'),
                        # Contenedor con el nombre de usuario y contraseña
                        ft.Container(
                            ft.TextField(width=300,height=40, label="Nombre de Usuario"),
                            padding= ft.padding.only(35, 10)
                            ),
                        ft.Container(
                            ft.TextField(width=300,height=40, label="Contraseña",password = True, can_reveal_password=True),
                                padding = ft.padding.only(35,10)
                            ),
                        # Contenedor del Botón
                        ft.Container(
                            ft.ElevatedButton(
                                content = ft.Text(
                                    'INICIAR',
                                    color = 'white',
                                    weight ='w500',
                                    ),
                                width =280,
                                bgcolor = 'black',
                                ),
                                padding = ft.padding.only(25,10)
                            ),
                        ft.Container(
                            ft.Row([
                                ft.Text(
                                    '¿No tiene una cuenta?'
                                    ),
                                ft.TextButton(
                                    'Crear una cuenta'
                                    ),
                                ], spacing=8),
                            padding = ft.padding.only(40)
                            ),
                        ],
                        alignment = ft.MainAxisAlignment.SPACE_EVENLY,
                        ),
                    gradient= ft.LinearGradient(['red', 'orange']),
                    width=380,
                    height =460,
                    border_radius=20
                ),
                ],
                alignment = ft.MainAxisAlignment.SPACE_EVENLY,
                ),
        padding= 10,
        )

def main(page:ft.Page):
    page.window_width =800
    page.window_height = 520
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    #page.window_bgcolor = ft.colors.TRANSPARENT
    #page.window_title_bar_buttons_hidden = True
    #page.window_frameless = True
    #page.window_title_bar_hidden = True
    #page.bgcolor = ft.colors.TRANSPARENT
    page.add(
            body
        )

ft.app(target=main)
