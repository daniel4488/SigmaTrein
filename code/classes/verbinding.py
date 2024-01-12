class Verbinding:
    def __init__(self, station_1: str, station_2: str, duur: int, traject_nummer: int):
        self.station_1: str = station_1
        self.station_2: str = station_2
        self.duur: int = duur
        self.is_gelegd: bool = False
        self.traject_nummer: int = traject_nummer

    def toggle_is_gelegd(self) -> None:
        self.is_gelegd = True 

    def reset_is_gelegd(self) -> None:
        self.is_gelegd = False