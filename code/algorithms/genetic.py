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
    def __init__(self):
        self.randomize = Randomize()
        self.population: list[Solution] = self.generate_population(5)

    def generate_population(self, size: int):
        return [self.randomize.generate_solution() for _ in range(size)]
    
    def fitness(self, solution: Solution) -> int:
        return solution.score
    
    def generate_children(self, solution: Solution, size: int) -> list[Solution]:
        children = []
        for i in range(size):
            hill_climber_child = HillClimber(solution)
            children.append(hill_climber_child.run(1))
            

        return children

    def run(self):
        highest_score = 0
        highest_score_child = 0
        for _ in range(100):

            for solution in self.population:
                if solution.score >= highest_score:
                    highest_score_solution = solution
            
            self.population.pop(highest_score_solution)
            
            new_highest_score = True
            while new_highest_score == True:

                new_highest_score = False
                children: list[Solution] = self.generate_children(highest_score_solution, 100)
                for child in children:
                    if child.score >= highest_score_child:
                        new_highest_score = True
                        highest_score_solution = child
        
        print(highest_score)
        print(highest_score_child)

               




        

        


        



        
         
    