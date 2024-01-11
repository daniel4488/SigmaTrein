from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize

if __name__ == "__main__":
    # Initialize raiLNL
    railNL = RailNL()

    randomize = Randomize(railNL.stations, railNL.verbindingen)

    randomize.make_random_trajectory()

    print(randomize.randomized_trajectory)