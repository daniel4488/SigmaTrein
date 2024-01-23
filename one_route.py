from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize
from code.visualisation.plot_single_track import PlotlyLoad

if __name__ == "__main__":
    # Initialize raiLNL
    railNL = RailNL(dataset="holland")

    randomize = Randomize(railNL.stations, railNL.connections)

    random_trajectory = randomize.make_trajectory()

    print(random_trajectory)

    # Visualization
    plot_device = PlotlyLoad()
    plot_device.draw_graph(random_trajectory.stations)
