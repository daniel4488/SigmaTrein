from code.classes.trajectory import Trajectory
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.solution import Solution
from code.classes.output import Output
from code.classes.railNL import RailNL
from code.classes.data import DataInfo
from code.classes.dataset_info import DatasetInfo
from code.visualisation.map import PlotlyLoad
from code.classes.write_file import ScoreFile

import random
import os
import copy


class Randomize:
    """
    Algorithm to generate a randomly chosen trajectory.
    Random starts with a dictionary with all station names and objects, a
    dictionary with all connection numbers and objects, the constrictions
    belonging to the used dataset. Moreover, it keeps track of the connections
    it has made, and the current solution.
    """

    def __init__(self, dataset: str) -> None:

        # make algorithm pseudo random
        # random.seed(324488)
        # random.seed(1309)
        # random.seed(239094)
        # random.seed(2024)

        self.dataset = dataset

        railNL = RailNL(dataset=dataset)

        self.stations: dict[str, Station] = railNL.stations
        self.connections: dict[int, Connection] = railNL.connections
        self.constrictions: DatasetInfo = self.set_constrictions(dataset)

        self.preferred_departure_holland = ["Den Helder", "Dordrecht", "Hoorn", "Schiphol Airport", "Gouda", "Heemstede-Aerdenhout", "Schiphol Airport"]
        self.preferred_departure_nationaal = ["Den Helder", "Dordrecht", "Hoorn", "Enschede", "Venlo", "Maastricht", "Heerlen", "Vlissingen", "Lelystad Centrum", "Groningen", "Leeuwarden", "Utrecht Centraal", "Utrecht Centraal", "Utrecht Centraal", "Utrecht Centraal", "Utrecht Centraal", "Amsterdam Centraal", "Amsterdam Centraal", "Amsterdam Centraal", "Amsterdam Centraal"]

        self.preferred_departure_copy = []
        
        self.prefixed = True
        self.used_connections: set[int] = set()
        self.solution: dict[int, list[str]] = {}

        self.verbose: bool = False

    def set_constrictions(self, dataset: str) -> DatasetInfo:
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

    def get_station(self, start: str, connection: int) -> tuple[str, Station]:
        """ Returns list with station name and object from given connection
            number. """

        name = self.connections[connection].get_destination_station(start)
        station = self.stations[name]
        return name, station

    def repopulate_possible_connections_for_all_stations(self) -> None:
        """ Prepare for the generation of a new trajectory. """

        for station in self.stations:
            self.stations[station].repopulate_possible_connections()

    def repopulate_preferred_departure_stations(self):

        if self.dataset == "holland":
            self.preferred_departure_copy = copy.deepcopy(self.preferred_departure_holland)
        else:
            self.preferred_departure_copy = copy.deepcopy(self.preferred_departure_nationaal)
            print(self.preferred_departure_copy)

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

    def choose_departure_station(self, trajectory: Trajectory) -> set[str, Station]:
        """ Generates a randomly chosen trajectory. If unique is True,
            then all connections can only be selected once. """


        # choose a random station to depart from
        departure_station = self.choose_station(list(self.stations.keys()))

        # add departure station to the trajectory
        trajectory.add_station(departure_station[0])

        return departure_station
    
    def choose_prefixed_departure_station(self, trajectory: Trajectory) -> set [str, Station]:
        if self.dataset == "holland":
            name = self.preferred_departure_copy.pop(0)
            station = self.stations[name]
            trajectory.add_station(name)
            return name, station
        
        if self.dataset == "nationaal":
            name = self.preferred_departure_copy.pop(0)
            station = self.stations[name]
            trajectory.add_station(name)
            return name, station

    def make_trajectory(self, unique: bool = False, prefixed: bool = True) -> Trajectory:
        # add randomly chosen connections and stations to trajectory as long as
        # restrictions are still met

        self.repopulate_possible_connections_for_all_stations()

        trajectory = Trajectory()
        self.prefixed = prefixed

        if prefixed:
            departure_station = self.choose_prefixed_departure_station(trajectory)
        else:
            departure_station = self.choose_departure_station(trajectory)

        while trajectory.duration <= int(self.constrictions.max_time) and \
                departure_station[1].possible_connections:

            # choose random connection number from possible connections at
            # departure station
            connection = random.choice(departure_station[1].
                                       possible_connections)

            # get destination station from chosen connection
            destination_station = self.get_station(departure_station[0],
                                                   connection)

            # remove created connection from destination and departure stations
            # possible connections
            if unique:
                self.update_connections(connection, departure_station[1],
                                        destination_station[1])

            # update total duration of the trajectory
            duration_candidate = trajectory.duration + \
                self.connections[connection].duration

            # add station to trajectory if it fits within time restriction
            if duration_candidate <= self.constrictions.max_time:
                self.update_trajectory(duration_candidate, connection,
                                       destination_station[0], trajectory)

                # update departure station to the current station
                departure_station = destination_station
            elif duration_candidate > self.constrictions.max_time and not \
                    unique:
                break

        return trajectory

    def reset_used_connections(self) -> None:
        self.used_connections.clear()

    @staticmethod
    def clear_scores_file() -> None:
        """ Clears the csv file from all old data. """

        file_path = "data/scores/random.csv"

        if os.path.exists(file_path):
            input("WARNING scores file will be deleted.")
            os.remove(file_path)

    def prepare_csv_file(self) -> None:
        """ Prepares the csv file for new data, or creates file
            if it does not exist yet. """

        self.clear_scores_file()

        if not (os.path.exists("data/scores") and os.path.isdir("data/scores")):
            os.mkdir("data/scores")

        with open("data/scores/random.csv", "w") as file:
            file.write("score\n")

    def run(self, iterations: int, visualize: bool, verbose: bool = False, write_output: bool = True) -> Solution | Output:
        """ Creates a solution of with the maximum amount of trajectories. """

        self.reset_used_connections()

        if self.prefixed:
            self.repopulate_preferred_departure_stations()

        trajectories = set()
        is_valid = False

        for _ in range(int(self.constrictions.max_trajectories)):
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

        # Visualization
        if visualize:
            plot_device = PlotlyLoad(dataset=self.dataset)
            plot_device.draw_graph(solution)

        return solution

    def create_score_file(self):
        """ Create an empty csv file for the scores. """

        score_file = ScoreFile("random.csv")
        score_file.prepare_file()
