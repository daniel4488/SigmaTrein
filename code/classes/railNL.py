from code.classes.station import Station
from code.classes.connection import Connection


class RailNL:
    """ The RailNL class loads the csv data into memory. """

    NUMBER_OF_CONNECTIONS: int = -1

    def __init__(self) -> None:
        """ Creates a RailNL object. """

        # Dictionary with station name as key mapping to its object
        self.stations: dict[str, Station] = {}

        # Dictionary with trajectory number as key mapping to its object
        self.connections: dict[int, Connection] = {}

        # Loads stations
        self.load_stations()

        # Loads connections
        self.load_connections()

    def load_stations(self) -> None:
        """ Converts the station data to Station classes. """
        
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
                
                # Create station object
                self.stations[station] = Station(station, float(x), float(y))

    def load_connections(self) -> None:
        """ Converts connections data to Connection classes. """

        with open("data/holland/ConnectiesHolland.csv", "r") as file:
            # Remove header
            _ = file.readline()

            # Keep track of the current trajectory number
            trajectory_number = 0

            for line in file:
                # Remove newline character
                line = line.strip()

                # Split line
                station_1, station_2, duration_str = line.split(",")

                # Convert string to integer
                duration = int(duration_str)

                # Add connection to both stations
                self.stations[station_1].add_connection(trajectory_number)
                self.stations[station_2].add_connection(trajectory_number)

                # Add a connection
                self.connections[trajectory_number] = (Connection(trajectory_number, station_1, station_2, duration))

                # Increment the current trajectory number
                trajectory_number += 1

            # Make number of connections / trajectories a class variable
            RailNL.NUMBER_OF_CONNECTIONS = trajectory_number
                