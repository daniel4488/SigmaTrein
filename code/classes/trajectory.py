
class Trajectory:
    """ Represents the route of a train. """
    def __init__(self) -> None:
        """ Creates a Trajectory object. """
        self.duration: int = 0
        self.stations: list[str] = []
        self.connections: set[int] = set()

    def add_station_to_trajectory(self, station: str) -> None:
        """ Adds a station / connection to the trajectory. """
        self.stations.append(station)

    def add_connection_number(self, connection_number: int) -> None:
        """ Add a station number to the trajectory. """
        self.connections.add(connection_number)

    def __str__(self) -> str:
        """ String representation of a Trajectory. """
        return "[" + ", ".join(map(str, self.stations)) + "]"
