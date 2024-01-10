from station import Station

# path finding problem
class Traject:
    def __init__(self):
        self.trajectduur: int = 0
        self.stations: list[Station] = []

    def voeg_station_toe(self, station):
        self.stations.append(station)

    def print_traject(self):
        print(self.stations)

    def print_trajectduur(self):
        print(self.trajectduur)
