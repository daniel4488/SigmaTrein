from code.classes.trajectory import Trajectory


class Solution:
    def __init__(self, trajectories: set[Trajectory], is_valid: bool):
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
            used_connections.union(traject.connections)
            Min += traject.duration
        p = len(used_connections) / 28

        K = p * 10000 - (T * 100 + Min)
        return K

    def write_score(self) -> None:
        with open("data/scores/random.csv", "a") as file:
            file.write(str(self.score))
            file.write("\n")

    def __str__(self) -> str:
        raise NotImplemented
