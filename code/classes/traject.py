# path finding problem
class Traject:
    def __init__(self) -> None:
        self.duration: int = 0
        self.stations: list[str] = []

    def add_station_to_trajectory(self, station: str) -> None:
        self.stations.append(station)

    def print_trajectory(self) -> None:
        print(self.stations)

    # def print_trajectory_duration(self) -> None:
    #     print(self.trajectduur)
