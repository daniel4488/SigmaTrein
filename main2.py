from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize
from code.visualisation.plot_single_track import PlotlyLoad
from code.visualisation.baseline import visualize_baseline, visualize_iterations_to_score
from code.algorithms.genetic import Genetic    
from code.algorithms.less_random import LessRandom


railNL = RailNL(dataset="holland")


# genetic = Genetic(railNL.stations, railNL.connections)
# solution = genetic.generate_solution()
# print(solution.score)
# print(solution.trajectories)

less_random = LessRandom(railNL.stations, railNL.connections)
less_random.run()