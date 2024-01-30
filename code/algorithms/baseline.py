from .randomize import Randomize
from code.visualisation.baseline import visualize_baseline


class Baseline(Randomize):

    def __init__(self, dataset: str) -> None:
        super().__init__(dataset=dataset)

    def run(self, iterations: int, visualize: bool, verbose: bool = False) -> None:
        self.verbose = verbose

        self.prepare_csv_file()

        try:
            for _ in range(iterations):
                super().run(iterations=1, visualize=False, verbose=verbose, write_output=True)
        except KeyboardInterrupt:
            pass

        if visualize:
            # csv
            data = "data/scores/random.csv"

            # histogram of scores from random algorithm
            visualize_baseline(data)
