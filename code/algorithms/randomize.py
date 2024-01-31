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


class Randomize:
    """
    Algorithm following a random algorithm.

    This algorithm chooses a random starting station. From there it randomly
    chooses a possible connection. This is done uptill the maximum time of
    a trajectory is reached. In this way, a solution of multiple trajectories
    is made. There are 2 special cases:
    * unique = True: the random algorithm will never choose a connection
                     more than once
    * prefixed = True: the random algorithm starts with a few prefixed stations

    Random starts with a dictionary with all station names and objects, a
    dictionary with all connection numbers and objects, the constrictions
    belonging to the used dataset. Moreover, it keeps track of the connections
    it has made, and the current solution.
    """

    def __init__(self, dataset: str) -> None:

        self.dataset = dataset
        self.verbose: bool = False

        # create dictionary for all stations and connections
        railNL = RailNL(dataset=dataset)
        self.stations: dict[str, Station] = railNL.stations
        self.connections: dict[int, Connection] = railNL.connections
        
        # set constrictions
        self.constrictions: DatasetInfo = self.set_constrictions(dataset)

        # set preferred first departure stations
        self.preferred_departure_holland = ["Den Helder", "Dordrecht", "Hoorn", "Schiphol Airport", "Gouda", "Heemstede-Aerdenhout", "Schiphol Airport"]
        self.preferred_departure_nationaal = ["Den Helder", "Dordrecht", "Hoorn", "Enschede", "Venlo", "Maastricht", "Heerlen", "Vlissingen", "Lelystad Centrum", "Groningen", "Leeuwarden", "Utrecht Centraal", "Utrecht Centraal", "Utrecht Centraal", "Utrecht Centraal", "Utrecht Centraal", "Amsterdam Centraal", "Amsterdam Centraal", "Amsterdam Centraal", "Amsterdam Centraal"]

        self.total_trajectories = 0

        # variable for keeping track of used connections
        self.used_connections: set[int] = set()

        # stores a solution
        self.solution: dict[int, list[str]] = {}

        self.highest_score = 0
        self.highest_score_solution: Solution = None

        # self.score_file = ScoreFile("baseline.csv")

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
        index = self.total_trajectories % self.constrictions.max_trajectories
        name = eval(f"self.preferred_departure_{self.dataset}[{index}]")
        station = self.stations[name]
        trajectory.add_station(name)
        return name, station

    def make_trajectory(self, unique: bool = False, prefixed: bool = True) -> Trajectory:
        # add randomly chosen connections and stations to trajectory as long as
        # restrictions are still met

        self.repopulate_possible_connections_for_all_stations()

        trajectory = Trajectory()

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
            # possible connections in unique is True
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

        # increment trajectory counter
        self.total_trajectories += 1

        return trajectory

    def reset_used_connections(self) -> None:
        """ Clears the list of all used connections. """

        self.used_connections.clear()

    def run(self, iterations: int, visualize: bool, verbose: bool = False, write_output: bool = True, auto_open: bool = False) -> Solution | Output:
        """ Creates a solution of with the maximum amount of trajectories. """

        self.reset_used_connections()

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
        if self.__class__.__name__ == "Randomize":
            solution = Output(trajectories, is_valid)
        else:
            solution = Solution(trajectories, is_valid)
            # self.score_file.write_score(solution.score)

        # if solution.score > self.highest_score:
        #     self.highest_score = solution.score
        #     self.highest_score_solution = solution

        if self.verbose:
            print(f"Score: {solution.score}")

            for trajectory in solution.trajectories:
                print("Stations:", end="")
                print(trajectory, end="")
                print()

        # visualization
        if visualize:
            plot_device = PlotlyLoad(dataset=self.dataset)
            plot_device.draw_graph(solution, auto_open)

        return solution
