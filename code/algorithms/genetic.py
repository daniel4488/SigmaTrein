from code.algorithms.hill_climber import HillClimber
from code.classes.solution import Solution
from code.classes.output import Output
from code.visualisation.baseline import visualize_iterations_to_score
from code.visualisation.map_class import MapVisualization

import copy


class Genetic(HillClimber, MapVisualization):
    """
    Class following the genetic algorithm.

    This algorithm creates a parent solution from our random algorithm. Then
    it creates new solutions, called children, by mutating the parent solution using
    the our Hill Climber algorithm. Next, it takes the child with the best score, and
    that one becomes the new parent solution. This process is repeated till there are
    no better scores found. Moreover, the algorithm can be repeated multiple times,
    this means that it automatically starts again with a whole new random solution.

    Genetic takes the HillClimber class as a parent.
    """

    def __init__(self, dataset: str):

        # call initializer of super class
        super().__init__(dataset=dataset)

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
            # create a children
            self.solution = copy.deepcopy(parent)

            # add parent trajectories to child
            self.trajectories = list(parent.trajectories)

            # add parent score to child
            self.score = parent.score

            # mutate child
            self.new_solution(mutations)

            # add new child to set with all children
            children.add(self.solution)

        return children

    def run(self, iterations: int, visualize: bool, repetitions: int = 2, number_of_children: int = 2000, verbose: bool = True, auto_open: bool = True) -> None:
        """ Runs the algorithm while there are children found with a higher score. This is done
            a amount of repititions. Every time it creates the given amount of children from a parent."""
        
        print("Running Genetic algorithm...")

        # prepare csv file
        self.score_file.prepare_file()

        # set all parameters to zero
        all_time_highest_score = 0

        # set a parametere that keeps track of the amount of iterations
        i = 0

        try:
            # repeat algorithm for the given amount of repititions
            for _ in range(repetitions):
                # generate parent solution
                parent = self.generate_parent()

                # set score variables
                new_highest_score = True
                highest_score_child = 0

                # run a while loop until no child with a higher score has been found
                while new_highest_score:
                    # set new_highest_score to False
                    new_highest_score = False

                    # generate a population of children based on parent
                    children: set[Solution] = self.generate_children(parent, number_of_children)

                    # iterate over all children
                    for child in children:
                        # print iterations
                        if i % 10000 == 0:
                            print(f"{i} iterations")
                        # write score of child to csv file
                        self.score_file.write_score(child.score)

                        # if this child's score is higher than till now highest child score
                        if child.score > highest_score_child:
                            # new highest score found to True
                            new_highest_score = True

                            # child solution becomes the new parent solution
                            parent = child

                            # keep track of the highest score found
                            highest_score_child = child.score

                            # create a solution with new highest score
                            solution = Solution(child.trajectories, True, self.__class__.__name__)

                        # update iterations parameter
                        i += 1

                # check the highest score found in this tree and compare it to the most successful tree
                if highest_score_child > all_time_highest_score:
                    all_time_highest_score = highest_score_child
                    all_time_highest_score_child_solution = solution

        except KeyboardInterrupt:
            pass

        Output(trajectories=all_time_highest_score_child_solution.trajectories, is_valid=all_time_highest_score_child_solution.is_valid)

        # create visualisation if visualize is True
        if visualize:
            self.create_visual(solution=all_time_highest_score_child_solution, path=self.scores_path, auto_open=auto_open)
