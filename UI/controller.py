import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._y = None
        self._s = None


    def fillDD(self):
        self._years = self._model.getY()
        for y in self._years:
            self._view.ddyear.options.append(ft.dropdown.Option(key=y,
                                                                on_click=self.choiceY))

        self._view.update_page()

    def choiceY(self, e):
        self._y = e.control.key
        if self._y is not None:
            self.fillS(self._y)

    def fillS(self, y):
        #self._y = self._view.ddyear.value
        self.s = self._model.getS(y)
        for s in self.s:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.update_page()

    def handle_graph(self, e):
        self._s = self._view.ddshape.value
        if self._y is not None and self._s is not None:
            self._model.creaG(self._y, self._s)
            nodi, archi = self._model.get()
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text(f"grafo creato con nodi: {nodi} e archi: {archi}"))

        else:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("seleziona anno e forma (Rispettivamente nell'ordine)"))
            return

        self.con, self.mas = self._model.stampa()
        self._view.txt_result1.controls.append(ft.Text(f"comp deboli: {self.con}"))
        for c in self.mas:
            self._view.txt_result1.controls.append(ft.Text(f"città: {c.city} - data: {c.datetime}"))
        self._view.update_page()

    def handle_path(self, e):
        best, punti = self._model.cerca()
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"punteggio: {punti}"))
        for a in best:
            self._view.txt_result2.controls.append(ft.Text(f" {a.id} - durata: {a.duration} - mese: {a.datetime.month}"))
        self._view.update_page()

