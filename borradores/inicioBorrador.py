import flet as ft
import datetime
import json
def main(page: ft.page):
    page.update()

    def changetab(e):
        # GET INDEX TAB
        my_index = e.control.selected_index
        homeTab.visible = True if my_index == 0 else False
        clienteTab.visible = True if my_index == 1 else False
        historialTab.visible = True if my_index == 2 else False
        perfilTab.visible = True if my_index == 3 else False
        page.update()

    def on_hover(e):
        e.control.bgcolor = "#3EC99D" if e.data == "true" else "#3F4450"
        e.control.update()

    def show_bs(e):
        editarVer_Equipo.open = True
        editarVer_Equipo.update()

    def close_bs(e):
        editarVer_Equipo.open = False
        editarVer_Equipo.update()


    def show_agEq(e):
        agregar_Equipo.open = True
        agregar_Equipo.update()

    def close_agEq(e):
        agregar_Equipo.open = False
        agregar_Equipo.update()

    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def change_date(e):
        dateString = (date_picker.value.strftime("%d/%m/%Y"))
        date_button.text = dateString
        date_button.update()
        print(dateString)

    def date_picker_dismissed(e):
        dateString = (date_picker.value.strftime("%d/%m/%Y"))
        date_button.text=dateString
        date_button.update()
        print(dateString)

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

    def leerClientesListo():
        with open('prueba.json', 'r') as file:
            data = json.load(file)

        equipos_Listos = []

        for i in data:
            estadoJson = i['estado']
            estadoListoEquipoLabel = ft.Text("En estado: ", color='#3F4450', size=17, weight='w400',
                                             spans=[ft.TextSpan(estadoJson,
                                                                ft.TextStyle(color='#3EC99D', weight='w500'))])
            nombreClienteEquipoLabel = ft.Text(i['nombre_cliente'], color='#3F4450', size=17, weight='w400')
            nombreEquipoLabel = ft.Text(i['modelo'], color='#3F4450', size=19, weight='w500')
            if estadoJson == 'LISTO':
                equipos_Listos.append(
                    ft.Container(
                        ft.Container(ft.Column([
                            ft.Row([nombreEquipoLabel, ft.IconButton(
                                icon=ft.icons.DELETE_FOREVER_ROUNDED,
                                icon_color="#3EC99D",
                                icon_size=30,
                                tooltip="Borrar Equipo",
                                on_click=open_dlg_modal,
                            ), ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([estadoListoEquipoLabel,
                                    ft.Container(ft.Column([
                                        ft.ElevatedButton(
                                            content=ft.Text('Ver/Editar', color='white',
                                                            weight='w100', ),
                                            bgcolor='#3F4450', on_hover=on_hover, on_click=show_bs)
                                    ]))
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            nombreClienteEquipoLabel,
                        ], spacing=0), width=560),
                        border=ft.border.all(0.5, color='#8993A7'), width=665, border_radius=3,
                        padding=ft.padding.only(25, 7, 20, 7)
                    )
                )
        return equipos_Listos

    def leerClientesPendiente():
        with open('prueba.json', 'r') as file:
            data = json.load(file)

        equipos_pendientes = []

        for i in data:
            estadoJson = i['estado']
            estadoEquipoLabel = ft.Text("En estado: ", color='#3F4450', size=17, weight='w400',
                                        spans=[ft.TextSpan(estadoJson, ft.TextStyle(color='#FF914D', weight='w500'))])
            nombreClienteEquipoLabel = ft.Text(i['nombre_cliente'], color='#3F4450', size=17, weight='w400')
            nombreEquipoLabel = ft.Text(i['modelo'], color='#3F4450', size=19, weight='w500')
            if estadoJson != 'LISTO':
                equipos_pendientes.append(
                    ft.Container(
                        ft.Container(ft.Column([
                            ft.Row([nombreEquipoLabel, ft.IconButton(
                                icon=ft.icons.DELETE_FOREVER_ROUNDED,
                                icon_color="#3EC99D",
                                icon_size=30,
                                tooltip="Borrar Equipo",
                                on_click=open_dlg_modal,
                            ), ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([estadoEquipoLabel,
                                    ft.Container(ft.Column([
                                        ft.ElevatedButton(
                                            content=ft.Text('Ver/Editar', color='white',
                                                            weight='w100', ),
                                            bgcolor='#3F4450', on_hover=on_hover, on_click=show_bs)
                                    ]))
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            nombreClienteEquipoLabel,
                        ], spacing=0), width=560),
                        border=ft.border.all(0.5, color='#8993A7'), width=665, border_radius=3,
                        padding=ft.padding.only(25, 7, 20, 7)
                    )
                )
        return equipos_pendientes



    page.navigation_bar = ft.NavigationBar(
        bgcolor="#3F4450",
        height=65,
        indicator_color=ft.colors.TRANSPARENT,
        overlay_color='#3EC99D',
        indicator_shape=ft.ContinuousRectangleBorder(radius=20),
        on_change=changetab,
        selected_index=0,
        destinations=[
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.HOME, size=35), selected_icon_content=ft.Icon(name=ft.icons.HOME, color='#3EC99D', size=45)),
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.PEOPLE, size=35), selected_icon_content=ft.Icon(name=ft.icons.PEOPLE, color='#3EC99D', size=45)),
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.NOTE_OUTLINED, size=35), selected_icon_content=ft.Icon(name=ft.icons.NOTE_ROUNDED, color='#3EC99D', size=45)),
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.PERSON_PIN, size=35), selected_icon_content=ft.Icon(name=ft.icons.PERSON_PIN_SHARP, color='#3EC99D', size=45)),
        ],
    )

    busquedaText = ft.TextField(width=650, height=35, label="Buscar Cliente/Equipo/ID", color='#3F4450',border_color='#3F4450',border_radius=20,
                                label_style=ft.TextStyle(color='#3F4450'), prefix_icon=ft.icons.SEARCH, focused_border_color='#3EC99D')


    nombreEquipo = "LAPTOP Lenovo Series 15A"
    estadoEquipo = "En espera"
    estadoEquipoListo = "LISTO"
    nombreCliente = "Paul Penafiel"
    observaciones = "Pantalla rota, necesita un cambio de pantalla en formato asdad"
    id_equipo = "IMP1234"
    marcaEquipo = "EPSON"
    celularCliente = "0987777777"


    nombreEquipoLabel = ft.Text(nombreEquipo, color='#3F4450', size=19, weight='w500')
    estadoEquipoLabel = ft.Text("En estado: ", color='#3F4450', size=17, weight='w400',
                                                    spans=[ft.TextSpan(estadoEquipo, ft.TextStyle(color='#FF914D', weight='w500'))])
    estadoListoEquipoLabel = ft.Text("En estado: ", color='#3F4450', size=17, weight='w400',
                           spans=[ft.TextSpan(estadoEquipoListo, ft.TextStyle(color='#3EC99D', weight='w500'))])
    nombreClienteEquipoLabel = ft.Text(nombreCliente, color='#3F4450', size=17, weight='w400')
    descriEquipoLabel = ft.Text("Observaciones: ", color='#3F4450', size=15, weight='w500',
                                                    spans=[ft.TextSpan(observaciones, ft.TextStyle(color='#3F4450', weight='w400'))], max_lines=5)

    # Formulario de Editar
    nombreEquipoEdit = ft.TextField(label="Nombre de equipo", value=nombreEquipo, read_only=True)
    nuevaObservacion = ft.TextField(label="Actualizar información", multiline=True, max_lines=5, disabled=True)
    nuevoEstado = ft.TextField(label="Nuevo Estado", disabled=True)
    equipoMarcaEdit = ft.TextField(label="Marca", value=marcaEquipo, read_only=True)
    nombreClienteEdit = ft.TextField(label="Nombre Cliente", value=nombreCliente, width=290, read_only=True)

    # Botones Formulario Editar
    editarButton = ft.ElevatedButton(content=ft.Text('Editar Información', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, on_click=editarFormulario)
    cerrarFormularioButton = ft.ElevatedButton(content=ft.Text('Cerrar Formulario', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, on_click=close_bs)
    notificarClienteButton = ft.ElevatedButton(content=ft.Text('Notificar Cliente', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, tooltip="Enviar notificacion con estado actual a cliente")
    # Ya editanto
    actualizarInfoButton = ft.ElevatedButton(content=ft.Text('Actualizar Datos', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, tooltip="Actualiza los cambios", disabled=True)
    cancelarEditButton = ft.ElevatedButton(content=ft.Text('Cancelar Cambios', color='white', weight='w300'),bgcolor='#3F4450', on_hover=on_hover, disabled=True, on_click=cancelarEditFormulario)


    date_picker = ft.DatePicker(
        on_change=change_date,
        on_dismiss=date_picker_dismissed,
        field_label_text="Ingresa una fecha",
        first_date=datetime.datetime(2024, 6, 1),
    )

    date_button = ft.ElevatedButton(
        "Fecha Actualización",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: date_picker.pick_date(),
        width=250,
        color='#3EC99D',
        disabled=True,
    )


    dlg_modal = ft.AlertDialog(
        modal=True,
        bgcolor='#3F4450',
        title=ft.Text("Confirmar"),
        content=ft.Text("¿Estas seguro de eliminar este equipo?"),
        actions=[
            ft.TextButton("Si", on_click=close_dlg),
            ft.TextButton("No", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    header = ft.Row([
                        ft.Container(
                            ft.Row([
                                ft.Container(ft.Image(src='../assets/logo.png', width=100), padding=ft.padding.only(10,5)),
                                ft.Container(ft.Image(src='../assets/logoName.png', width=245), padding=ft.padding.only(15,15))
                            ])),
                        ft.Container(
                            ft.Row([
                                busquedaText,
                                ft.Container(ft.IconButton(icon = ft.icons.EXIT_TO_APP,icon_color='#3EC99D',icon_size=45,tooltip="Cerrar Sesión",
                                                           padding=ft.padding.only(60,0,20))
                          )])
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


    editarVer_Equipo = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    # Contenido del formulario antes de los botones
                    ft.Container(ft.Text("Información de ", size=35, spans=[ft.TextSpan("Equipo", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center),

                    # ID ---------------------------------------------------------------------------------------
                    ft.Container(ft.Text("ID: ", size=22,spans=[ft.TextSpan(id_equipo, ft.TextStyle(color='#3EC99D'))]),alignment=ft.alignment.center),

                    # Boton Ver Historial ----------------------------------------------------------------------
                    ft.Container(ft.TextButton("Ver historial", style=ft.ButtonStyle(color=ft.colors.WHITE)), alignment=ft.alignment.center_right),

                    # TextField nombre del equipo --------------------------------------------------------------
                    ft.Container(nombreEquipoEdit, bgcolor=ft.colors.WHITE10),

                    # Text Fields con la marca, y el nombre del cliente ----------------------------------------
                    ft.Container(ft.Row([
                        ft.Container(equipoMarcaEdit,bgcolor=ft.colors.WHITE10),
                        ft.Container(nombreClienteEdit, bgcolor=ft.colors.WHITE10),
                    ])),

                    # Boton para seleccionar la fecha. Y textfield del Número de contacto del cliente -----------
                    ft.Container(ft.Row([
                        ft.Container(date_button, padding=ft.padding.only(25)),
                        ft.Container(ft.TextField(label="Celular Contacto", value=celularCliente, read_only=True),bgcolor=ft.colors.WHITE10, width=290),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),),

                    # Label que muestra el estado actual, y text field para modificar el estado -----------------
                    ft.Container(ft.Row([
                        ft.Container(ft.Text("Estado Actual: ", size=18,spans=[ft.TextSpan(estadoEquipo, ft.TextStyle(color='#3EC99D'))]),padding=ft.padding.only(50,13,50,13), bgcolor=ft.colors.WHITE10, border_radius=5,border=ft.border.all(1, color=ft.colors.BLACK)),
                        ft.Container(nuevoEstado,bgcolor=ft.colors.WHITE10, width=290),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ),

                    # Texto que muestra la ultima observacion --------------------------------------------------
                    ft.Container(ft.Text("Observaciones: ", color='#3EC99D', size=16,
                                        spans=[ft.TextSpan(observaciones, ft.TextStyle(color=ft.colors.WHITE))], max_lines=4), bgcolor=ft.colors.WHITE10, border_radius=5,
                                 border=ft.border.all(1, color=ft.colors.BLACK), padding=ft.padding.all(12)),

                    # Text Field para la nueva observacion -----------------------------------------------------
                    ft.Container(nuevaObservacion, bgcolor=ft.colors.WHITE10),

                    # ----------------------------Botones Editar------------------------------------------------
                    ft.Container(ft.Row([
                        editarButton,
                        notificarClienteButton,
                        cerrarFormularioButton,
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND), padding=ft.padding.only(0,20)),
                    # ----------------------------Botones Ya editando------------------------------------------------
                    ft.Container(ft.Row([
                        actualizarInfoButton,
                        cancelarEditButton,
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND), padding=ft.padding.only(0,20)),
                ],
                tight=True, spacing=8
            ),
            padding=20, height=700, width=700,
        ),
        open=False, is_scroll_controlled=True, dismissible=False
    )

    agregar_Equipo = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Container(ft.Text("Registrar Nuevo ", size=35,
                                         spans=[ft.TextSpan("Equipo", ft.TextStyle(color='#3EC99D'))]),
                                 alignment=ft.alignment.center),
                    ft.Container(
                        ft.Text("ID: ", size=22, spans=[ft.TextSpan(id_equipo, ft.TextStyle(color='#3EC99D'))]),
                        alignment=ft.alignment.center),
                    ft.Container(ft.TextField(label="Nombre de equipo"), bgcolor=ft.colors.WHITE10),
                    ft.Container(ft.Row([
                        ft.Container(ft.TextField(label="Marca"), bgcolor=ft.colors.WHITE10),
                        ft.Container(ft.TextField(label="Nombre Cliente", width=290),
                                     bgcolor=ft.colors.WHITE10),
                    ])),
                    ft.Container(ft.Row([
                        ft.Container(
                            ft.TextField(label="Celular Contacto", width=300, read_only=True),
                            bgcolor=ft.colors.WHITE10),
                    ]))
                ],
                tight=True, spacing=8
            ),
            padding=20, height=700, width=700
        ),
        open=False, is_scroll_controlled=True
    )

    homeTab = ft.Container(
                ft.Column(controls=[
                    header,
                    ft.Divider(height=5, thickness=1),
                    # Texto titular
                    ft.Row([ft.Text(" "),ft.Text(" "), ft.Container(ft.Text('Bienvenido Nuevamente ', width=380, size=22, weight='w250', text_align='center',color='#3F4450',
                                        spans=[ft.TextSpan("Usuario", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center,
                                 padding=ft.padding.only(0,10,0,5)),
                            ft.ElevatedButton(content=ft.Text('Agregar Equipo',color='white',weight='w200',),bgcolor='#3F4450', on_hover=on_hover, on_click=show_agEq)],
                           alignment=ft.MainAxisAlignment.SPACE_AROUND),


                    # Contenedores de los dos cuadritos principales
                    ft.Container(
                        ft.Row([
                            ft.Container(ft.Column([
                                ft.Container(ft.Text("Equipos ", width=380, size=20, weight='w250', text_align='center', color='#3F4450',
                                        spans=[ft.TextSpan("Pendientes", ft.TextStyle(color='#3EC99D'))]), alignment=ft.alignment.center,
                                             padding=ft.padding.only(0,0,0,20)),

                                # Columna para desplegar las tarjetas de información en equipos pendientes
                                ft.Container(ft.Column(controls=leerClientesPendiente(), scroll=ft.ScrollMode.ALWAYS, height=415
                                ))
                            ]),width=670, height=495, border_radius=30, border=ft.border.all(2, color='#8993A7'), padding=ft.padding.all(10)
                            ),


                            # Segundo contenedor
                            ft.Container(ft.Column([
                                ft.Container(ft.Text("Equipos ", width=380, size=20, weight='w250', text_align='center',
                                                     color='#3F4450',
                                                     spans=[ft.TextSpan("Por Retirar", ft.TextStyle(color='#3EC99D'))]),
                                             alignment=ft.alignment.center, padding=ft.padding.only(0, 0, 0, 20)),



                                # Columna para desplegar las tarjetas de información de equipos listos
                                ft.Container(ft.Column(controls=leerClientesListo(), scroll=ft.ScrollMode.ALWAYS, height=415
                                ))
                            ]), width=670, height=495, border_radius=30, border=ft.border.all(2, color='#8993A7'),
                                padding=ft.padding.all(10)
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    )
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
            content=ft.Column([
                homeTab,
                clienteTab,
                historialTab,
                perfilTab,
                date_button
            ]),
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
    page.add(inicio)


ft.app(target=main)