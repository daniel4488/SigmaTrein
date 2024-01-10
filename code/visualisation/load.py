import networkx as nx
from pyvis.network import Network


class Load:
    def __init__(self) -> None:
        # Initiate empty undirected graph
        self.G: nx.Graph = nx.Graph()

        # Add nodes to the graph
        self.add_nodes()

        # Add edges to the graph
        self.add_edges()

        # Visualize graph
        self.draw_graph()

    def add_nodes(self) -> None:

        # Open StationsHolland.csv
        with open("../data/holland/StationsHolland.csv", "r") as file:
            # Remove header
            _ = file.readline()

            # Iterate over rest of the file
            for line in file:
                # Remove newline character at the end
                line = line.strip()

                # Split line based on a comma
                station, y, x = line.split(",")

                # Station has attributes y and x
                station_attr = {
                    "y": float(y),
                    "x": float(x)
                }

                # Add node to the graph
                self.G.add_node(station, **station_attr)

    def add_edges(self) -> None:

        # Open ConnectiesHolland.csv
        with open("../data/holland/ConnectiesHolland.csv", "r") as file:
            # Remove header
            _ = file.readline()

            for line in file:
                # Remove newline character
                line = line.strip()

                # Split line
                station1, station2, distance = line.split(",")

                # Edges attributes
                edge_attr = {
                    "distance": int(distance),
                    "title": distance
                }

                # Add edge to graph
                self.G.add_edge(station1, station2, **edge_attr)

    def draw_graph(self) -> None:

        # pos = nx.kamada_kawai_layout(self.G)
        #
        # nx.draw_networkx(G=self.G, pos=pos)
        # plt.show()
        # plt.savefig("output.png")

        net = Network()
        net.from_nx(self.G)
        net.save_graph("networkx-pyvis.html")












if __name__ == "__main__":
    load = Load()
