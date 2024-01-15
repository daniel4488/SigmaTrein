from code.classes.trajectory import Trajectory


class Solution:
    def __init__(self, trajectories: [Trajectory]):
        self.is_valid: bool = False
        self.score: float = self.calculate_score()
        self.trajectories = trajectories

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
            used_connection.union(traject.connections)
            Min += traject.duration
        p = len(used_connection) / 28

        K = p * 10000 - (T * 100 + Min)
        return K


    def make_valid(self) -> None:
        self.is_valid = True

    def __str__(self) -> str:
        raise NotImplemented
