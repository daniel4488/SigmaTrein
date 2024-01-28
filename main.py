from code.classes.railNL import RailNL
from code.algorithms.randomize import Randomize
from code.visualisation.plot_single_track import PlotlyLoad
from code.visualisation.baseline import visualize_baseline, visualize_iterations_to_score

import argparse
import textwrap


if __name__ == "__main__":

    description = r'''
                                             (@@@)     (@@@@@)
                                       (@@)     (@@@@@@@)        (@@@@@@@)
                                 (@@@@@@@)   (@@@@@)       (@@@@@@@@@@@)
                            (@@@)     (@@@@@@@)   (@@@@@@)             (@@@)
                       (@@@@@@)    (@@@@@@)                (@)
                   (@@@)  (@@@@)           (@@)
                (@@)              (@@@)
               .-.
               ] [    .-.      _    .-----.
             ."   """"   """""" """"| .--`
            (:--:--:--:--:--:--:--:-| [___    .------------------------.
             |C&O  :  :  :  :  :  : [_9_] |'='|.----------------------.|
            /|.___________________________|___|'--.___.--.___.--.___.-'|
           / ||_.--.______.--.______.--._ |---\'--\-.-/==\-.-/==\-.-/-'/--
          /__;^=(==)======(==)======(==)=^~^^^ ^^^^(-)^^^^(-)^^^^(-)^^^ aac
        ~~~^~~~~^~~~^~~~^~~~^~~~^~~~^~~~^~~~^~~~^~~~^~~~^~~~^~~~^~~~^~~~^~~~
        
                    /$$$$$$  /$$                                  
                   /$$__  $$|__/                                  
                  | $$  \__/ /$$  /$$$$$$  /$$$$$$/$$$$   /$$$$$$ 
                  |  $$$$$$ | $$ /$$__  $$| $$_  $$_  $$ |____  $$
                   \____  $$| $$| $$  \ $$| $$ \ $$ \ $$  /$$$$$$$
                   /$$  \ $$| $$| $$  | $$| $$ | $$ | $$ /$$__  $$
                  |  $$$$$$/| $$|  $$$$$$$| $$ | $$ | $$|  $$$$$$$
                   \______/ |__/ \____  $$|__/ |__/ |__/ \_______/
                                 /$$  \ $$                        
                                |  $$$$$$/                        
                                 \______/                         
        '''

    epilog = "Authors: Daniël Frijns, Timo Nijkamp & Roos van der Neut"

    # initialise parser
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog
    )

    # add dataset command line argument with default value
    parser.add_argument(
        "--dataset", "-d",
        default="nationaal",
        choices=["holland", "nationaal"],
        help="sets the dataset to be used, defaults to nationaal"
    )

    # add verbose command line argument
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="prints detailed debugging statements"
    )

    # add algorithm as positional command line argument
    # parser.add_argument(
    #     "algorithm",
    #     choices=["randomize", "less_random", "hill_climber", "simulated_annealing", "genetic", "sigma"],
    #     help="choose an algorithm to run"
    # )

    # parse the command line argument
    args = parser.parse_args()

    # initialize raiLNL
    # railNL = RailNL(dataset=args.dataset)

    # initialise random algorithm
    randomize = Randomize(args.dataset)

    # make baseline
    randomize.make_baseline(verbose=args.verbose)

    # csv
    data = "data/scores/random.csv"

    # histogram of scores from random algorithm
    visualize_baseline(data)

    # plot scores of iterations from random algorithm
    visualize_iterations_to_score(data)
