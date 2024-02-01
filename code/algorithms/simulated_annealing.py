from code.algorithms.hill_climber import HillClimber
from code.classes.solution import Solution

import numpy as np
import random


class SimulatedAnnealing(HillClimber):
    """
    Algorithm following the Simulated Annealing algorithm.

    Simulated annealing originates and is inspired by the annealing process in metallurgy,
    in which metal is heated to a high temperature and then gradually cooled down.
    The algorithm of simulated annealing works in a similar way.
    Simulated annealing falls in the class of iterative metaheuristic algorithms.
    It starts with a very high temperature and gradually cools down.
    While the temperature decreases it becomes less likely that it accepts worse solutions.
    In that way, the algorithm ideally converges.
    The difference with hill climber is that it not only makes improvements,
    but also could accept downturns.
    The idea behind this is that simulated annealing could escape from a local maxima,
    where hill climber would end, and reach the global maxima.

    Simulated annealing has a parameter that can be set which is the starting temperature.
    There are also a number of ways how the cooling down could be implemented.
    In this version, simulated annealing is implemented with the following cooling down schemes:
    *   linear
    *   exponential
    *   root
    *   constant

    There is an argument available to choose between the different cooling down schemes,
    by default it is set to linear.

    SimulatedAnnealing takes the HillClimber class as a parent. Furthermore, it has a
    float for the starting temperature, and a float for the current temperature.
    """

    def __init__(self, dataset: str, start_temperature: float = 10, cooling_scheme: str = "linear", alpha: float = 0.99) -> None:

        # call initializer of super class
        super().__init__(dataset=dataset)

        self.start_temperature: float = start_temperature
        self.temperature: float = start_temperature

        # multiple cooling scheme techniques
        schemes = {"linear", "exponential", "constant", "root"}
        assert cooling_scheme in schemes

        self.cooling_scheme = cooling_scheme
        self.alpha = alpha

    def update_temperature(self) -> None:
        """
        This function implements a *linear* cooling scheme.
        Temperature will become zero after all iterations passed to the run()
        method have passed.

        Cooling down schemes:
        *   Linear
        *   Exponential
        *   Constant
        *   Root
        """

        # print number of iterations if verbose is True
        print(f"total iter: {self.iterations}") if self.verbose else None

        match self.cooling_scheme:
            case "linear":
                self.temperature = max(self.temperature - self.start_temperature / self.iterations, 1e-4)
            case "exponential":
                self.temperature *= self.alpha
            case "root":
                self.temperature -= np.sqrt(self.temperature)
            case "constant":
                pass

    def check_score(self, new_solution: Solution) -> bool:
        """ Override this function from Hill Climber. """

        new_score = new_solution.calculate_score()

        if self.verbose:
            print(f"Old score: {self.score}")
            print(f"New score: {new_score}")

        # calculate the acceptance probability of the change
        delta = (self.score - new_score)

        if self.verbose:
            print(f"delta: {delta}")
            print(f"temperature: {self.temperature}")
            print(f"x: {-delta / self.temperature}")

        probability = np.exp(np.longdouble(-delta / self.temperature))

        print(f"probability: {probability}") if self.verbose else None

        # NOTE: Keep in mind that if we want to maximize the value, we use:
        # delta = old_value - new_value

        # draw a random number
        rand = random.random()

        # cooling down
        self.update_temperature()

        # accept new state if random number is below probability
        if rand < probability:
            self.solution.trajectories = new_solution.trajectories
            self.score = new_score

            if self.verbose:
                print(f"Accepted {new_score}")

            return True

        return False
