from code.classes.trajectory import Trajectory
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.solution import Solution
from code.classes.output import Output
from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize

import random
import copy
import os


class HillClimber:
    """ Algorithm following the Hill Climber technique. """

    def __init__(self, dataset: str):
        self.verbose = False
        self.railNL = RailNL(dataset=dataset)
        self.randomize = Randomize(dataset, self.railNL.stations, self.railNL.connections)
        self.solution: Solution = None
        self.trajectories: list[Trajectory] = None
        self.score: int = None
        self.iterations: int = None

    def make_first_solution(self):
        """ Creates a random solution to begin the Hill Climber algorithm. """

        self.solution = self.randomize.make_solution(write_output=False)
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

        new_trajectory = self.randomize.make_trajectory()
        self.trajectories.append(new_trajectory)
        # save new set of trajectories in new solution object
        new_solution.trajectories = set(self.trajectories)
        # update score of solution to new score
        self.solution.score = new_solution.calculate_score()

    def check_score(self, new_solution: Solution):
        """ Checks and accepts better solutions than the current one. """

        new_score = new_solution.calculate_score()

        if self.verbose:
            print(f"Old score: {self.score}")
            print(f"New score: {new_score}")

        if new_score > self.score:
            # change trajectories of solution to improved trajectories
            self.solution.trajectories = new_solution.trajectories
            # change score to new score
            self.score = new_score
            # update score of solution to improved score
            self.solution.score = new_score

            if self.verbose:
                print(f"Accepted {new_score}")
            return True
        return False

    @staticmethod
    def clear_scores_file() -> None:
        file_path = "data/scores/hill_climber.csv"

        if os.path.exists(file_path):
            input("WARNING scores file will be deleted.")
            os.remove(file_path)

    def prepare_csv_file(self) -> None:
        self.clear_scores_file()

        if not (os.path.exists("data/scores") and os.path.isdir("data/scores")):
            os.mkdir("data/scores")

        with open("data/scores/hill_climber.csv", "w") as file:
            file.write("score\n")

    def write_score(self) -> None:
        with open("data/scores/hill_climber.csv", "a") as file:
            file.write(str(self.score))
            file.write("\n")

    def run(self, iterations: int, mutations: int = 1, verbose: bool = False):
        """ Runs the Hill Climber algorithm for a given amount of iterations. """

        self.verbose = verbose

        self.iterations = iterations
        self.make_first_solution()
        self.prepare_csv_file()

        for _ in range(iterations):
            self.new_solution(mutations)

            # write score to csv file
            self.write_score()

    def new_solution(self, mutations: int) -> Solution:
        """ Creates a new solution with the given amount of mutations. """

        new_solution = copy.deepcopy(self.solution)

        for _ in range(mutations):
            # choose random trajectory
            trajectory = self.choose_trajectory()
            # delete trajectory
            self.delete_trajectory(trajectory, new_solution)

            # if there are no more trajectories to mutate or delete, stop loop
            if not self.trajectories:
                break

        # if score is not better, mutate trajectory
        if not self.check_score(new_solution):
            for _ in range(mutations):
                # try a new trajectory
                self.mutate_trajectory(trajectory, new_solution)
                # check score
                self.check_score(new_solution)
