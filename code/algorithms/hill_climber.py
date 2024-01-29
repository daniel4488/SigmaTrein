from code.classes.trajectory import Trajectory
from code.classes.solution import Solution
from code.classes.railNL import RailNL
from code.classes.write_file import ScoreFile
from code.algorithms.randomize import Randomize
from code.functions.to_snake_case import to_snake_case
from code.visualisation.baseline import visualize_iterations_to_score

import random
import copy


class HillClimber:
    """
    Algorithm following the Hill Climber technique.
    Hill Climber starts with data from a RailNL object and an initial random
    solution. Furthermore, it keeps track of the current trajectories of the
    possible new solution, the score of the current best solution, and the
    number of iterations.
    """

    def __init__(self, dataset: str):

        self.verbose = False
        self.railNL = RailNL(dataset=dataset)
        self.randomize = Randomize(dataset)
        self.solution: Solution = None
        self.trajectories: list[Trajectory] = None
        self.score: int = None
        self.iterations: int = None
        self.scores_path: str = f"data/scores/{to_snake_case(self.__class__.__name__)}.csv"
        self.score_file: ScoreFile = ScoreFile(f"{to_snake_case(self.__class__.__name__)}.csv")

    def make_first_solution(self):
        """ Creates a solution with the random algorithm to
            begin the Hill Climber algorithm. """

        self.solution = self.randomize.run(iterations=1, visualize=False, write_output=False)
        self.score = self.solution.score
        self.trajectories = list(self.solution.trajectories)

    def choose_trajectory(self):
        """ Selects random trajectory from current solution. """

        trajectory = random.choice(self.trajectories)
        return trajectory

    def delete_trajectory(self, trajectory: Trajectory, new_solution: Solution):
        """ Deletes a trajectory. """

        self.trajectories.remove(trajectory)
        # save new set of trajectories in new solution object
        new_solution.trajectories = set(self.trajectories)

    def mutate_trajectory(self, trajectory: Trajectory, new_solution: Solution):
        """ Mutates a trajectory and the new solution. """

        # create new random trajectory
        new_trajectory = self.randomize.make_trajectory()
        self.trajectories.append(new_trajectory)

        # save new set of trajectories in new solution object
        new_solution.trajectories = set(self.trajectories)

        # update score of solution to new score
        self.solution.score = new_solution.calculate_score()

    def check_score(self, new_solution: Solution):
        """ Checks scores of new solutions, and accepts mutations
            if they result in a higher score. """

        new_score = new_solution.calculate_score()

        # prints old and new scores if verbose is True
        if self.verbose:
            print(f"Old score: {self.score}")
            print(f"New score: {new_score}")

        # updates the new solution and score instance and return True,
        # if the new score is higher than the old one
        if new_score > self.score:
            self.solution.trajectories = new_solution.trajectories
            self.score = new_score
            self.solution.score = new_score

            if self.verbose:
                print(f"Accepted {new_score}")
            return True
        return False

    def run(self, iterations: int, visualize: bool, mutations: int = 1,
            verbose: bool = False):
        """ Runs the Hill Climber algorithm for a given amount
            of iterations and mutations. """

        self.verbose = verbose

        self.iterations = iterations
        self.make_first_solution()
        self.score_file.prepare_file()

        # create new solutions and save scores
        for _ in range(iterations):
            self.new_solution(mutations)
            self.score_file.write_score(self.score)

        if visualize:
            visualize_iterations_to_score(data=self.scores_path)

    def new_solution(self, mutations: int) -> Solution:
        """ Creates a new solution with the given amount of mutations. """

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
                self.mutate_trajectory(trajectory, new_solution)
                self.check_score(new_solution)
