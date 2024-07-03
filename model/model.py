import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self.nodi = []
        self.idMap = {}
        self.adiacenti = []
        self.connessi = []
        self.predecessori = []
        self.successori = []
        self._solBest = []


    def buildGraph(self, anno):
        self._grafo.clear()
        self.nodi = DAO.getStates(anno)
        self._grafo.add_nodes_from(self.nodi)
        self.addEdges(anno)

    def addEdges(self, anno):
        self._grafo.clear_edges()
        for n1, n2 in DAO.getConnessioni(anno):
            if n1 != n2:
                if self._grafo.has_edge(n1, n2) is False:
                    self._grafo.add_edge(n1, n2)

    def getAdiacent(self, stato):
        self.adiacenti = ["successori"]
        for e in self._grafo.successors(stato):
            self.adiacenti.append(e)
        self.adiacenti.append("predecessori")
        for e2 in self._grafo.predecessors(stato):
            self.adiacenti.append(e2)
        return self.adiacenti

    def getConnectedComponents(self, stato):
        return nx.dfs_tree(self._grafo, stato)

    def getBestPath(self, stato):
        self._solBest = []
        parziale = [stato]
        self.ricorsione(parziale)
        print(self._solBest)
        return self._solBest

    def ricorsione(self, parziale):
        if len(parziale) > len(self._solBest):
            self._solBest = copy.deepcopy(parziale)

        for n in self._grafo.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self.ricorsione(parziale)
                parziale.pop()

    def getYear(self):
        return DAO.getYearAvv()

    def getCaratteristiche(self):
        return len(self._grafo.nodes), len(self._grafo.edges)
