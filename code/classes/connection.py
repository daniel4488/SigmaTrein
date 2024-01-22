class Connection:
    """ Represents a connection between two train stations. """

    def __init__(self, trajectory_number: int, station_1: str, station_2: str, duration: float) -> None:
        """ Creates a Connection object. """
        self.connection_number: int = trajectory_number
        self.station_1: str = station_1
        self.station_2: str = station_2
        self.duration: float = duration

    def get_destination_station(self, departure_station: str) -> str:
        """ Given one station, returns the other end of the connection. """
        if self.station_1 == departure_station:
            return self.station_2
        elif self.station_2 == departure_station:
            return self.station_1
        else:
            return ""
