from code.algorithms.randomize import Randomize
from code.classes.railNL import RailNL
from code.classes.solution import Solution
from code.classes.trajectory import Trajectory
from code.classes.write_file import ScoreFile
from code.functions.to_snake_case import to_snake_case
from code.visualisation.map_class import MapVisualization

import copy
import random
from tqdm import tqdm


class HillClimber(MapVisualization):
    """
    Algorithm following the Hill Climber technique.

    This algorithm starts by creating a solution from our random algorithm.
    Thereafter, it starts deleting a chosen number of trajectories, and checks
    if these solutions return better scores. If not, it tries to make random
    new solutions for every deleted trajectory. This process is repeated for
    a given amount of iterations.

    Hill Climber starts with data from a RailNL object and an initial random
    solution. Furthermore, it keeps track of the current trajectories of the
    possible new solution, the score of the current best solution, and the
    number of iterations.
    """

    def __init__(self, dataset: str):

        self.dataset = dataset
        self.verbose = False
        self.railNL = RailNL(dataset=dataset)
        self.randomize = Randomize(dataset)

        # variables to keep track of current solution
        self.solution: Solution | None = None
        self.trajectories: list[Trajectory] | None = None
        self.score: int | None = None
        self.iterations: int | None = None

        # initialize score file
        self.scores_path: str = f"data/scores/{to_snake_case(self.__class__.__name__)}.csv"
        self.score_file: ScoreFile = ScoreFile(f"{to_snake_case(self.__class__.__name__)}.csv")

    def make_first_solution(self):
        """ Creates a solution with the random algorithm to
            begin the Hill Climber algorithm. """

        self.solution = self.randomize.run(iterations=1, visualize=False, write_output=False, auto_open=False)
        self.score = self.solution.score
        self.trajectories = list(self.solution.trajectories)
        self.solution.algorithm = self.__class__.__name__

    def choose_trajectory(self):
        """ Selects random trajectory from current solution. """

        trajectory = random.choice(self.trajectories)
        return trajectory

    def delete_trajectory(self, trajectory: Trajectory, new_solution: Solution):
        """ Deletes a trajectory. """

        self.trajectories.remove(trajectory)
        # save new set of trajectories in new solution object
        new_solution.trajectories = set(self.trajectories)

    def mutate_trajectory(self, new_solution: Solution):
        """ Mutates a trajectory and the new solution. """

        # create new random trajectory
        new_trajectory = self.randomize.make_trajectory(unique=True, prefixed=False)
        self.trajectories.append(new_trajectory)

        # save new set of trajectories in new solution object
        new_solution.trajectories = set(self.trajectories)

    def check_score(self, new_solution: Solution):
        """ Checks scores of new solutions, and accepts mutations
            if they result in a higher score. """

        new_score = new_solution.calculate_score()
    
        # prints old and new scores if verbose is True
        if self.verbose:
            print(f"Old score: {self.score}")
            print(f"New score: {new_score}")

        # updates the new solution and score instance and return True,
        # if the new score is higher than the current one
        if new_score > self.score:
            self.solution.trajectories = new_solution.trajectories
            self.score = new_score
            self.solution.score = new_score

            if self.verbose:
                print(f"Accepted {new_score}")
            return True
        return False

    def run(self, iterations: int, visualize: bool, mutations: int = 4,
            verbose: bool = False, auto_open: bool = True):
        """ Runs the Hill Climber algorithm for a given amount
            of iterations and mutations. """
        
        print(f"Running {self.__class__.__name__} algorithm...")

        self.verbose = verbose

        self.iterations = iterations
        self.make_first_solution()
        self.score_file.prepare_file()

        # create new solutions and save scores
        try:
            for _ in tqdm(range(iterations)):
                self.new_solution(mutations)
                self.score_file.write_score(self.score)

        except KeyboardInterrupt:
            pass

        # print name of used algorithm and its score if verbose is True
        if self.verbose:
            algorithm = self.__class__.__name__
            print(f"{algorithm} highest score: {self.score}")

        # create visualisation if visualize is True
        if visualize:
            self.create_visual(solution=self.solution, path=self.scores_path, auto_open=auto_open)

    def new_solution(self, mutations: int):
        """ Performs a given amount of mutations on the current solution, and takes on
            a new solution if its score is better. """

        new_solution = copy.deepcopy(self.solution)

        # delete mutations amount of randomly chosen trajectories
        for _ in range(mutations):
            trajectory = self.choose_trajectory()
            self.delete_trajectory(trajectory, new_solution)

            # if there are no more trajectories to delete, stop loop
            if not self.trajectories:
                break

        # if score is not better, create new trajectory
        if not self.check_score(new_solution):
            # create new trajectories and check their scores
            for _ in range(mutations):
                self.mutate_trajectory(new_solution)
                self.check_score(new_solution)
        else:
            self.solution.score = new_solution.calculate_score()
