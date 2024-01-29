from code.classes.trajectory import Trajectory
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.solution import Solution
from code.classes.output import Output
from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize
from code.algorithms.hill_climber import HillClimber
from code.functions.to_snake_case import to_snake_case
from code.visualisation.baseline import visualize_iterations_to_score

import random
import copy
import os


class Genetic(HillClimber):
    """
    Class describing the genetic algorithm.
    """

    def __init__(self, dataset: str):

        # call initializer of super class
        super().__init__(dataset=dataset)

#__________________________________Genetic algorithm_________________________________#
    def generate_parent(self):
        """ Create random starting solution. """

        return self.randomize.run(iterations=1, visualize=False, write_output=False)

    def fitness(self, solution: Solution) -> int:
        """ Return score of given solution. """

        return solution.score

    def generate_children(self, parent: Solution, size: int, mutations: int = 2) -> list[Solution]:
        """ Return set of new solutions, created with the Hill Climber alogirthm
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

    def run(self, iterations: int, visualize: bool, repititions: int = 1, verbose: bool = True):
        random.seed(123)
        self.prepare_csv_file()

        # set all parameters to zero
        all_time_highest_score_child = 0

        for _ in range(repititions):
            # highest_score = 0

            # generate parent solution
            parent = self.generate_parent()

            # set new_highest_score to True
            new_highest_score = True
            # set highest_score_child to zero
            highest_score_child = 0

            # run a while loop untill no child with a higher score has been found
            # i.e. till children generate better children run this loop
            while new_highest_score == True:
                # set new_highest_score to False
                new_highest_score = False

                # generate a population of children based on parent
                children: list[Solution] = self.generate_children(parent, 2000)

                # iterate over all children 
                for child in children:
                    # write score of child
                    self.write_score(child.score)
                    # if this childs score is higher than till now highest child score

                    if child.score > highest_score_child:
                        # set new_highest_score found to True
                        new_highest_score = True
                        # the child with the highest score becomes the new parent
                        parent = child
                        # keep track of the highest score found
                        highest_score_child = child.score

            # check the highest score found in this tree and compare it to the most succesful tree
            if highest_score_child > all_time_highest_score_child:
                all_time_highest_score_child = highest_score_child

        print(all_time_highest_score_child)

        if visualize:
            visualize_iterations_to_score(data=self.scores_path)

    

#__________________________________File writing__________________________________#
    
    def write_score(self, score) -> None:
            with open("data/scores/genetic.csv", "a") as file:
                file.write(str(score))
                file.write("\n")

    @staticmethod
    def clear_scores_file() -> None:
        file_path = "data/scores/genetic.csv"

        if os.path.exists(file_path):
            input("WARNING scores file will be deleted.")
            os.remove(file_path)

    def prepare_csv_file(self) -> None:
        self.clear_scores_file()

        if not (os.path.exists("data/scores") and os.path.isdir("data/scores")):
            os.mkdir("data/scores")

        with open("data/scores/genetic.csv", "w") as file:
            file.write("score\n")
   