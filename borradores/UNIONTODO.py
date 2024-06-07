import flet as ft
import datetime
import json
import re
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
        ventana.update()
    def inicioExitoso(e):
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
                                   height=35, bgcolor='#3F4450', on_click=inicioExitoso)
    botonRecuperar = ft.ElevatedButton(content=ft.Text('Enviar Clave', color='white', weight='w400', ), width=250,
                                       height=35, bgcolor='#3F4450', on_click=claveEnviada)



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
    def close_agEq(e):
        nombreNuevoEquipo.value = ""
        marcaNuevoEquipo.value = ""
        nombreClienteNuevoEquipo.value = ""
        estadoNuevoEquipo.value = ""
        observacionNuevoEquipo.value = ""
        agregar_Equipo.open = False
        agregar_Equipo.update()

    # Funcion para abrir y cerrar el cuadro de dialogo de Confirmar
    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()
    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    # Funcion oara cambiar la fecha, o si cancela
    def change_date(e):
        dateString = (date_picker.value.strftime("%d/%m/%Y"))
        date_button.text = dateString
        date_button.update()
    def date_picker_dismissed(e):
        dateString = (date_picker.value.strftime("%d/%m/%Y"))
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
        nuevaObservacion.disabled = True
        nuevaObservacion.update()
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
        with open('prueba.json', 'r') as file:
            data = json.load(file)
        equipos_Listos = []
        for i in data:
            estadoJson = i['estado']
            estadoListoEquipoLabel = ft.Text("En estado: ", color='#3F4450', size=17, weight='w400',spans=[ft.TextSpan(estadoJson,ft.TextStyle(color='#3EC99D', weight='w500'))])
            nombreClienteEquipoLabel = ft.Text(i['nombre_cliente'], color='#3F4450', size=17, weight='w400')
            nombreEquipoLabel = ft.Text(i['modelo'], color='#3F4450', size=19, weight='w500')
            observaciones = ft.Text(i['observaciones'], color='#3F4450', size=17, weight='w400')
            if estadoJson == 'LISTO':
                equipos_Listos.append(
                    ft.Container(
                        ft.Container(ft.Column([
                            ft.Row([nombreEquipoLabel, ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED,icon_color="#3EC99D",icon_size=30,tooltip="Borrar Equipo",on_click=open_dlg_modal,), ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([estadoListoEquipoLabel,ft.Container(ft.Column([ft.ElevatedButton(content=ft.Text('Ver/Editar', color='white',weight='w100', ),bgcolor='#3F4450', on_hover=on_hover, on_click=lambda e, equipo=i: show_bs(e, equipo))]))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            nombreClienteEquipoLabel,
                            observaciones,
                        ], spacing=0), width=560),
                        border=ft.border.all(0.5, color='#8993A7'), width=665, border_radius=3,padding=ft.padding.only(25, 7, 20, 7)
                    )
                )
        return equipos_Listos

    # Crear tarjetas de información de los clientes pendientes
    def leerClientesPendiente():
        with open('prueba.json', 'r') as file:
            data = json.load(file)
        equipos_pendientes = []
        for i in data:
            estadoJson = i['estado']
            estadoEquipoLabel = ft.Text("En estado: ", color='#3F4450', size=17, weight='w400',spans=[ft.TextSpan(estadoJson, ft.TextStyle(color='#FF914D', weight='w500'))])
            nombreClienteEquipoLabel = ft.Text(i['nombre_cliente'], color='#3F4450', size=17, weight='w400')
            nombreEquipoLabel = ft.Text(i['modelo'], color='#3F4450', size=19, weight='w500')
            observaciones = ft.Text(i['observaciones'], color='#3F4450', size=17, weight='w400')
            if estadoJson != 'LISTO':
                equipos_pendientes.append(
                    ft.Container(
                        ft.Container(ft.Column([ft.Row([nombreEquipoLabel, ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED,icon_color="#3EC99D",icon_size=30,tooltip="Borrar Equipo",on_click=open_dlg_modal,), ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([estadoEquipoLabel,ft.Container(ft.Column([ft.ElevatedButton(content=ft.Text('Ver/Editar', color='white',weight='w100', ),bgcolor='#3F4450', on_hover=on_hover, on_click=lambda e, equipo=i: show_bs(e, equipo))]))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            nombreClienteEquipoLabel,
                            observaciones
                        ], spacing=0), width=560),border=ft.border.all(0.5, color='#8993A7'), width=665, border_radius=3,padding=ft.padding.only(25, 7, 20, 7)
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

    # Pestaña para confirmar borrado
    dlg_modal = ft.AlertDialog(
        modal=True,
        bgcolor='#3F4450',
        title=ft.Text("Confirmar"),
        content=ft.Text("¿Estas seguro de eliminar este equipo?"),
        actions=[ft.TextButton("Si", on_click=close_dlg),ft.TextButton("No", on_click=close_dlg),],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    # Seleccionador de Fecha
    date_picker = ft.DatePicker(on_change=change_date,on_dismiss=date_picker_dismissed,field_label_text="Ingresa una fecha",first_date=datetime.datetime(2024, 6, 1),
                                )
    # Boton para el seleccionador de fecha
    date_button = ft.ElevatedButton("Fecha Actualización",icon=ft.icons.CALENDAR_MONTH,on_click=lambda _: date_picker.pick_date(),width=250,color='#3EC99D',disabled=True,
    )

    # Header Principal
    header = ft.Row([
        ft.Container(ft.Row([ft.Container(ft.Image(src='../assets/logo.png', width=100), padding=ft.padding.only(10, 5)),ft.Container(ft.Image(src='../assets/logoName.png', width=245), padding=ft.padding.only(15, 15))])),
        ft.Container(ft.Row([busquedaText,ft.Container(ft.IconButton(icon=ft.icons.EXIT_TO_APP, icon_color='#3EC99D', icon_size=45,tooltip="Cerrar Sesión", padding=ft.padding.only(60, 0, 20)))])
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

    # Ya editanto
    nuevoEstado = ft.TextField(label="Nuevo Estado", disabled=True)
    nuevaObservacion = ft.TextField(label="Actualizar información", multiline=True, max_lines=3, disabled=True)
    actualizarInfoButton = ft.ElevatedButton(content=ft.Text('Actualizar Datos', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, tooltip="Actualiza los cambios", disabled=True)
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


    # Formulario agregar computadora variables ----------------------------------------------------------------------
    nombreNuevoEquipo = ft.TextField(label="Nombre de equipo")
    marcaNuevoEquipo = ft.TextField(label="Marca")
    nombreClienteNuevoEquipo = ft.TextField(label="Nombre Cliente", width=290)
    estadoNuevoEquipo = ft.TextField(label="Estado")
    observacionNuevoEquipo = ft.TextField(label="Observaciones")
    # Botones para agregar

    aceptaryPdfButton = ft.ElevatedButton(content=ft.Text('Registrar y Crear PDF', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, tooltip="Registra y Crea un PDF")
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
        ),open=False, is_scroll_controlled=True
    )

    # Pestaña Home Principal
    homeTab = ft.Container(
                ft.Column(controls=[
                    header,
                    ft.Divider(height=5, thickness=1),
                    # Texto titular
                    ft.Row([ft.Text(" "),ft.Text(" "), ft.Container(ft.Text('Bienvenido Nuevamente ', width=380, size=22, weight='w250', text_align='center',color='#3F4450',spans=[ft.TextSpan("Usuario", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center,padding=ft.padding.only(0,10,0,5)),
                            ft.ElevatedButton(content=ft.Text('Agregar Equipo',color='white',weight='w200',),bgcolor='#3F4450', on_hover=on_hover, on_click=show_agEq)],alignment=ft.MainAxisAlignment.SPACE_AROUND),

                    # Contenedores de los dos cuadritos principales
                    ft.Container(
                        ft.Row([
                            ft.Container(ft.Column([
                                ft.Container(ft.Text("Equipos ", width=380, size=20, weight='w250', text_align='center', color='#3F4450',spans=[ft.TextSpan("Pendientes", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center,padding=ft.padding.only(0,0,0,20)),
                                # Columna para desplegar las tarjetas de información en equipos pendientes
                                ft.Container(ft.Column(controls=leerClientesPendiente(), scroll=ft.ScrollMode.ALWAYS, height=415))
                            ]),width=670, height=495, border_radius=30, border=ft.border.all(1.5, color='#8993A7'), padding=ft.padding.all(10)
                            ),
                            # Segundo contenedor
                            ft.Container(ft.Column([
                                ft.Container(ft.Text("Equipos ", width=380, size=20, weight='w250', text_align='center',color='#3F4450',spans=[ft.TextSpan("Por Retirar", ft.TextStyle(color='#3EC99D'))]),alignment=ft.alignment.center, padding=ft.padding.only(0, 0, 0, 20)),

                                # Columna para desplegar las tarjetas de información de equipos listos
                                ft.Container(ft.Column(controls=leerClientesListo(), scroll=ft.ScrollMode.ALWAYS, height=415))
                            ]), width=670, height=495, border_radius=30, border=ft.border.all(1.5, color='#8993A7'),padding=ft.padding.all(10)
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),)
                ]), visible= True, width=1400, height=715
    )

    clienteTab = ft.Container(
                ft.Column(controls=[
                    header,
                    ft.Divider(height=5, thickness=1),
                    ft.Container(
                        ft.Text('Pestaña ', width=380, size=22, weight='w250', text_align='center',color='#3F4450',
                                spans=[ft.TextSpan("Clientes", ft.TextStyle(color='#3EC99D'))]),
                        alignment=ft.alignment.center, padding=ft.padding.only(0, 10))
                ]), visible= False, width=1400, height=715
    )


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

    perfilTab = ft.Container(
                ft.Column(controls=[
                    header,
                    ft.Divider(height=5, thickness=1),
                    ft.Container(
                        ft.Text('Técnico Administrador ', width=380, size=22, weight='w250', text_align='center', color='#3F4450',
                                spans=[ft.TextSpan("Usuario", ft.TextStyle(color='#3EC99D'))]),
                        alignment=ft.alignment.center, padding=ft.padding.only(0, 10))
                ]), visible= False, width=1400, height=715
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
    page.overlay.append(date_picker)
    #page.add(inicio)
    page.add(
        ventana
    )

ft.app(target=main)