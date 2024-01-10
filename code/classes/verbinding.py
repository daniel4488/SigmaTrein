class Verbinding: 
    def __init__(self, station_1, station_2, duur, traject_nummer):
        self.station_1 = station_1
        self.station_2 = station_2
        self.duur = duur
        self.is_gelegd = False
        self.traject_nummer = traject_nummer

    def toggle_is_gelegd(self):
        self.is_gelegd = True 

    def reset_is_gelegd(self):
        self.is_gelegd = False