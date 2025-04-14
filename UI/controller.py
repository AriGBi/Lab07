import flet as ft

from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()
        mediaMilano,mediaTorino,mediaGenova= self._model.get_all_situazioni(self._mese)
        self._view.lst_result.controls.append(ft.Text("L'umidità media del mese selezionato è: "))
        self._view.lst_result.controls.append(ft.Text(f"Milano: {round(mediaMilano,3)}"))
        self._view.lst_result.controls.append(ft.Text(f"Torino: {round(mediaTorino,3)}"))
        self._view.lst_result.controls.append(ft.Text(f"Genova: {round(mediaGenova,3)}"))
        self._view.update_page()



    def handle_sequenza(self, e):
        pass

    def read_mese(self, e):
        self._mese = int(e.control.value)

