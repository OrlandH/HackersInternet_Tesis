import flet as ft
import re


def main(page: ft.Page):
    def animate(e):
        ventana.content = restaurar if ventana.content == login else login
        ventana.update()
    def volverLogin(e):
        ventana.content = login
        ventana.update()
    def claveEnviada(e):
        ventana.content = exito
        correoElectronico.value = ''
        passLogin.value = ''
        ventana.update()
    def validarCamposLogin(e) -> None:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        aux = re.match(pattern,correoElectronico.value) is not None
        if aux:
            label2.value=''
            botonRecuperar.disabled = False
            if correoElectronico.value == '' or passLogin.value == '':
                label.value = 'Llena todos los campos por favor'
                botonLogin.disabled = True
            else:
                label.value = ''
                botonLogin.disabled = False
        else:
            label2.value='Ingresa un correo Válido'
            botonLogin.disabled = True
            botonRecuperar.disabled = True

        page.update()


    label = ft.Text('', width=360, size=10, weight='w900', text_align='center', color=ft.colors.RED)
    label2 = ft.Text('', width=360, size=10, weight='w900', text_align='center', color=ft.colors.RED)

    correoElectronico = ft.TextField(width=340, height=40, label="Correo Electronico", border_color='#3F4450',border_radius=20, color='#3F4450', label_style=ft.TextStyle(color='#3F4450'), keyboard_type=ft.KeyboardType.EMAIL, on_change=validarCamposLogin, on_focus=validarCamposLogin)

    passLogin = ft.TextField(width=340, height=40, label="Contraseña", password=True, can_reveal_password=True,border_color='#3F4450', border_radius=20, color='#3F4450',label_style=ft.TextStyle(color='#3F4450'), on_change=validarCamposLogin, on_focus=validarCamposLogin)

    botonLogin = ft.ElevatedButton(content=ft.Text('Iniciar Sesión',color='white',weight='w400',),width=250,height=35, bgcolor='#3F4450')
    botonRecuperar = ft.ElevatedButton(content=ft.Text('Enviar Clave', color='white', weight='w400', ), width=250,height=35, bgcolor='#3F4450', on_click=claveEnviada)




    login = ft.Container(
        ft.Row([
            ft.Container(
                ft.Column(controls=[
                    # Contenedor con el logo
                    ft.Container(
                        ft.Image(src='../Resources/logo.png', width=350, ),
                        padding=ft.padding.only(180, 1)
                    ),
                    ft.Container(
                        ft.Image(src='../Resources/logoName.png', width=350, ),
                        padding=ft.padding.only(180, -10)
                    ),
                    # Texto Bienvenida
                    ft.Container(
                        ft.Text('Bienvenido', width=360, size=20, weight='w900', text_align='center', color='#3F4450'),
                        padding=ft.padding.only(170, -20)
                    ),
                    ft.Container(
                        label2,
                        padding=ft.padding.only(170, 10)
                    ),
                    # Contenedor con el nombre de usuario y contraseña
                    ft.Container(
                        correoElectronico,
                        padding=ft.padding.only(200, 15)
                    ),
                    ft.Container(
                        passLogin,
                        padding=ft.padding.only(200, 15)
                    ),
                    ft.Container(
                        ft.Row([
                            ft.Text(
                                '¿Problemas para iniciar?', color='#3F4450'
                            ),
                            ft.TextButton(
                                'Recuperar Cuenta', on_click=animate, style=ft.ButtonStyle(color='#3EC99D',)
                            ),
                        ], spacing=4),
                        padding=ft.padding.only(225)
                    ),
                    # Contenedor del Botón
                    ft.Container(
                        botonLogin,
                        padding=ft.padding.only(240, 10)
                    ),
                    ft.Container(
                        label,
                        padding=ft.padding.only(170, 10)
                    )
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


    restaurar = ft.Container(
        ft.Row([
            ft.Container(
                ft.Column(controls=[
                    # Contenedor con el logo
                    ft.Container(
                        ft.Image(src='../Resources/logo.png', width=350, ),
                        padding=ft.padding.only(180, 1)
                    ),
                    ft.Container(
                        ft.Image(src='../Resources/logoName.png', width=350, ),
                        padding=ft.padding.only(180, -10)
                    ),
                    # Texto Bienvenida
                    ft.Container(
                        ft.Text('Recuperar Clave', width=360, size=20, weight='w900', text_align='center', color='#3F4450'),
                        padding=ft.padding.only(170, -20)
                    ),
                    ft.Container(
                        label2,
                        padding=ft.padding.only(170, 10)
                    ),
                    # Contenedor con el correo electronico
                    ft.Container(
                        correoElectronico,
                        padding=ft.padding.only(200, 15)
                    ),
                    # Contenedor del Botón
                    ft.Container(
                        botonRecuperar,
                        padding=ft.padding.only(240, 10)
                    ),
                    ft.Container(
                        ft.Row([
                            ft.Text(
                                '¿Volvemos?', color='#3F4450'
                            ),
                            ft.TextButton(
                                'Iniciar Sesion', style=ft.ButtonStyle(color='#3EC99D'), on_click=animate
                            ),
                        ], spacing=4),
                        padding=ft.padding.only(280)
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
    exito = ft.Container(
        ft.Row([
            ft.Container(
                ft.Column(controls=[
                    # Contenedor con el logo
                    ft.Container(
                        ft.Image(src='../Resources/logo.png', width=350, ),
                        padding=ft.padding.only(180, 1)
                    ),
                    ft.Container(
                        ft.Image(src='../Resources/logoName.png', width=350, ),
                        padding=ft.padding.only(180, -10)
                    ),
                    # Texto Bienvenida
                    ft.Container(
                        ft.Text('Clave Enviada', width=360, size=25, weight='w900', text_align='center',
                                color='#3F4450'),
                        padding=ft.padding.only(175, -40)
                    ),
                    ft.Container(
                        ft.Text('Revisa tu correo Electrónico', color='#3F4450'
                            ),
                        padding=ft.padding.only(265, -50)
                    ),
                    # Contenedor del Botón
                    ft.Container(
                        ft.ElevatedButton(
                            content=ft.Text(
                                'VOLVER',
                                color='white',
                                weight='w400',
                            ),
                            on_click=volverLogin,
                            width=250,
                            height=40,
                            bgcolor='#3F4450',
                        ),
                        padding=ft.padding.only(232)
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



    ventana = ft.AnimatedSwitcher(login, transition=ft.AnimatedSwitcherTransition.FADE, duration=600,
                                  reverse_duration=100, switch_in_curve=ft.AnimationCurve.LINEAR,
                                  switch_out_curve=ft.AnimationCurve.LINEAR,)

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
    page.title = 'Hackers Internet'
    page.window_resizable= False
    page.add(
        ft.Column(
            [ventana, footer],
            expand=True,
            alignment=ft.MainAxisAlignment.END,
        )
    )

ft.app(target = main)