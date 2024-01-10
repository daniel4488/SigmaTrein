class Verbinding: 
    def __init__(self, station_1, station_2, duur):
        self.station_1 = station_1
        self.station_2 = station_2
        self.duur = duur
        self.isgelegd = False

    def toggle_isgelegd(self):
        self.isgelegd = True 