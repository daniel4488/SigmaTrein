from code.classes.trajectory import Trajectory
from code.classes.connection import Connection
from code.classes.station import Station
from code.classes.solution import Solution
from code.classes.output import Output
from code.algorithms.advanced_random import AdvancedRandom
from code.classes.write_file import ScoreFile
from code.visualisation.map_class import MapVisualization
from code.visualisation.baseline import visualize_baseline, visualize_iterations_to_score

import random
import copy


class Sigma(AdvancedRandom, MapVisualization):
    """
    Algorithm following our custom Sigma algorithm.

    This algorithm has a list with a few predetermined consecutive stations
    and connections. These are fixed pieces where some trajectories must start
    with. From there on out it fills up every trajectory with randomly chosen
    connections.

    Sigma takes the AdvancedRandom class as a parent. Furthermore it has a list
    with prefixed routes and a list with corresponding connections. 
    """

    def __init__(self, dataset: str):

        super().__init__(dataset=dataset)

        self.score_file = ScoreFile("sigma.csv")
        self.highest_score_file = ScoreFile("sigma_highest.csv")
        self.highest_score_file.prepare_file()

        # list with pre-fixed routes that start a trajectory
        self.standard_stations = [["Maastricht", "Sittard", "Heerlen", "Sittard", "Roermond", "Weert", "Eindhoven"],
                                       ["Venlo", "Helmond", "Eindhoven"], ["Vlissingen", "Roosendaal"],
                                       ["Den Helder", "Alkmaar"], ["Enschede", "Hengelo", "Almelo"], ["Lelystad Centrum", "Almere Centrum"]
                                       , ["Zwolle", "Assen", "Groningen", "Leeuwarden", "Heerenveen", "Steenwijk", "Zwolle"]]
        
        # list with corresponding connection numbers to the prefixed routes,
        # in each list the last number represents the trajectory duration
        self.standard_connections = [[76, 77, 77, 78, 79, 80, 91], 
                                                  [81, 82, 39], [75, 63], [71, 36], 
                                                  [88, 72, 17], [73, 14],
                                                  [74, 83, 84, 86, 85, 87, 146]]
        
        # empty lists where copies of the lists above can be stored
        self.standard_stations_copy = []
        self.standard_connections_copy = []

    def choose_predetermined_first_departure_station(self, trajectory: Trajectory):
        """ Prefixed list of stations and connections are added to a trajectory,
            from there a random connection to a departure station is chosen. The
            departure station is returned. """

        # if there are still standard trajectories
        if self.standard_stations_copy:
            # select stations and connections lists from standard list
            stations: list[str] = self.standard_stations_copy.pop()
            connections: list[int] = self.standard_connections_copy.pop()

            # add every station, connection and their duration to the trajectory
            trajectory.duration += connections.pop()

            for station in stations:
                trajectory.add_station(station)

            for connection in connections:
                trajectory.add_connection_number(connection)

            departure_station = (stations[-1], self.stations[stations[-1]])

        # if there are no more predetermined stations, choose a random next one
        else:
            departure_station = self.choose_station(list(self.stations.keys()))

            # add random departure station to the trajectory
            trajectory.add_station(departure_station[0])

        return departure_station

    def make_sigma_trajectory(self) -> Trajectory:
        """ Returns a trajectory that starts with a predetermined part, and
            is supplemented with random stations. """

        # initialize empty trajectory
        trajectory = Trajectory()

        departure_station = self.choose_predetermined_first_departure_station(trajectory)
        
        return self.make_advanced_trajectory(trajectory, departure_station)
    
    def run(self, iterations: int, visualize: bool, verbose: bool, auto_open: bool):
        """ Runs """
        
        # prepare csv file
        self.score_file.prepare_file()

        is_valid = False

        # set a parameter that keeps track of the highest score
        highest_score = 0 
        # set a parametere that keeps track of the amount of iterations
        i = 0
        for _ in range(iterations):
            # print iterations
            print(i)
            # while no valid solution is valid, i.e. all connections used by trajectories
            while not is_valid:

                self.reset_used_connections()
                # repopulate the standard trajectories copy
                self.standard_stations_copy = copy.deepcopy(self.standard_stations)
                # repopulate the standard trajectories connections copy
                self.standard_connections_copy = copy.deepcopy(self.standard_connections)
                # make sure that the trajectories set is empty
                trajectories = set()
                # create at most the maximum amount of new trajectories 
                for _ in range(int(self.constrictions.max_trajectories)):
                    # make random trajectory
                    current_trajectory = self.make_sigma_trajectory()

                    # add to set of trajectories
                    trajectories.add(current_trajectory)

                    # add trajectory connections to used_connections
                    self.used_connections.update(current_trajectory.connections)
                    # check if a solution is valid if all connections are used
                    if len(self.used_connections) == 89:
                        is_valid = True
                        break
                        

            i += 1
            # NEW
            trajectories = list(trajectories)

            solution = Solution(trajectories, is_valid, self.__class__.__name__)

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
                print(highest_score)

            is_valid = False

        Output(highest_score_solution.trajectories, is_valid)

        if visualize:
            self.visualize(solution=highest_score_solution, auto_open=auto_open)
            visualize_iterations_to_score("data/scores/sigma_highest.csv", auto_open=auto_open)
            visualize_baseline("data/scores/sigma.csv")
