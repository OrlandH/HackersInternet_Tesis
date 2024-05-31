import flet as ft


def main(page: ft.page):
    page.update()

    def changetab(e):
        # GET INDEX TAB
        my_index = e.control.selected_index
        homeTab.visible = True if my_index == 0 else False
        clienteTab.visible = True if my_index == 1 else False
        equiposTab.visible = True if my_index == 2 else False
        historialTab.visible = True if my_index == 3 else False
        perfilTab.visible = True if my_index == 4 else False
        page.update()

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
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.PEOPLE_OUTLINE, size=35), selected_icon_content=ft.Icon(name=ft.icons.PEOPLE, color='#3EC99D', size=45)),
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.COMPUTER, size=35), selected_icon_content=ft.Icon(name=ft.icons.COMPUTER, color='#3EC99D', size=45)),
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.NOTE_OUTLINED, size=35), selected_icon_content=ft.Icon(name=ft.icons.NOTE_ROUNDED, color='#3EC99D', size=45)),
            ft.NavigationDestination(icon_content=ft.Icon(name=ft.icons.PERSON_PIN_OUTLINED, size=35), selected_icon_content=ft.Icon(name=ft.icons.PERSON_PIN_SHARP, color='#3EC99D', size=45)),
        ],
    )

    busquedaText = ft.TextField(width=620, height=35, label="Buscar Cliente/Equipo/ID", color='#3F4450',border_color='#3F4450',border_radius=20, label_style=ft.TextStyle(color='#3F4450'), prefix_icon=ft.icons.SEARCH, focused_border_color='#3EC99D')
    homeTab = ft.Container(
                ft.Column(controls=[
                    ft.Row([
                        ft.Container(
                            ft.Row([
                                ft.Container(ft.Image(src='../assets/logo.png', width=100), padding=ft.padding.only(10,5)),
                                ft.Container(ft.Image(src='../assets/logoName.png', width=245), padding=ft.padding.only(15,15))
                            ])),
                        ft.Container(
                            ft.Row([
                                busquedaText,
                                ft.Container(ft.IconButton(icon = ft.icons.EXIT_TO_APP,icon_color='#3EC99D',icon_size=45,tooltip="Cerrar Sesión", padding=ft.padding.only(60,0,20))
                          )])
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(height=5, thickness=1)
                ]), visible= True, width=1400, height=715
    )

    clienteTab = ft.Container(
        ft.Row([
            ft.Container(
                ft.Column(controls=[
                    ft.Container(
                        ft.Image(src='../assets/logo.png', width=100),
                        padding=ft.padding.only(1, 1), alignment=ft.alignment.top_left
                    ),
                ])
            )
        ]
        ), visible= False, width=1400, height=715
    )

    equiposTab = ft.Container(
        ft.Row([
            ft.Container(
                ft.Column(controls=[
                    ft.Container(
                        ft.Image(src='../assets/logo.png', width=100),
                        padding=ft.padding.only(1, 1), alignment=ft.alignment.top_left
                    ),
                ])
            )
        ]
        ), visible= False, width=1400, height=715
    )

    historialTab = ft.Container(
        ft.Row([
            ft.Container(
                ft.Column(controls=[
                    ft.Container(
                        ft.Image(src='../assets/logo.png', width=100),
                        padding=ft.padding.only(1, 1), alignment=ft.alignment.top_left
                    ),
                ])
            )
        ]
        ), visible= False, width=1400, height=715
    )

    perfilTab = ft.Container(
        ft.Row([
            ft.Container(
                ft.Column(controls=[
                    ft.Container(
                        ft.Image(src='../assets/logo.png', width=100),
                        padding=ft.padding.only(1, 1), alignment=ft.alignment.top_left
                    ),
                ])
            )
        ]
        ), visible= False, width=1400, height=715
    )

    inicio = ft.Container(
            content=ft.Column([
                homeTab,
                clienteTab,
                equiposTab,
                historialTab,
                perfilTab
            ]),
        )


    page.window_width = 1400
    page.window_height = 780
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.bgcolor = ft.colors.WHITE
    page.title = 'Hackers Internet'
    page.window_resizable= False
    page.add(inicio)


ft.app(target=main)