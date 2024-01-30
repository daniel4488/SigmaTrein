from code.classes.solution import Solution
from code.algorithms.hill_climber import HillClimber
from code.visualisation.baseline import visualize_iterations_to_score

import random
import copy


class Genetic(HillClimber):
    """
    Class describing the genetic algorithm.
    """

    def __init__(self, dataset: str):

        # call initializer of super class
        super().__init__(dataset=dataset)

    def generate_parent(self):
        """ Create random starting solution. """

        return self.randomize.run(iterations=1, visualize=False, write_output=False)

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

    def run(self, iterations: int, visualize: bool, repetitions: int = 1, children: int = 2000, verbose: bool = True):
        random.seed(123)
        self.score_file.prepare_file()

        # set all parameters to zero
        all_time_highest_score_child = 0

        for _ in range(repetitions):
            # highest_score = 0

            # generate parent solution
            parent = self.generate_parent()

            # set new_highest_score to True
            new_highest_score = True
            # set highest_score_child to zero
            highest_score_child = 0

            # run a while loop until no child with a higher score has been found
            # i.e. till children generate better children run this loop
            while new_highest_score:
                # set new_highest_score to False
                new_highest_score = False

                # generate a population of children based on parent
                children: set[Solution] = self.generate_children(parent, children)

                # iterate over all children 
                for child in children:
                    # write score of child
                    self.score_file.write_score(child.score)
                    # if this child's score is higher than till now highest child score

                    if child.score > highest_score_child:
                        # set new_highest_score found to True
                        new_highest_score = True
                        # the child with the highest score becomes the new parent
                        parent = child
                        # keep track of the highest score found
                        highest_score_child = child.score

            # check the highest score found in this tree and compare it to the most successful tree
            if highest_score_child > all_time_highest_score_child:
                all_time_highest_score_child = highest_score_child

        print(all_time_highest_score_child)

        if visualize:
            visualize_iterations_to_score(data=self.scores_path)
