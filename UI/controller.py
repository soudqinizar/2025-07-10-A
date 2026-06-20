import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._categoriesMap = {}


    def fillCategories(self):
        categories = self._model.getCategories()
        for c in categories:
            self._categoriesMap[c.category_id] = c
            self._view._ddcategory.options.append(
                ft.dropdown.Option(key=c.category_id, text=c.category_name))


    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Date selezionate:", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Start date: {self._view._dp1.value}"))
        self._view.txt_result.controls.append(ft.Text(f"End date: {self._view._dp2.value}"))
        categoria = self._categoriesMap[int(self._view._ddcategory.value)]
        da = self._view._dp1.value
        a = self._view._dp2.value
        self._model.buildGraph(categoria, da, a)
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Num nodi: {self._model.getNumNodes()}"))
        self._view.txt_result.controls.append(ft.Text(f"Num archi: {self._model.getNumEdges()}"))


        self._view.update_page()


    def handleBestProdotti(self, e):
        self._view.txt_result.controls.append(ft.Text("Top 5 prodotti più venduti", color="green"))
        top5 = self._model.getBestProduct()

        for i in top5:
            self._view.txt_result.controls.append(ft.Text(f"{i[0]} with score {i[1]}"))


        nodi = self._model.getNodes()

        self._view._ddProdStart.options.clear()  # <-- AGGIUNGI
        self._view._ddProdEnd.options.clear()



        for n in nodi:
            self._view._ddProdStart.options.append(
                ft.dropdown.Option(key=n.product_id, text=str(n)))
            self._view._ddProdEnd.options.append(
                ft.dropdown.Option(key=n.product_id, text=str(n)))


        self._view.update_page()

    def handleCercaCammino(self, e):
        lun = int(self._view._txtInLun.value)
        startId = int(self._view._ddProdStart.value)
        endId = int(self._view._ddProdEnd.value)

        start = self._model.getProductById(startId)
        end = self._model.getProductById(endId)

        bestPath, bestScore = self._model.path(start, end, lun)

        if bestPath is None:
            self._view.txt_result.controls.append(
                ft.Text("Nessun cammino trovato con questi parametri", color="red"))
        else:
            self._view.txt_result.controls.append(
                ft.Text(f"Trovato cammino ottimo con peso {bestScore}", color="green"))
            for i in bestPath:
                self._view.txt_result.controls.append(ft.Text(f"{i}"))

        self._view.update_page()


    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
