import flet as ft

class ViewMain:
    def __init__(self, page, presenter):
        self.page = page
        self.presenter = presenter

        # Parametros y variables necesarias inicializar Login y Recuperar
        self.label = ft.Text('', width=360, size=10, weight='w900', text_align='center', color=ft.colors.RED)
        self.label2 = ft.Text('', width=360, size=10, weight='w900', text_align='center', color=ft.colors.RED)
        self.correoElectronico = ft.TextField(width=340, height=40, label="Correo Electronico", border_color='#3F4450',border_radius=20, color='#3F4450', label_style=ft.TextStyle(color='#3F4450'),keyboard_type=ft.KeyboardType.EMAIL, on_change=self.presenter.validarCamposLogin,on_focus=self.presenter.validarCamposLogin)
        self.passLogin = ft.TextField(width=340, height=40, label="Contraseña", password=True, can_reveal_password=True,border_color='#3F4450', border_radius=20, color='#3F4450',label_style=ft.TextStyle(color='#3F4450'), on_change=self.presenter.validarCamposLogin,on_focus=self.presenter.validarCamposLogin)
        self.botonLogin = ft.ElevatedButton(content=ft.Text('Iniciar Sesión', color='white', weight='w400'),width=250, height=35, bgcolor='#3F4450')
        self.botonRecuperar = ft.ElevatedButton(content=ft.Text('Enviar Clave', color='white', weight='w400'),width=250, height=35, bgcolor='#3F4450', on_click=self.presenter.claveEnviada)
        self.footer = ft.Container(height=100, alignment=ft.alignment.center, bgcolor='#3F4450')

        # Construir Vistas
        self.build_login()
        self.build_restaurar()
        self.build_exito()

        # Parametros para la ventana principal
        self.ventana = ft.AnimatedSwitcher(self.login, transition=ft.AnimatedSwitcherTransition.FADE, duration=600,reverse_duration=100, switch_in_curve=ft.AnimationCurve.LINEAR,switch_out_curve=ft.AnimationCurve.LINEAR)
        self.page.window_width = 1400
        self.page.window_height = 780
        self.page.vertical_alignment = "center"
        self.page.horizontal_alignment = "center"
        self.page.bgcolor = ft.colors.WHITE
        self.page.title = 'Hackers Internet'
        self.page.window_resizable = False
        page.window_maximizable = False
        self.page.add(self.ventana)

    # Build del Login
    def build_login(self):
        self.login = ft.Container(
            ft.Row([
                ft.Container(
                    ft.Column(controls=[
                        ft.Container(ft.Image(src='assets/logo.png', width=350), alignment=ft.alignment.center),
                        ft.Container(ft.Image(src='assets/logoName.png', width=350), alignment=ft.alignment.center),
                        ft.Container(ft.Text('Bienvenido', width=360, size=20, weight='w900', text_align='center',color='#3F4450'), alignment=ft.alignment.center),
                        ft.Container(self.label2, alignment=ft.alignment.center),
                        ft.Container(self.correoElectronico, alignment=ft.alignment.center, padding=ft.padding.only(0,15)),
                        ft.Container(self.passLogin, alignment=ft.alignment.center, padding=ft.padding.only(0,25)),
                        ft.Container(ft.Row([ft.Text('¿Problemas para iniciar?', color='#3F4450'),ft.TextButton('Recuperar Cuenta', on_click=self.presenter.login_Recuperar, style=ft.ButtonStyle(color='#3EC99D')),], spacing=4), padding=ft.padding.only(550)),
                        ft.Container(self.botonLogin, alignment=ft.alignment.center, padding=ft.padding.only(0,15)),
                        ft.Container(self.label, alignment=ft.alignment.center),
                        ft.Container(self.footer, padding=ft.padding.only(-10,0,0,-75)),
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY), width=1400, height=600),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        )

    # Build del restaurar
    def build_restaurar(self):
        self.restaurar = ft.Container(
            ft.Row([
                ft.Container(
                    ft.Column(controls=[
                        ft.Container(ft.Image(src='assets/logo.png', width=350), alignment=ft.alignment.center),
                        ft.Container(ft.Image(src='assets/logoName.png', width=350), alignment=ft.alignment.center),
                        ft.Container(ft.Text('Recuperar Clave', width=360, size=20, weight='w900', text_align='center',color='#3F4450'), alignment=ft.alignment.center),
                        ft.Container(self.label2, alignment=ft.alignment.center),
                        ft.Container(self.correoElectronico, padding=ft.padding.only(0, 15), alignment=ft.alignment.center),
                        ft.Container(self.botonRecuperar, padding=ft.padding.only(0, 15), alignment=ft.alignment.center),
                        ft.Container(ft.Row([ft.Text('¿Volvemos?', color='#3F4450'),ft.TextButton('Iniciar Sesion', style=ft.ButtonStyle(color='#3EC99D'), on_click=self.presenter.login_Recuperar),], spacing=4), padding=ft.padding.only(610)),
                        ft.Container(self.footer, padding=ft.padding.only(-10, 0, 0, -83)),
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY), width=1400, height=600),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        )

    # Build Mensaje Enviado
    def build_exito(self):
        self.exito = ft.Container(
            ft.Row([
                ft.Container(
                    ft.Column(controls=[
                        ft.Container(ft.Image(src='assets/logo.png', width=350), alignment=ft.alignment.center),
                        ft.Container(ft.Image(src='assets/logoName.png', width=350), alignment=ft.alignment.center),
                        ft.Container(ft.Text('Clave Enviada', width=360, size=25, weight='w900', text_align='center',color='#3F4450'), alignment=ft.alignment.center),
                        ft.Container(ft.Text('Revisa tu correo Electrónico', color='#3F4450'), alignment=ft.alignment.center),
                        ft.Container(ft.ElevatedButton(content=ft.Text('VOLVER', color='white', weight='w400'),on_click=self.presenter.volverLogin, width=250, height=40,bgcolor='#3F4450'), padding=ft.padding.only(0,15),alignment=ft.alignment.center),
                        ft.Container(self.footer, padding=ft.padding.only(-10, 0, 0, -98)),
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY), width=1400, height=600),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        )


    # Actualizar Vista
    def update_view(self):
        self.page.update()

    # Actualizar Contenido
    def set_content(self, content):
        self.ventana.content = content
        self.update_view()
