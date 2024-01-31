from code.classes.solution import Solution
from code.classes.trajectory import Trajectory

import csv


class Output(Solution):
    """
    Class describing the solution of an algorithm.
    Class Output inherits from Solution.
    Output extents the solution class by writing an output file. This output file
    is a csv file consisting of every trajectory of a solution, and its score.
    """

    def __init__(self, trajectories: list[Trajectory], is_valid: bool,
                 verbose: bool = False) -> None:

        super().__init__(trajectories, is_valid, verbose=verbose)
        self.write_output()

    def write_output(self) -> None:
        """ Generates output file "output.csv". """

        # open a CSV file for writing
        with open("output.csv", "w", newline="") as csvfile:
            # create a CSV writer object
            writer = csv.writer(csvfile)

            # write header
            writer.writerow(["train", "stations"])

            # write trajectory
            for count, trajectory in enumerate(self.trajectories):
                writer.writerow([f"train_{count + 1}", str(trajectory)])

            # write score
            writer.writerow(["score", self.score])
