import flet as ft
from ViewMain import ViewMain
from presenter import Presenter

def main(page: ft.Page):
    presenter = Presenter(None)
    view = ViewMain(page, presenter)
    presenter.view = view

ft.app(target=main)
