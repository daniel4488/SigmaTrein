class Connection:
    """
    Class describing a connection between two train stations.
    Connection object contains a connection number, station 1 and
    station 2, the duration of the connection and the weight.
    """

    def __init__(self, trajectory_number: int, station_1: str,
                 station_2: str, duration: float) -> None:

        self.connection_number: int = trajectory_number
        self.station_1: str = station_1
        self.station_2: str = station_2
        self.duration: float = duration
        self.weight: int = 0

    def get_destination_station(self, departure_station: str) -> str:
        """ Given one station, returns the other end of the connection. """

        if self.station_1 == departure_station:
            return self.station_2
        elif self.station_2 == departure_station:
            return self.station_1
        else:
            return ""

    def reset_weight(self):

        self.weight = 0
