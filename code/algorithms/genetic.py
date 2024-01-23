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
    def __init__(self, dataset: str):
        self.dataset = dataset
        self.railNL = RailNL(dataset=dataset)
        self.randomize = Randomize(self.railNL.stations, self.railNL.connections)
        # self.population: list[Solution] = self.generate_population(1000)
        self.seed = 0

    def generate_parent(self):
        return self.randomize.make_solution(False)
    
    def fitness(self, solution: Solution) -> int:
        return solution.score
    
    def generate_children(self, parent: Solution, size: int) -> list[Solution]:
        children = []
        
        
        for i in range(size):
            self.seed += 1
            hill_climber_child = HillClimber(self.dataset)
         
            hill_climber_child.solution = copy.deepcopy(parent)
            hill_climber_child.trajectories = list(parent.trajectories)
            hill_climber_child.score = parent.score
            # print(f"old score {hill_climber_child.score}")

            hill_climber_child.make_solution()
            children.append(hill_climber_child.solution)
            # print(f"new score {hill_climber_child.score}")
        
        return children

    def run(self):
        
        self.prepare_csv_file()

        highest_score_child = 0
        all_time_highest_score_child = 0
        iterations = 0

        for _ in range(1):
            highest_score = 0
            # for i, solution in enumerate(self.population):
            #     if solution.score >= highest_score:
            #         highest_score_solution = solution
            #         highest_score_solution_index = i
            #         highest_score = solution.score

            parent = self.generate_parent()
   
            new_highest_score = True
            highest_score_child = 0
            while new_highest_score == True:
                new_highest_score = False
                children: list[Solution] = self.generate_children(parent, 15000)
                for child in children:
                    iterations += 1
                    print(iterations)
                    self.write_score(child.score)
                    if child.score > highest_score_child:
                        new_highest_score = True
                        parent = child
                        highest_score_child = child.score
            
            if highest_score_child > all_time_highest_score_child:
                all_time_highest_score_child = highest_score_child

        print(all_time_highest_score_child)

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

               




        

        


        



        
         
    