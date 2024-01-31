from code.classes.solution import Solution
from code.algorithms.hill_climber import HillClimber
from code.visualisation.baseline import visualize_iterations_to_score
from code.visualisation.map_class import MapVisualization
from code.classes.output import Output

import random
import copy


class Genetic(HillClimber, MapVisualization):
    """
    Class following the genetic algorithm.

    This algorithm creates a parent solution from the our random algorithm. Then
    it creates new solutions, called children, by mutating the parent solution using
    the Hill Climber technique. It then takes the child with the best score, and
    that one becomes the parent solution. This process is repeated for a certain
    amount of iterations.

    Genetic takes HillClimber class as a parent.
    """

    def __init__(self, dataset: str):

        # call initializer of super class
        super().__init__(dataset=dataset)

        self.dataset = dataset

    def generate_parent(self):
        """ Create a random starting solution. """

        return self.randomize.run(iterations=1, visualize=False, write_output=False, auto_open=False)

    def generate_children(self, parent: Solution, size: int, mutations: int = 2) -> set[Solution]:
        """ Return set of new solutions, created with the Hill Climber algorithm
            from the parent solution. """

        # create an empty list where children can be stored
        children = set()

        # create a size amount of children
        for _ in range(size):
            self.solution = copy.deepcopy(parent)
            self.trajectories = list(parent.trajectories)
            self.score = parent.score

            self.new_solution(mutations)
            children.add(self.solution)

        return children

    def run(self, iterations: int, visualize: bool, repetitions: int = 1, number_of_children: int = 2000, verbose: bool = True, auto_open: bool = True):
        """ Runs the algorithm while there are children found with a higher score. This is done
            a amount of repititions. Every time it creates the given amount of children from a parent."""

        self.score_file.prepare_file()

        # set all parameters to zero
        all_time_highest_score = 0

        # repeat algorithm for the given amount of repititions
        for _ in range(repetitions):
            # generate parent solution
            parent = self.generate_parent()

            # set score variables
            new_highest_score = True
            highest_score_child = 0

            try:
                # run a while loop until no child with a higher score has been found
                while new_highest_score:
                    # set new_highest_score to False
                    new_highest_score = False

                    # generate a population of children based on parent
                    children: set[Solution] = self.generate_children(parent, number_of_children)

                    # iterate over all children
                    for child in children:
                        # write score of child to csv file
                        self.score_file.write_score(child.score)

                        # if this child's score is higher than till now highest child score
                        if child.score > highest_score_child:
                            new_highest_score = True
                            # child solution becomes the new parent solution
                            parent = child
                            # keep track of the highest score found
                            highest_score_child = child.score

                            solution = Solution(child.trajectories, True, self.__class__.__name__)

            except KeyboardInterrupt:
                pass

            # check the highest score found in this tree and compare it to the most successful tree
            if highest_score_child > all_time_highest_score:
                all_time_highest_score = highest_score_child
                all_time_highest_score_child_solution = solution

        

        if visualize:
            Output(all_time_highest_score_child_solution.trajectories, is_valid = True)
            self.visualize(solution=all_time_highest_score_child_solution, auto_open=auto_open)
            visualize_iterations_to_score(data=self.scores_path, auto_open=auto_open)
