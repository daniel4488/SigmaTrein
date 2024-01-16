from code.classes.solution import Solution
from code.classes.trajectory import Trajectory

import csv


class Output(Solution):

    def __init__(self, trajectories: set[Trajectory], is_valid: bool):
        super().__init__(trajectories, is_valid)
        self.write_output()

    def write_output(self) -> None:
        # Open a CSV file for writing
        with open("output.csv", "w", newline="") as csvfile:
            # Create a CSV writer object
            writer = csv.writer(csvfile)

            # Write header
            writer.writerow(["train", "stations"])

            # Write trajectory
            for count, trajectory in enumerate(self.trajectories):
                writer.writerow([f"train_{count + 1}", str(trajectory)])

            # Write score
            writer.writerow(["score", self.score])
