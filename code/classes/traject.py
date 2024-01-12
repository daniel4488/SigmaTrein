# path finding problem
class Traject:
    def __init__(self) -> None:
        self.trajectduur: int = 0
        self.stations: list[str] = []

    def voeg_station_toe(self, station: str) -> None:
        self.stations.append(station)

    def print_traject(self) -> None:
        print(self.stations)

    def print_trajectduur(self) -> None:
        print(self.trajectduur)
