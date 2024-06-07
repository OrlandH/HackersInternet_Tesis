import re

class Presenter:
    def __init__(self, view):
        self.view = view

    def login_Recuperar(self, e):
        self.view.set_content(self.view.restaurar if self.view.ventana.content == self.view.login else self.view.login)

    def volverLogin(self, e):
        self.view.set_content(self.view.login)

    def claveEnviada(self, e):
        self.view.set_content(self.view.exito)
        self.view.correoElectronico.value = ''
        self.view.passLogin.value = ''
        self.view.update_view()

    def validarCamposLogin(self, e):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        aux = re.match(pattern, self.view.correoElectronico.value) is not None
        if aux:
            self.view.label2.value = ''
            self.view.botonRecuperar.disabled = False
            if self.view.correoElectronico.value == '' or self.view.passLogin.value == '':
                self.view.label.value = 'Llena todos los campos por favor'
                self.view.botonLogin.disabled = True
            else:
                self.view.label.value = ''
                self.view.botonLogin.disabled = False
        else:
            self.view.label2.value = 'Ingresa un correo Válido'
            self.view.botonLogin.disabled = True
            self.view.botonRecuperar.disabled = True

        self.view.update_view()

