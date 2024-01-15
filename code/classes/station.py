class Station:
    """ Class representing a train station. """

    def __init__(self, station_name: str, x: float, y: float):
        """ Creates a new Station object. """
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
        # Possible bug: could be that there are more possible connections than connections
        # In that case there will be duplicates in possible connections
        # Question: is order important for connections? if not -> change to set
        # A set will also prevent having duplicates
        self.possible_connections = []
        for value in self.connections:
            self.possible_connections.append(value)

    def remove_possible_connection(self, connection_number: int) -> None:
        """ Remove a possible connection from the list. """
        self.possible_connections.remove(connection_number)

    def __str__(self) -> str:
        """ Gives the string representation. """
        return self.station_name
