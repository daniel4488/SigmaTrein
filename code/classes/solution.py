from code.classes.trajectory import Trajectory
from code.classes.railNL import RailNL


class Solution:
    """ Solution class to hold all information of one schedule. """
    def __init__(self, trajectories: set[Trajectory], is_valid: bool):
        """ Creates a Solution object. """
        self.is_valid: bool = is_valid
        self.trajectories: set[Trajectory] = trajectories
        self.score: float = self.calculate_score()
        self.write_score()

    def calculate_score(self) -> float:
        """
        Calculates the score of the Solution.

        Formula: K = p * 10000 - (T * 100 + Min)
        p: fraction of used connections
        T: number of trajectories
        Min: number of minutes used in all trajectories
        """
        # number of trajectories
        T = len(self.trajectories)

        # initialise set of used connections
        used_connections = set()

        # initialise number of minutes
        Min = 0.0

        # iterate over trajectories in the schedule
        for traject in self.trajectories:
            # add connections to set of used connections
            used_connections.update(traject.connections)

            # increment number of minutes
            Min += traject.duration

        # make sure variable holding number of connection has not the default value
        assert RailNL.NUMBER_OF_CONNECTIONS != -1

        # calculate fraction of used connections
        p = len(used_connections) / RailNL.NUMBER_OF_CONNECTIONS

        # calculate score
        K = p * 10000 - (T * 100 + Min)
        print(f"T = {T}")
        print(f"Min = {Min}")
        print(f"p = {p}")

        # return score
        return K

    def write_score(self) -> None:
        """ Append score to a scores csv file. """
        with open("data/scores/random.csv", "a") as file:
            file.write(str(self.score))
            file.write("\n")
