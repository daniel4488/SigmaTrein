from code.classes.station import Station
from code.classes.connection import Connection


class RailNL:
    """
    Class that loads the csv data into memory.
    RailNL object contains a dictionary with station names as keys
    and station objects as values, a dictionary with connection
    numbers as keys and connection objects as values.
    """

    NUMBER_OF_CONNECTIONS: int = -1

    DATASET: str = "none"

    CONNECTIONS: dict[int, Connection] = None

    def __init__(self, dataset: str) -> None:

        # name of the dataset in lowercase
        self.dataset = dataset.lower()
        RailNL.DATASET = dataset

        self.stations: dict[str, Station] = {}
        self.connections: dict[int, Connection] = {}

        self.load_stations()
        self.load_connections()

        # global connections
        RailNL.CONNECTIONS = self.connections

    def load_stations(self) -> None:
        """ Converts the station data to Station classes and loads
            them into the stations dictionary. """

        # open StationsHolland.csv
        with open(f"data/{self.dataset}/Stations{self.dataset.capitalize()}.csv", "r") as file:
            # remove header
            _ = file.readline()

            # strip and split lines by comma's
            for line in file:
                line = line.strip()
                station, y, x = line.split(",")

                # create station object
                self.stations[station] = Station(station, float(x), float(y))

    def load_connections(self) -> None:
        """ Converts connections data to Connection classes and
            loads them into the connections dictionary. """

        with open(f"data/{self.dataset}/Connecties{self.dataset.capitalize()}.csv", "r") as file:
            # remove header
            _ = file.readline()

            # keep track of the current trajectory number
            trajectory_number = 0

            # strip and split line by comma's
            for line in file:
                line = line.strip()
                station_1, station_2, duration_str = line.split(",")

                # convert string to integer
                duration = float(duration_str)

                # add connection to both stations
                self.stations[station_1].add_connection(trajectory_number)
                self.stations[station_2].add_connection(trajectory_number)

                # add a connection to connections dictionary
                self.connections[trajectory_number] = (Connection
                                                       (trajectory_number,
                                                        station_1,
                                                        station_2,
                                                        duration))

                # increment the current trajectory number
                trajectory_number += 1

            # make number of connections / trajectories a class variable
            RailNL.NUMBER_OF_CONNECTIONS = trajectory_number
