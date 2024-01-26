from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize
from code.visualisation.plot_single_track import PlotlyLoad
from code.visualisation.baseline import visualize_baseline, visualize_iterations_to_score

import argparse


if __name__ == "__main__":

    # initialise parser
    parser = argparse.ArgumentParser(description="Run the main function of the RailNL case.")

    # add dataset command line argument with default value
    parser.add_argument("--dataset", "-d", default="nationaal", choices=["holland", "nationaal"])

    # add verbose command line argument
    parser.add_argument("--verbose", "-v", default=False, type=bool, nargs="?", const=True)

    # parse the command line argument
    args = parser.parse_args()

    # initialize raiLNL
    railNL = RailNL(dataset=args.dataset)

    # initialise random algorithm
    randomize = Randomize(args.dataset, railNL.stations, railNL.connections)

    # make baseline
    randomize.make_baseline(verbose=args.verbose)

    # csv
    data = "data/scores/random.csv"

    # histogram of scores from random algorithm
    visualize_baseline(data)

    # plot scores of iterations from random algorithm
    visualize_iterations_to_score(data)
