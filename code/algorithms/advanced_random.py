from code.algorithms.randomize import Randomize
from code.classes.output import Output
from code.classes.solution import Solution
from code.classes.station import Station
from code.classes.trajectory import Trajectory
from code.classes.write_file import ScoreFile
from code.visualisation.baseline import visualize_baseline
from code.visualisation.map_class import MapVisualization


class AdvancedRandom(Randomize, MapVisualization):
    """
    Algorithm following our custom Advanced Random algorithm.

    This algorithm chooses a random departing station. From there, it uses a
    heuristic, to choose random between connections with the lowest weight.
    This weight is determined by how many times the connection has been made
    in prior trajectories.

    AdvancedRandom takes the Randomize class as a parent.
    """

    def __init__(self, dataset: str):

        super().__init__(dataset=dataset)

        self.score_file = ScoreFile("advanced.csv")
        self.highest_score_file = ScoreFile("advanced_highest.csv")

    def reset_used_connections_and_weight(self) -> None:
        """ Clear the instance list of used connections and set weight of every
            connection back to zero. """

        self.used_connections.clear()
        for _, connection_object in self.connections.items():
            connection_object.reset_weight()

    def make_advanced_trajectory(self, trajectory: Trajectory,
                                 departure_station: tuple[str, Station]) \
            -> Trajectory:
        """ Generates a randomly chosen trajectory with unique connections and
            increases weight of chosen connections. """

        self.repopulate_possible_connections_for_all_stations()

        # add stations to trajectory while there are possible connections
        while departure_station[1].possible_connections:

            possible_connections = departure_station[1] \
                .return_possible_connections()

            # select connection with lowest weight using lambda function
            connection = min(possible_connections,
                             key=lambda connection:
                             self.connections[connection].weight)

            # get destination station from chosen connection
            destination_station = self.get_station(departure_station[0],
                                                   connection)

            # remove created connection from destination and departure
            # station's possible connections
            self.update_connections(connection, departure_station[1],
                                    destination_station[1])

            # update total duration of the trajectory
            duration_candidate = trajectory.duration + \
                self.connections[connection].duration

            # add station to trajectory if it fits within time restriction
            if duration_candidate <= self.constrictions.max_time:
                self.update_trajectory(duration_candidate, connection,
                                       destination_station[0], trajectory)

                # increase weight of connection
                self.connections[connection].weight += 1
                # update departure station to the current station
                departure_station = destination_station

        return trajectory

    def run(self, iterations: int, visualize: bool, verbose: bool = False,
            write_output: bool = True,
            auto_open: bool = False) -> Solution | Output:
        """ Creates solutions with the maximum amount of trajectories and
            saves their scores in a csv file. """

        self.score_file.prepare_file()
        self.highest_score_file.prepare_file()

        highest_score = 0

        try:
            for _ in range(iterations):

                self.reset_used_connections_and_weight()
                trajectories = set()

                # loop for the maximum amount of trajectories
                for _ in range(int(self.constrictions.max_trajectories)):

                    current_trajectory = Trajectory()

                    departure_station = self.choose_departure_station(current_trajectory)

                    # make advanced trajectory and add to set of trajectories
                    trajectories.add(self.make_advanced_trajectory
                                     (current_trajectory, departure_station))

                    # add trajectory connections to used_connections
                    self.used_connections.update(current_trajectory.connections)

                    if len(self.used_connections) == 89:
                        break

                trajectories = list(trajectories)

                # create the solution object and write the score to a csv file
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

                    print(highest_score)
        except KeyboardInterrupt:
            pass

        if visualize:
            self.create_visual(solution=highest_score_solution,
                               path="data/scores/advanced_highest.csv",
                               auto_open=auto_open)
            visualize_baseline("data/scores/advanced.csv")


if __name__ == "__main__":
    advancedRandom = AdvancedRandom()
    advancedRandom.run(100, True, False, True)
