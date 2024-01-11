class Verbinding:
    def __init__(self, trajectory_number: int, station_1: str, station_2: str, duration: int):
        self.connection_number: int = trajectory_number
        self.station_1: str = station_1
        self.station_2: str = station_2
        self.duration: int = duration
        