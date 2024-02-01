import networkx as nx


class Load:
    """
    Class used to create the background of the visualisation picture. It
    creates a node on the coordinates of every station, and edges between
    nodes that have an existing connection.
    """

    def __init__(self, dataset: str) -> None:

        self.DATASET = dataset

        # initiate empty undirected graph
        self.G: nx.Graph = nx.Graph()

        # add nodes and edges to the graph
        self.add_nodes()
        self.add_edges()

    def add_nodes(self) -> None:
        """ Adds the coordinates to the graph as nodes. """

        with open(f"data/{self.DATASET}/Stations{self.DATASET.capitalize()}.csv", "r") as file:
            # remove header
            _ = file.readline()

            for line in file:
                # strip and split lines on comma
                line = line.strip()
                station, y, x = line.split(",")

                # station has attributes y and x
                station_attr = {
                    "y": float(y),
                    "x": float(x)
                }

                # add node to the graph
                self.G.add_node(station, **station_attr)

    def add_edges(self) -> None:
        """ Adds the connections between nodes to the graph as edges. """

        with open(f"data/{self.DATASET}/Connecties{self.DATASET.capitalize()}.csv", "r") as file:
            # remove header
            _ = file.readline()

            for line in file:
                # strip and split lines on comma
                line = line.strip()
                station1, station2, distance = line.split(",")

                # edge had attributes distance and title
                edge_attr = {
                    "distance": int(distance.strip(".0")),
                    "title": distance
                }

                # add edge to graph
                self.G.add_edge(station1, station2, **edge_attr)
