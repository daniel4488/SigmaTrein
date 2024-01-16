from code.classes.trajectory import Trajectory
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.solution import Solution
from code.classes.output import Output
from code.classes.railNL import RailNL

import random

class LessRandom:
    def __init__(self, stations: dict[str, Station], connections: dict[int, Connection]):
        self.stations = stations
        self.connections = connections

        self.preferred_departure = ["Den Helder", "Dordrecht", "Hoorn", "Schiphol Airport", "Gouda", "Heemstede-Aerdenhout", "Schiphol Airport"]
        self.preferred_departure_copy = []

        self.used_connections: set = set()
        # self.population = self.generate_population(5)


    def generate_solution(self):
        """
        CAUTION: may run indefinitely
        """
        while (not (solution := self.make_random_solution()).is_valid):
            print(solution.is_valid)
            continue

        return solution

    def generate_population(self, size: int):
        return [self.generate_solution() for _ in range(size)]
    
    def fitness(self, solution: Solution) -> int:
        return solution.score

    def repopulate_possible_connections_for_all_stations(self) -> None:
        """ Prepare for the generation of a new trajectory. """
        for station in self.stations:
            self.stations[station].repopulate_possible_connections()

    def repopulate_preferred_departure_stations(self) -> None:
        self.preferred_departure_copy = self.preferred_departure[:]
         
    def make_random_trajectory(self) -> Trajectory:
        """ Generates a randomly chosen trajectory. """
        
        self.repopulate_possible_connections_for_all_stations()

        # initialize empty trajectory
        random_trajectory = Trajectory()
        
        # choose a random station to depart from
        random_departure_station = self.preferred_departure_copy.pop(0)
        random_departure_station_object = self.stations[random_departure_station]

        # add departure station to the trajectory
        random_trajectory.add_station_to_trajectory(random_departure_station)

        # add stations to trajectory as long as its duration is less than 120 mins,
        # and there are still possible connections
        while random_trajectory.duration <= 120 and random_departure_station_object.possible_connections:
            
            # choose random connection number from possible connections at departure station
            random_connection = random.choice(random_departure_station_object.possible_connections)
            

            # get name of destination station from chosen connection 
            random_destination_station = self.connections[random_connection].get_destination_station(random_departure_station)

            # get destination station object
            random_destination_station_object = self.stations[random_destination_station]

            # remove created connection from destination and departure station's possible connections
            random_destination_station_object.remove_possible_connection(random_connection)
            random_departure_station_object.remove_possible_connection(random_connection)

            # update total duration of the trajectory
            duration_candidate = random_trajectory.duration + self.connections[random_connection].duration
            # add station to trajectory if it fits within 120 mins
            if duration_candidate <= 120:
                # add station to trajectory
                random_trajectory.add_station_to_trajectory(random_destination_station)

                # promote candidate
                random_trajectory.duration = duration_candidate

                random_trajectory.add_connection_number(random_connection)

                # update departure station to the current station
                random_departure_station = random_destination_station
                random_departure_station_object = random_destination_station_object

        # create trajectory list of stations
        return random_trajectory
    
    def reset_used_connections(self) -> None:
        self.used_connections.clear()

    def make_random_solution(self):
        self.reset_used_connections()

        trajectories = set()
        is_valid = False

        for _ in range(7):
            # Make random trajectory
            current_trajectory = self.make_random_trajectory()

            # Add to set of trajectories
            trajectories.add(current_trajectory)

            # Add trajectory connections to used_connections
            self.used_connections.update(current_trajectory.connections)

            if len(self.used_connections) == RailNL.NUMBER_OF_CONNECTIONS:
                is_valid = True
                print(is_valid)
                break
            
        solution = Solution(trajectories, is_valid)
        score = solution.score
            
        return score

    def run(self) -> None:

        number_of_simulations = 10000
        highest_score = 0

        for _ in range(number_of_simulations):
            self.repopulate_preferred_departure_stations()
            score = self.make_random_solution()

            if score > highest_score:
                highest_score = score

        print(highest_score)