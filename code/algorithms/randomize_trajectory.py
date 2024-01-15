from code.classes.trajectory import Trajectory
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.solution import Solution

import random
import os


class RandomizeTrajectory:
    """ Algorithm to generate a randomly chosen trajectory. """

    def __init__(self, stations: dict[str, Station], connections: dict[int, Connection]) -> None:
        """ Initiates the random algorithm. """

        self.stations: dict[str, Station] = stations
        self.connections: dict[int, Connection] = connections

        self.used_connections: set = set()
        self.solution: dict[int, list[str]] = {}

    def repopulate_possible_connections_for_all_stations(self) -> None:
        """ Prepare for the generation of a new trajectory. """
        for station in self.stations:
            self.stations[station].repopulate_possible_connections()

    def make_random_trajectory(self) -> Trajectory:
        """ Generates a randomly chosen trajectory. """
        
        self.repopulate_possible_connections_for_all_stations()

        # initialize empty trajectory
        random_trajectory = Trajectory()
        
        # choose a random station to depart from
        random_departure_station = random.choice(list(self.stations.keys()))
        random_departure_station_object = self.stations[random_departure_station]

        # add departure station to the trajectory
        random_trajectory.add_station_to_trajectory(random_departure_station)

        # add stations to trajectory as long as its duration is less than 120 mins,
        # and there are still possible connections
        while random_trajectory.duration <= 120 and random_departure_station_object.possible_connections:
            
            # choose random connection number from possible connections at departure station
            random_connection = random.choice(random_departure_station_object.possible_connections)
            random_trajectory.add_connection_number(random_connection)

            # get name of destination station from chosen connection 
            random_destination_station = self.connections[random_connection].get_destination_station(random_departure_station)

            # get destination station object
            random_destination_station_object = self.stations[random_destination_station]

            # remove created connection from destination and departure station's possible connections
            random_destination_station_object.remove_possible_connection(random_connection)
            random_departure_station_object.remove_possible_connection(random_connection)

            # add duration of created connection to duration of the trajectory
            random_trajectory.duration += self.connections[random_connection].duration

            # add station to trajectory if it fits within 120 mins
            if random_trajectory.duration <= 120:
                random_trajectory.add_station_to_trajectory(random_destination_station)

            # update departure station to the current station
            random_departure_station = random_destination_station
            random_departure_station_object = random_destination_station_object

        # create trajectory list of stations
        return random_trajectory

    def reset_used_connections(self) -> None:
        self.used_connections.clear()

    @staticmethod
    def clear_scores_file() -> None:
        file_path = "data/scores/random.csv"

        if os.path.exists(file_path):
            input("WARNING scores file will be deleted.")
            os.remove(file_path)

    def make_random_solution(self) -> None:
        self.reset_used_connections()

        if not (os.path.exists("data/scores") and os.path.isdir("data/scores")):
            os.mkdir("data/scores")

        trajectories = set()
        is_valid = False

        for i in range(1, 7):
            # Make random trajectory
            current_trajectory = self.make_random_trajectory()

            # Add to set of trajectories
            trajectories.add(current_trajectory)

            # Add trajectory connections to used_connections
            self.used_connections.union(current_trajectory.connections)

            if len(self.used_connections) == 28:
                is_valid = True

        # Create solution instance
        solution = Solution(trajectories, is_valid)
        print(f"Score: {solution.score}")

        for trajectory in solution.trajectories:
            print("Stations:", end="")
            print(trajectory, end="")
            print()

    def make_baseline(self) -> None:
        self.clear_scores_file()

        number_of_simulations = 1

        for _ in range(number_of_simulations):
            self.make_random_solution()



