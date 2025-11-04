import os
import matplotlib.pyplot as plt
import networkx as nx
from graph import GraphGenerator, GraphExporter

def visualize_graph(G, title):
    pos = {n: (data["x"], data["y"]) for n, data in G.nodes(data=True)}
    nx.draw(G, pos, with_labels=True, node_size=400)
    plt.title(title)
    plt.show()

def main():
    seed = 106078
    generator = GraphGenerator(seed)

    output_dir = "generated_graphs"
    os.makedirs(output_dir, exist_ok=True)

    densities = [0.125, 0.25, 0.50, 0.75]

    for n in range(4, 11):
        for density in densities:
            graph = generator.generate_graph(n, density)

            filename = f"graph_n{n}_d{density}.json"
            filepath = os.path.join(output_dir, filename)

            GraphExporter.save_graph(graph, filepath)


            print(f"Grafo guardado: {filepath} | Nodes: {n}, Edges: {graph.num_edges()}")

         
            G = GraphExporter.to_networkx(graph)
            visualize_graph(G, f"Grafo n={n}, density={density}")

if __name__ == "__main__":
    main()
