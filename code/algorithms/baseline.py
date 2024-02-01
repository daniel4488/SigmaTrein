from code.algorithms.randomize import Randomize
from code.classes.output import Output
from code.classes.solution import Solution
from code.classes.write_file import ScoreFile
from code.visualisation.baseline import visualize_baseline
from code.visualisation.map_class import MapVisualization

from tqdm import tqdm


class Baseline(Randomize, MapVisualization):
    """
    Class to create a baseline from our random algorithm.
    """

    def __init__(self, dataset: str) -> None:

        super().__init__(dataset=dataset)
        # Create score file
        self.score_file = ScoreFile("baseline.csv")
        self.highest_score = 0
        self.highest_score_solution: Solution | None = None

    def run(self, iterations: int, visualize: bool, verbose: bool = False, auto_open: bool = False, unique: bool = True, prefixed: bool = False) -> None:
        """ Runs baseline for random algorthm. """

        print("Creating baseline...")

        self.verbose = verbose

        self.score_file.prepare_file()

        try:
            # create solutions and write score to score file
            for _ in tqdm(range(iterations)):
                
                solution = super().run(iterations=1, visualize=False, verbose=verbose, write_output=True, auto_open=auto_open, unique=unique, prefixed=prefixed)

                # write score to csv file
                self.score_file.write_score(solution.score)

                # check if a new highest score has been found
                if solution.score > self.highest_score:
                    self.highest_score = solution.score
                    self.highest_score_solution = solution

        except KeyboardInterrupt:
            pass

        # create output object
        Output(self.highest_score_solution.trajectories, True)

        # visualize results
        if visualize:
            data = "data/scores/baseline.csv"

            # create map
            self.visualize(solution=self.highest_score_solution, auto_open=auto_open)
            # histogram of scores from random algorithm
            visualize_baseline(data)
