import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapProduct = {}
        self._bestPath = None
        self._bestScore = -1


    def path(self, startNode, endNode, lun):
        self._bestPath = None
        self._bestScore = -1
        parziale = [startNode]
        self._ricorsione(parziale,lun,endNode)
        return self._bestPath, self._bestScore


    def _ricorsione(self, parziale, lun, end):
        ultimo = parziale[-1]

        #caso terminale
        if( len(parziale) == (int(lun))):
            if( ultimo == end):
                score = self._calcolaPeso(parziale)
                if score > self._bestScore:
                    self._bestScore = score
                    self._bestPath = copy.deepcopy(parziale)
            return

        #caso esplorazione
        for vicino in self._graph.successors(ultimo):
            if vicino not in parziale:
                parziale.append(vicino)
                self._ricorsione(parziale,lun,end)
                parziale.pop()


    def _calcolaPeso(self, parziale):
        peso = 0
        for i in range( len(parziale) - 1):
            peso += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return peso



    def buildGraph(self, categoria, da, a):
        self._graph.clear()
        self._idMapProduct = {}

        nodes = DAO.getAllNodes(categoria)
        print(f"DEBUG - righe da getAllNodes: {len(nodes)}")
        print(f"DEBUG - product_id distinti: {len(set(n.product_id for n in nodes))}")

        for n in nodes:
            self._idMapProduct[n.product_id] = n
        self._graph.add_nodes_from(nodes)
        print(f"DEBUG - nodi nel grafo dopo add_nodes_from: {len(self._graph.nodes)}")

        edges = DAO.getAllEdges(categoria, da, a)

        for coppia1 in edges:
            for coppia2 in edges:
                if coppia1 != coppia2:
                    vendite1 = int(coppia1[1])
                    vendite2 = int(coppia2[1])
                    weight = vendite1 + vendite2

                    p1 = self._idMapProduct[coppia1[0]]
                    p2 = self._idMapProduct[coppia2[0]]
                    if vendite1 == vendite2:
                        self._graph.add_edge(p1, p2, weight=weight)
                        self._graph.add_edge(p2, p1, weight=weight)
                    elif vendite1 > vendite2:
                        self._graph.add_edge(p1, p2, weight=weight)
                    else:
                        self._graph.add_edge(p2, p1, weight=weight)



    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        return DAO.getAllCategories()

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNodes(self):
        return list(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getBestProduct(self):
        risultato = []
        bestValore = None

        for nodo in self._graph.nodes:
            sommaUscenti = 0
            for u,v,data in self._graph.out_edges(nodo, data=True):
                sommaUscenti += data['weight']

            sommaEntranti = 0
            for u,v,data in self._graph.in_edges(nodo, data=True):
                sommaEntranti += data['weight']

            differenza = sommaUscenti - sommaEntranti

            risultato.append((nodo, differenza))

        risultato.sort(key=lambda x:x[1], reverse=True)


        return risultato[:5]

    def getProductById(self, product_id):
        return self._idMapProduct[product_id]
