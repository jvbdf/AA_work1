import random
import math 
import os
import networkx as nx
from networkx.readwrite import json_graph
import json

class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vertex({self.id}, x={self.x}, y={self.y})"

    def position(self):
        return (self.x, self.y)


class Graph:
    
    def __init__(self):
     
        self.nodes = []
        self.edges = set()  

    def add_node(self, id, x, y):
        node = Node(id, x, y)
        self.nodes.append(node)

    def add_edge(self, u, v):
        if u != v:
            self.edges.add(tuple(sorted((u, v))))

    def num_nodes(self):
        return len(self.nodes)

    def num_edges(self):
        return len(self.edges)

    def get_nodes_ids(self):
        return [node.id for node in self.nodes]

    def __repr__(self):
        return f"Graph(nodes={len(self.nodes)}, edges={len(self.edges)})"
    
class GraphGenerator:

    def __init__(self, seed):
        self.seed = seed
        random.seed(self.seed)

    def _is_too_close(self, x, y, nodes, min_dist):
        for node in nodes:
            if math.dist((x, y), (node.x, node.y)) < min_dist:
                return True
        return False

    def generate_nodes(self, n, min_dist=5):
        nodes = []
        while len(nodes) < n:
            x = random.randint(1, 500)
            y = random.randint(1, 500)
            if not self._is_too_close(x, y, nodes, min_dist):
                nodes.append(Node(len(nodes), x, y))
        return nodes

    def generate_edges_by_density(self, graph, density):
        n = graph.num_nodes()
        max_edges = n * (n - 1) // 2
        num_edges = max(1, int(density * max_edges))

        possible_edges = [(i, j) for i in range(n) for j in range(i + 1, n)]

        selected_edges = random.sample(possible_edges, num_edges)

        for u, v in selected_edges:
            graph.add_edge(u, v)

    def generate_graph(self, n, density, min_dist=5):
        graph = Graph()
        graph.nodes = self.generate_nodes(n, min_dist)
        self.generate_edges_by_density(graph, density)
        return graph

class GraphExporter:
    
    @staticmethod
    def to_networkx(graph):
        G = nx.Graph()
        for node in graph.nodes:
            G.add_node(node.id, x=node.x, y=node.y)
        for (u, v) in graph.edges:
            G.add_edge(u, v)
        return G

    @staticmethod
    def save_graph(graph, filepath):
        try:
            G = GraphExporter.to_networkx(graph)
            data = json_graph.node_link_data(G)
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            raise RuntimeError(f"Falha ao guardar o grafo: {e}")

    @staticmethod
    def load_graph(filepath):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            G = json_graph.node_link_graph(data)
            for n, attr in G.nodes(data=True):
                G.nodes[n]['x'] = int(attr['x'])
                G.nodes[n]['y'] = int(attr['y'])
            return G
        except Exception as e:
            raise RuntimeError(f"Falha ao carregar o grafo: {e}")
        
    