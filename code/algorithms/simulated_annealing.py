from .hill_climber import HillClimber
from ..classes.solution import Solution

import math
import random
import numpy as np


def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-x))


class SimulatedAnnealing(HillClimber):

    def __init__(self, dataset: str) -> None:
        # call initializer of super class
        super().__init__(dataset=dataset)

        # starting temperature
        self.start_temperature: float = 1.0

        # current temperature
        self.temperature: float = 1.0

    def update_temperature(self) -> None:
        """
        This function implements a *linear* cooling scheme.
        Temperature will become zero after all iterations passed to the run()
        method have passed.

        Hill climber needs to keep track of number of iterations

        Cooling down schemes:
        *   Linear
        *   Exponential
        *   Geometric decaying
        *
        """
        print(f"total iter: {self.iterations}") if self.verbose else None
        # self.temperature = max(self.temperature - self.start_temperature / self.iterations, 1e-4)

        # Exponential would look like this:
        # alpha = 0.99
        # self.temperature = self.temperature * alpha

        # where alpha can be any value below 1 but above 0

        # Square root
        self.temperature = np.sqrt(self.temperature)

    def check_score(self, new_solution: Solution) -> bool:
        """ Override this function from hill climber. """

        new_score = new_solution.calculate_score()

        print() if self.verbose else None

        if self.verbose:
            print(f"Old score: {self.score}")
            print(f"New score: {new_score}")

        # calculate the acceptance probability of the change
        delta = (self.score - new_score) / 70
        print(f"delta: {delta}") if self.verbose else None
        print(f"temperature: {self.temperature}") if self.verbose else None
        print(f"x: {-delta / self.temperature}") if self.verbose else None
        probability = np.exp(np.longdouble(-delta / self.temperature))
        # probability = sigmoid(x=-delta)
        print(f"probability: {probability}") if self.verbose else None

        # NOTE: Keep in mind that if we want to maximize the value, we use:
        # delta = old_value - new_value

        # draw a random number
        rand = random.random()

        # cooling down
        self.update_temperature()

        # accept new state if random number is below probability
        if rand < probability:
            # change trajectories of solution to improved trajectories
            self.solution.trajectories = new_solution.trajectories

            # change score to new score
            self.score = new_score

            if self.verbose:
                print(f"Accepted {new_score}")

            return True

        return False
