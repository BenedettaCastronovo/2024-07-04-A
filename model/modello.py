from database.DAO import DAO
import networkx as nx
import copy

class Model:
    def __init__(self):
        self.g = nx.DiGraph()
        self.mappaN = {}
        self.best = {}
        self.punti = 0

    def creaG(self, y, s):
        self.g.clear()
        self.n = DAO.getN(y, s)
        self.g.add_nodes_from(self.n)
        for n in self.n:
            self.mappaN[n.id] = n

        self.archi = DAO.getA(y, s) #devo filtrare senno considero nodi in piu
        for u,v in self.archi:
            self.g.add_edge(self.mappaN[u], self.mappaN[v])

        #for u in self.g.nodes():
         #   for v in self.g.nodes():
          #      if u != v and DAO.has_edge(u, v):
           #         if u.datetime < v.datetime:
            #            self.g.add_edge(u, v)

    def getY(self):
        return DAO.getY()

    def getS(self, y):
        return DAO.getS(y)

    def stampa(self):
        comp = list(nx.weakly_connected_components(self.g))
        self.mas = max(comp, key=len)
        return len(comp), self.mas

    def get(self):
        return len(self.g.nodes()), len(self.g.edges()) #qua faccio cosi

    def cerca(self):
        self.best = {}
        self.punti = 0
        for n in self.g.nodes():
            parziale = [n]
            self.ric(parziale)
        return self.best, self.punti

    def ric(self, parziale):
        if self.costo(parziale) > self.punti:
            self.best = copy.deepcopy(parziale)
            self.punti = self.costo(parziale)

        for n in self.g.successors(parziale[-1]):
            if self.is_valid(parziale, n):
                parziale.append(n)
                self.ric(parziale)
                parziale.pop()

    def is_valid(self, parziale, v):
        if parziale[-1].duration < v.duration:
            if len(parziale) > 3:
                somma = sum(1 for n in parziale if n.datetime.month == v.datetime.month)
                if somma >= 3:
                    return False
                else:
                    return True
            else:
                return True
        return False

    def costo(self, parziale):
        costo = 100 #primo elemento
        for i in range(1, len(parziale)):
            if parziale[i-1].datetime.month == parziale[i].datetime.month:
                costo+= 200
            costo+= 100

        return costo



