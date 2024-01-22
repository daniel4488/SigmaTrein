from code.classes.station import Station
from code.classes.connection import Connection


class RailNL:
    """ The RailNL class loads the csv data into memory. """

    NUMBER_OF_CONNECTIONS: int = -1

    DATASET: str = "none"

    def __init__(self, dataset: str) -> None:
        """ Creates a RailNL object. """

        # name of the dataset in lowercase
        self.dataset = dataset.lower()
        RailNL.DATASET = dataset

        # dictionary with station name as key mapping to its object
        self.stations: dict[str, Station] = {}

        # dictionary with trajectory number as key mapping to its object
        self.connections: dict[int, Connection] = {}

        # loads stations
        self.load_stations()

        # loads connections
        self.load_connections()

    def load_stations(self) -> None:
        """ Converts the station data to Station classes. """
        
        # open StationsHolland.csv
        with open(f"data/{self.dataset}/Stations{self.dataset.capitalize()}.csv", "r") as file:
            # remove header
            _ = file.readline()

            # iterate over rest of the file
            for line in file:
                # remove newline character at the end
                line = line.strip()

                # split line based on a comma
                station, y, x = line.split(",")
                
                # create station object
                self.stations[station] = Station(station, float(x), float(y))

    def load_connections(self) -> None:
        """ Converts connections data to Connection classes. """

        with open(f"data/{self.dataset}/Connecties{self.dataset.capitalize()}.csv", "r") as file:
            # remove header
            _ = file.readline()

            # keep track of the current trajectory number
            trajectory_number = 0

            for line in file:
                # remove newline character
                line = line.strip()

                # split line
                station_1, station_2, duration_str = line.split(",")

                duration = float(duration_str)
                # convert string to integer

                # add connection to both stations
                self.stations[station_1].add_connection(trajectory_number)
                self.stations[station_2].add_connection(trajectory_number)

                # add a connection
                self.connections[trajectory_number] = (Connection(trajectory_number, station_1, station_2, duration))

                # increment the current trajectory number
                trajectory_number += 1

            # make number of connections / trajectories a class variable
            RailNL.NUMBER_OF_CONNECTIONS = trajectory_number
                