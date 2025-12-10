import random


class Graph:
    def __init__(self, vertices):
        self.V = vertices  
        self.graph = [] 

    
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])


    def from_matrix(self, matrix):
        self.graph = [] 
        self.V = len(matrix)
        for i in range(self.V):
            for j in range(i + 1, self.V):
                if matrix[i][j] != 0:
                    self.addEdge(i, j, matrix[i][j])

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
                    self.addEdge(u, v, w)
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
                    self.addEdge(i, j, weight)
        
        print(f"граф на {self.V} вершин. щільність {density}")


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

    def boruvkaMST(self):
        parent = []
        rank = []
        cheapest = []
        numTrees = self.V
        MSTweight = 0

        for node in range(self.V):
            parent.append(node)
            rank.append(0)
            cheapest = [-1] * self.V

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
                        self.union(parent, rank, set1, set2)
                        print(f"Ребро {u}-{v} з вагою {w} додано до MST")
                        numTrees = numTrees - 1
            
            cheapest = [-1] * self.V

        print(f"вага MST: {MSTweight}\n")



if __name__ == "__main__":
    
    print("вручну")
    g = Graph(4)
    g.addEdge(0, 1, 10)
    g.addEdge(0, 2, 6)
    g.addEdge(0, 3, 5)
    g.addEdge(1, 3, 15)
    g.addEdge(2, 3, 4)
    
    matrix = g.to_matrix()
    print("матриця суміжності:")
    for row in matrix: print(row)
    
    g.boruvkaMST()

    print("з матриці")
    input_matrix = [
        [0,  10, 6,  5],  
        [10, 0,  0,  15], 
        [6,  0,  0,  4], 
        [5,  15, 4,  0]  
    ]
    
    g2 = Graph(4) 
    g2.from_matrix(input_matrix) 
    g2.boruvkaMST() 

    print("зі списку")
    input_list = {
        0: [[1, 10], [2, 6], [3, 5]],
        1: [[0, 10], [3, 15]],
        2: [[0, 6], [3, 4]],
        3: [[0, 5], [1, 15], [2, 4]]
    }
    
    g3 = Graph(4)
    g3.from_adj_list(input_list)
    g3.boruvkaMST()
