from code.classes.trajectory import Trajectory
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.solution import Solution
from code.classes.output import Output
from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize

import random

class Genetic:
    def __init__(self):
        self.randomize = Randomize()
        self.population = self.generate_population(5)

    def generate_population(self, size: int):
        return [self.randomize.generate_solution() for _ in range(size)]
    
    def fitness(self, solution: Solution) -> int:
        return solution.score

    def repopulate_possible_connections_for_all_stations(self) -> None:
        """ Prepare for the generation of a new trajectory. """
        for station in self.stations:
            self.stations[station].repopulate_possible_connections()
         
    