from .randomize import Randomize
from code.visualisation.baseline import visualize_baseline
from code.classes.output import Output
from code.classes.write_file import ScoreFile
from code.classes.solution import Solution
from code.visualisation.map_class import MapVisualization


class Baseline(Randomize, MapVisualization):

    def __init__(self, dataset: str) -> None:
        super().__init__(dataset=dataset)
        self.score_file = ScoreFile("baseline.csv")
        self.highest_score = 0
        self.highest_score_solution: Solution = None

    def run(self, iterations: int, visualize: bool, verbose: bool = False, auto_open: bool = False) -> None:
        self.verbose = verbose

        self.score_file.prepare_file()

        try:
            for _ in range(iterations):
                solution = super().run(iterations=1, visualize=False, verbose=verbose, write_output=True, auto_open=auto_open)
                self.score_file.write_score(solution.score)

                if solution.score > self.highest_score:
                    self.highest_score = solution.score
                    self.highest_score_solution = solution

        except KeyboardInterrupt:
            pass

        Output(self.highest_score_solution.trajectories, True)

        if visualize:
            # csv
            data = "data/scores/baseline.csv"

            # map
            self.visualize(solution=self.highest_score_solution, auto_open=auto_open)

            # histogram of scores from random algorithm
            visualize_baseline(data)
