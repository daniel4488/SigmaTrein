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
from code.algorithms.randomize import Randomize
from code.visualisation.baseline import visualize_baseline, visualize_iterations_to_score

import random


class AdvancedRandom(Randomize, MapVisualization):
    def __init__(self, dataset: str):
        super().__init__(dataset=dataset)

        self.score_file = ScoreFile("advanced.csv")
        self.highest_score_file = ScoreFile("advanced_highest.csv")
    
    def reset_used_connections_and_weight(self) -> None:
        self.used_connections.clear()
        for _, connection_object in self.connections.items():
            connection_object.reset_weight()

    def make_advanced_trajectory(self, trajectory: Trajectory, departure_station: tuple[str, Station]) -> Trajectory:
        """ Generates a randomly chosen trajectory. """

        self.repopulate_possible_connections_for_all_stations()

        # choose the first departure station
        # departure_station = self.choose_first_departure_station(trajectory)

        # add stations to trajectory as long as its duration is less than 120 mins,
        # and there are still possible connections
        while departure_station[1].possible_connections:
            # choose random connection number from possible connections at departure station
            # connection = departure_station[1].return_random_connection()

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
            if duration_candidate <= self.constrictions.max_time:
                self.update_trajectory(duration_candidate, connection, destination_station[0], trajectory)

                # New
                self.connections[connection].weight += 1
                # update departure station to the current station
                departure_station = destination_station

        # print(trajectory.stations)

        return trajectory
    
    def run(self, iterations: int, visualize: bool, verbose: bool = False, write_output: bool = True, auto_open: bool = False) -> Solution | Output:
        self.score_file.prepare_file()
        self.highest_score_file.prepare_file()

        
        highest_score = 0
        
        i = 0
        
        for _ in range(iterations):
            print(i)
            self.reset_used_connections_and_weight()
            
            trajectories = set()
            for _ in range(20):

                current_trajectory = Trajectory()
                
                departure_station = self.choose_departure_station(current_trajectory)

                # make random trajectory and add to set of trajectories
                trajectories.add(self.make_trajectory(current_trajectory, departure_station))

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
            self.visualize(solution=highest_score_solution, auto_open=auto_open)
            visualize_iterations_to_score("data/scores/advanced_highest.csv", auto_open=auto_open)
            visualize_baseline("data/scores/advanced.csv")

if __name__ == "__main__":
    advancedRandom = AdvancedRandom()
    advancedRandom.run(100, True, False, True)