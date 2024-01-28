from code.classes.trajectory import Trajectory
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.solution import Solution
from code.classes.output import Output
from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize
from code.algorithms.hill_climber import HillClimber

import random
import copy
import os


class Genetic:
    """ Class describing the genetic algorithm. """

    def __init__(self, dataset: str):
        self.dataset = dataset
        self.railNL = RailNL(dataset=dataset)
        self.randomize = Randomize(dataset, self.railNL.stations, self.railNL.connections)
        self.solution: Solution = None
        self.trajectories: list[Trajectory] = None
        self.score: int = None
        self.iterations: int = None
        self.verbose = False

#__________________________________Genetic algorithm_________________________________#
    def generate_parent(self):
        return self.randomize.make_solution(False)

    def fitness(self, solution: Solution) -> int:
        return solution.score

    def generate_children(self, parent: Solution, size: int) -> list[Solution]:
        # create an empty list where children can be stored
        children = set()

        # create a size amount of children
        for _ in range(size):
            self.solution = copy.deepcopy(parent)
            self.trajectories = list(parent.trajectories)
            self.score = parent.score

            self.new_solution(2)
            children.add(self.solution)

        return children

    def run(self):
        random.seed(123)
        self.prepare_csv_file()

        # set all parameters to zero
        all_time_highest_score_child = 0
        iterations = 0

        for _ in range(1):
            # highest_score = 0

            # generate parent
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
                children: list[Solution] = self.generate_children(parent, 20000)

                # iterate over all children 
                for child in children:
                    # count for iterations
                    iterations += 1
                    # print iteration
                    print(iterations)
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

#__________________________________Hill Climber__________________________________#

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
        else:
            return False
    
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
        else:
            self.solution.score = new_solution.calculate_score()
    

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

                




            

            


            



        
         
    