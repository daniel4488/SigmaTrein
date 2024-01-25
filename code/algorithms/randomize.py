from code.classes.trajectory import Trajectory
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.solution import Solution
from code.classes.output import Output
from code.classes.railNL import RailNL

import random
import os


class Randomize:
    """ Algorithm to generate a randomly chosen trajectory. """

    def __init__(self, stations: dict[str, Station], connections: dict[int, Connection]) -> None:
        """ Initiates the random algorithm. """

        # make algorithm pseudo random
        # random.seed(324488)
        # random.seed(1309)
        # random.seed(239094)
        # random.seed(2024)

        self.stations: dict[str, Station] = stations
        self.connections: dict[int, Connection] = connections

        self.used_connections: set[int] = set()
        self.solution: dict[int, list[str]] = {}

        self.verbose: bool = False

    def choose_station(self, stations: list[str]) -> tuple[str, Station]:
        """ Chooses a random station from the given list and returns a list
            with its name and object. """

        name = random.choice(stations)
        station = self.stations[name]
        return name, station

    def get_station(self, start: str, connection: int) -> tuple[str, Station]:
        """ Returns list with station name and object from given connection number. """

        name = self.connections[connection].get_destination_station(start)
        station = self.stations[name]
        return name, station

    def repopulate_possible_connections_for_all_stations(self) -> None:
        """ Prepare for the generation of a new trajectory. """

        for station in self.stations:
            self.stations[station].repopulate_possible_connections()

    @staticmethod
    def update_connections(connection: int, departure: Station, destination: Station) -> None:
        """ Removes a made connection from the possible connections of the
            departure station, as well as from the destination station. """

        departure.remove_possible_connection(connection)
        destination.remove_possible_connection(connection)

    @staticmethod
    def update_trajectory(duration: float, connection: int, station: str, trajectory: Trajectory) -> None:
        """ Adds new connection and station to the given trajectory, and
            updates its total time. """

        trajectory.add_station_to_trajectory(station)
        trajectory.duration = duration
        trajectory.add_connection_number(connection)

    def make_trajectory(self, unique: bool = False) -> Trajectory:
        """ Generates a randomly chosen trajectory. If unique is True,
            then all connections can only be selected once. """
        
        self.repopulate_possible_connections_for_all_stations()

        # initialize empty trajectory
        trajectory = Trajectory()
        
        # choose a random station to depart from
        departure_station = self.choose_station(list(self.stations.keys()))

        # add departure station to the trajectory
        trajectory.add_station_to_trajectory(departure_station[0])

        # add stations to trajectory as long as its duration is less than 120 mins,
        # and there are still possible connections
        while trajectory.duration <= 120 and departure_station[1].possible_connections:
            
            # choose random connection number from possible connections at departure station
            connection = random.choice(departure_station[1].possible_connections)

            # get destination station from chosen connection 
            destination_station = self.get_station(departure_station[0], connection)

            # remove created connection from destination and departure station's possible connections
            if unique:
                self.update_connections(connection, departure_station[1], destination_station[1])

            # update total duration of the trajectory
            duration_candidate = trajectory.duration + self.connections[connection].duration

            # add station to trajectory if it fits within 120 mins
            if duration_candidate <= 120:
                self.update_trajectory(duration_candidate, connection, destination_station[0], trajectory)

                # update departure station to the current station
                departure_station = destination_station

        return trajectory

    def reset_used_connections(self) -> None:
        self.used_connections.clear()

    @staticmethod
    def clear_scores_file() -> None:
        file_path = "data/scores/random.csv"

        if os.path.exists(file_path):
            input("WARNING scores file will be deleted.")
            os.remove(file_path)

    def prepare_csv_file(self) -> None:
        self.clear_scores_file()

        if not (os.path.exists("data/scores") and os.path.isdir("data/scores")):
            os.mkdir("data/scores")

        with open("data/scores/random.csv", "w") as file:
            file.write("score\n")

    def make_solution(self, write_output: bool) -> Solution | Output:
        """ Creates a solution of max. 7 trajectories. """

        self.reset_used_connections()

        trajectories = set()
        is_valid = False

        for _ in range(7):
            # make random trajectory
            current_trajectory = self.make_trajectory()

            # add to set of trajectories
            trajectories.add(current_trajectory)

            # add trajectory connections to used_connections
            self.used_connections.update(current_trajectory.connections)

            if len(self.used_connections) == RailNL.NUMBER_OF_CONNECTIONS:
                is_valid = True
                break

        # create solution instance
        if write_output:
            solution = Output(trajectories, is_valid)
        else:
            solution = Solution(trajectories, is_valid)

        if self.verbose:
            print(f"Score: {solution.score}")

            for trajectory in solution.trajectories:
                print("Stations:", end="")
                print(trajectory, end="")
                print()

        return solution

    def make_baseline(self, verbose: bool = False) -> None:
        self.verbose = verbose

        self.prepare_csv_file()

        number_of_simulations = 1

        for _ in range(number_of_simulations):
            self.make_solution(write_output=True)

   
