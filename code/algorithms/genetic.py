from code.classes.trajectory import Trajectory
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.solution import Solution
from code.classes.output import Output
from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize
from code.algorithms.hill_climber import HillClimber

import random

class Genetic:
    def __init__(self, dataset: str):
        self.dataset = dataset
        self.railNL = RailNL(dataset=dataset)
        self.randomize = Randomize(self.railNL.stations, self.railNL.connections)
        self.population: list[Solution] = self.generate_population(5)

    def generate_population(self, size: int):
        return [self.randomize.make_solution(False) for _ in range(size)]
    
    def fitness(self, solution: Solution) -> int:
        return solution.score
    
    def generate_children(self, solution: Solution, size: int) -> list[Solution]:
        children = []
        for i in range(size):
            hill_climber_child = HillClimber(self.dataset)
            hill_climber_child.solution = solution
            hill_climber_child.trajectories = list(solution.trajectories)
            hill_climber_child.score = solution.score
            children.append(hill_climber_child.make_solution())
            

        return children

    def run(self):
        
        highest_score_child = 0
        all_time_highest_score_child = 0

        for _ in range(5):
            highest_score = 0
            for i, solution in enumerate(self.population):
                if solution.score >= highest_score:
                    highest_score_solution = solution
                    highest_score_solution_index = i
                    highest_score = solution.score

            
            self.population.pop(highest_score_solution_index)
            
            new_highest_score = True
            while new_highest_score == True:

                new_highest_score = False
                children: list[Solution] = self.generate_children(highest_score_solution, 10)
                for child in children:
                    if child.score > highest_score_child:
                        new_highest_score = True
                        highest_score_solution = child
            
            if highest_score_child > all_time_highest_score_child:
                all_time_highest_score_child = highest_score_child

        
        print(highest_score)
        print(all_time_highest_score_child)

               




        

        


        



        
         
    