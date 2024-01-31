from code.algorithms.randomize import Randomize
from code.classes.output import Output
from code.classes.solution import Solution
from code.classes.write_file import ScoreFile
from code.visualisation.baseline import visualize_baseline
from code.visualisation.map_class import MapVisualization


class Baseline(Randomize, MapVisualization):
    """
    Class to create a baseline from our random algorithm.
    """

    def __init__(self, dataset: str) -> None:

        super().__init__(dataset=dataset)
        self.score_file = ScoreFile("baseline.csv")
        self.highest_score = 0
        self.highest_score_solution: Solution = None

    def run(self, iterations: int, visualize: bool, verbose: bool = False, auto_open: bool = False, unique: bool = True, prefixed: bool = False) -> None:
        
        print("Creating baseline...")
        self.verbose = verbose

        self.score_file.prepare_file()

        i = 0

        try:
            for _ in range(iterations):
                if i % 10000 == 0:
                    print(f"{i} iterations")
                solution = super().run(iterations=1, visualize=False, verbose=verbose, write_output=True, auto_open=auto_open, unique=unique, prefixed=prefixed)
                self.score_file.write_score(solution.score)

                if solution.score > self.highest_score:
                    self.highest_score = solution.score
                    self.highest_score_solution = solution

                i += 1

        except KeyboardInterrupt:
            pass

        Output(self.highest_score_solution.trajectories, True)

        if visualize:
            data = "data/scores/baseline.csv"
            # map
            self.visualize(solution=self.highest_score_solution, auto_open=auto_open)

            # histogram of scores from random algorithm
            visualize_baseline(data)
