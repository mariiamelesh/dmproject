import random
import time

class Graph:
    def __init__(self, vertices):
        self.V = vertices  
        self.graph = [] 

    
    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])


    def from_matrix(self, matrix):
        self.graph = [] 
        self.V = len(matrix)
        for i in range(self.V):
            for j in range(i + 1, self.V):
                if matrix[i][j] != 0:
                    self.add_edge(i, j, matrix[i][j])

    def to_matrix(self):
        matrix = [[0 for _ in range(self.V)] for _ in range(self.V)]
        
        for u, v, w in self.graph:
            matrix[u][v] = w
            matrix[v][u] = w 
        return matrix

    def from_adj_list(self, adj_list):
        self.graph = [] 
        self.V = len(adj_list)
        
        added_edges = set() 
        
        for u in adj_list:
            for v, w in adj_list[u]:
                edge_signature = tuple(sorted((u, v)))
                if edge_signature not in added_edges:
                    self.add_edge(u, v, w)
                    added_edges.add(edge_signature)

    def to_adj_list(self):
        adj_list = {i: [] for i in range(self.V)}
        for u, v, w in self.graph:
            adj_list[u].append([v, w])
            adj_list[v].append([u, w])
        return adj_list
    
    def generate_random_graph(self, num_vertices, density):
  
        self.V = num_vertices
        self.graph = []  
        for i in range(self.V):
            for j in range(i + 1, self.V):
                if random.random() < density:
                    weight = random.randint(1, 100)
                    self.add_edge(i, j, weight)


    def find(self, parent, i):
        if parent[i] != i:
            parent[i] = self.find(parent, parent[i])
        return parent[i]

    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def boruvkaMST(self, f):
        parent = []
        rank = []
        cheapest = []
        numTrees = self.V
        MSTweight = 0

        for node in range(self.V):
            parent.append(node)
            rank.append(0)
            cheapest = [-1] * self.V
        edges = []
        while numTrees > 1:
            
            for i in range(len(self.graph)):
                u, v, w = self.graph[i]
                set1 = self.find(parent, u)
                set2 = self.find(parent, v)

                if set1 != set2:
                    if cheapest[set1] == -1 or cheapest[set1][2] > w:
                        cheapest[set1] = [u, v, w]
                    if cheapest[set2] == -1 or cheapest[set2][2] > w:
                        cheapest[set2] = [u, v, w]
            for node in range(self.V):
                if cheapest[node] != -1:
                    u, v, w = cheapest[node]
                    set1 = self.find(parent, u)
                    set2 = self.find(parent, v)

                    if set1 != set2:
                        MSTweight += w
                        print(w)
                        self.union(parent, rank, set1, set2)
                        edges.append((u, v, w))
                        numTrees = numTrees - 1
            
            cheapest = [-1] * self.V
        #print(f"Ребра MST: {edges}\n Вага MST: {MSTweight}\n")




if __name__ == "__main__":

    # експериментні дані
    random_nodes = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
    random_density = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    # матриці суміжності
    f = open("log.txt", "a", encoding="utf-8")
    f.write("ДОСЛІД 1. МАТРИЦІ СУМІЖНОСТІ\n")
    g = Graph(0)
    dict = {}
    for node in random_nodes:
        avgtime_list = []
        for density in random_density:
            time_list = []
            for _ in range(30):
                g.generate_random_graph(node, density, f)
                g.from_matrix(g.to_matrix())
                start = time.time()
                g.boruvkaMST(f)
                end = time.time()
                time_list.append(end-start)
            avg_time = round(sum(time_list)/len(time_list), 5)
            avgtime_list.append(avg_time)
        f.write(f"\n{node}: {avgtime_list}")

    # списки суміжності
    f = open("log.txt", "a", encoding="utf-8")
    f.write("ДОСЛІД 2. СПИСКИ СУМІЖНОСТІ\n")
    g = Graph(0)
    dict = {}
    for node in random_nodes:
        avgtime_list = []
        for density in random_density:
            time_list = []
            for i in range(30):
                g.generate_random_graph(node, density, f)
                g.from_adj_list(g.to_adj_list())
                start = time.time()
                g.boruvkaMST(f)
                end = time.time()
                time_list.append(end-start)
            avg_time = round(sum(time_list)/len(time_list), 5)
            avgtime_list.append(avg_time)
        f.write(f"\n{node}: {avgtime_list}")
