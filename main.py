from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize
from code.visualisation.plot_single_track import PlotlyLoad
from code.visualisation.baseline import visualize_baseline, visualize_iterations_to_score

import argparse


def valid_dataset(arg: str) -> str:
    """ Function to check if the given dataset argument is correct. """
    valid_arguments = {"holland", "nationaal"}

    if arg not in valid_arguments:
        raise argparse.ArgumentTypeError
    return arg


def valid_verbose(arg: str) -> bool:
    """ Function to check if the given verbose argument is correct. """
    valid_arguments = {"False", "True"}

    if arg not in valid_arguments:
        raise argparse.ArgumentTypeError
    return bool(arg)


if __name__ == "__main__":

    # initialise parser
    parser = argparse.ArgumentParser(description="Run the main function of the RailNL case.")

    # add dataset command line argument with default value
    parser.add_argument("--dataset", "-d", default="holland", type=valid_dataset)

    # add verbose command line argument
    parser.add_argument("--verbose", "-v", default=False, type=valid_verbose)

    # parse the command line argument
    args = parser.parse_args()

    # initialize raiLNL
    railNL = RailNL(dataset=args.dataset)

    # initialise random algorithm
    randomize = Randomize(railNL.stations, railNL.connections)

    # make baseline
    randomize.make_baseline(verbose=args.verbose)

    # csv
    data = "data/scores/random.csv"

    # histogram of scores from random algorithm
    visualize_baseline(data)

    # plot scores of iterations from random algorithm
    visualize_iterations_to_score(data)
