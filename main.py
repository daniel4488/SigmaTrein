from code.classes.railNL import RailNL
from code.algorithms.randomize_trajectory import RandomizeTrajectory
from code.visualisation.plot_single_track import PlotlyLoad
from code.visualisation.baseline import visualize_baseline, visualize_iterations_to_score

import argparse


def valid_argument(arg: str) -> str:
    """ Function to check if the given command line argument is correct. """
    valid_arguments = {"holland", "nationaal"}

    if arg not in valid_arguments:
        raise argparse.ArgumentTypeError
    return arg


if __name__ == "__main__":

    # initialise parser
    parser = argparse.ArgumentParser(description="Run the main function of the RailNL case.")

    # add command line argument with default value
    parser.add_argument("--dataset", "-d", default="holland", type=valid_argument)

    # parse the command line argument
    args = parser.parse_args()

    # Initialize raiLNL
    railNL = RailNL(dataset=args.dataset)

    randomize = RandomizeTrajectory(railNL.stations, railNL.connections)

    randomize.make_baseline()

    # histogram of scores from random algorithm
    visualize_baseline()

    # plot scores of iterations from random algorithm
    visualize_iterations_to_score()

    # random_trajectory = randomize.make_random_trajectory()
    #
    # print(random_trajectory)
    #
    # # Visualization
    # plot_device = PlotlyLoad()
    # plot_device.draw_graph(random_trajectory.stations)
