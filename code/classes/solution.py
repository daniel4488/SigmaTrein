from code.classes.trajectory import Trajectory
from code.classes.railNL import RailNL


class Solution:
    def __init__(self, trajectories: set[Trajectory], is_valid: bool, verbose: bool = False):
        self.verbose: bool = verbose
        self.is_valid: bool = is_valid
        self.trajectories: set[Trajectory] = trajectories
        self.score: float = self.calculate_score()
        self.write_score()

    def calculate_score(self) -> float:
        """
        Formula: K = p * 10000 - (T * 100 + Min)
        p: fraction of used connections
        T: number of trajectories
        Min: number of minutes used in all trajectories
        """
        T = len(self.trajectories)
        used_connections = set()
        Min = 0
        for traject in self.trajectories:
            used_connections.update(traject.connections)
            Min += traject.duration
        assert RailNL.NUMBER_OF_CONNECTIONS != -1
        p = len(used_connections) / RailNL.NUMBER_OF_CONNECTIONS

        K = p * 10000 - (T * 100 + Min)
        if self.verbose:
            print(f"T = {T}")
            print(f"Min = {Min}")
            print(f"p = {p}")
        return K

    def write_score(self) -> None:
        with open("data/scores/random.csv", "a") as file:
            file.write(str(self.score))
            file.write("\n")

    def check_is_valid(self, new_trajectory: Trajectory):

        if RailNL.DATASET == "holland":
            return len(self.trajectories) <= 7 and new_trajectory.duration <= 120
        else:
            return len(self.trajectories) <= 20 and new_trajectory.duration <= 180