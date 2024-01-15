# path finding problem
class Trajectory:
    """ Represents the route of a train. """
    def __init__(self) -> None:
        """ Creates a Trajectory object. """
        self.duration: int = 0
        self.stations: list[str] = []

    def add_station_to_trajectory(self, station: str) -> None:
        """ Adds a station / connection to the trajectory. """
        self.stations.append(station)

    # def print_trajectory(self) -> None:
    #     print(self.stations)

    # def print_trajectory_duration(self) -> None:
    #     print(self.trajectduur)
