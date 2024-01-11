from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize
from code.visualisation.plot_single_track import PlotlyLoad

if __name__ == "__main__":
    # Initialize raiLNL
    railNL = RailNL()

    randomize = Randomize(railNL.stations, railNL.verbindingen)

    randomize.make_random_trajectory()

    print(randomize.randomized_trajectory)

    # Visualization
    plot_device = PlotlyLoad()
    plot_device.draw_graph(randomize.randomized_trajectory)
