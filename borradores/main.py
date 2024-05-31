import flet as ft
from borradores.LoginView import LoginView
from presenter import LoginPresenter

def main(page: ft.Page):
    presenter = LoginPresenter(None)
    view = LoginView(page, presenter)
    presenter.view = view

ft.app(target=main)
