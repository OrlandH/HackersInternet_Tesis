import flet as ft
import datetime
import re
import requests

valorNombreAdmin = ""
valorCelAdmin = ""
valCorreoAdmin = ""
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
        url = "https://tesis-kphi.onrender.com/api/admin/login"
        headers = {'Content-Type': 'application/json'}
        data = {
            "correo": correoElectronico.value,
            "password": passLogin.value
        }

        try:
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
                print(f"Error en el login: {response.status_code}")
                label.value = "Credenciales Incorrectas"
                passLogin.value = ''
                page.update()
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud: {e}")
            label.value="Error con el servidor"
            passLogin.value = ''
            page.update()
    def recuperar_admin(e):
        url = "https://tesis-kphi.onrender.com/api/admin/recuperar-password"
        headers = {'Content-Type': 'application/json'}
        data = {
            "correo": correoElectronico.value,
        }
        try:
            response = requests.post(url, json=data, headers=headers)

            # Verificar si la solicitud tuvo éxito
            if response.status_code == 200:
                response_data = response.json()
                print(response_data.get("msg"))
                claveEnviada(e=None)
            else:
                print(f"Error en el login: {response.status_code}")
                label2.value = "Correo Incorrecto"
                correoElectronico.value = ''
                page.update()
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud: {e}")
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
                        ft.Image(src='../assets/logo.png', width=350, ),
                        padding=ft.padding.only(180, 1)
                    ),
                    ft.Container(
                        ft.Image(src='../assets/logoName.png', width=350, ),
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
                        ft.Image(src='../assets/logo.png', width=350, ),
                        padding=ft.padding.only(180, 1)
                    ),
                    ft.Container(
                        ft.Image(src='../assets/logoName.png', width=350, ),
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
                        ft.Image(src='../assets/logo.png', width=350, ),
                        padding=ft.padding.only(180, 1)
                    ),
                    ft.Container(
                        ft.Image(src='../assets/logoName.png', width=350, ),
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

    # Funcion para que el formulario de editar se abra con la información actual, y abajo para cerrar
    def show_bs(e, equipo):
        nombreEquipoEdit.value = equipo['modelo']
        id_EquipoEdit.value = equipo['id']
        estadoEquipoEdit.value = equipo['estado']
        equipoMarcaEdit.value = equipo['marca']
        nombreClienteEdit.value = equipo['nombre_cliente']
        observacionActualEdit.value = equipo['observaciones']
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

    # Funcion oara cambiar la fecha, o si cancela
    def change_date(e):
        dateString = (date_picker.value.strftime("%Y-%m-%d"))
        date_button.text = dateString
        print(dateString)
        date_button.update()
    def date_picker_dismissed(e):
        dateString = (date_picker.value.strftime("%Y-%m-%d"))
        date_button.text=dateString
        date_button.update()
        print(dateString)

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
        date_button.disabled = False
        date_button.update()
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
        nuevaObservacion.disabled = True
        nuevaObservacion.update()
        nuevoEstado.clean()
        nuevoEstado.disabled = True
        nuevoEstado.update()
        equipoMarcaEdit.read_only = True
        equipoMarcaEdit.update()
        nombreClienteEdit.read_only = True
        nombreClienteEdit.update()
        date_button.disabled = True
        date_button.update()
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
        url = "https://tesis-kphi.onrender.com/api/equipos"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            data = "Error al Obtener datos"
        equipos_Listos = []
        for i in data:
            estadoJson = i['estado']
            estadoListoEquipoLabel = ft.Text("En estado: ", color='#3F4450', size=17, weight='w400',spans=[ft.TextSpan(estadoJson,ft.TextStyle(color='#3EC99D', weight='w500'))])
            nombreClienteEquipoLabel = ft.Text(i['nombre_cliente'], color='#3F4450', size=17, weight='w400')
            nombreEquipoLabel = ft.Text(i['modelo'], color='#3F4450', size=19, weight='w500')
            observaciones = ft.Text("Observaciones:", color='#3EC99D', size=17, weight='w400',spans=[ft.TextSpan(i['observaciones'], ft.TextStyle(color='#3F4450', weight='w400'))])
            if estadoJson.lower() == 'listo':
                equipos_Listos.append(
                    ft.Container(
                        ft.Container(ft.Column([
                            ft.Row([nombreEquipoLabel, ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED,icon_color="#3EC99D",icon_size=30,tooltip="Borrar Equipo",on_click=lambda e, equipo=i: open_dlg_modal(e, equipo),), ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([ft.Container(estadoListoEquipoLabel, padding=ft.padding.only(0,-20)),ft.Container(ft.ElevatedButton(content=ft.Text('Ver/Editar', color='white',weight='w100', ),bgcolor='#3F4450', on_hover=on_hover, on_click=lambda e, equipo=i: show_bs(e, equipo)))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Container(nombreClienteEquipoLabel, padding=ft.padding.only(0,-15)),
                            observaciones,
                        ], spacing=0), width=560),
                        border=ft.border.all(0.5, color='#8993A7'), width=665, border_radius=3,padding=ft.padding.only(25, 7, 20, 7)
                    )
                )
        return equipos_Listos

    # Crear tarjetas de información de los clientes pendientes
    def leerClientesPendiente():
        url = "https://tesis-kphi.onrender.com/api/equipos"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            data = "Error al Obtener datos"
        equipos_pendientes = []
        for i in data:
            estadoJson = i['estado']
            estadoEquipoLabel = ft.Text("En estado: ", color='#3F4450', size=17, weight='w400',spans=[ft.TextSpan(estadoJson, ft.TextStyle(color='#FF914D', weight='w500'))])
            nombreClienteEquipoLabel = ft.Text(i['nombre_cliente'], color='#3F4450', size=17, weight='w400')
            nombreEquipoLabel = ft.Text(i['modelo'], color='#3F4450', size=19, weight='w500')
            observaciones = ft.Text("Observaciones:", color='#3EC99D', size=17, weight='w400',spans=[ft.TextSpan(i['observaciones'], ft.TextStyle(color='#3F4450', weight='w400'))])
            if estadoJson.lower() != 'listo':
                equipos_pendientes.append(
                    ft.Container(
                        ft.Container(ft.Column([ft.Row([nombreEquipoLabel,
                                                        ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED,
                                                                      icon_color="#3EC99D", icon_size=30,
                                                                      tooltip="Borrar Equipo",
                                                                      on_click=lambda e, equipo=i: open_dlg_modal(e, equipo), ), ],
                                                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                ft.Row(
                                                    [ft.Container(estadoEquipoLabel, padding=ft.padding.only(0, -20)),
                                                     ft.Container(ft.ElevatedButton(
                                                         content=ft.Text('Ver/Editar', color='white', weight='w100', ),
                                                         bgcolor='#3F4450', on_hover=on_hover,
                                                         on_click=lambda e, equipo=i: show_bs(e, equipo)))],
                                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                ft.Container(nombreClienteEquipoLabel, padding=ft.padding.only(0, -15)),
                                                observaciones
                                                ], spacing=0), width=560), border=ft.border.all(0.5, color='#8993A7'),
                        width=665, border_radius=3, padding=ft.padding.only(25, 7, 20, 7)
                    )
                )
        return equipos_pendientes

    # Funciones Globales ------------------------------------------------------------------------------------------------------------------------
    # Tabs de navegación
    page.navigation_bar = ft.NavigationBar(bgcolor="#3F4450",height=65,indicator_color=ft.colors.TRANSPARENT,overlay_color='#3EC99D',indicator_shape=ft.ContinuousRectangleBorder(radius=20),on_change=changetab,selected_index=0,
        destinations=[
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.HOME, size=35), selected_icon_content=ft.Icon(name=ft.icons.HOME, color='#3EC99D', size=45)),
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.PEOPLE, size=35), selected_icon_content=ft.Icon(name=ft.icons.PEOPLE, color='#3EC99D', size=45)),
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.NOTE_OUTLINED, size=35), selected_icon_content=ft.Icon(name=ft.icons.NOTE_ROUNDED, color='#3EC99D', size=45)),
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.PERSON_PIN, size=35), selected_icon_content=ft.Icon(name=ft.icons.PERSON_PIN_SHARP, color='#3EC99D', size=45)),
        ],)

    # Barra de busqueda general
    busquedaText = ft.TextField(width=650, height=35, label="Buscar Cliente/Equipo/ID", color='#3F4450',border_color='#3F4450',border_radius=20,label_style=ft.TextStyle(color='#3F4450'), prefix_icon=ft.icons.SEARCH, focused_border_color='#3EC99D')
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def eliminarEquipo(e, id_Equipo):
        # Construye la URL con el ID del equipo
        url = f"https://tesis-kphi.onrender.com/api/equipo/{id_Equipo}"

        try:
            # Realiza la solicitud DELETE
            response = requests.delete(url)
            response.raise_for_status()  # Lanza una excepción si hay un error en la solicitud
            print(f"Equipo con ID {id_Equipo} eliminado correctamente.")
            contenedorEquiposListos.controls.clear()
            contenedorEquiposListos.controls.extend(leerClientesListo())
            contenedorEquiposListos.update()
            contenedorEquiposPendientes.controls.clear()
            contenedorEquiposPendientes.controls.extend(leerClientesPendiente())
            contenedorEquiposPendientes.update()
        except requests.exceptions.RequestException as err:
            print(f"Error al eliminar el equipo con ID {id_Equipo}: {err}")

        # Cierra el diálogo después de eliminar
        close_dlg(e)

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
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Seleccionador de Fecha
    date_picker = ft.DatePicker(on_change=change_date,on_dismiss=date_picker_dismissed,field_label_text="Ingresa una fecha",first_date=datetime.datetime(2024, 6, 1),
                                )
    # Boton para el seleccionador de fecha
    date_button = ft.ElevatedButton("Fecha Actualización",icon=ft.icons.CALENDAR_MONTH,on_click=lambda _: date_picker.pick_date(),width=250,color='#3EC99D',disabled=True,
    )

    # Header Principal
    header = ft.Row([
        ft.Container(ft.Row([ft.Container(ft.Image(src='../assets/logo.png', width=100), padding=ft.padding.only(10, 5)),ft.Container(ft.Image(src='../assets/logoName.png', width=245), padding=ft.padding.only(15, 15))])),
        ft.Container(ft.Row([busquedaText,ft.Container(ft.IconButton(icon=ft.icons.EXIT_TO_APP, icon_color='#3EC99D', icon_size=45,tooltip="Cerrar Sesión", padding=ft.padding.only(60, 0, 20), on_click=open_cerrarSesion_modal))])
        )], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


    # Formulario de Editar Variables Necesarias----------------------------------------------------------------------------------------------------------
    id_EquipoEdit = ft.TextField(value="", read_only=True, border="none", text_size=25)
    nombreEquipoEdit = ft.TextField(label="Nombre de equipo", value="", read_only=True)
    equipoMarcaEdit = ft.TextField(label="Marca", value="", read_only=True)
    estadoEquipoEdit = ft.TextField(value="", read_only=True, border="none", text_size=18)
    nombreClienteEdit = ft.TextField(label="Nombre Cliente", value="", width=290, read_only=True)
    observacionActualEdit = ft.TextField(value="", read_only=True, border="none", text_size=16, max_lines=3)

    # Botones Formulario Editar
    editarButton = ft.ElevatedButton(content=ft.Text('Editar Información', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, on_click=editarFormulario)
    cerrarFormularioButton = ft.ElevatedButton(content=ft.Text('Cerrar Formulario', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, on_click=close_bs)
    notificarClienteButton = ft.ElevatedButton(content=ft.Text('Notificar Cliente', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, tooltip="Enviar notificacion con estado actual a cliente")


    def validarClienteEditar(e):
        url = "https://tesis-kphi.onrender.com/api/clientes"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print("Error al Obtener datos")

        for cliente in data:
            if cliente['nombre'] == nombreClienteEdit.value:
                cliente_id = cliente['id']
                print(f"Si existe, ID del cliente: {cliente_id}")
                ActualizarEquipo(cliente_id)
                break
            else:
                open_ErrorModal(e)

    def ActualizarEquipo(id):
        url = f"https://tesis-kphi.onrender.com/api/equipo/{id_EquipoEdit.value}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "marca": equipoMarcaEdit.value,
            "modelo": nombreEquipoEdit.value,
            "estado": nuevoEstado.value,
            "id_cliente": id,
            "observaciones": nuevaObservacion.value
        }

        try:
            response = requests.put(url, json=data, headers=headers)
            response.raise_for_status()  # Verificar si la solicitud tuvo éxito
            print("Equipo editado exitosamente")
            open_ExitoModalEdit()
        except requests.exceptions.RequestException as e:
            print(e)
            open_ErrorModal(e)

    # Ya editanto
    nuevoEstado = ft.TextField(label="Nuevo Estado", disabled=True)
    nuevaObservacion = ft.TextField(label="Actualizar información", multiline=True, max_lines=3, disabled=True)
    actualizarInfoButton = ft.ElevatedButton(content=ft.Text('Actualizar Datos', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, tooltip="Actualiza los cambios", disabled=True, on_click=validarClienteEditar)
    cancelarEditButton = ft.ElevatedButton(content=ft.Text('Cancelar Cambios', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, disabled=True, on_click=cancelarEditFormulario)



    # Formulario de Ver/Editar datos Computadoras

    editarVer_Equipo = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    # Contenido del formulario antes de los botones
                    ft.Container(ft.Text("Información de ", size=35, spans=[ft.TextSpan("Equipo", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center, padding=ft.padding.only(0,25)),

                    # ID -------------------------------------------------------------
                    ft.Container(ft.Row([ft.Container(ft.Text("ID:", size=25, color='#3EC99D')),ft.Container(id_EquipoEdit)], alignment=ft.MainAxisAlignment.CENTER), padding=ft.padding.only(260,-25), margin=0),

                    # Boton Ver Historial --------------------------------------------
                    ft.Container(ft.TextButton("Ver historial", style=ft.ButtonStyle(color=ft.colors.WHITE)), alignment=ft.alignment.center_right, margin=0, padding=ft.padding.only(0,-15)),

                    # TextField nombre del equipo ------------------------------------
                    ft.Container(nombreEquipoEdit, bgcolor=ft.colors.WHITE10),

                    # Text Fields con la marca, y el nombre del cliente --------------
                    ft.Container(ft.Row([ft.Container(equipoMarcaEdit,bgcolor=ft.colors.WHITE10),ft.Container(nombreClienteEdit, bgcolor=ft.colors.WHITE10),])),

                    # Label que muestra el estado actual -----------------
                    ft.Container(ft.Row([ft.Container(ft.Text("Estado Actual:", size=18, color='#3EC99D'),padding=ft.padding.only(20,13,40,13)),ft.Container(estadoEquipoEdit)], alignment=ft.MainAxisAlignment.START)),

                    # Texto que muestra la ultima observacion --------------------------------------------------
                    ft.Container(ft.Row([ft.Container(ft.Text("Observaciones:", size=16, color='#3EC99D'),padding=ft.padding.only(20, 13, 40, 13)),ft.Container(observacionActualEdit, width=400)], alignment=ft.MainAxisAlignment.START)),

                    # Boton para seleccionar la fecha. Y textfield Para actualizar el estado -----------
                    ft.Container(ft.Row([date_button,ft.Container(nuevoEstado, bgcolor=ft.colors.WHITE10, width=290),],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)),

                    # Text Field para la nueva observacion -----------------------------------------------------
                    ft.Container(nuevaObservacion, bgcolor=ft.colors.WHITE10),

                    # ----------------------------Botones Editar------------------------------------------------
                    ft.Container(ft.Row([editarButton,notificarClienteButton,cerrarFormularioButton,], alignment=ft.MainAxisAlignment.SPACE_AROUND), padding=ft.padding.only(0,-1)),
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
        estadoNuevoEquipo.value = ""
        observacionNuevoEquipo.value = ""
        agregar_Equipo.open = False
        agregar_Equipo.update()

    def validarCliente(e):
        url = "https://tesis-kphi.onrender.com/api/clientes"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print("Error al Obtener datos")

        for cliente in data:
            if cliente['nombre'] == nombreClienteNuevoEquipo.value:
                cliente_id = cliente['id']
                print(f"Si existe, ID del cliente: {cliente_id}")
                registrarEquipo_PDF(cliente_id)
                break
            else:
                open_ErrorModal(e)
    def registrarEquipo_PDF(id):
        url = "https://tesis-kphi.onrender.com/api/equipo"
        headers = {'Content-Type': 'application/json'}
        data = {
            "marca": marcaNuevoEquipo.value,
            "modelo": nombreNuevoEquipo.value,
            "estado": estadoNuevoEquipo.value,
            "id_cliente": id,
            "observaciones": observacionNuevoEquipo.value,
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Verificar si la solicitud tuvo éxito
            print("Equipo creado exitosamente")
            open_ExitoModal()
        except requests.exceptions.RequestException as e:
            open_ErrorModal(e)


    # Formulario agregar computadora variables ----------------------------------------------------------------------
    nombreNuevoEquipo = ft.TextField(label="Nombre de equipo")
    marcaNuevoEquipo = ft.TextField(label="Marca")
    nombreClienteNuevoEquipo = ft.TextField(label="Nombre Cliente", width=290)
    estadoNuevoEquipo = ft.TextField(label="Estado")
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

                    # Marca del equipo y Nombre del cliente
                    ft.Container(ft.Row([ft.Container(marcaNuevoEquipo, bgcolor=ft.colors.WHITE10),ft.Container(nombreClienteNuevoEquipo,bgcolor=ft.colors.WHITE10),])),

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


    contenedorEquiposPendientes = ft.Column(controls=leerClientesPendiente(), scroll=ft.ScrollMode.ALWAYS, height=415)
    contenedorEquiposListos = ft.Column(controls=leerClientesListo(), scroll=ft.ScrollMode.ALWAYS, height=415)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Pestaña Home Principal
    homeTab = ft.Container(
                ft.Column(controls=[
                    header,
                    ft.Divider(height=5, thickness=1),
                    # Texto titular
                    ft.Row([ft.Text(" "),ft.Text(" "), ft.Container(ft.Text('Bienvenido Nuevamente ', width=380, size=22, weight='w250', text_align='center',color='#3F4450',spans=[ft.TextSpan("Técnico", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center,padding=ft.padding.only(0,10,0,5)),
                            ft.ElevatedButton(content=ft.Text('Agregar Equipo',color='white',weight='w300',),bgcolor='#3F4450', on_hover=on_hover, on_click=show_agEq )],alignment=ft.MainAxisAlignment.SPACE_AROUND),

                    # Contenedores de los dos cuadritos principales
                    ft.Container(
                        ft.Row([
                            ft.Container(ft.Column([
                                ft.Container(ft.Text("Equipos ", width=380, size=20, weight='w250', text_align='center', color='#3F4450',spans=[ft.TextSpan("Pendientes", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center,padding=ft.padding.only(0,0,0,20)),
                                # Columna para desplegar las tarjetas de información en equipos pendientes
                                contenedorEquiposPendientes
                            ]),width=670, height=495, border_radius=30, border=ft.border.all(1.5, color='#8993A7'), padding=ft.padding.all(10)
                            ),
                            # Segundo contenedor
                            ft.Container(ft.Column([
                                ft.Container(ft.Text("Equipos ", width=380, size=20, weight='w250', text_align='center',color='#3F4450',spans=[ft.TextSpan("Por Retirar", ft.TextStyle(color='#3EC99D'))]),alignment=ft.alignment.center, padding=ft.padding.only(0, 0, 0, 20)),

                                # Columna para desplegar las tarjetas de información de equipos listos
                                contenedorEquiposListos
                            ]), width=670, height=495, border_radius=30, border=ft.border.all(1.5, color='#8993A7'),padding=ft.padding.all(10)
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),)
                ]), visible= True, width=1400, height=715
    )




#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Pestaña de Clientes y sus funciones
    def leerClientesRegistrados():
        url = "https://tesis-kphi.onrender.com/api/clientes"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            data = "Error al Obtener datos"
        #with open('pruebaclientes.json', 'r') as file:
            #data = json.load(file)
        clientes_registrados = []
        for i in data:
            nombreClienteEquipoLabel = ft.Text(i['nombre'], color='#3F4450', size=19, weight='w500')
            celularClienteEquipoLabel = ft.Text(i['telefono'], color='#3F4450', size=17, weight='w400')
            emailClienteEquipoLabel = ft.Text(i['correo'], color='#3F4450', size=17, weight='w400')
            clientes_registrados.append(
                ft.Container(
                    ft.Container(ft.Column([ft.Row([nombreClienteEquipoLabel, ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED,icon_color="#3EC99D",icon_size=30,tooltip="Borrar Equipo",on_click=open_dlg_modal,), ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([ft.Container(celularClienteEquipoLabel, padding=ft.padding.only(0,-25)),ft.Container(ft.ElevatedButton(content=ft.Text('Ver/Editar', color='white',weight='w100', ),bgcolor='#3F4450', on_hover=on_hover, on_click=lambda e, equipo=i: show_bs(e, equipo)))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(emailClienteEquipoLabel, padding=ft.padding.only(0,-20))
                    ], spacing=0), width=560),border=ft.border.all(0.5, color='#8993A7'), width=665, border_radius=3,padding=ft.padding.only(25, 7, 20, 7)
                )
            )
        return clientes_registrados

    def show_agCliente(e):
        agregar_Cliente.open = True
        agregar_Cliente.update()
    def close_agCliente(e):
        nombreNuevoCliente.value = ""
        correoNuevoCliente.value = ""
        celulardelNuevoCliente.value = ""
        agregar_Cliente.open = False
        agregar_Cliente.update()

    # Formulario agregar cliente variables ----------------------------------------------------------------------
    nombreNuevoCliente = ft.TextField(label="Nombre del Cliente")
    correoNuevoCliente = ft.TextField(label="Correo Electronico del Cliente")
    celulardelNuevoCliente = ft.TextField(label="Celular del Cliente", width=290)

    # Botones para agregar

    registrarClientesButton = ft.ElevatedButton(content=ft.Text('Registrar Cliente', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, tooltip="Registra un nuevo cliente")
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

                    # Nombre  del Nuevo cliente
                    ft.Container(nombreNuevoCliente, bgcolor=ft.colors.WHITE10),

                    # Correo electronico y celular del cliente
                    ft.Container(ft.Row([ft.Container(correoNuevoCliente, bgcolor=ft.colors.WHITE10),
                                         ft.Container(celulardelNuevoCliente, bgcolor=ft.colors.WHITE10), ])),

                    # ----------------------------Botones Crear------------------------------------------------
                    ft.Container(
                        ft.Row([cancelarRegistroCliente, registrarClientesButton], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                        padding=ft.padding.only(0, 20)),
                ], tight=True, spacing=8
            ), padding=20, height=400, width=700
        ), open=False, is_scroll_controlled=True, dismissible=False
    )

    clienteTab = ft.Container(
                ft.Column(controls=[
                    header,
                    ft.Divider(height=5, thickness=1),
                    # Texto titular
                    ft.Row([ft.Text(" "), ft.Container(ft.Text('Registro de ', width=380, size=22, weight='w250', text_align='center',color='#3F4450',spans=[ft.TextSpan("Clientes", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center,padding=ft.padding.only(150,10,0,5)),
                            ft.ElevatedButton(content=ft.Text('Agregar Cliente',color='white',weight='w300',),bgcolor='#3F4450', on_hover=on_hover, on_click=show_agCliente)],alignment=ft.MainAxisAlignment.SPACE_AROUND),

                    # Contenedores de los dos cuadritos principales
                    ft.Container(
                            ft.Container(ft.Column([
                                ft.Container(ft.Text("Clientes ", width=380, size=20, weight='w250', text_align='center', color='#3F4450',spans=[ft.TextSpan("Registros", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center,padding=ft.padding.only(0,0,0,20)),
                                # Columna para desplegar las tarjetas de información en equipos pendientes
                                ft.Container(ft.Column(controls=leerClientesRegistrados(), scroll=ft.ScrollMode.ALWAYS, height=415))
                                ]),width=670, height=495, border_radius=30, border=ft.border.all(1.5, color='#8993A7'), padding=ft.padding.all(10)
                            ), alignment=ft.alignment.center
                    )
                ]), visible= True, width=1400, height=715
    )




# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Historial Tab de equipos
    historialTab = ft.Container(
                ft.Column(controls=[
                    header,
                    ft.Divider(height=5, thickness=1),
                    ft.Container(
                        ft.Text('Pestaña ', width=380, size=22, weight='w250', text_align='center', color='#3F4450',
                                spans=[ft.TextSpan("Historial", ft.TextStyle(color='#3EC99D'))]),
                        alignment=ft.alignment.center, padding=ft.padding.only(0, 10))
                ]), visible= False, width=1400, height=715
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
        url = "https://tesis-kphi.onrender.com/api/admin/login"
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
        url = f"https://tesis-kphi.onrender.com/api/admin/{id}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "correo": correoAdminText.value,
            "nombre": nombreAdminText.value,
            "telefono": celularAdminText.value,
            "password": passwordAdminText.value,
        }

        try:
            response = requests.put(url, json=data, headers=headers)
            response.raise_for_status()  # Verificar si la solicitud tuvo éxito
            print("Datos editados exitosamente")
            page.client_storage.set("nombre", nombreAdminText.value)
            page.client_storage.set("telefono", celularAdminText.value)
            page.client_storage.set("correo", correoAdminText.value)
            page.update()
            cancelarEditarInformacionAdmin(e)
        except requests.exceptions.RequestException as e:
            print(e)
            labelPasAdmin.value ='Error al Actualizar'

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
        url = "https://tesis-kphi.onrender.com/api/admin/login"
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
    def ActualizarPassAdmin(e, id):
        url = f"https://tesis-kphi.onrender.com/api/admin/{id}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "correo": page.client_storage.get('correo'),
            "nombre": page.client_storage.get('nombre'),
            "telefono": page.client_storage.get('telefono'),
            "password": passNuevaText.value,
        }

        try:
            response = requests.put(url, json=data, headers=headers)
            response.raise_for_status()  # Verificar si la solicitud tuvo éxito
            print("Contraseña editada exitosamente")
            passActualText.value = ''
            passActualText.update()
            passNuevaText.value = ''
            passNuevaText.update()
            passNuevaConf.value = ''
            passNuevaConf.update()
            CancelarActualizarPass(e)
        except requests.exceptions.RequestException as e:
            print(e)
            labelNuevaPass.value ='Error al Actualizar'


    nombreAdminText = ft.TextField(width=630, height=40, label="Nombre del Cliente", color='#3F4450',
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
                                    bgcolor='#3F4450', on_hover=on_hover, disabled=True, width=310, on_click=validarAdminEditar)
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
                                            bgcolor='#3F4450', on_hover=on_hover,width=310, on_click=ActualizarPass)
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
                                ft.Container(ft.Text("Información del ", width=380, size=20, weight='w250', text_align='center', color='#3F4450',spans=[ft.TextSpan("Técnico", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center,padding=ft.padding.only(0,0,0,20)),
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
                                        botonEditar, botonCancelarEditar
                                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)),
                                    ft.Container(ft.Divider(height=5, thickness=1, color='#8993A7')),
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
                                ], scroll=ft.ScrollMode.ALWAYS,height=520, spacing=10))
                                ]),width=670, height=550, border_radius=30, border=ft.border.all(1.5, color='#8993A7'), padding=ft.padding.only(20,40,20,20)
                            ), alignment=ft.alignment.center
                    )
                ]), visible= True, width=1400, height=715
    )

    inicio = ft.Container(
            content=ft.Column([homeTab,clienteTab,historialTab,perfilTab,date_button]),
        )


    page.window_width = 1400
    page.window_height = 780
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.bgcolor = ft.colors.WHITE
    page.title = 'Hackers Internet'
    page.window_resizable= False
    page.window_maximizable = False
    page.overlay.append(editarVer_Equipo)
    page.overlay.append(agregar_Equipo)
    page.overlay.append(agregar_Cliente)
    page.overlay.append(date_picker)
    page.add(
        ventana
    )

ft.app(target=main)