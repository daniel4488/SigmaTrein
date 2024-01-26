from code.classes.trajectory import Trajectory
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.solution import Solution
from code.classes.output import Output
from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize

import random
import copy
import os

class Sigma:
    def __init__(self):
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
        
        # dictionaries with all leftover stations when prefixed routes are layed out
        self.stations: dict[str, Station] = {}
        # dictionaries with all leftover connections when prefixed routes are layed out
        self.connections: dict[str, Connection] = {}

        # initialize an empty set where used connections are going to be stored
        self.used_connections: set[int] = set()

        # indicate that we do not want print statements
        self.verbose = False

        self.load_stations()
        self.load_special_connections()

    def load_stations(self) -> None:
        """ Converts the station data to Station classes. """
        
        # open StationsHolland.csv
        with open(f"data/nationaal/sigmastations.csv", "r") as file:
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
                self.connections[trajectory_number] = Connection(trajectory_number, station_1, station_2, duration)

                # increment the current trajectory number
                trajectory_number += 1

            # make number of connections / trajectories a class variable
            # RailNL.NUMBER_OF_CONNECTIONS = trajectory_number

    def repopulate_possible_connections_for_all_stations(self) -> None:
        """ Prepare for the generation of a new trajectory. """

        for station in self.stations:
            self.stations[station].repopulate_possible_connections()
    
    def make_trajectory(self) -> Trajectory:
        """ Generates a randomly chosen trajectory. """
        

        self.repopulate_possible_connections_for_all_stations()


        # initialize empty trajectory
        trajectory = Trajectory()
        
        if self.standard_trajectories_copy:
            stations: list[str] = self.standard_trajectories_copy.pop(0)
            connections: list[int] = self.standard_trajectories_connections_copy.pop(0)
            trajectory.duration += connections.pop()

            for station in stations:
                trajectory.add_station_to_trajectory(station)

            for connection in connections:
                trajectory.add_connection_number(connection)

            departure_station = (stations[-1], self.stations[stations[-1]])
        else:
            # choose a random station to depart from
            departure_station = self.choose_station(list(self.stations.keys()))

            # add departure station to the trajectory
            trajectory.add_station_to_trajectory(departure_station[0])

        # add stations to trajectory as long as its duration is less than 120 mins,
        # and there are still possible connections
        while trajectory.duration <= 180 and departure_station[1].possible_connections:
            
            # choose random connection number from possible connections at departure station
            #connection = departure_station[1].return_random_connection()

            possible_connections = departure_station[1].return_possible_connections()

            
            # find the connection with the lowest weight using a lambda function
            connection = min(possible_connections, key=lambda connection: self.connections[connection].weight)


            # get destination station from chosen connection 
            destination_station = self.get_station(departure_station[0], connection)

            # remove created connection from destination and departure station's possible connections
            self.update_connections(connection, departure_station[1], destination_station[1])

            # update total duration of the trajectory
            duration_candidate = trajectory.duration + self.connections[connection].duration

            # add station to trajectory if it fits within 120 mins
            if duration_candidate <= 180:
                self.update_trajectory(duration_candidate, connection, destination_station[0], trajectory)

                # New
                self.connections[connection].weight += 1
                # update departure station to the current station
                departure_station = destination_station

        return trajectory
    
    def reset_used_connections(self) -> None:
        self.used_connections.clear()
        for _, connection_object in self.connections.items():
            connection_object.reset_weight()

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
    
    def run(self, write_output = True):

        random.seed(27012001)
        
        self.reset_used_connections()

        trajectories = set()
        is_valid = False
        highest_score = 0 
        iterations = 1
        i = 0
        for _ in range(iterations):
            print(i)
            while is_valid == False:
                self.reset_used_connections()
                self.standard_trajectories_copy = copy.deepcopy(self.standard_trajectories)
                self.standard_trajectories_connections_copy = copy.deepcopy(self.standard_trajectories_connections)

                trajectories = set()
                for _ in range(20):
                    # make random trajectory
                    current_trajectory = self.make_trajectory()

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
        return highest_score_solution

    # def make_baseline(self, verbose: bool = False) -> None:
    #     self.verbose = verbose

    #     self.prepare_csv_file()

    #     number_of_simulations = 100

    #     for _ in range(number_of_simulations):
    #         self.make_solution(write_output=True)