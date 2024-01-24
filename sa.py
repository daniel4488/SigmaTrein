from code.algorithms.simulated_annealing import SimulatedAnnealing
from code.visualisation.baseline import visualize_iterations_to_score

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

    # hill climber
    sa = SimulatedAnnealing(args.dataset)

    # run hill climber
    sa.run(iterations=3000, verbose=args.verbose)

    # csv file
    data = "data/scores/hill_climber.csv"

    # visualize
    visualize_iterations_to_score(data=data)
