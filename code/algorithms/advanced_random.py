from code.classes.trajectory import Trajectory
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.data import DataInfo
from code.classes.dataset_info import DatasetInfo
from code.classes.railNL import RailNL
from code.classes.solution import Solution
from code.classes.output import Output
from code.classes.write_file import ScoreFile
from code.visualisation.map_class import MapVisualization
from code.visualisation.baseline import visualize_baseline, visualize_iterations_to_score

import random


class AdvancedRandom(MapVisualization):
    def __init__(self, dataset: str):
        # set dataset
        self.dataset = dataset

        self.score_file = ScoreFile("advanced.csv")
        self.highest_score_file = ScoreFile("advanced_highest.csv")

        self.railNL = RailNL(dataset=dataset)

        # dictionary for all stations
        self.stations: dict[str, Station] = dict()

        # set constrictions
        self.constrictions: DatasetInfo = self.set_constrictions(dataset)

         # variable for keeping track of used connections
        self.used_connections: set[int] = set()
        
        # stores a solution
        self.solution: dict[int, list[str]] = {}

        # False for no print statements, true for print statements
        self.verbose: bool = False

        # load all stations independent of RailNL class
        self.load_stations()

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

    @staticmethod
    def set_constrictions(dataset: str) -> DatasetInfo:
        """ Sets the restrictions on trajectories for the chosen dataset. """

        data_info = DataInfo

        if dataset == "holland":
            return data_info.holland
        elif dataset == "nationaal":
            return data_info.nationaal
        
    def choose_station(self, stations: list[str]) -> tuple[str, Station]:
        """ Returns a list with the name and object of a randomly chosen
            station. """

        name = random.choice(stations)
        station = self.stations[name]
        return name, station
    
    def get_station(self, start: str, connection: int, connections: dict[int, Connection]) -> tuple[str, Station]:
        """ Returns list with station name and object from given connection
            number. """

        name = connections[connection].get_destination_station(start)
        station = self.stations[name]
        return name, station
    
    def repopulate_possible_connections_for_all_stations(self) -> None:
        """ Prepare for the generation of a new trajectory. """

        for station in self.stations:
            self.stations[station].repopulate_possible_connections()

    @staticmethod
    def update_connections(connection: int, departure: Station,
                           destination: Station) -> None:
        """ Removes a made connection from the possible connections of the
            departure station, as well as from the destination station. """

        departure.remove_possible_connection(connection)
        destination.remove_possible_connection(connection)

    @staticmethod
    def update_trajectory(duration: float, connection: int, station: str,
                          trajectory: Trajectory) -> None:
        """ Adds new connection and station to the given trajectory, and
            updates its total time. """

        trajectory.add_station(station)
        trajectory.duration = duration
        trajectory.add_connection_number(connection)

    def choose_first_departure_station(self, trajectory: Trajectory):
        # choose a random station to depart from
        departure_station = self.choose_station(list(self.stations.keys()))

        # add departure station to the trajectory
        trajectory.add_station(departure_station[0])

        return departure_station
    
    def reset_used_connections(self, connections: dict[int, Connection]) -> None:
        self.used_connections.clear()
        for _, connection_object in connections.items():
            connection_object.reset_weight()

    def make_trajectory(self, trajectory: Trajectory, departure_station: tuple[str, Station], connections: dict[int, Connection]) -> Trajectory:
        """ Generates a randomly chosen trajectory. """

        # choose the first departure station
        # departure_station = self.choose_first_departure_station(trajectory)

        # add stations to trajectory as long as its duration is less than 120 mins,
        # and there are still possible connections
        while departure_station[1].possible_connections:
            
            # choose random connection number from possible connections at departure station
            # connection = departure_station[1].return_random_connection()

            possible_connections = departure_station[1].return_possible_connections()
            
            # find the connection with the lowest weight using a lambda function
            connection = min(possible_connections, key=lambda connection: connections[connection].weight)

            # get destination station from chosen connection 
            destination_station = self.get_station(departure_station[0], connection, connections)

            # remove created connection from destination and departure station's possible connections
            self.update_connections(connection, departure_station[1], destination_station[1])

            # update total duration of the trajectory
            duration_candidate = trajectory.duration + connections[connection].duration

            # add station to trajectory if it fits within 120 mins
            if duration_candidate <= self.constrictions.max_time:
                self.update_trajectory(duration_candidate, connection, destination_station[0], trajectory)

                # New
                connections[connection].weight += 1
                # update departure station to the current station
                departure_station = destination_station

        return trajectory
    
    def run(self, iterations: int, visualize: bool, verbose: bool = False, write_output: bool = True, auto_open: bool = False) -> Solution | Output:
        self.score_file.prepare_file()

        
        highest_score = 0
        
        i = 0
        
        for _ in range(iterations):
            print(i)
            self.reset_used_connections(RailNL.CONNECTIONS)
            
            trajectories = set()
            for _ in range(20):
                # make random trajectory
                current_trajectory: Trajectory = self.make_trajectory(RailNL.CONNECTIONS)

                # add to set of trajectories
                trajectories.add(current_trajectory)

                # add trajectory connections to used_connections
                self.used_connections.update(current_trajectory.connections)
            
                if len(self.used_connections) == 89:
                        break
                
            i += 1

            trajectories = list(trajectories)
            solution = Solution(trajectories, False, self.__class__.__name__)

            self.score_file.write_score(solution.score)

            if solution.score > highest_score:
                highest_score = solution.score
                highest_score_solution = solution

                self.highest_score_file.write_score(highest_score)

            if self.verbose:
                print(f"Score: {solution.score}")

                for trajectory in solution.trajectories:
                    print("Stations:", end="")
                    print(trajectory, end="")
                    print()
            
        print(highest_score) if self.verbose else None
        Output(highest_score_solution.trajectories, False)

        if visualize:
            self.visualize(solution=highest_score_solution)
            visualize_iterations_to_score("data/scores/sigma_highest.csv")
            visualize_baseline("data/scores/sigma.csv")

if __name__ == "__main__":
    advancedRandom = AdvancedRandom()
    advancedRandom.run(100, True, False, True)