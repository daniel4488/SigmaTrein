from code.classes.railNL import RailNL
# from code.algorithms.randomize import Randomize
from code.visualisation.plot_single_track import PlotlyLoad
from code.visualisation.baseline import visualize_baseline, visualize_iterations_to_score
from code.functions.to_camel_case import to_camel_case

import argparse
import textwrap


def valid_iterations(arg: str) -> int:
    """ Function to check if the given verbose argument is correct. """

    if not arg.isdigit():
        raise argparse.ArgumentTypeError("please enter an integer number as iterations")

    if not int(arg) > 0:
        raise argparse.ArgumentTypeError("iterations can only be larger than zero")

    return int(arg)


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
        default=False,
        help="prints detailed debugging statements"
    )

    # default iterations number
    default_iterations: dict[str, int] = {
        "randomize": 1,
        "less_random": 10000,
        "hill_climber": 300000,
        "simulated_annealing": 30000,
        "genetic": 1,
        "sigma": 4,
        "baseline": 100000
    }

    # add algorithm as positional command line argument
    parser.add_argument(
        "algorithm",
        choices=list(default_iterations.keys()),
        help="choose an algorithm to run"
    )

    # add no-visual as optional command line argument
    parser.add_argument(
        "--visual_off",
        action="store_true",
        default=False,
        help="turns off automatically showing the visual"
    )

    # add iterations flag as optional command line argument
    parser.add_argument(
        "--iterations", "-i",
        type=valid_iterations,
        help="manually specify the number of iterations"
    )

    # parse the command line argument
    args = parser.parse_args()

    # set default arguments for iterations argument
    if args.iterations is None:
        args.iterations = default_iterations[args.algorithm]

    # class name of algorithm
    algorithm_class = to_camel_case(args.algorithm)

    # import chosen algorithm
    exec(f"from code.algorithms.{args.algorithm} import {algorithm_class}")

    # initialise random algorithm
    exec(f"{args.algorithm} = {algorithm_class}('{args.dataset}')")

    # run chosen algorithm
    exec(f"{args.algorithm}.run(iterations={args.iterations}, visualize={not args.visual_off}, verbose={args.verbose})")
