from .randomize import Randomize
from code.visualisation.baseline import visualize_baseline


class Baseline(Randomize):

    def __init__(self, dataset: str) -> None:
        super().__init__(dataset=dataset)

    def run(self, iterations: int, visualize: bool, verbose: bool = False) -> None:
        self.verbose = verbose

        self.prepare_csv_file()

        for _ in range(iterations):
            self.make_solution(write_output=True)

        if visualize:
            # csv
            data = "data/scores/random.csv"

            # histogram of scores from random algorithm
            visualize_baseline(data)
