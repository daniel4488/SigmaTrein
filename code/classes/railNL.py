from code.classes.station import Station
from code.classes.traject import Traject
from code.classes.connection import Connection


class RailNL:
    def __init__(self) -> None:
        # Dict met de naam van het station als key en een bijbehordend object
        self.stations: dict[str, Station] = {}
        # Dict met het trajectnummer als key en een bijbehordend object
        self.verbindingen: dict[int, Connection] = {}
        # Dict met de trajectnaam als key en een bijbehordend object
        self.trajecten: list[Traject] = []

        # Laad de stations in
        self.laad_stations()
        # Laad de verbindingen in
        self.laad_verbindingen()

    def laad_stations(self) -> None:
        # Open StationsHolland.csv
        with open("data/holland/StationsHolland.csv", "r") as file:
            # Remove header
            _ = file.readline()

            # Iterate over rest of the file
            for line in file:
                # Remove newline character at the end
                line = line.strip()

                # Split line based on a comma
                station, y, x = line.split(",")
                
                self.stations[station] = Station(station, float(x), float(y))

    def laad_verbindingen(self) -> None:

        with open("data/holland/ConnectiesHolland.csv", "r") as file:
            # Remove header
            _ = file.readline()

            traject_nummer = 0

            for line in file:
                # Remove newline character
                line = line.strip()

                # Split line
                station_1, station_2, duur_str = line.split(",")

                # Convert van string naar integer
                duur = int(duur_str)

                # Voeg verbinding toe voor beide stations
                self.stations[station_1].add_connection(traject_nummer)
                self.stations[station_2].add_connection(traject_nummer)

                # Voeg verbinding toe 
                self.verbindingen[traject_nummer] = (Connection(traject_nummer, station_1, station_2, duur))

                # Houd bij welk trajectnummer dit was
                traject_nummer += 1
                
            

