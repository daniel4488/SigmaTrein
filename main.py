from code.functions.to_camel_case import to_camel_case
from code.classes.data import DataInfo

import argparse
import textwrap
import os


def valid_iterations(arg: str) -> int:
    """ Function to check if the given iterations argument is correct. """

    if not arg.isdigit():
        raise argparse.ArgumentTypeError("please enter an integer number as iterations")

    if not int(arg) > 0:
        raise argparse.ArgumentTypeError("iterations can only be larger than zero")

    return int(arg)


def valid_mutations(arg: str) -> int:
    """ Function to check if the given mutations argument is correct. """

    if not arg.isdigit() or arg == "0":
        raise argparse.ArgumentTypeError("please enter a strictly positive integer number as mutation")

    return int(arg)


def valid_temperature(arg: str) -> float:
    """ Function to check the start temperature of simulated annealing. """

    try:
        arg_float = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("start temperature needs to be a floating point number or integer")

    if arg_float <= 0:
        raise argparse.ArgumentTypeError("start temperature needs to be strictly positive")

    return arg_float


def valid_cooling_down(arg: str) -> str:
    """ Function to check the cooling down scheme of simulated annealing. """
    schemes = {"linear", "exponential", "constant", "root"}

    if arg not in schemes:
        raise argparse.ArgumentTypeError("cooling down scheme can only be linear, exponential, root or constant")

    return arg


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
        "advanced_random": 1000,
        "hill_climber": 300000,
        "simulated_annealing": 30000,
        "genetic": 1,
        "sigma": 1000,
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
        help="manually specify the number of iterations, default is 1"
    )

    # add optional argument for mutations in hill climber
    parser.add_argument(
        "--mutations",
        type=valid_mutations,
        help="specify number of mutations made at each hill climber iteration"
    )

    # add optional argument for simulated annealing starting temperature
    parser.add_argument(
        "--start_temperature",
        type=valid_temperature,
        help="sets the start temperature for simulated annealing"  # TODO: add default
    )

    # add optional argument simulated annealing cooling down scheme
    parser.add_argument(
        "--cooling_down",
        type=valid_cooling_down,
        help="sets the cooling down scheme for simulated annealing defaults to linear"
    )

    # add optional argument for alpha parameter of simulated annealing exponential cooling down
    parser.add_argument(
        "--alpha",
        type=valid_temperature,
        help="sets the alpha parameter for simulated annealing exponential cooling down"
    )

    # add option to turn experiment on or off
    parser.add_argument(
        "--experiment",
        action="store_true",
        default=False,
        help="runs an experiment for the chosen algorithm, only available for hill climber and simulated annealing"
    )

    # add optional argument to turn off automatically showing the visualization
    parser.add_argument(
        "--disable_auto_open",
        action="store_true",
        default=False,
        help="option to turn off automatically opening html files"
    )

    # parse the command line argument
    args = parser.parse_args()

    # iterations argument cannot be set on random algorithm
    if args.iterations is not None and args.algorithm == "randomize":
        parser.error("setting iterations for randomize has no effect")

    # mutations option is only compatible with hill climber algorithm
    if args.mutations and args.algorithm != "hill_climber":
        parser.error("--mutations can only be set in combination with hill_climber algorithm")

    # mutations cannot be larger than the number of trajectories
    if args.mutations and args.mutations > getattr(DataInfo, args.dataset).max_trajectories:
        raise argparse.ArgumentTypeError("mutations cannot be larger than the number of trajectories")

    # start temperature option is only compatible with simulated annealing
    if args.start_temperature and args.algorithm != "simulated_annealing":
        parser.error("--start_temperature can only be set in combination with simulated_annealing algorithm")

    # cooling down is only compatible with simulated annealing
    if args.cooling_down and args.algorithm != "simulated_annealing":
        parser.error("--cooling_down can only be set in combination with simulated_annealing algorithm")

    # alpha + exponential cooling down + simulated annealing
    if args.alpha and (args.algorithm != "simulated_annealing" or args.cooling_down != "exponential"):
        parser.error("--alpha parameter is exclusive to exponential cooling down of simulated annealing")

    # experiment only works with hill climber or simulated annealing
    if args.experiment and (args.algorithm not in {"simulated_annealing", "hill_climber"}):
        parser.error("experiment only works with simulated_annealing or hill_climber")

    # set default arguments for iterations argument
    if args.iterations is None:
        args.iterations = default_iterations[args.algorithm]

    # experiment
    if args.experiment:
        os.system(f"python3 code/experiments/{args.algorithm}.py")

    # handle special run case with mutations option on hill climber
    if args.mutations:
        from code.algorithms.hill_climber import HillClimber
        hill_climber = HillClimber(dataset=args.dataset)
        hill_climber.run(
            iterations=args.iterations,
            visualize=(not args.visual_off),
            mutations=args.mutations,
            verbose=args.verbose,
            auto_open=(not args.disable_auto_open)
        )
        exit(0)

    # handle special run case with start temperature
    if args.start_temperature:
        from code.algorithms.simulated_annealing import SimulatedAnnealing
        simulated_annealing = SimulatedAnnealing(dataset=args.dataset, start_temperature=args.start_temperature)
        simulated_annealing.run(
            iterations=args.iterations,
            visualize=(not args.visual_off),
            verbose=args.verbose,
            auto_open=(not args.disable_auto_open)
        )
        exit(0)

    # handle special run case with cooling down scheme
    if args.cooling_down:
        if not args.start_temperature:
            args.start_temperature = 10

        from code.algorithms.simulated_annealing import SimulatedAnnealing

        if args.alpha:
            simulated_annealing = SimulatedAnnealing(
                dataset=args.dataset,
                start_temperature=args.start_temperature,
                cooling_scheme="exponential",
                alpha=args.alpha
            )
        else:
            simulated_annealing = SimulatedAnnealing(
                dataset=args.dataset,
                start_temperature=args.start_temperature,
                cooling_scheme=args.cooling_down
            )

        simulated_annealing.run(
            iterations=args.iterations,
            visualize=(not args.visual_off),
            verbose=args.verbose,
            auto_open=(not args.disable_auto_open)
        )
        exit(0)

    # class name of algorithm
    algorithm_class = to_camel_case(args.algorithm)

    # import chosen algorithm
    exec(f"from code.algorithms.{args.algorithm} import {algorithm_class}")

    # initialise random algorithm
    exec(f"{args.algorithm} = {algorithm_class}('{args.dataset}')")

    # run chosen algorithm
    exec(f"{args.algorithm}.run(iterations={args.iterations}, visualize={not args.visual_off}, verbose={args.verbose}, auto_open={not args.disable_auto_open})")
