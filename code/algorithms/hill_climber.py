from code.classes.trajectory import Trajectory
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.solution import Solution
from code.classes.output import Output
from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize

import random
import copy


class HillClimber:
    """ Algorithm following the Hill Climber technique. """

    def __init__(self, solution: Solution):
        self.verbose = False
        self.solution = copy.deepcopy(solution)
        self.trajectories = list(self.solution.trajectories)
        self.score = self.solution.score

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

        self.delete_trajectory(trajectory, new_solution)
        new_trajectory = Randomize.make_trajectory()
        self.trajectories.append(new_trajectory)
        # save new set of trajectories in new solution object
        new_solution.trajectories = set(trajectories)

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
            return True
        return False

    def run(self, iterations: int, verbose: bool = False):
        """ Runs the Hill Climber algorithm for a given amount of iterations. """
        self.verbose = verbose

        for iteration in range(iterations):
            new_solution = copy.deepcopy(self.solution)
            # choose random trajectory
            trajectory = self.choose_trajectory()
            # delete trajectory
            self.delete_trajectory(trajectory, new_solution)

            # if score is not better, mutate trajectory
            if not self.check_score(new_solution):
                # try a new trajectory
                self.mutate_trajectory(trajectory, new_solution)
                # check score
                self.check_score(new_solution)
