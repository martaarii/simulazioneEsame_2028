import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        # anno + avvistamenti
        for anno, navv in self._model.getYear():
            self._view.dd_anno.options.append(ft.dropdown.Option(text=f"{anno} ({navv})", key=f"{anno}"))

    def fillDDState(self):
        self._view.dd_stato.options.clear()
        for s in self._model._grafo.nodes:
            self._view.dd_stato.options.append(ft.dropdown.Option(text=s))

    def hanldle_graph(self, e):
        self._view.txt_result.controls.clear()
        anno = self._view.dd_anno.value
        if anno is None:
            self._view.create_alert("Selezionare un anno!")
            return
        self._model.buildGraph(int(anno))
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato!"))
        nNodes, nEdges = self._model.getCaratteristiche()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nNodes} nodi"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nEdges} archi"))
        self.fillDDState()
        self._view.update_page()

    def handle_sequenza(self, e):
        self._view.txt_result.controls.clear()
        stato = self._view.dd_stato.value
        if stato is None:
            self._view.create_alert("Selezionare uno stato!")
            return
        print(self._model.getConnectedComponents(stato))
        self._view.txt_result.controls.append(ft.Text(f"I nodi adiacenti allo stato {stato} sono:"))
        for adiacenti in self._model.getAdiacent(stato):
            self._view.txt_result.controls.append(ft.Text(f"{adiacenti}"))
        conness = self._model.getConnectedComponents(stato)
        self._view.txt_result.controls.append(ft.Text(f"I nodi connessi allo stato {stato} sono {len(conness)}:"))
        for conn in conness:
            self._view.txt_result.controls.append(ft.Text(f"{conn}"))
        self._view.update_page()

    def handle_analizza(self, e):
        pass

    def handle_avvistamenti(self, e):
        self._view.txt_result.controls.clear()
        stato = self._view.dd_stato.value
        if stato is None:
            self._view.create_alert("Selezionare uno stato!")
            return
        path = self._model.getBestPath(stato)
        self._view.txt_result.controls.append(ft.Text(f"Percorso migliore di lunghezza {len(path)}"))
        for s in path:
            self._view.txt_result.controls.append(ft.Text(f"{s}"))
        self._view.update_page()