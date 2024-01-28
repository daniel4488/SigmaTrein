
class Trajectory:
    """
    Class describing the route of a train.
    Trajectory object contains a float which is the duration of the whole
    trajectory, a list with the station names it travels accross, and a list
    of the connections corresponding to this.
    """

    def __init__(self) -> None:

        self.duration: float = 0.0
        self.stations: list[str] = []
        self.connections: list = []

    def add_station(self, station: str) -> None:
        """ Adds station to trajectory. """

        self.stations.append(station)

    def add_connection_number(self, connection_number: int) -> None:
        """ Adds connection number to trajectory. """

        self.connections.append(connection_number)

    def __str__(self) -> str:
        """ String representation of a trajectory. """

        return "[" + ", ".join(map(str, self.stations)) + "]"
