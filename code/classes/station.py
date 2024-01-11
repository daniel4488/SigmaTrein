class Station:
    """ Class voor station. """

    def __init__(self, station_name: str, x: float, y: float):
        self.station_name: str = station_name
        self.x: float = x
        self.y: float = y
        self.connections: list[int] = []
        self.possible_connections: list[int] = []

    def add_connection(self, traject_nummer: int) -> None:
        """ Voeg nieuwe verbinding toe aan het station. """
        self.connections.append(traject_nummer)
    
    def repopulate_possible_connections(self) -> None:
        for value in self.connections:
            self.possible_connections.append(value)

    def remove_possible_connection(self, verbinding_nummer: int) -> None:
        self.possible_connections.remove(verbinding_nummer)

    def __str__(self) -> str:
        return self.station_name
