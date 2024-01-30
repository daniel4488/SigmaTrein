from code.classes.trajectory import Trajectory
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.solution import Solution
from code.classes.output import Output
from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize
from code.visualisation.map_class import MapVisualization
from code.algorithms.advanced_random import AdvancedRandom
from code.classes.data import DataInfo

import random
import copy
import os


class Sigma(MapVisualization, AdvancedRandom):
    def __init__(self, dataset: str):

        super().__init__(dataset=dataset)


        # initialize a list with pre-fixed routes that start of a trajectory
        self.standard_trajectories = [["Maastricht", "Sittard", "Heerlen", "Sittard", "Roermond", "Weert", "Eindhoven"],
                                       ["Venlo", "Helmond", "Eindhoven"], ["Vlissingen", "Roosendaal"],
                                       ["Den Helder", "Alkmaar"], ["Enschede", "Hengelo", "Almelo"], ["Lelystad Centrum", "Almere Centrum"]
                                       , ["Zwolle", "Assen", "Groningen", "Leeuwarden", "Heerenveen", "Steenwijk", "Zwolle"]]
        
        # initialize a list with the corresponding connection numbers
        self.standard_trajectories_connections = [[76, 77, 77, 78, 79, 80, 91], 
                                                  [81, 82, 39], [75, 63], [71, 36], 
                                                  [88, 72, 17], [73, 14],
                                                  [74, 83, 84, 86, 85, 87, 146]]
        
        # empty lists where copies of the above lists can be stored
        self.standard_trajectories_copy = []
        self.standard_trajectories_connections_copy = []

        # dictionaries with all leftover connections when prefixed routes are layed out
        self.special_connections: dict[int, Connection] = {}


        # indicate that we do not want print statements
        self.verbose = False

        self.load_special_connections()
        
    def load_special_connections(self):
        with open("data/nationaal/sigmanationaal.csv", "r") as file:
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
                self.special_connections[trajectory_number] = Connection(trajectory_number, station_1, station_2, duration)

                # increment the current trajectory number
                trajectory_number += 1

            # make number of connections / trajectories a class variable
            # RailNL.NUMBER_OF_CONNECTIONS = trajectory_number

    def choose_predetermined_first_departure_station(self, trajectory: Trajectory):

        if self.standard_trajectories_copy:
            stations: list[str] = self.standard_trajectories_copy.pop(0)
            connections: list[int] = self.standard_trajectories_connections_copy.pop(0)
            trajectory.duration += connections.pop()

            for station in stations:
                trajectory.add_station(station)

            for connection in connections:
                trajectory.add_connection_number(connection)

            departure_station = (stations[-1], self.stations[stations[-1]])
        else:
            # choose a random station to depart from
            departure_station = self.choose_station(list(self.stations.keys()))

            # add departure station to the trajectory
            trajectory.add_station(departure_station[0])

        return departure_station
    
    def make_sigma_trajectory(self) -> Trajectory:
        """ Generates a randomly chosen trajectory. """

        self.repopulate_possible_connections_for_all_stations()

        # initialize empty trajectory
        trajectory = Trajectory()

        departure_station = self.choose_predetermined_first_departure_station(trajectory)
        
        return self.make_trajectory(trajectory, departure_station, self.special_connections)
    
    def run(self, iterations: int, visualize: bool, verbose: bool):

        random.seed(27012001)
        
        self.reset_used_connections(self.special_connections)

        trajectories = set()
        is_valid = False
        highest_score = 0 
        # iterations = 1
        i = 0
        for _ in range(iterations):
            print(i)
            while is_valid == False:
                self.reset_used_connections(self.special_connections)
                self.standard_trajectories_copy = copy.deepcopy(self.standard_trajectories)
                self.standard_trajectories_connections_copy = copy.deepcopy(self.standard_trajectories_connections)

                trajectories = set()
                for _ in range(20):
                    # make random trajectory
                    current_trajectory = self.make_sigma_trajectory()

                    # add to set of trajectories
                    trajectories.add(current_trajectory)

                    # add trajectory connections to used_connections
                    self.used_connections.update(current_trajectory.connections)
                    # print(len(self.used_connections))
                    if len(self.used_connections) == 89:
                        is_valid = True

            i += 1
            # NEW
            trajectories = list(trajectories)

            # create solution instance
            # if write_output:
            # else:
            solution = Solution(trajectories, is_valid, self.__class__.__name__)

            if solution.score > highest_score:
                highest_score = solution.score
                highest_score_solution = Output(trajectories, is_valid)


            if self.verbose:
                print(f"Score: {solution.score}")

                for trajectory in solution.trajectories:
                    print("Stations:", end="")
                    print(trajectory, end="")
                    print()
            
            is_valid = False

        
        print(highest_score)

        if visualize:
            self.visualize(solution=highest_score_solution)

        return highest_score_solution

    # def make_baseline(self, verbose: bool = False) -> None:
    #     self.verbose = verbose

    #     self.prepare_csv_file()

    #     number_of_simulations = 100

    #     for _ in range(number_of_simulations):
    #         self.make_solution(write_output=True)