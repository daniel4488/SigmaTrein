import random


class Station:
    """
    Class describing a train station.
    Station object contains a string with its name, an x- and
    y-coordinate, a list with the connections from itself to other
    stations, and a list with possible connections that can be used
    to keep track of already chosen connections.
    """

    def __init__(self, station_name: str, x: float, y: float):

        self.station_name: str = station_name
        self.x: float = x
        self.y: float = y
        self.connections: list[int] = []
        self.possible_connections: list[int] = []

    def add_connection(self, connection_number: int) -> None:
        """ Adds a new connection to the train station. """

        self.connections.append(connection_number)

    def repopulate_possible_connections(self) -> None:
        """ Add connections to possible connections. """

        self.possible_connections = []
        for value in self.connections:
            self.possible_connections.append(value)

    def remove_possible_connection(self, connection_number: int) -> None:
        """ Remove a possible connection from the list. """

        self.possible_connections.remove(connection_number)

    def return_random_connection(self) -> int:
        """ Returns a randomly chosen connection from the possible
            connections. """

        return random.choice(self.possible_connections)

    def return_possible_connections(self) -> list[int]:
        """ Returns list with possible connections. """

        return self.possible_connections

    def __str__(self) -> str:
        """ Gives the string representation. """

        return self.station_name
