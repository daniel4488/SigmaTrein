from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize
from code.visualisation.map import PlotlyLoad

if __name__ == "__main__":

    # init dataset
    dataset = "nationaal"

    # Initialize raiLNL
    railNL = RailNL(dataset=dataset)

    randomize = Randomize(dataset=dataset)

    solution = randomize.run(iterations=1, visualize=True, verbose=False, write_output=True)

    # Visualization
    # plot_device = PlotlyLoad(dataset=dataset)
    # plot_device.draw_graph(solution)
