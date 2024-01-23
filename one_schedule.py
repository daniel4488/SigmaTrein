from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize
from code.visualisation.map import PlotlyLoad

if __name__ == "__main__":

    # init dataset
    dataset = "holland"

    # Initialize raiLNL
    railNL = RailNL(dataset=dataset)

    randomize = Randomize(railNL.stations, railNL.connections)

    solution = randomize.make_solution(write_output=True)

    # Visualization
    plot_device = PlotlyLoad(dataset=dataset)
    plot_device.draw_graph(solution)
