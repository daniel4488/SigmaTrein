from .randomize import Randomize
from code.visualisation.baseline import visualize_baseline
from code.classes.output import Output


class Baseline(Randomize):

    def __init__(self, dataset: str) -> None:
        super().__init__(dataset=dataset)

    def run(self, iterations: int, visualize: bool, verbose: bool = False) -> None:
        self.verbose = verbose

        self.score_file.prepare_file()

        try:
            for _ in range(iterations):
                super().run(iterations=1, visualize=False, verbose=verbose, write_output=True)
        except KeyboardInterrupt:
            pass

        if visualize:
            # csv
            data = "data/scores/baseline.csv"
            Output(self.highest_score_solution.trajectories, True)
            # histogram of scores from random algorithm
            visualize_baseline(data)
