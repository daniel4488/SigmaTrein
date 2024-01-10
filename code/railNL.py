from station import Station
from traject import Traject
from verbinding import Verbinding

class RailNL:
    def __init__(self):
        self.stations: list[Station] = []
        self.verbindingen: list[Verbinding] = []
        self.trajecten: list[Traject] = []

    def laad_stations(self):
        pass

    def laad_verbindingen(self):
        pass

    def maak_traject(self):
        pass