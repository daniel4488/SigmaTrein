from code.classes.railNL import RailNL
from code.algorithms.randomize_trajectory import RandomizeTrajectory
from code.visualisation.plot_single_track import PlotlyLoad
from code.visualisation.baseline import visualize_baseline, visualize_iterations_to_score
from code.algorithms.genetic import Genetic    


railNL = RailNL(dataset="holland")


genetic = Genetic(railNL.stations, railNL.connections)
solution = genetic.generate_solution()
print(solution.score)
print(solution.trajectories)