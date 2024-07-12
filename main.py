import os
import sys
import timeit
import flet as ft
import re
import psutil
import requests
import webbrowser
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from datetime import datetime
import getpass

usuario_actual = getpass.getuser()
valorNombreAdmin = ""
valorCelAdmin = ""
valCorreoAdmin = ""
urlEndpoint = 'URL DEL BACKEND'

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

imageLogo = resource_path('assets/logo.png')
imageLogoName = resource_path('assets/logoName.png')
def agregar_encabezado(canvas, doc, logo_path, logo_name_path):
    canvas.saveState()
    canvas.drawImage(logo_path, 40, 720, width=1.8 * inch, height=1.5 * inch,mask='auto')
    canvas.drawImage(logo_name_path, 200, 750, width=4 * inch, height=0.5 * inch,mask='auto')
    canvas.line(40, 712, 550, 712)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(150, 695, "Ficha Técnica de Ingreso para Mantenimiento")
    canvas.restoreState()
# Función para crear la tabla de datos
def crear_tabla_de_datos(data):
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    tabla_data = [["Fecha Ingreso:", fecha_actual],["ID", data["id"]],["Marca", data["marca"]],["Modelo", data["modelo"]],["Estado", data["estado"]],["Nombre Cliente", data["nombre Cliente"]],["Observaciones", data["observaciones"]]]
    tabla = Table(tabla_data, colWidths=[150, 300])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    return tabla


# Función para crear el pie de página
def agregar_pie_de_pagina(canvas, doc, telefono):
    canvas.saveState()
    canvas.setFont("Helvetica", 10)
    canvas.drawString(40, 50, "Hackers Internet")
    canvas.setFillColor(colors.blue)
    canvas.drawString(400, 50, f"Tel: {telefono}")
    canvas.restoreState()


# Crear el documento PDF
def crear_ficha_tecnica(nombre_archivo, data, logo_path, logo_name_path, telefono):
    doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
    story = []

    # Agregar encabezado
    story.append(Spacer(1, 1.5 * inch))

    # Agregar tabla de datos
    tabla = crear_tabla_de_datos(data)
    story.append(tabla)

    # Crear PDF
    doc.build(story,
              onFirstPage=lambda canvas, doc: agregar_encabezado(canvas, doc, logo_path, logo_name_path),
              onLaterPages=lambda canvas, doc: agregar_pie_de_pagina(canvas, doc, telefono))
def main(page: ft.page):
    page.update()
    # Funciones para el inicio de sesión
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
        label2.value= ''
        ventana.update()

    def login_admin(e):
        url = f"{urlEndpoint}/admin/login"
        headers = {'Content-Type': 'application/json'}
        data = {
            "correo": correoElectronico.value,
            "password": passLogin.value
        }

        try:
            print(f"FUNCION [login]\n--------------------------------------------")

            start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
            cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud

            response = requests.post(url, json=data, headers=headers)



            # Verificar si la solicitud tuvo éxito
            if response.status_code == 200:
                response_data = response.json()
                # Realizar la acción con la información de la respuesta
                nombreAdminText.value = response_data.get("nombre")
                celularAdminText.value = response_data.get("telefono")
                correoAdminText.value = response_data.get("correo")
                page.client_storage.set("nombre", response_data.get("nombre"))
                page.client_storage.set("correo", response_data.get("correo"))
                page.client_storage.set("telefono", response_data.get("telefono"))
                inicioExitoso()

            else:
                label.value = "Credenciales Incorrectas"
                passLogin.value = ''
                page.update()

            end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
            cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
            execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
            # Mostrar resultados de rendimiento
            print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
            print(f"Uso de CPU antes: {cpu_usage_before}%")
            print(f"Uso de CPU después: {cpu_usage_after}%")

        except requests.exceptions.RequestException as e:
            label.value = "Error con el servidor"
            passLogin.value = ''
            page.update()
    def recuperar_admin(e):
        url = f"{urlEndpoint}/admin/recuperar-password"
        headers = {'Content-Type': 'application/json'}
        data = {"correo": correoElectronico.value,}
        try:
            response = requests.post(url, json=data, headers=headers)
            # Verificar si la solicitud tuvo éxito
            if response.status_code == 200:
                claveEnviada(e=None)
            else:
                label2.value = "Correo Incorrecto"
                correoElectronico.value = ''
                page.update()
        except requests.exceptions.RequestException as e:
            label2.value="Error con el servidor"
            correoElectronico.value = ''
            page.update()
    def inicioExitoso():
        label.value=''
        correoElectronico.value = ''
        passLogin.value = ''
        ventana.content = inicio
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


    # Parametros necesarios pal Login:
    label = ft.Text('', width=360, size=10, weight='w900', text_align='center', color=ft.colors.RED)
    label2 = ft.Text('', width=360, size=10, weight='w900', text_align='center', color=ft.colors.RED)

    correoElectronico = ft.TextField(width=340, height=40, label="Correo Electronico", border_color='#3F4450',
                                     border_radius=20, color='#3F4450', label_style=ft.TextStyle(color='#3F4450'),
                                     keyboard_type=ft.KeyboardType.EMAIL, on_change=validarCamposLogin,
                                     on_focus=validarCamposLogin)

    passLogin = ft.TextField(width=340, height=40, label="Contraseña", password=True, can_reveal_password=True,
                             border_color='#3F4450', border_radius=20, color='#3F4450',
                             label_style=ft.TextStyle(color='#3F4450'), on_change=validarCamposLogin,
                             on_focus=validarCamposLogin)

    botonLogin = ft.ElevatedButton(content=ft.Text('Iniciar Sesión', color='white', weight='w400', ), width=250,
                                   height=35, bgcolor='#3F4450', on_click=login_admin)
    botonRecuperar = ft.ElevatedButton(content=ft.Text('Enviar Clave', color='white', weight='w400', ), width=250,
                                       height=35, bgcolor='#3F4450', on_click=recuperar_admin)



    login = ft.Container(
        ft.Row([
            ft.Container(
                ft.Column(controls=[
                    # Contenedor con el logo
                    ft.Container(
                        ft.Image(src=imageLogo, width=350, ),
                        padding=ft.padding.only(180, 1)
                    ),
                    ft.Container(
                        ft.Image(src=imageLogoName, width=350, ),
                        padding=ft.padding.only(180, -10)
                    ),
                    # Texto Bienvenida
                    ft.Container(
                        ft.Text('Bienvenido', width=360, size=20, weight='w900', text_align='center', color='#3F4450'),
                        padding=ft.padding.only(170, -18)
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
                        ft.Image(src=imageLogo, width=350, ),
                        padding=ft.padding.only(180, 1)
                    ),
                    ft.Container(
                        ft.Image(src=imageLogoName, width=350, ),
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
                        ft.Image(src=imageLogo, width=350, ),
                        padding=ft.padding.only(180, 1)
                    ),
                    ft.Container(
                        ft.Image(src=imageLogoName, width=350, ),
                        padding=ft.padding.only(180, -10)
                    ),
                    # Texto Bienvenida
                    ft.Container(
                        ft.Text('Clave Temporal Enviada', width=360, size=25, weight='w900', text_align='center',
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




# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



    # Funcion para cambiar los TABS
    def changetab(e):
        # GET INDEX TAB
        my_index = e.control.selected_index
        homeTab.visible = True if my_index == 0 else False
        clienteTab.visible = True if my_index == 1 else False
        historialTab.visible = True if my_index == 2 else False
        perfilTab.visible = True if my_index == 3 else False
        page.update()

    # Funcion para que cambie en los hover el color
    def on_hover(e):
        e.control.bgcolor = "#3EC99D" if e.data == "true" else "#3F4450"
        e.control.update()

    def handle_ClickEditar_Historial(e):
        close_bs(e)
        equipo = page.client_storage.get("equipoCache")
        show_bsHistorial(e, equipo)
    # Funcion para que el formulario de editar se abra con la información actual, y abajo para cerrar
    def show_bs(e, equipo):
        try:
            print(f"FUNCION [Ver equipo]\n--------------------------------------------")
            start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
            cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud
            nombreEquipoEdit.value = equipo['modelo']
            id_EquipoEdit.value = equipo['id']
            estadoEquipoEdit.value = equipo['estado']
            equipoMarcaEdit.value = equipo['marca']
            nombreClienteEdit.value = equipo['nombre_cliente']
            observacionActualEdit.value = equipo['observaciones']
            page.client_storage.set("equipoCache", equipo)

            url = f"{urlEndpoint}/clientes"
            try:

                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                for cliente in data:
                    if cliente['nombre'] == equipo['nombre_cliente']:
                        cliente_id = cliente['id']
                        url2 = f"{urlEndpoint}/cliente/{cliente_id}"
                        try:

                            response = requests.get(url2)
                            response.raise_for_status()
                            data2 = response.json()
                            celularClienteEdit.value = data2['telefono']

                        except requests.exceptions.RequestException as e:
                            print("Error al Obtener Celular del Cliente")
                        break
                    else:
                        celularClienteEdit.value = ""

                end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
                cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
                execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
                # Mostrar resultados de rendimiento
                print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
                print(f"Uso de CPU antes: {cpu_usage_before}%")
                print(f"Uso de CPU después: {cpu_usage_after}%")
            except requests.exceptions.RequestException as e:
                print("Error al Obtener datos")
        except Exception as e:
            print(f"Error en función show_bs: {e}")

        editarVer_Equipo.open = True
        editarVer_Equipo.update()

    def close_bs(e):
        editarVer_Equipo.open = False
        editarVer_Equipo.update()

    # Funcion para que el formulario de agregar se abra con la información actual, y abajo para cerrar
    def show_agEq(e):
        agregar_Equipo.open = True
        agregar_Equipo.update()

    # Funcion para abrir y cerrar el cuadro de dialogo de Confirmar
    def open_dlg_modal(e, equipo):
        id_Equipo = equipo['id']
        page.dialog = dlg_modal(id_Equipo)
        page.dialog.open = True
        page.update()
    def close_dlg(e):
        page.dialog.open = False
        page.update()

    # Funcion para abrir y cerrar el cuadro de dialogo de Confirmar para cerrar sesion
    def open_cerrarSesion_modal(e):
        page.dialog = sesion_modal
        sesion_modal.open = True
        page.update()
    def close_cerrarSesion_modal(e):
        sesion_modal.open = False
        page.update()

    # Funcion para abrir y cerrar el cuadro de dialogo de Confirmar para cerrar sesion
    def open_ErrorModal(e):
        page.dialog = ERROR_Modal
        ERROR_Modal.open = True
        page.update()
    def close_ErrorModal(e):
        ERROR_Modal.open = False
        page.update()

    def cerrarSesion(e):
        ventana.content = login
        sesion_modal.open = False
        ventana.update()
        page.update()


    # Funcion para habilitar la edición de formulario
    def editarFormulario(e):
        nombreEquipoEdit.read_only = False
        nombreEquipoEdit.update()
        nuevaObservacion.disabled = False
        nuevaObservacion.update()
        nuevoEstado.disabled = False
        nuevoEstado.update()
        equipoMarcaEdit.read_only = False
        equipoMarcaEdit.update()
        nombreClienteEdit.read_only = False
        nombreClienteEdit.update()
        cerrarFormularioButton.disabled = True
        cerrarFormularioButton.update()
        notificarClienteButton.disabled = True
        notificarClienteButton.update()
        actualizarInfoButton.disabled = False
        actualizarInfoButton.update()
        cancelarEditButton.disabled = False
        cancelarEditButton.update()
        editarButton.disabled = True
        editarButton.update()

    # Funcion para cancelar la edicion de formulario
    def cancelarEditFormulario(e):
        nombreEquipoEdit.read_only = True
        nombreEquipoEdit.update()
        nuevaObservacion.clean()
        nuevaObservacion.value = ""
        nuevaObservacion.disabled = True
        nuevaObservacion.update()
        nuevoEstado.clean()
        nuevoEstado.value = ""
        nuevoEstado.disabled = True
        nuevoEstado.update()
        equipoMarcaEdit.read_only = True
        equipoMarcaEdit.update()
        nombreClienteEdit.read_only = True
        nombreClienteEdit.update()
        cerrarFormularioButton.disabled = False
        cerrarFormularioButton.update()
        notificarClienteButton.disabled = False
        notificarClienteButton.update()
        actualizarInfoButton.disabled = True
        actualizarInfoButton.update()
        cancelarEditButton.disabled = True
        cancelarEditButton.update()
        editarButton.disabled = False
        editarButton.update()

    # Crear tarjetas de informacion de los clientes listos
    def leerClientesListo():
        url = f"{urlEndpoint}/equipos"
        try:
            print(f"FUNCION [leerClientesListo]\n--------------------------------------------")

            start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
            cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()



            equipos_Listos = []
            for i in data:
                estadoJson = i['estado']
                estadoListoEquipoLabel = ft.Text("En estado: ", color='#3F4450', size=17, weight='w400', spans=[
                    ft.TextSpan(estadoJson, ft.TextStyle(color='#3EC99D', weight='w500'))])
                nombreClienteEquipoLabel = ft.Text(i['nombre_cliente'], color='#3F4450', size=17, weight='w400')
                nombreEquipoLabel = ft.Text(f"{i['marca']} {i['modelo']}", color='#3F4450', size=19, weight='w500')
                observaciones = ft.Text("Observaciones:", color='#3EC99D', size=17, weight='w400', spans=[
                    ft.TextSpan(i['observaciones'], ft.TextStyle(color='#3F4450', weight='w400'))])
                if estadoJson.lower() == 'listo' and estadoJson.lower() != 'entregado':
                    equipos_Listos.append(ft.Container(ft.Container(ft.Column([
                        ft.Row([nombreEquipoLabel,
                                ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED, icon_color="#3EC99D", icon_size=30,
                                              tooltip="Borrar Equipo",
                                              on_click=lambda e, equipo=i: open_dlg_modal(e, equipo), ), ],
                               alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([ft.Container(estadoListoEquipoLabel, padding=ft.padding.only(0, -20)), ft.Container(
                            ft.ElevatedButton(content=ft.Text('Ver/Editar', color='white', weight='w100', ),
                                              bgcolor='#3F4450', on_hover=on_hover,
                                              on_click=lambda e, equipo=i: show_bs(e, equipo)))],
                               alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(nombreClienteEquipoLabel, padding=ft.padding.only(0, -15)),
                        observaciones, ], spacing=0), width=560),
                        border=ft.border.all(0.5, color='#8993A7'), width=665, border_radius=3,
                        padding=ft.padding.only(25, 7, 20, 7))
                    )

            end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
            cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
            execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
            # Mostrar resultados de rendimiento
            print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
            print(f"Uso de CPU antes: {cpu_usage_before}%")
            print(f"Uso de CPU después: {cpu_usage_after}%")

            return equipos_Listos

        except requests.exceptions.RequestException as e:
            print("Error al Obtener datos")
            return []

    # Crear tarjetas de información de los clientes pendientes
    def leerClientesPendiente():
        url = f"{urlEndpoint}/equipos"
        try:
            print(f"FUNCION [leerClientesPendiente]\n--------------------------------------------")

            start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
            cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()



            equipos_pendientes = []
            for i in data:
                estadoJson = i['estado']
                estadoEquipoLabel = ft.Text("En estado: ", color='#3F4450', size=17, weight='w400', spans=[
                    ft.TextSpan(estadoJson, ft.TextStyle(color='#FF914D', weight='w500'))])
                nombreClienteEquipoLabel = ft.Text(i['nombre_cliente'], color='#3F4450', size=17, weight='w400')
                nombreEquipoLabel = ft.Text(f"{i['marca']} {i['modelo']}", color='#3F4450', size=19, weight='w500')
                observaciones = ft.Text("Observaciones:", color='#3EC99D', size=17, weight='w400', spans=[
                    ft.TextSpan(i['observaciones'], ft.TextStyle(color='#3F4450', weight='w400'))])
                if estadoJson.lower() != 'listo' and estadoJson.lower() != 'entregado':
                    equipos_pendientes.append(
                        ft.Container(
                            ft.Container(ft.Column([ft.Row([nombreEquipoLabel,
                                                            ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED,
                                                                          icon_color="#3EC99D", icon_size=30,
                                                                          tooltip="Borrar Equipo",
                                                                          on_click=lambda e, equipo=i: open_dlg_modal(e,
                                                                                                                      equipo)), ],
                                                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                    ft.Row(
                                                        [ft.Container(estadoEquipoLabel,
                                                                      padding=ft.padding.only(0, -20)),
                                                         ft.Container(ft.ElevatedButton(
                                                             content=ft.Text('Ver/Editar', color='white',
                                                                             weight='w100', ),
                                                             bgcolor='#3F4450', on_hover=on_hover,
                                                             on_click=lambda e, equipo=i: show_bs(e, equipo)))],
                                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                    ft.Container(nombreClienteEquipoLabel,
                                                                 padding=ft.padding.only(0, -15)),
                                                    observaciones
                                                    ], spacing=0), width=560),
                            border=ft.border.all(0.5, color='#8993A7'),
                            width=665, border_radius=3, padding=ft.padding.only(25, 7, 20, 7)
                        )
                    )
            end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
            cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
            execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
            # Mostrar resultados de rendimiento
            print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
            print(f"Uso de CPU antes: {cpu_usage_before}%")
            print(f"Uso de CPU después: {cpu_usage_after}%")

            return equipos_pendientes

        except requests.exceptions.RequestException as e:
            print("Error al Obtener datos")
            return []

    # Funciones Globales ------------------------------------------------------------------------------------------------------------------------


    def handle_ClickBusquedaEstado(e, equipo):
        close_busqueda(e)
        show_bs(e, equipo)
    def handle_ClickBusquedaEstadoCliente(e, cliente):
        close_busqueda(e)
        show_bsCliente(e, cliente)
    def close_busqueda(e):
        ver_ResultadoBusqueda.open = False
        ver_ResultadoBusqueda.update()

    def show_Busqueda(e, campo):
        print(f"FUNCION [BUSQUEDA]\n--------------------------------------------")
        start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
        cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud
        busquedaText.value = ''
        busquedaText.update()
        header.update()
        page.update()
        if campo.lower() in ['en espera', 'en mantenimiento', 'listo', 'ingresado', 'entregado']:
            contenedorResultadoBusqueda.controls.clear()
            contenedorResultadoBusqueda.controls.extend(buscarEstado(e, campo))
            contenedorResultadoBusqueda.update()
        else:
            resultados = []
            urlModelo = f"{urlEndpoint}/equipos/modelo/{campo}"
            try:
                response = requests.get(urlModelo)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.RequestException as ex:
                data = "Error al Obtener datos"
            if isinstance(data, list) and data:
                for i in data:
                    nombre = buscarNombre(e, i['id_cliente'])
                    i["nombre_cliente"] = nombre
                    nombreClienteEquipoLabel = ft.Text(i["nombre_cliente"], color=ft.colors.WHITE, size=17,weight='w400')
                    estadoJson = i['estado']
                    if estadoJson.lower() == 'listo':
                        estadoEquipoLabel = ft.Text("En estado: ", color=ft.colors.WHITE, size=17, weight='w400',spans=[ft.TextSpan(estadoJson,ft.TextStyle(color='#3EC99D', weight='w500'))])
                    else:
                        estadoEquipoLabel = ft.Text("En estado: ", color=ft.colors.WHITE, size=17, weight='w400',spans=[ft.TextSpan(estadoJson,ft.TextStyle(color='#FF914D', weight='w500'))])
                    nombreEquipoLabel = ft.Text(f"{i['marca']} {i['modelo']}", color=ft.colors.WHITE, size=19,weight='w500')
                    observaciones = ft.Text("Observaciones:", color='#3EC99D', size=17, weight='w400', spans=[ft.TextSpan(i['observaciones'], ft.TextStyle(color=ft.colors.WHITE, weight='w400'))])
                    resultados.append(
                        ft.Container(
                            ft.Container(ft.Column([ft.Row([nombreEquipoLabel],
                                                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                    ft.Container(nombreClienteEquipoLabel, padding=ft.padding.only(0)),
                                                    ft.Row(
                                                        [ft.Container(estadoEquipoLabel,
                                                                      padding=ft.padding.only(0, -20)),
                                                         ft.Container(ft.ElevatedButton(
                                                             content=ft.Text('Ver/Editar', color='white',
                                                                             weight='w100', ),
                                                             bgcolor='#3F4450', on_hover=on_hover,
                                                             on_click=lambda e, equipo=i: handle_ClickBusquedaEstado(e,
                                                                                                                     equipo)))],
                                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                    ft.Container(observaciones, padding=ft.padding.only(0, -12)),
                                                    ], spacing=0), width=560),
                            border=ft.border.all(0.5, color='#8993A7'),
                            width=665, border_radius=3, padding=ft.padding.only(25, 7, 20, 7)
                        )
                    )

            urlMarca = f"{urlEndpoint}/equipos/marca/{campo}"
            try:
                response = requests.get(urlMarca)
                response.raise_for_status()
                data = response.json()

            except requests.exceptions.RequestException as ex:
                data = "Error al Obtener datos"


            if isinstance(data, list) and data:
                for i in data:
                    nombre = buscarNombre(e, i['id_cliente'])
                    i["nombre_cliente"] = nombre
                    nombreClienteEquipoLabel = ft.Text(i["nombre_cliente"], color=ft.colors.WHITE, size=17,
                                                       weight='w400')
                    estadoJson = i['estado']
                    if estadoJson.lower() == 'listo':
                        estadoEquipoLabel = ft.Text("En estado: ", color=ft.colors.WHITE, size=17, weight='w400',
                                                    spans=[
                                                        ft.TextSpan(estadoJson,
                                                                    ft.TextStyle(color='#3EC99D', weight='w500'))])
                    else:
                        estadoEquipoLabel = ft.Text("En estado: ", color=ft.colors.WHITE, size=17, weight='w400',
                                                    spans=[
                                                        ft.TextSpan(estadoJson,
                                                                    ft.TextStyle(color='#FF914D', weight='w500'))])

                    nombreEquipoLabel = ft.Text(f"{i['marca']} {i['modelo']}", color=ft.colors.WHITE, size=19,
                                                weight='w500')
                    observaciones = ft.Text("Observaciones:", color='#3EC99D', size=17, weight='w400', spans=[
                        ft.TextSpan(i['observaciones'], ft.TextStyle(color=ft.colors.WHITE, weight='w400'))])

                    resultados.append(
                        ft.Container(
                            ft.Container(ft.Column([ft.Row([nombreEquipoLabel],
                                                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                    ft.Container(nombreClienteEquipoLabel, padding=ft.padding.only(0)),
                                                    ft.Row(
                                                        [ft.Container(estadoEquipoLabel,
                                                                      padding=ft.padding.only(0, -20)),
                                                         ft.Container(ft.ElevatedButton(
                                                             content=ft.Text('Ver/Editar', color='white',
                                                                             weight='w100', ),
                                                             bgcolor='#3F4450', on_hover=on_hover,
                                                             on_click=lambda e, equipo=i: handle_ClickBusquedaEstado(e,
                                                                                                                     equipo)))],
                                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                    ft.Container(observaciones, padding=ft.padding.only(0, -12)),
                                                    ], spacing=0), width=560),
                            border=ft.border.all(0.5, color='#8993A7'),
                            width=665, border_radius=3, padding=ft.padding.only(25, 7, 20, 7)
                        )
                    )

            urlNombre = f"{urlEndpoint}/clientes"
            try:
                response = requests.get(urlNombre)
                response.raise_for_status()
                data = response.json()

            except requests.exceptions.RequestException as ex:
                data = "Error al Obtener datos"

            for i in data:
                if i['nombre'].lower() == campo.lower():
                    nombreClienteEquipoLabel = ft.Text(i['nombre'], color=ft.colors.WHITE, size=19, weight='w500')
                    celularClienteEquipoLabel = ft.Text(i['telefono'], color=ft.colors.WHITE, size=17, weight='w400')
                    emailClienteEquipoLabel = ft.Text(i['correo'], color=ft.colors.WHITE, size=17, weight='w400')
                    resultados.append(
                        ft.Container(
                            ft.Container(ft.Column([ft.Row([nombreClienteEquipoLabel],
                                                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                    ft.Row([ft.Container(celularClienteEquipoLabel,
                                                                         padding=ft.padding.only(0)), ft.Container(
                                                        ft.ElevatedButton(
                                                            content=ft.Text('Ver/Editar', color='white',
                                                                            weight='w100', ),
                                                            bgcolor='#3F4450', on_hover=on_hover,
                                                            on_click=lambda e,
                                                                            cliente=i: handle_ClickBusquedaEstadoCliente(
                                                                e, cliente)))],
                                                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                    ft.Container(emailClienteEquipoLabel, padding=ft.padding.only(0))
                                                    ], spacing=0), width=560),
                            border=ft.border.all(0.5, color='#8993A7'),
                            width=665, border_radius=3, padding=ft.padding.only(25, 7, 20, 7)
                        )
                    )

                    urlPorNombre = f"{urlEndpoint}/equipos/cliente/{i['id']}"
                    try:
                        response = requests.get(urlPorNombre)
                        response.raise_for_status()
                        data = response.json()

                    except requests.exceptions.RequestException as ex:
                        data = "Error al Obtener datos"


                    if isinstance(data, list) and data:
                        for d in data:
                            nombre = buscarNombre(e, d['id_cliente'])
                            d["nombre_cliente"] = nombre
                            nombreClienteEquipoLabel = ft.Text(d["nombre_cliente"], color=ft.colors.WHITE, size=17,
                                                               weight='w400')
                            estadoJson = d['estado']
                            if estadoJson.lower() == 'listo':
                                estadoEquipoLabel = ft.Text("En estado: ", color=ft.colors.WHITE, size=17,
                                                            weight='w400', spans=[
                                        ft.TextSpan(estadoJson, ft.TextStyle(color='#3EC99D', weight='w500'))])
                            else:
                                estadoEquipoLabel = ft.Text("En estado: ", color=ft.colors.WHITE, size=17,
                                                            weight='w400', spans=[
                                        ft.TextSpan(estadoJson, ft.TextStyle(color='#FF914D', weight='w500'))])

                            nombreEquipoLabel = ft.Text(f"{d['marca']} {d['modelo']}", color=ft.colors.WHITE, size=19,
                                                        weight='w500')
                            observaciones = ft.Text("Observaciones:", color='#3EC99D', size=17, weight='w400', spans=[
                                ft.TextSpan(d['observaciones'], ft.TextStyle(color=ft.colors.WHITE, weight='w400'))])

                            resultados.append(
                                ft.Container(
                                    ft.Container(ft.Column([ft.Row([nombreEquipoLabel],
                                                                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                            ft.Container(nombreClienteEquipoLabel,
                                                                         padding=ft.padding.only(0)),
                                                            ft.Row(
                                                                [ft.Container(estadoEquipoLabel,
                                                                              padding=ft.padding.only(0, -20)),
                                                                 ft.Container(ft.ElevatedButton(
                                                                     content=ft.Text('Ver/Editar', color='white',
                                                                                     weight='w100', ),
                                                                     bgcolor='#3F4450', on_hover=on_hover,
                                                                     on_click=lambda e,
                                                                                     equipo=d: handle_ClickBusquedaEstado(
                                                                         e, equipo)))],
                                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                            ft.Container(observaciones,
                                                                         padding=ft.padding.only(0, -12)),
                                                            ], spacing=0), width=560), border=ft.border.all(0.5,
                                                                                                            color='#8993A7'),
                                    width=665, border_radius=3, padding=ft.padding.only(25, 7, 20, 7)
                                )
                            )
            resultados.append(
                ft.Container(
                    ft.Container(ft.Column([ft.Text('SIN MÁS RESULTADOS')], spacing=0), width=560),
                    border=ft.border.all(0.5, color='#8993A7'),
                    width=665, border_radius=3, padding=ft.padding.only(25, 7, 20, 7)
                )
            )

            contenedorResultadoBusqueda.controls.clear()
            contenedorResultadoBusqueda.controls.extend(resultados)
            contenedorResultadoBusqueda.update()
            page.update()

        ver_ResultadoBusqueda.open = True
        ver_ResultadoBusqueda.update()
        end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
        cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
        execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Uso de CPU antes: {cpu_usage_before}%")
        print(f"Uso de CPU después: {cpu_usage_after}%")

    def buscarNombre(e, id):

        url = f"{urlEndpoint}/cliente/{id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            nombre = data['nombre']
        except requests.exceptions.RequestException as e:
            data = "Error al Obtener el Nombre"
            nombre = "No encontrado"
            print("ERROR Obteniendo el Nombre")
        return nombre

    def buscarEstado(e, campo):
        url = f"{urlEndpoint}/equipos/estado/{campo}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(f"Código de estado: {response.status_code}")
        except requests.exceptions.RequestException as e:
            data = "Error al Obtener datos"
            print("ERROR Obteniendo equipos")
        equipos_encontrado = []
        for i in data:
            nombre = buscarNombre(e, i['id_cliente'])
            i["nombre_cliente"] = nombre
            nombreClienteEquipoLabel = ft.Text(i["nombre_cliente"], color=ft.colors.WHITE, size=17, weight='w400')
            estadoJson = i['estado']
            if estadoJson.lower() == 'listo':
                estadoEquipoLabel = ft.Text("En estado: ", color=ft.colors.WHITE, size=17, weight='w400', spans=[
                    ft.TextSpan(estadoJson, ft.TextStyle(color='#3EC99D', weight='w500'))])
            else:
                estadoEquipoLabel = ft.Text("En estado: ", color=ft.colors.WHITE, size=17, weight='w400',spans=[ft.TextSpan(estadoJson, ft.TextStyle(color='#FF914D', weight='w500'))])

            nombreEquipoLabel = ft.Text(f"{i['marca']} {i['modelo']}", color=ft.colors.WHITE, size=19, weight='w500')
            observaciones = ft.Text("Observaciones:", color='#3EC99D', size=17, weight='w400',spans=[ft.TextSpan(i['observaciones'], ft.TextStyle(color=ft.colors.WHITE, weight='w400'))])

            equipos_encontrado.append(
                ft.Container(
                    ft.Container(ft.Column([ft.Row([nombreEquipoLabel],
                                                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                            ft.Container(nombreClienteEquipoLabel, padding=ft.padding.only(0)),
                                            ft.Row(
                                                [ft.Container(estadoEquipoLabel, padding=ft.padding.only(0, -20)),
                                                 ft.Container(ft.ElevatedButton(
                                                     content=ft.Text('Ver/Editar', color='white', weight='w100', ),
                                                     bgcolor='#3F4450', on_hover=on_hover,
                                                     on_click=lambda e, equipo=i: handle_ClickBusquedaEstado(e, equipo)))],
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                            ft.Container(observaciones, padding=ft.padding.only(0,-12)),
                                            ], spacing=0), width=560), border=ft.border.all(0.5, color='#8993A7'),
                    width=665, border_radius=3, padding=ft.padding.only(25, 7, 20, 7)
                )
            )
        return equipos_encontrado

    # Tabs de navegación
    page.navigation_bar = ft.NavigationBar(bgcolor="#3F4450",height=65,indicator_color=ft.colors.TRANSPARENT,overlay_color='#3EC99D',indicator_shape=ft.ContinuousRectangleBorder(radius=20),on_change=changetab,selected_index=0,
        destinations=[
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.HOME, size=35), selected_icon_content=ft.Icon(name=ft.icons.HOME, color='#3EC99D', size=45)),
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.PEOPLE, size=35), selected_icon_content=ft.Icon(name=ft.icons.PEOPLE, color='#3EC99D', size=45)),
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.NOTE_OUTLINED, size=35), selected_icon_content=ft.Icon(name=ft.icons.NOTE_ROUNDED, color='#3EC99D', size=45)),
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.PERSON_PIN, size=35), selected_icon_content=ft.Icon(name=ft.icons.PERSON_PIN_SHARP, color='#3EC99D', size=45)),
        ],)

    # Barra de busqueda general
    botonBusqueda = ft.IconButton(icon=ft.icons.SEARCH,icon_size=30, icon_color="#3EC99D",on_click=lambda e: show_Busqueda(e, busquedaText.value))
    busquedaText = ft.TextField(width=470, height=42, label="Buscar", color='#3F4450',border_color='#3F4450',border_radius=20,label_style=ft.TextStyle(color='#3F4450'), focused_border_color='#3EC99D')

    contenedorResultadoBusqueda = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=580)
    ver_ResultadoBusqueda = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    # Contenido del formulario antes de los botones
                    ft.Container(ft.Text("Resultado  ", size=35, spans=[ft.TextSpan("Busqueda", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center, padding=ft.padding.only(0,25)),
                    ft.Container(contenedorResultadoBusqueda),
                ],tight=True, spacing=8
            ),padding=20, height=900, width=700,
        ),open=False, is_scroll_controlled=True, #dismissible=False
    )

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def eliminarEquipo(e, id_Equipo):
        print(f"FUNCION [Eliminar Equipo]\n--------------------------------------------")
        start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
        cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud
        url = f"{urlEndpoint}/equipo/{id_Equipo}"
        try:
            response = requests.delete(url)
            response.raise_for_status()
            contenedorEquiposListos.controls.clear()
            contenedorEquiposListos.controls.extend(leerClientesListo())
            contenedorEquiposListos.update()
            contenedorEquiposPendientes.controls.clear()
            contenedorEquiposPendientes.controls.extend(leerClientesPendiente())
            contenedorEquiposPendientes.update()
        except requests.exceptions.RequestException as err:
            print(f"Error al eliminar el equipo con ID {id_Equipo}: {err}")

        close_dlg(e)

        end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
        cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
        execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Uso de CPU antes: {cpu_usage_before}%")
        print(f"Uso de CPU después: {cpu_usage_after}%")

    # Pestaña para confirmar borrado
    def dlg_modal(id_Equipo):
        return ft.AlertDialog(
            modal=True,
            bgcolor='#3F4450',
            title=ft.Text("Confirmar"),
            content=ft.Text("¿Estás seguro de eliminar este equipo?"),
            actions=[
                ft.TextButton("Sí", on_click=lambda e: eliminarEquipo(e, id_Equipo)),
                ft.TextButton("No", on_click=close_dlg)
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

    # Pestaña para confirmar borrado
    sesion_modal = ft.AlertDialog(
        modal=True,
        bgcolor='#3F4450',
        title=ft.Text("Cerrar Sesión"),
        content=ft.Text("¿Estas seguro de Cerrar Sesion?"),
        actions=[ft.TextButton("Si", on_click=cerrarSesion),ft.TextButton("No", on_click=close_cerrarSesion_modal),],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    # Pestaña para errores
    ERROR_Modal = ft.AlertDialog(
        modal=True,
        bgcolor='#3F4450',
        title=ft.Text("ERROR"),
        content=ft.Text("Valide los campos correctamente, y verifique existencias"),
        actions=[ft.TextButton("Ok", on_click=close_ErrorModal)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    # Funcion para abrir y cerrar el cuadro de dialogo de Confirmar para cerrar sesion
    def open_ExitoModal():
        page.dialog = EXITO_Modal
        EXITO_Modal.open = True
        page.update()
    def close_ExitoModal(e):
        nombreNuevoEquipo.value = ""
        marcaNuevoEquipo.value = ""
        nombreClienteNuevoEquipo.value = ""
        estadoNuevoEquipo.value = ""
        observacionNuevoEquipo.value = ""
        agregar_Equipo.update()
        contenedorEquiposListos.controls.clear()
        contenedorEquiposListos.controls.extend(leerClientesListo())
        contenedorEquiposListos.update()
        contenedorEquiposPendientes.controls.clear()
        contenedorEquiposPendientes.controls.extend(leerClientesPendiente())
        contenedorEquiposPendientes.update()
        homeTab.update()
        inicio.update()
        EXITO_Modal.open = False
        page.update()

    # Pestaña para proceso exitoso
    EXITO_Modal = ft.AlertDialog(
        modal=True,
        bgcolor='#3F4450',
        title=ft.Text("Listo!"),
        content=ft.Text("El proceso se realizo correctamente"),
        actions=[ft.TextButton("Ok", on_click=close_ExitoModal)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    def open_ExitoModalEdit():
        page.dialog = EXITO_Edit_Modal
        EXITO_Edit_Modal.open = True
        page.update()
    def close_ExitoModalEdit(e):
        cancelarEditFormulario(e)
        contenedorEquiposListos.controls.clear()
        contenedorEquiposListos.controls.extend(leerClientesListo())
        contenedorEquiposListos.update()
        contenedorEquiposPendientes.controls.clear()
        contenedorEquiposPendientes.controls.extend(leerClientesPendiente())
        contenedorEquiposPendientes.update()
        homeTab.update()
        inicio.update()
        EXITO_Edit_Modal.open = False
        close_bs(e)
        page.update()

    # Pestaña para proceso exitoso
    EXITO_Edit_Modal = ft.AlertDialog(
        modal=True,
        bgcolor='#3F4450',
        title=ft.Text("Listo!"),
        content=ft.Text("El proceso se realizo correctamente"),
        actions=[ft.TextButton("Ok", on_click=close_ExitoModalEdit)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    def open_NotificarExito(e):
        page.dialog = EXITO_Notificar
        EXITO_Notificar.open = True
        page.update()
    def close_NotificarExito(e):
        EXITO_Notificar.open = False
        page.update()

    # Pestaña para proceso exitoso
    EXITO_Notificar = ft.AlertDialog(
        modal=True,
        bgcolor='#3F4450',
        title=ft.Text("Listo!"),
        content=ft.Text("Se envió la notificación correctamente"),
        actions=[ft.TextButton("Ok", on_click=close_NotificarExito)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    def open_NotificarFallo(e):
        page.dialog = ERROR_Notificar
        ERROR_Notificar.open = True
        page.update()
    def close_NotificarFallo(e):
        ERROR_Notificar.open = False
        page.update()

    # Pestaña para proceso exitoso
    ERROR_Notificar = ft.AlertDialog(
        modal=True,
        bgcolor='#3F4450',
        title=ft.Text("ERROR"),
        content=ft.Text("No se pudo enviar la notificación, intenta de Nuevo"),
        actions=[ft.TextButton("Ok", on_click=close_NotificarFallo)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    def notificarEquipo(e, id_Equipo):
        print(f"FUNCION [Notificar Equipo]\n--------------------------------------------")
        start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
        cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud
        url = f"{urlEndpoint}/equipos/{id_Equipo}/notificar"
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                open_NotificarExito(e)
            else:
                open_NotificarFallo(e)
        except requests.exceptions.RequestException as e:
            open_NotificarFallo(e)
        end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
        cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
        execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Uso de CPU antes: {cpu_usage_before}%")
        print(f"Uso de CPU después: {cpu_usage_after}%")
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Header Principal
    header = ft.Row([
        ft.Container(ft.Row([ft.Container(ft.Image(src=imageLogo, width=100), padding=ft.padding.only(10, 5)), ft.Container(ft.Image(src=imageLogoName, width=245), padding=ft.padding.only(15, 15))])),
        ft.Container(ft.Row([busquedaText,botonBusqueda,ft.Container(ft.IconButton(icon=ft.icons.EXIT_TO_APP, icon_color='#3EC99D', icon_size=45,tooltip="Cerrar Sesión", padding=ft.padding.only(60, 0, 20), on_click=open_cerrarSesion_modal))])
        )], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


    # Formulario de Editar Variables Necesarias----------------------------------------------------------------------------------------------------------
    id_EquipoEdit = ft.TextField(value="", read_only=True, border="none", text_size=25)
    nombreEquipoEdit = ft.TextField(label="Nombre de equipo", value="", read_only=True)
    equipoMarcaEdit = ft.TextField(label="Marca", value="", read_only=True)
    estadoEquipoEdit = ft.TextField(value="", read_only=True, border="none", text_size=18)
    nombreClienteEdit = ft.TextField(label="Nombre Cliente", value="", width=290, read_only=True)
    celularClienteEdit = ft.TextField(label="Celular Cliente", value="", width=165, read_only=True)
    observacionActualEdit = ft.TextField(value="", read_only=True, border="none", text_size=16, max_lines=3)

    # Botones Formulario Editar
    editarButton = ft.ElevatedButton(content=ft.Text('Editar Información', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, on_click=editarFormulario)
    cerrarFormularioButton = ft.ElevatedButton(content=ft.Text('Cerrar Formulario', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, on_click=close_bs)
    notificarClienteButton = ft.ElevatedButton(content=ft.Text('Notificar Cliente', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, tooltip="Enviar notificacion con estado actual a cliente", on_click=lambda e: notificarEquipo(e, id_EquipoEdit.value))


    def validarClienteEditar(e):
        if nuevoEstado.value == '':
            nuevoEstado.value = estadoEquipoEdit.value
            nuevoEstado.update()
        if nuevaObservacion.value == '':
            nuevaObservacion.value = observacionActualEdit.value
            nuevaObservacion.update()
        url = f"{urlEndpoint}/clientes"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print("Error al Obtener datos")
            open_ErrorModal(e)
        for cliente in data:
            if cliente['nombre'] == nombreClienteEdit.value:
                cliente_id = cliente['id']
                print(f"Si existe, ID del cliente: {cliente_id}")
                ActualizarEquipo(cliente_id)
                break

    def ActualizarEquipo(id):
        url = f"{urlEndpoint}/equipo/{id_EquipoEdit.value}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "marca": equipoMarcaEdit.value,
            "modelo": nombreEquipoEdit.value,
            "estado": nuevoEstado.value,
            "id_cliente": id,
            "observaciones": nuevaObservacion.value
        }

        try:
            start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
            cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud

            response = requests.put(url, json=data, headers=headers)
            response.raise_for_status()  # Verificar si la solicitud tuvo éxito

            end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
            cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
            execution_time = end_time - start_time  # Tiempo total de ejecución en segundos

            open_ExitoModalEdit()
            print("FUNCION ACTUALIZAR EQUIPO\n---------------------------------")
            # Mostrar resultados de rendimiento
            print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
            print(f"Uso de CPU antes: {cpu_usage_before}%")
            print(f"Uso de CPU después: {cpu_usage_after}%")

        except requests.exceptions.RequestException as e:
            open_ErrorModal(e)

    # Ya editanto
    #nuevoEstado = ft.TextField(label="Nuevo Estado", disabled=True)
    nuevoEstado = ft.Dropdown(options=[
        ft.dropdown.Option("Ingresado"),
        ft.dropdown.Option("En espera"),
        ft.dropdown.Option("En mantenimiento"),
        ft.dropdown.Option("Listo"),
        ft.dropdown.Option("Entregado"),
    ], label="Nuevo Estado", disabled=True)
    nuevaObservacion = ft.TextField(label="Actualizar información", multiline=True, max_lines=3, disabled=True)
    actualizarInfoButton = ft.ElevatedButton(content=ft.Text('Actualizar Datos', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, tooltip="Actualiza los cambios", disabled=True, on_click=validarClienteEditar)
    cancelarEditButton = ft.ElevatedButton(content=ft.Text('Cancelar Cambios', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, disabled=True, on_click=cancelarEditFormulario)


    def whatsapp_redirectEdit(e):
        webbrowser.open_new_tab(f'https://wa.me/593{celularClienteEdit.value}')
    # Formulario de Ver/Editar datos Computadoras

    editarVer_Equipo = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    # Contenido del formulario antes de los botones
                    ft.Container(ft.Text("Información de ", size=35, spans=[ft.TextSpan("Equipo", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center, padding=ft.padding.only(0,25)),

                    # ID -------------------------------------------------------------
                    ft.Container(ft.Row([ft.Container(ft.Text("ID:", size=25, color='#3EC99D')),ft.Container(id_EquipoEdit)], alignment=ft.MainAxisAlignment.CENTER), padding=ft.padding.only(180,-25), margin=0),

                    # Boton Ver Historial --------------------------------------------
                    ft.Container(ft.Row([
                                     ft.Container(ft.TextButton("Contactar", style=ft.ButtonStyle(color=ft.colors.WHITE), on_click=whatsapp_redirectEdit), alignment=ft.alignment.center_right, margin=0, padding=ft.padding.only(0,-5)),
                                 ft.Container(ft.TextButton("Ver historial", style=ft.ButtonStyle(color=ft.colors.WHITE), on_click=lambda e:handle_ClickEditar_Historial(e)), alignment=ft.alignment.center_right, margin=0, padding=ft.padding.only(0,-5))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)),
                    #ft.Container(ft.TextButton("Ver historial", style=ft.ButtonStyle(color=ft.colors.WHITE), on_click=lambda e:handle_ClickEditar_Historial(e)), alignment=ft.alignment.center_right, margin=0, padding=ft.padding.only(0,-5)),

                    # TextField nombre del equipo ------------------------------------
                    ft.Container(nombreEquipoEdit, bgcolor=ft.colors.WHITE10),

                    # Text Fields con la marca, y el nombre del cliente --------------
                    ft.Container(ft.Row([ft.Container(equipoMarcaEdit,bgcolor=ft.colors.WHITE10),ft.Container(nombreClienteEdit, bgcolor=ft.colors.WHITE10),])),

                    # Label que muestra el estado actual -----------------
                    ft.Container(ft.Row([ft.Container(ft.Text("Estado Actual:", size=18, color='#3EC99D'),padding=ft.padding.only(20,13,40,13)),ft.Container(estadoEquipoEdit, width=240), ft.Container(celularClienteEdit, padding=ft.padding.only(0), bgcolor=ft.colors.WHITE10)], alignment=ft.MainAxisAlignment.START)),

                    # Texto que muestra la ultima observacion --------------------------------------------------
                    ft.Container(ft.Row([ft.Container(ft.Text("Observaciones:", size=16, color='#3EC99D'),padding=ft.padding.only(20, 13, 40, 13)),ft.Container(observacionActualEdit, width=400)], alignment=ft.MainAxisAlignment.START)),

                    # Boton para seleccionar la fecha. Y textfield Para actualizar el estado -----------
                    ft.Container(nuevoEstado, bgcolor=ft.colors.WHITE10),

                    # Text Field para la nueva observacion -----------------------------------------------------
                    ft.Container(nuevaObservacion, bgcolor=ft.colors.WHITE10),

                    # ----------------------------Botones Editar------------------------------------------------
                    ft.Container(ft.Row([editarButton,notificarClienteButton,cerrarFormularioButton,], alignment=ft.MainAxisAlignment.SPACE_AROUND), padding=ft.padding.only(0,-1)),
                    ft.Divider(height=5, thickness=2),
                    # ----------------------------Botones Ya editando------------------------------------------------
                    ft.Container(ft.Row([actualizarInfoButton,cancelarEditButton,], alignment=ft.MainAxisAlignment.SPACE_AROUND), padding=ft.padding.only(0,0)),
                ],tight=True, spacing=8
            ),padding=20, height=900, width=700,
        ),open=False, is_scroll_controlled=True, dismissible=False
    )

    def close_agEq(e):
        nombreNuevoEquipo.value = ""
        marcaNuevoEquipo.value = ""
        nombreClienteNuevoEquipo.value = ""
        observacionNuevoEquipo.value = ""
        tipoNuevoEquipo.value = ""
        agregar_Equipo.open = False
        agregar_Equipo.update()

    def validarCliente(e):
        url = f"{urlEndpoint}/clientes"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print("Error al Obtener datos")
        for cliente in data:
            if cliente['nombre'] == nombreClienteNuevoEquipo.value:
                cliente_id = cliente['id']
                registrarEquipo_PDF(cliente_id)
                break
            else:
                open_ErrorModal(e)
    def registrarEquipo_PDF(id):
        print(f"FUNCION [Registrar Equipo con PDF]\n--------------------------------------------")
        start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
        cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud
        if estadoNuevoEquipo.value == "":
            estadoNuevoEquipo.value = 'Ingresado'
        url = f"{urlEndpoint}/equipo"
        headers = {'Content-Type': 'application/json'}
        data = {"marca": marcaNuevoEquipo.value,"modelo": nombreNuevoEquipo.value,"estado": estadoNuevoEquipo.value,"id_cliente": id,"observaciones": observacionNuevoEquipo.value,"tipo": tipoNuevoEquipo.value,}
        logo_path = "assets/logo.png"
        logo_name_path = "assets/logoName.png"
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Verificar si la solicitud tuvo éxito
            data2 = response.json()
            data = {"id": data2['id'],"marca": data2['marca'],"modelo": data2['modelo'],"estado": data2['estado'],"nombre Cliente": nombreClienteNuevoEquipo.value,"observaciones": data2['observaciones'],}
            open_ExitoModal()
            crear_ficha_tecnica(f"C:/Users/{usuario_actual}/Desktop/ficha_tecnica_ingreso_{data2['id']}.pdf", data, imageLogo, imageLogoName, telefono=00000)
        except requests.exceptions.RequestException as e:
            open_ErrorModal(e)
        end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
        cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
        execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Uso de CPU antes: {cpu_usage_before}%")
        print(f"Uso de CPU después: {cpu_usage_after}%")


    # Formulario agregar computadora variables ----------------------------------------------------------------------
    nombreNuevoEquipo = ft.TextField(label="Nombre de equipo")
    marcaNuevoEquipo = ft.TextField(label="Marca")
    nombreClienteNuevoEquipo = ft.TextField(label="Nombre Cliente")
    tipoNuevoEquipo = ft.TextField(label="Tipo Equipo", width=290)
    estadoNuevoEquipo = ft.TextField(label="Estado", value="Ingresado", read_only=True)
    observacionNuevoEquipo = ft.TextField(label="Observaciones")
    # Botones para agregar

    aceptaryPdfButton = ft.ElevatedButton(content=ft.Text('Registrar y Crear PDF', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, tooltip="Registra y Crea un PDF", on_click=validarCliente)
    cancelarRegistro = ft.ElevatedButton(content=ft.Text('Cancelar Registro', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, on_click=close_agEq)

    # Formulario de agregar computadora
    agregar_Equipo = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    # Titulo
                    ft.Container(ft.Text("Registrar Nuevo ", size=35,spans=[ft.TextSpan("Equipo", ft.TextStyle(color='#3EC99D'))]),alignment=ft.alignment.center),

                    # Nombre  del Equipo Modelo
                    ft.Container(nombreNuevoEquipo, bgcolor=ft.colors.WHITE10),

                    ft.Container(nombreClienteNuevoEquipo, bgcolor=ft.colors.WHITE10),

                    # Marca del equipo y Nombre del cliente
                    ft.Container(ft.Row([ft.Container(marcaNuevoEquipo, bgcolor=ft.colors.WHITE10),ft.Container(tipoNuevoEquipo,bgcolor=ft.colors.WHITE10),])),

                    # Estado del Equipo
                    ft.Container(estadoNuevoEquipo, bgcolor=ft.colors.WHITE10),

                    # Observaciones del equipo
                    ft.Container(observacionNuevoEquipo, bgcolor=ft.colors.WHITE10),

                    # ----------------------------Botones Crear------------------------------------------------
                    ft.Container(ft.Row([cancelarRegistro,aceptaryPdfButton,], alignment=ft.MainAxisAlignment.SPACE_AROUND), padding=ft.padding.only(0, 20)),
                ],tight=True, spacing=8
            ),padding=20, height=500, width=700
        ),open=False, is_scroll_controlled=True, dismissible=False
    )


    contenedorEquiposPendientes = ft.Column(controls=leerClientesPendiente(), scroll=ft.ScrollMode.ALWAYS, height=390)
    contenedorEquiposListos = ft.Column(controls=leerClientesListo(), scroll=ft.ScrollMode.ALWAYS, height=390)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Pestaña Home Principal
    homeTab = ft.Container(
                ft.Column(controls=[
                    header,
                    ft.Divider(height=5, thickness=1),
                    # Texto titular
                    ft.Row([ft.Text(" "),ft.Text(" "), ft.Container(ft.Text('Bienvenido Nuevamente ', width=380, size=22, weight='w250', text_align='center',color='#3F4450',spans=[ft.TextSpan("Técnico", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center,padding=ft.padding.only(0,5,0,5)),
                            ft.ElevatedButton(content=ft.Text('Agregar Equipo',color='white',weight='w300',),bgcolor='#3F4450', on_hover=on_hover, on_click=show_agEq )],alignment=ft.MainAxisAlignment.SPACE_AROUND),

                    # Contenedores de los dos cuadritos principales
                    ft.Container(
                        ft.Row([
                            ft.Container(ft.Column([
                                ft.Container(ft.Text("Equipos ", width=380, size=18, weight='w250', text_align='center', color='#3F4450',spans=[ft.TextSpan("Pendientes", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center,padding=ft.padding.only(0,0,0,5)),
                                # Columna para desplegar las tarjetas de información en equipos pendientes
                                contenedorEquiposPendientes
                            ]),width=620, height=460, border_radius=30, border=ft.border.all(1.5, color='#8993A7'), padding=ft.padding.all(5)
                            ),
                            # Segundo contenedor
                            ft.Container(ft.Column([
                                ft.Container(ft.Text("Equipos ", width=380, size=18, weight='w250', text_align='center',color='#3F4450',spans=[ft.TextSpan("Por Retirar", ft.TextStyle(color='#3EC99D'))]),alignment=ft.alignment.center, padding=ft.padding.only(0, 0, 0, 5)),

                                # Columna para desplegar las tarjetas de información de equipos listos
                                contenedorEquiposListos
                            ]), width=620, height=460, border_radius=30, border=ft.border.all(1.5, color='#8993A7'),padding=ft.padding.all(5)
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),)
                ]), visible= True, width=1300, height=670
    )




#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Pestaña de Clientes y sus funciones
    def leerClientesRegistrados():
        print(f"FUNCION [Clientes Registrados]\n--------------------------------------------")
        start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
        cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud
        url = f"{urlEndpoint}/clientes"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            data = "Error al Obtener datos"
        clientes_registrados = []
        for i in data:
            nombreClienteEquipoLabel = ft.Text(i['nombre'], color='#3F4450', size=19, weight='w500')
            celularClienteEquipoLabel = ft.Text(i['telefono'], color='#3F4450', size=17, weight='w400')
            emailClienteEquipoLabel = ft.Text(i['correo'], color='#3F4450', size=17, weight='w400')
            clientes_registrados.append(
                ft.Container(
                    ft.Container(ft.Column([ft.Row([nombreClienteEquipoLabel, ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED,icon_color="#3EC99D",icon_size=30,tooltip="Borrar Equipo",on_click=lambda e, cliente=i: openmodal_ClienteDel(e, cliente)), ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([ft.Container(celularClienteEquipoLabel, padding=ft.padding.only(0,-25)),ft.Container(ft.ElevatedButton(content=ft.Text('Ver/Editar', color='white',weight='w100', ),bgcolor='#3F4450', on_hover=on_hover, on_click=lambda e, cliente=i: show_bsCliente(e, cliente)))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(emailClienteEquipoLabel, padding=ft.padding.only(0,-20))
                    ], spacing=0), width=560),border=ft.border.all(0.5, color='#8993A7'), width=665, border_radius=3,padding=ft.padding.only(25, 7, 20, 7)
                )
            )

        end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
        cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
        execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Uso de CPU antes: {cpu_usage_before}%")
        print(f"Uso de CPU después: {cpu_usage_after}%")
        return clientes_registrados

    def show_agCliente(e):
        agregar_Cliente.open = True
        agregar_Cliente.update()
    def close_agCliente(e):
        nombreNuevoCliente.value = ""
        correoNuevoCliente.value = ""
        celulardelNuevoCliente.value = ""
        labelCorreoCliente.value = ''
        agregar_Cliente.open = False
        agregar_Cliente.update()


    # Funcion para abrir y cerrar el cuadro de dialogo de Confirmar
    def openmodal_ClienteDel(e, cliente):
        id_Cliente = cliente['id']
        page.dialog = modalDelCliente(id_Cliente)
        page.dialog.open = True
        page.update()
    def closemodal_ClienteDel(e):
        page.dialog.open = False
        page.update()

    def modalDelCliente(id_Cliente):
        return ft.AlertDialog(
            modal=True,
            bgcolor='#3F4450',
            title=ft.Text("Confirmar"),
            content=ft.Text("¿Estás seguro de eliminar este Cliente?"),
            actions=[
                ft.TextButton("Sí", on_click=lambda e: eliminarCliente(e, id_Cliente)),
                ft.TextButton("No", on_click=closemodal_ClienteDel),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

    def eliminarCliente(e, id_Cliente):
        print(f"FUNCION [Eliminar Cliente]\n--------------------------------------------")
        start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
        cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud
        # Construye la URL con el ID del Cliente
        url = f"{urlEndpoint}/cliente/{id_Cliente}"

        try:
            # Realiza la solicitud DELETE
            response = requests.delete(url)
            response.raise_for_status()  # Lanza una excepción si hay un error en la solicitud
            print(f"Cliente con ID {id_Cliente} eliminado correctamente.")
            contenedorListarClientes.controls.clear()
            contenedorListarClientes.controls.extend(leerClientesRegistrados())
            contenedorListarClientes.update()
        except requests.exceptions.RequestException as err:
            print(f"Error al eliminar el Cliente con ID {id_Cliente}: {err}")

        end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
        cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
        execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Uso de CPU antes: {cpu_usage_before}%")
        print(f"Uso de CPU después: {cpu_usage_after}%")
        # Cierra el diálogo después de eliminar
        close_dlg(e)

    def validarCorreoCliente(e) -> None:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        aux = re.match(pattern,correoNuevoCliente.value) is not None
        if aux:
            labelCorreoCliente.value=''
            registrarClientesButton.disabled = False
        else:
            labelCorreoCliente.value='Ingresa un correo Válido'
            registrarClientesButton.disabled = True

        page.update()

    def registrarCliente(e):
        print(f"FUNCION [Registrar Cliente]\n--------------------------------------------")
        start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
        cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud
        url = f"{urlEndpoint}/cliente"
        headers = {'Content-Type': 'application/json'}
        data = {"correo": correoNuevoCliente.value,"nombre": nombreNuevoCliente.value,"telefono": celulardelNuevoCliente.value,}
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Verificar si la solicitud tuvo éxito
            contenedorListarClientes.controls.clear()
            contenedorListarClientes.controls.extend(leerClientesRegistrados())
            contenedorListarClientes.update()
            clienteTab.update()
            inicio.update()
            page.update()
            close_agCliente(e)
        except requests.exceptions.RequestException as e:
            labelCorreoCliente.value = 'Error en la solicitud'

        end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
        cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
        execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Uso de CPU antes: {cpu_usage_before}%")
        print(f"Uso de CPU después: {cpu_usage_after}%")



    # Formulario agregar cliente variables ----------------------------------------------------------------------
    labelCorreoCliente = ft.Text('', width=360, size=12, weight='w900', text_align='center', color=ft.colors.RED)
    nombreNuevoCliente = ft.TextField(label="Nombre del Cliente")
    correoNuevoCliente = ft.TextField(label="Correo Electronico del Cliente", on_change=validarCorreoCliente, on_focus=validarCorreoCliente)
    celulardelNuevoCliente = ft.TextField(label="Celular del Cliente", width=290)

    # Botones para agregar

    registrarClientesButton = ft.ElevatedButton(content=ft.Text('Registrar Cliente', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, tooltip="Registra un nuevo cliente", on_click=registrarCliente)
    cancelarRegistroCliente = ft.ElevatedButton(content=ft.Text('Cancelar Registro', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, on_click=close_agCliente)


    # Formulario de agregar Cliente
    agregar_Cliente = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    # Titulo
                    ft.Container(ft.Text("Registrar Nuevo ", size=35,
                                         spans=[ft.TextSpan("Cliente", ft.TextStyle(color='#3EC99D'))]),
                                 alignment=ft.alignment.center),

                    # Nombre del Nuevo cliente
                    ft.Container(nombreNuevoCliente, bgcolor=ft.colors.WHITE10),

                    # Correo electronico y celular del cliente
                    ft.Container(ft.Row([ft.Container(correoNuevoCliente, bgcolor=ft.colors.WHITE10),
                                         ft.Container(celulardelNuevoCliente, bgcolor=ft.colors.WHITE10), ])),
                    ft.Container(labelCorreoCliente),
                    # ----------------------------Botones Crear------------------------------------------------
                    ft.Container(
                        ft.Row([cancelarRegistroCliente, registrarClientesButton], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                        padding=ft.padding.only(0, 20)),
                ], tight=True, spacing=8
            ), padding=20, height=400, width=700
        ), open=False, is_scroll_controlled=True, dismissible=False
    )
    def show_bsCliente(e, cliente):
        nombreClienteEditar.value = cliente['nombre']
        id_ClienteEdit.value = cliente['id']
        correoClienteEditar.value = cliente['correo']
        celularClienteEditar.value = cliente['telefono']
        page.client_storage.set("nombreClienteEdit", cliente['nombre'])
        contenedorListarEquiposCliente.controls.clear()
        contenedorListarEquiposCliente.controls.extend(leerEquiposCliente(e, id_ClienteEdit.value))
        contenedorListarEquiposCliente.update()
        editarVer_Cliente.open = True
        editarVer_Cliente.update()
    def close_bsCliente(e):
        editarVer_Cliente.open = False
        editarVer_Cliente.update()

    def editarClienteFormulario(e):
        page.client_storage.set("nombreCliente", nombreClienteEditar.value,)
        page.client_storage.set("correoCliente", correoClienteEditar.value,)
        page.client_storage.set("telefonoCliente", celularClienteEditar.value,)
        nombreClienteEditar.read_only = False
        nombreClienteEditar.update()
        correoClienteEditar.read_only = False
        correoClienteEditar.update()
        celularClienteEditar.read_only = False
        celularClienteEditar.update()
        cerrarFormularioEditClienteButton.disabled = True
        cerrarFormularioEditClienteButton.update()
        actualizarClienteButton.disabled = False
        actualizarClienteButton.update()
        cancelarEditClienteButton.disabled = False
        cancelarEditClienteButton.update()
        editarClienteButton.disabled = True
        editarClienteButton.update()

    # Funcion para cancelar la edicion de formulario
    def cancelarEditClienteFormulario(e):
        nombreClienteEditar.value = page.client_storage.get("nombreCliente")
        correoClienteEditar.value = page.client_storage.get("correoCliente")
        celularClienteEditar.value = page.client_storage.get("telefonoCliente")
        nombreClienteEditar.read_only = True
        nombreClienteEditar.update()
        correoClienteEditar.read_only = True
        correoClienteEditar.update()
        celularClienteEditar.read_only = True
        celularClienteEditar.update()
        cerrarFormularioEditClienteButton.disabled = False
        cerrarFormularioEditClienteButton.update()
        actualizarClienteButton.disabled = True
        actualizarClienteButton.update()
        cancelarEditClienteButton.disabled = True
        cancelarEditClienteButton.update()
        editarClienteButton.disabled = False
        editarClienteButton.update()
    def validarCorreoClienteEdit(e) -> None:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        aux = re.match(pattern,correoClienteEditar.value) is not None
        if aux:
            labelEditarCliente.value=''
            actualizarClienteButton.disabled = False
        else:
            labelEditarCliente.value='Ingresa un correo Válido'
            actualizarClienteButton.disabled = True

        page.update()
    def ActualizarCliente(e):
        print(f"FUNCION [Actualizar Cliente]\n--------------------------------------------")
        start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
        cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud
        page.client_storage.set("nombreCliente", nombreClienteEditar.value,)
        page.client_storage.set("correoCliente", correoClienteEditar.value,)
        page.client_storage.set("telefonoCliente", celularClienteEditar.value,)
        id = id_ClienteEdit.value
        url = f"{urlEndpoint}/cliente/{id}"
        headers = {'Content-Type': 'application/json'}
        data = {"correo": correoClienteEditar.value,"nombre": nombreClienteEditar.value,"telefono": celularClienteEditar.value,}
        try:
            response = requests.put(url, json=data, headers=headers)
            response.raise_for_status()  # Verificar si la solicitud tuvo éxito
            contenedorListarClientes.controls.clear()
            contenedorListarClientes.controls.extend(leerClientesRegistrados())
            contenedorListarClientes.update()
            contenedorListarEquiposCliente.controls.clear()
            contenedorListarEquiposCliente.controls.extend(leerEquiposCliente(e, id_ClienteEdit.value))
            contenedorListarEquiposCliente.update()
            clienteTab.update()
            inicio.update()
            page.update()
            cancelarEditClienteFormulario(e)
        except requests.exceptions.RequestException as e:
            labelEditarCliente.value = 'Error Actualizando Datos'

        end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
        cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
        execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Uso de CPU antes: {cpu_usage_before}%")
        print(f"Uso de CPU después: {cpu_usage_after}%")


    def whatsapp_redirect(e):
        webbrowser.open_new_tab(f'https://wa.me/593{celularClienteEditar.value}')

    def handle_Click(e, equipo):
        close_bsCliente(e)
        show_bs(e, equipo)

    def handleClick_AG(e):
        close_bsCliente(e)
        show_agEq(e)
        nombreClienteNuevoEquipo.value = page.client_storage.get("nombreClienteEdit")
        nombreClienteNuevoEquipo.update()

    def leerEquiposCliente(e, id):
        print(f"FUNCION [Leer Equipo de un Cliente]\n--------------------------------------------")
        start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
        cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud
        url = f'{urlEndpoint}/equipos/cliente/{id}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if response.status_code == 200:
                nombre_cliente = page.client_storage.get("nombreClienteEdit")
                for item in data:
                    item["nombre_cliente"] = nombre_cliente

            print("Obteniendo Datos")
        except requests.exceptions.RequestException as e:
            data = "Error al Obtener datos"
            print("ERROR Obteniendo equipos")
        equipos_cliente = []
        if response.status_code == 200:
            for i in data:
                estadoJson = i['estado']
                if estadoJson.lower() == 'listo':
                    estadoEquipoLabel = ft.Text("En estado: ", color=ft.colors.WHITE, size=17, weight='w400', spans=[
                        ft.TextSpan(estadoJson, ft.TextStyle(color='#3EC99D', weight='w500'))])
                else:
                    estadoEquipoLabel = ft.Text("En estado: ", color=ft.colors.WHITE, size=17, weight='w400',spans=[ft.TextSpan(estadoJson, ft.TextStyle(color='#FF914D', weight='w500'))])
                nombreEquipoLabel = ft.Text(f"{i['marca']} {i['modelo']}", color=ft.colors.WHITE, size=19, weight='w500')
                observaciones = ft.Text("Observaciones:", color='#3EC99D', size=17, weight='w400',spans=[ft.TextSpan(i['observaciones'], ft.TextStyle(color=ft.colors.WHITE, weight='w400'))])

                equipos_cliente.append(
                    ft.Container(
                        ft.Container(ft.Column([ft.Row([nombreEquipoLabel,
                                                        ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED,
                                                                      icon_color="#3EC99D", icon_size=20,
                                                                      tooltip="Borrar Equipo",
                                                                      on_click=lambda e, equipo=i: open_dlg_modal(e, equipo)), ],
                                                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                ft.Row(
                                                    [ft.Container(estadoEquipoLabel, padding=ft.padding.only(0, -20)),
                                                     ft.Container(ft.ElevatedButton(
                                                         content=ft.Text('Ver/Editar', color='white', weight='w100', ),
                                                         bgcolor='#3F4450', on_hover=on_hover,
                                                         on_click=lambda e, equipo=i: handle_Click(e, equipo)))],
                                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                ft.Container(observaciones, padding=ft.padding.only(0,-12))
                                                ], spacing=0), width=560), border=ft.border.all(0.5, color='#8993A7'),
                        width=665, border_radius=3, padding=ft.padding.only(25, 7, 20, 7)
                    )
                )
        else:
            equipos_cliente.append(
                ft.Container(
                    ft.Container(ft.Column([ft.Text('SIN EQUIPOS')], spacing=0), width=560), border=ft.border.all(0.5, color='#8993A7'),
                    width=665, border_radius=3, padding=ft.padding.only(25, 7, 20, 7)
                )
            )
        end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
        cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
        execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Uso de CPU antes: {cpu_usage_before}%")
        print(f"Uso de CPU después: {cpu_usage_after}%")
        return equipos_cliente



    nombreClienteEditar = ft.TextField(label="Nombre del Cliente", value='', read_only=True)
    correoClienteEditar = ft.TextField(label="Correo del Cliente", value='', read_only=True, on_focus=validarCorreoClienteEdit, on_change=validarCorreoClienteEdit)
    celularClienteEditar = ft.TextField(label="Celular del Cliente", width=290, value='', read_only=True, keyboard_type=ft.KeyboardType.NUMBER)
    id_ClienteEdit = ft.TextField(value="", read_only=True, border="none", text_size=15)
    labelEditarCliente = ft.Text('', width=360, size=12, weight='w900', text_align='center', color=ft.colors.RED)

    actualizarClienteButton = ft.ElevatedButton(content=ft.Text('Actualizar Datos', color='white', weight='w300'),
                                             bgcolor='#3F4450', on_hover=on_hover, tooltip="Actualiza los cambios",
                                             disabled=True, on_click=ActualizarCliente)
    cancelarEditClienteButton = ft.ElevatedButton(content=ft.Text('Cancelar Cambios', color='white', weight='w300'),
                                           bgcolor='#3F4450', on_hover=on_hover, disabled=True,
                                           on_click=cancelarEditClienteFormulario)
    editarClienteButton = ft.ElevatedButton(content=ft.Text('Editar Información', color='white', weight='w300'),
                                     bgcolor='#3F4450', on_hover=on_hover, on_click=editarClienteFormulario)
    cerrarFormularioEditClienteButton = ft.ElevatedButton(content=ft.Text('Cerrar Formulario', color='white', weight='w300'),
                                               bgcolor='#3F4450', on_hover=on_hover, on_click=close_bsCliente)

    contenedorListarEquiposCliente = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=200)
    editarVer_Cliente = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    # Contenido del formulario antes de los botones
                    ft.Container(ft.Text("Información de ", size=35,
                                         spans=[ft.TextSpan("Cliente", ft.TextStyle(color='#3EC99D'))]),
                                 alignment=ft.alignment.center, padding=ft.padding.only(0, 10)),

                    # ID -------------------------------------------------------------
                    ft.Container(
                        ft.Row([ft.Container(ft.Text("ID:", size=18, color='#3EC99D')), ft.Container(id_ClienteEdit)],
                               alignment=ft.MainAxisAlignment.CENTER), padding=ft.padding.only(260, -25), margin=0),
                    # Boton Ver Historial --------------------------------------------
                    ft.Container(ft.Row([ft.Container(ft.TextButton("Agregar Equipo", style=ft.ButtonStyle(color=ft.colors.WHITE), on_click=handleClick_AG),
                                 alignment=ft.alignment.center_right, margin=0, padding=ft.padding.only(0, 0)),
                                         ft.Container(ft.TextButton("Contactar", style=ft.ButtonStyle(color=ft.colors.WHITE), on_click=whatsapp_redirect),
                                 alignment=ft.alignment.center_right, margin=0, padding=ft.padding.only(0, 0)),], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),),
                    ft.Container(labelEditarCliente),
                    # TextField nombre del Cliente ------------------------------------
                    ft.Container(nombreClienteEditar, bgcolor=ft.colors.WHITE10),

                    # Text Fields con el celular, y el correo del cliente --------------
                    ft.Container(ft.Row([ft.Container(correoClienteEditar, bgcolor=ft.colors.WHITE10),
                                         ft.Container(celularClienteEditar, bgcolor=ft.colors.WHITE10), ])),

                    # ----------------------------Botones Editar------------------------------------------------
                    ft.Container(ft.Row([editarClienteButton, cerrarFormularioEditClienteButton, ],
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND), padding=ft.padding.only(0, -1)),
                    ft.Divider(height=5, thickness=2),
                    # ----------------------------Botones Ya editando------------------------------------------------
                    ft.Container(ft.Row([actualizarClienteButton, cancelarEditClienteButton, ],
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND), padding=ft.padding.only(0, 0)),

                    ft.Container(ft.Text("Equipos ", size=25,
                                         spans=[ft.TextSpan("Registrados", ft.TextStyle(color='#3EC99D'))]),
                                 alignment=ft.alignment.center),
                    ft.Container(contenedorListarEquiposCliente),
                ], tight=True, spacing=8
            ), padding=20, height=900, width=700,
        ), open=False, is_scroll_controlled=True, dismissible=False
    )



    contenedorListarClientes = ft.Column(controls=leerClientesRegistrados(), scroll=ft.ScrollMode.ALWAYS, height=415)


    clienteTab = ft.Container(
                ft.Column(controls=[
                    header,
                    ft.Divider(height=5, thickness=1),
                    # Texto titular
                    ft.Row([ft.Text(" "), ft.Container(ft.Text('Registro de ', width=380, size=22, weight='w250', text_align='center',color='#3F4450',spans=[ft.TextSpan("Clientes", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center,padding=ft.padding.only(150,5,0,5)),
                            ft.ElevatedButton(content=ft.Text('Agregar Cliente',color='white',weight='w300',),bgcolor='#3F4450', on_hover=on_hover, on_click=show_agCliente)],alignment=ft.MainAxisAlignment.SPACE_AROUND),

                    # Contenedores de los dos cuadritos principales
                    ft.Container(
                            ft.Container(ft.Column([
                                ft.Container(ft.Text("Clientes ", width=380, size=20, weight='w250', text_align='center', color='#3F4450',spans=[ft.TextSpan("Registros", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center,padding=ft.padding.only(0,0,0,5)),
                                # Columna para desplegar las tarjetas de información en equipos pendientes
                                ft.Container(contenedorListarClientes)
                                ]),width=670, height=472, border_radius=30, border=ft.border.all(1.5, color='#8993A7'), padding=ft.padding.all(5)
                            ), alignment=ft.alignment.center
                    )
                ]), visible= True, width=1300, height=670
    )




# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Crear tarjetas de información de los equipos para historial
    def leerEquiposHistorial():
        print(f"FUNCION [Pestaña Historial Equipos]\n--------------------------------------------")
        start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
        cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud
        url = f"{urlEndpoint}/equipos"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            data = "Error al Obtener datos"
        equipos_historial = []
        for i in data:
            estadoJson = i['estado']
            idEquipoLabel = ft.Text(i['id'], color='#3EC99D', size=18, weight='w500')
            estadoEquipoLabel = ft.Text("Estado Actual: ", color='#3F4450', size=17, weight='w400',spans=[ft.TextSpan(estadoJson, ft.TextStyle(color='#3F4450', weight='w500'))])
            nombreClienteEquipoLabel = ft.Text(i['nombre_cliente'], color='#3F4450', size=17, weight='w400')
            nombreEquipoLabel = ft.Text(f"{i['marca']} {i['modelo']}", color='#3F4450', size=19, weight='w400')
            equipos_historial.append(
                ft.Container(
                    ft.Container(ft.Column([ft.Container(idEquipoLabel), ft.Container(nombreEquipoLabel),
                                            ft.Row(
                                                [ft.Container(estadoEquipoLabel, padding=ft.padding.only(0, -13)),
                                                 ft.Container(ft.ElevatedButton(
                                                     content=ft.Text('Ver/Editar', color='white', weight='w100', ),
                                                     bgcolor='#3F4450', on_hover=on_hover,
                                                     on_click=lambda e, equipo=i: show_bsHistorial(e, equipo)))],
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                            ft.Container(nombreClienteEquipoLabel, padding=ft.padding.only(0, -15)),
                                            ], spacing=0), width=700), border=ft.border.all(0.5, color='#8993A7'),
                    width=710, border_radius=3, padding=ft.padding.only(25, 7, 20, 7)
                )
            )
        end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
        cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
        execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Uso de CPU antes: {cpu_usage_before}%")
        print(f"Uso de CPU después: {cpu_usage_after}%")
        return equipos_historial



    def leerHistorial(e, id):

        url = f'{urlEndpoint}/mantenimiento/equipo/{id}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            mantenimientos = data.get('mantenimientos', [])
            equipos_historial = []
            for mantenimiento in mantenimientos:
                estado_actual = mantenimiento.get("estado_actual")
                descripcion = mantenimiento.get("descripcion")
                fecha = mantenimiento.get("fecha")
                fechaHistorial = ft.Text("Fecha: ", color='#3EC99D', size=17, weight='w400', spans=[ft.TextSpan(fecha, ft.TextStyle(color=ft.colors.WHITE, weight='w400'))])
                estadoHistorial = ft.Text("Estado: ", color='#3EC99D', size=16, weight='w400', spans=[ft.TextSpan(estado_actual, ft.TextStyle(color=ft.colors.WHITE, weight='w300'))])
                descripcionHistorial = ft.Text("Observacion Dada: ", color='#FF914D', size=16, weight='w400', spans=[ft.TextSpan(descripcion, ft.TextStyle(color=ft.colors.WHITE, weight='w300'))])
                equipos_historial.append(ft.Container(ft.Container(ft.Column([
                            ft.Container(fechaHistorial, padding=ft.padding.only(0, -12)),
                            ft.Container(estadoHistorial, padding=ft.padding.only(0, -12)),
                            ft.Container(descripcionHistorial, padding=ft.padding.only(0, -12)),], spacing=15), width=560), border=ft.border.all(0.5, color='#8993A7'),width=665, border_radius=3, padding=ft.padding.only(25, 15, 20, 7))
                )
        except requests.exceptions.RequestException as e:
            print(f"ERROR Obteniendo equipos {e}")
        return equipos_historial


    def whatsapp_redirectHIST(e):
        webbrowser.open_new_tab(f'https://wa.me/593{celularClienteHist.value}')

    def handle_ClickHistorial(e):
        close_bsHistorial(e)
        equipo = page.client_storage.get("equipoCache")
        show_bs(e, equipo)
    def close_bsHistorial(e):
        ver_historialEquipo.open = False
        ver_historialEquipo.update()
    def show_bsHistorial(e, equipo):
        print(f"FUNCION [Ver historial de 1 equipo]\n--------------------------------------------")
        start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
        cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud

        nombreEquipoHist.value = f"{equipo['marca']} {equipo['modelo']}"
        id_EquipoHist.value = equipo['id']
        nombreClienteHist.value = equipo['nombre_cliente']
        page.client_storage.set("equipoCache", equipo)
        url = f"{urlEndpoint}/clientes"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print("Error al Obtener datos")
        for cliente in data:
            if cliente['nombre'] == equipo['nombre_cliente']:
                cliente_id = cliente['id']
                url2 = f"{urlEndpoint}/cliente/{cliente_id}"
                try:
                    response = requests.get(url2)
                    response.raise_for_status()
                    data2 = response.json()
                    celularClienteHist.value = data2['telefono']
                except requests.exceptions.RequestException as e:
                    print("Error al Obtener Celular del Cliente")
                break
            else:
                celularClienteHist.value = ""

        contenedorRegistroHistorico.controls.clear()
        contenedorRegistroHistorico.controls.extend(leerHistorial(e, id_EquipoHist.value))
        contenedorRegistroHistorico.update()
        ver_historialEquipo.open = True
        ver_historialEquipo.update()
        end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
        cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
        execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Uso de CPU antes: {cpu_usage_before}%")
        print(f"Uso de CPU después: {cpu_usage_after}%")

    contenedorHistorialEquipos = ft.Column(controls=leerEquiposHistorial(), scroll=ft.ScrollMode.ALWAYS, height=415)

    id_EquipoHist = ft.TextField(value="", read_only=True, border="none", text_size=25)
    nombreEquipoHist = ft.TextField(label="Nombre de equipo", value="", read_only=True)
    nombreClienteHist = ft.TextField(label="Nombre Cliente", value="", read_only=True)
    celularClienteHist = ft.TextField(label="Celular Cliente", value="", width=290, read_only=True)

    cerrarHistorialButton = ft.ElevatedButton(
        content=ft.Text('Cerrar Pestaña', color='white', weight='w300'),
        bgcolor='#3F4450', on_hover=on_hover, on_click=close_bsHistorial)

    contenedorRegistroHistorico = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=200)
    ver_historialEquipo = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    # Contenido del formulario antes de los botones
                    ft.Container(ft.Text("Historial de ", size=35, spans=[ft.TextSpan("Equipo", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center, padding=ft.padding.only(0,25)),

                    # ID -------------------------------------------------------------
                    ft.Container(ft.Row([ft.Container(ft.Text("ID:", size=25, color='#3EC99D')),ft.Container(id_EquipoHist)], alignment=ft.MainAxisAlignment.CENTER), padding=ft.padding.only(180,-25), margin=0),

                    # Boton Editar --------------------------------------------
                    ft.Container(ft.Row([ft.Container(
                        ft.TextButton("Editar", style=ft.ButtonStyle(color=ft.colors.WHITE),
                                      on_click=lambda e: handle_ClickHistorial(e)),
                        alignment=ft.alignment.center_right, margin=0, padding=ft.padding.only(0, 0)),
                                         ft.Container(
                                             ft.TextButton("Contactar", style=ft.ButtonStyle(color=ft.colors.WHITE),
                                                           on_click=whatsapp_redirectHIST),
                                             alignment=ft.alignment.center_right, margin=0,
                                             padding=ft.padding.only(0, 0)), ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ),

                    # TextField nombre del equipo ------------------------------------
                    ft.Container(nombreEquipoHist, bgcolor=ft.colors.WHITE10),

                    # Text Fields con la marca, y el nombre del cliente --------------
                    ft.Container(ft.Row([ft.Container(nombreClienteHist,bgcolor=ft.colors.WHITE10),ft.Container(celularClienteHist, bgcolor=ft.colors.WHITE10),])),

                    ft.Divider(height=5, thickness=1),
                    ft.Container(cerrarHistorialButton, alignment=ft.alignment.center),
                    ft.Divider(height=5, thickness=1),
                    ft.Container(ft.Text("Historial ", size=25,
                                         spans=[ft.TextSpan("Mantenimiento", ft.TextStyle(color='#3EC99D'))]),
                                 alignment=ft.alignment.center),
                    ft.Container(contenedorRegistroHistorico),
                ],tight=True, spacing=8
            ),padding=20, height=700, width=700,
        ),open=False, is_scroll_controlled=True, dismissible=False
    )

    # Historial Tab de equipos
    historialTab = ft.Container(
                ft.Column(controls=[
                    header,
                    ft.Divider(height=5, thickness=1),
                    ft.Container(
                        ft.Text('Pestaña ', width=380, size=20, weight='w250', text_align='center', color='#3F4450',
                                spans=[ft.TextSpan("Historial", ft.TextStyle(color='#3EC99D'))]),
                        alignment=ft.alignment.center, padding=ft.padding.only(0, 5)),

                    ft.Container(
                        ft.Container(ft.Column([
                            ft.Container(ft.Text("Equipos ", width=380, size=20, weight='w250', text_align='center',
                                                 color='#3F4450',
                                                 spans=[ft.TextSpan("Registrados", ft.TextStyle(color='#3EC99D'))]),
                                         alignment=ft.alignment.center, padding=ft.padding.only(0, 0, 0, 5)),
                            # Columna para desplegar las tarjetas de información en equipos pendientes
                            ft.Container(contenedorHistorialEquipos)
                        ]), width=715, height=480, border_radius=30, border=ft.border.all(1.5, color='#8993A7'),
                            padding=ft.padding.all(5)
                        ), alignment=ft.alignment.center
                    )

                ]), visible= False, width=1300, height=670
    )

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def editarInformacionAdmin(e):
        nombreAdminText.read_only = False
        nombreAdminText.update()
        celularAdminText.read_only = False
        celularAdminText.update()
        correoAdminText.disabled = False
        correoAdminText.update()
        passwordAdminText.disabled = False
        passwordAdminText.update()
        botonEditar.disabled = True
        botonEditar.update()
        botonCancelarEditar.disabled = False
        botonCancelarEditar.update()

    def cancelarEditarInformacionAdmin(e):
        nombreAdminText.value =page.client_storage.get('nombre')
        nombreAdminText.read_only = True
        nombreAdminText.update()
        celularAdminText.value = page.client_storage.get('telefono')
        celularAdminText.read_only = True
        celularAdminText.update()
        correoAdminText.value = page.client_storage.get('correo')
        correoAdminText.disabled = True
        correoAdminText.update()
        passwordAdminText.value = ""
        passwordAdminText.disabled = True
        passwordAdminText.update()
        botonEditar.disabled = False
        botonEditar.update()
        labelPasAdmin.value = ''
        labelPasAdmin.update()
        labelAdmin.value = ''
        labelAdmin.update()
        botonCancelarEditar.disabled = True
        botonCancelarEditar.update()
        botonActualizar.disabled = True
        botonActualizar.update()

    def validarCamposEditAdmin(e) -> None:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        aux = re.match(pattern,correoAdminText.value) is not None
        if aux:
            labelAdmin.value=''
            if passwordAdminText.value == '':
                labelPasAdmin.value = 'Ingresa tu contraseña para los cambios'
                botonActualizar.disabled = True
            else:
                labelPasAdmin.value = ''
                botonActualizar.disabled = False
        else:
            labelAdmin.value='Ingresa un correo Válido'
            botonActualizar.disabled = True

        page.update()

    def validarCamposNuevaPass(e) -> None:
        if passNuevaConf.value == '' or passNuevaText.value == '' or passActualText.value == '':
            labelNuevaPass.value = 'Llena todos los campos'
            botonActuPass.disabled = True
        else:
            if passNuevaText.value == passNuevaConf.value:
                botonActuPass.disabled = False
                labelNuevaPass.value = ''
            else:
                labelNuevaPass.value = 'Los valores deben ser iguales'
                botonActuPass.disabled = True
        page.update()

    def validarAdminEditar(e):
        url = f"{urlEndpoint}/admin/login"
        headers = {'Content-Type': 'application/json'}
        data = {
            "correo": page.client_storage.get('correo'),
            "password": passwordAdminText.value
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            # Verificar si la solicitud tuvo éxito
            if response.status_code == 200:
                response_data = response.json()
                ActualizarAdmin(e, response_data.get('id'))
            else:
                labelPasAdmin.value = "Credenciales Incorrectas"
                passwordAdminText.value = ''
                page.update()
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud: {e}")
            labelPasAdmin.value = "Error con el servidor"
            passwordAdminText.value = ''
            page.update()



    def ActualizarAdmin(e, id):
        print(f"FUNCION [Actualizar Información Admin]\n--------------------------------------------")
        start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
        cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud
        url = f"{urlEndpoint}/admin/{id}"
        headers = {'Content-Type': 'application/json'}
        data = {"correo": correoAdminText.value,"nombre": nombreAdminText.value,"telefono": celularAdminText.value,"password": passwordAdminText.value,}
        try:
            response = requests.put(url, json=data, headers=headers)
            response.raise_for_status()  # Verificar si la solicitud tuvo éxito
            page.client_storage.set("nombre", nombreAdminText.value)
            page.client_storage.set("telefono", celularAdminText.value)
            page.client_storage.set("correo", correoAdminText.value)
            page.update()
            cancelarEditarInformacionAdmin(e)
        except requests.exceptions.RequestException as e:
            labelPasAdmin.value ='Error al Actualizar'
        end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
        cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
        execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Uso de CPU antes: {cpu_usage_before}%")
        print(f"Uso de CPU después: {cpu_usage_after}%")

    def ActualizarPass(e):
        passActualText.disabled = False
        passActualText.update()
        passNuevaConf.disabled = False
        passNuevaConf.update()
        passNuevaText.disabled = False
        passNuevaText.update()
        botonEditPass.disabled = True
        botonEditPass.update()
        botonActuPass.disabled = False
        botonActuPass.update()
        botonCancelarPass.disabled = False
        botonCancelarPass.update()
    def CancelarActualizarPass(e):
        passActualText.value = ''
        passNuevaText.value = ''
        passNuevaConf.value = ''
        passActualText.disabled = True
        passActualText.update()
        passNuevaConf.disabled = True
        passNuevaConf.update()
        passNuevaText.disabled = True
        passNuevaText.update()
        botonEditPass.disabled = False
        botonEditPass.update()
        botonActuPass.disabled = True
        botonActuPass.update()
        botonCancelarPass.disabled = True
        botonCancelarPass.update()
        labelNuevaPass.value = ''
        labelNuevaPass.update()

    def validarAdminPassEditar(e):
        print(f"FUNCION [Cambiar Contraseña]\n--------------------------------------------")
        start_time = timeit.default_timer()  # Iniciar tiempo de ejecución
        cpu_usage_before = psutil.cpu_percent()  # Uso de CPU antes de la solicitud
        url = f"{urlEndpoint}/admin/login"
        headers = {'Content-Type': 'application/json'}
        data = {
            "correo": page.client_storage.get('correo'),
            "password": passActualText.value
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            # Verificar si la solicitud tuvo éxito
            if response.status_code == 200:
                response_data = response.json()
                ActualizarPassAdmin(e, response_data.get('id'))
            else:
                labelNuevaPass.value = "Credenciales Incorrectas"
                passActualText.value = ''
                page.update()
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud: {e}")
            labelNuevaPass.value = "Error con el servidor"
            passActualText.value = ''
            page.update()
        end_time = timeit.default_timer()  # Finalizar tiempo de ejecución
        cpu_usage_after = psutil.cpu_percent()  # Uso de CPU después de la solicitud
        execution_time = end_time - start_time  # Tiempo total de ejecución en segundos
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Uso de CPU antes: {cpu_usage_before}%")
        print(f"Uso de CPU después: {cpu_usage_after}%")
    def ActualizarPassAdmin(e, id):
        url = f"{urlEndpoint}/admin/{id}"
        headers = {'Content-Type': 'application/json'}
        data = {"correo": page.client_storage.get('correo'),"nombre": page.client_storage.get('nombre'),"telefono": page.client_storage.get('telefono'),"password": passNuevaText.value,}
        try:
            response = requests.put(url, json=data, headers=headers)
            response.raise_for_status()  # Verificar si la solicitud tuvo éxito
            passActualText.value = ''
            passActualText.update()
            passNuevaText.value = ''
            passNuevaText.update()
            passNuevaConf.value = ''
            passNuevaConf.update()
            CancelarActualizarPass(e)
        except requests.exceptions.RequestException as e:
            labelNuevaPass.value ='Error al Actualizar'


    nombreAdminText = ft.TextField(width=630, height=40, label="Nombre del Técnico Administrador", color='#3F4450',
                                border_color='#3F4450', border_radius=20, label_style=ft.TextStyle(color='#3F4450'),
                                 focused_border_color='#3EC99D', read_only=True)
    celularAdminText = ft.TextField(width=310, height=40, label="Celular del Contacto", color='#3F4450',
                                   border_color='#3F4450', border_radius=20, label_style=ft.TextStyle(color='#3F4450'),
                                   focused_border_color='#3EC99D', read_only=True)
    correoAdminText = ft.TextField(width=310, height=40, label="Correo Electrónico", color='#3F4450',
                                   border_color='#3F4450', border_radius=20, label_style=ft.TextStyle(color='#3F4450'),
                                   focused_border_color='#3EC99D', disabled=True, on_change=validarCamposEditAdmin, on_focus=validarCamposEditAdmin)

    passwordAdminText = ft.TextField(width=310, height=40, label="Contraseña Confirmar", color='#3F4450',
                                   border_color='#3F4450', border_radius=20, label_style=ft.TextStyle(color='#3F4450'),
                                   focused_border_color='#3EC99D', disabled=True, password=True, can_reveal_password=True, on_change=validarCamposEditAdmin, on_focus=validarCamposEditAdmin)

    botonEditar = ft.ElevatedButton(content=ft.Text('Editar Informacion', color='white', weight='w300'),bgcolor='#3F4450', width=275,on_hover=on_hover, on_click=editarInformacionAdmin)
    botonActualizar = ft.ElevatedButton(content=ft.Text('Confirmar y Actualizar', color='white', weight='w300'),
                                    bgcolor='#3F4450', on_hover=on_hover, disabled=True, width=275, on_click=validarAdminEditar)
    botonCancelarEditar = ft.ElevatedButton(content=ft.Text('Cancelar Cambios', color='white', weight='w300'),
                                    bgcolor='#3F4450', on_hover=on_hover, disabled=True, on_click=cancelarEditarInformacionAdmin, width=275)

    #-----------------------------------ACTUALIZAR CONTRASEÑA---------------------------------------------
    passActualText = ft.TextField(width=310, height=40, label="Contraseña Actual", color='#3F4450',
                                    border_color='#3F4450', border_radius=20, label_style=ft.TextStyle(color='#3F4450'),
                                    focused_border_color='#3EC99D', disabled=True, password=True, on_change=validarCamposNuevaPass)
    passNuevaText = ft.TextField(width=310, height=40, label="Nueva Contraseña", color='#3F4450',
                                  border_color='#3F4450', border_radius=20, label_style=ft.TextStyle(color='#3F4450'),
                                  focused_border_color='#3EC99D', disabled=True, password=True, can_reveal_password=True, on_change=validarCamposNuevaPass)
    passNuevaConf = ft.TextField(width=310, height=40, label="Confirmar Contraseña", color='#3F4450',
                                  border_color='#3F4450', border_radius=20, label_style=ft.TextStyle(color='#3F4450'),
                                  focused_border_color='#3EC99D', disabled=True, password=True, on_change=validarCamposNuevaPass)

    botonEditPass = ft.ElevatedButton(content=ft.Text('Nueva Contraseña', color='white', weight='w300'),
                                            bgcolor='#3F4450', on_hover=on_hover,width=275, on_click=ActualizarPass)
    botonActuPass = ft.ElevatedButton(content=ft.Text('Actualizar Contraseña', color='white', weight='w300'),
                                      bgcolor='#3F4450', on_hover=on_hover, disabled=True,
                                      width=275, on_click=validarAdminPassEditar)
    botonCancelarPass = ft.ElevatedButton(content=ft.Text('Cancelar', color='white', weight='w300'),
                                      bgcolor='#3F4450', on_hover=on_hover, disabled=True,
                                      width=275, on_click=CancelarActualizarPass)

    labelAdmin = ft.Text('', width=360, size=12, weight='w900', text_align='center', color=ft.colors.RED)
    labelPasAdmin = ft.Text('', width=360, size=12, weight='w900', text_align='center', color=ft.colors.RED)
    labelNuevaPass = ft.Text('', width=360, size=12, weight='w900', text_align='center', color=ft.colors.RED)
    # Perfil del Técnico
    perfilTab = ft.Container(
                ft.Column(controls=[
                    header,
                    ft.Divider(height=5, thickness=1),
                    # Contenedores de los dos cuadritos principales
                    ft.Container(
                            ft.Container(ft.Column([
                                ft.Container(ft.Text("Información del ", width=380, size=28, weight='w250', text_align='center', color='#3F4450',spans=[ft.TextSpan("Técnico", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center,padding=ft.padding.only(0,-20,0,2)),
                                # Columna para desplegar las tarjetas de información en equipos pendientes
                                ft.Container(ft.Column([
                                    nombreAdminText,
                                    ft.Container(ft.Row([
                                        celularAdminText, correoAdminText
                                    ])),
                                    ft.Container(ft.Row([
                                        ft.Text(""), labelAdmin,
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), padding=ft.padding.only(0,-15,0,-10)),
                                    ft.Container(ft.Row([
                                        passwordAdminText, botonActualizar
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)),
                                    ft.Container(labelPasAdmin, padding=ft.padding.only(0,-13,0,-10)),
                                    ft.Container(ft.Row([
                                        ft.Container(botonEditar), ft.Container(botonCancelarEditar)
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)),
                                    ft.Container(ft.Divider(height=7, thickness=1, color='#8993A7'), padding=ft.padding.only(0,5,0,5)),
                                    ft.Container(ft.Row([
                                        passActualText, passNuevaText
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)),
                                    ft.Container(ft.Row([
                                        botonEditPass, passNuevaConf
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)),
                                    ft.Container(labelNuevaPass, padding=ft.padding.only(0,-15,0,-10)),
                                    ft.Container(ft.Row([
                                        botonActuPass, botonCancelarPass
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)),
                                ], scroll=ft.ScrollMode.ALWAYS,height=480, spacing=10))
                                ]),width=670, height=520, border_radius=30, border=ft.border.all(1.5, color='#8993A7'), padding=ft.padding.only(20,40,20,20)
                            ), alignment=ft.alignment.center
                    )
                ]), visible= True, width=1300, height=670
    )

    inicio = ft.Container(
            content=ft.Column([homeTab,clienteTab,historialTab,perfilTab]),
        )


    page.window_width = 1300
    page.window_height = 750
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.bgcolor = ft.colors.WHITE
    page.title = 'Hackers Internet'
    page.window_resizable= False
    page.window_maximizable = True
    page.overlay.append(editarVer_Equipo)
    page.overlay.append(editarVer_Cliente)
    page.overlay.append(agregar_Equipo)
    page.overlay.append(agregar_Cliente)
    page.overlay.append(ver_historialEquipo)
    page.overlay.append(ver_ResultadoBusqueda)
    page.theme_mode = ft.ThemeMode.DARK
    page.add(
        ventana
    )

ft.app(target=main)