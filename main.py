from code.classes.railNL import RailNL
from code.algorithms.randomize_trajectory import RandomizeTrajectory
from code.visualisation.plot_single_track import PlotlyLoad

if __name__ == "__main__":
    # Initialize raiLNL
    railNL = RailNL()

    randomize = RandomizeTrajectory(railNL.stations, railNL.connections)

    randomize.make_baseline()

    # random_trajectory = randomize.make_random_trajectory()
    #
    # print(random_trajectory)
    #
    # # Visualization
    # plot_device = PlotlyLoad()
    # plot_device.draw_graph(random_trajectory.stations)
