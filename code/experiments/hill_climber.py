"""
Experiment for hill climbers parameter mutations
Settings
*   seed 7807719 set in randomize.py
*   seed 4668890 set in algorithms/hill_climber.py


Initial hill_climber solution is made by randomize with unique=True and prefixed=False

A single mutation in hill climber is replacing a traject with a new one

The number of iterations is kept constant at 50000
The initial solution is also constant because the seed is set
Therefore the only difference in each run is the number of mutations
This makes it possible to test only for the mutations parameter

The outcome of this experiment is that mutations equaling four gives the best result
"""

import os
import subprocess


params = [1, 2, 3, 4, 5, 6, 7]

path = "code/experiments/hill_climber/"

# check if hill climber output directory exists
if not (os.path.exists(path) and os.path.isdir(path)):
    os.mkdir(path)

for param in params:
    # status message
    print(f"Running parameter: mutations = {param}")

    # set filename
    filename = f"hill_climber_mutations_equals_{param}.html"

    # default html file location
    default_output = ".tmp/iter_to_score.html"

    # run hill_climber algorithm with mutations parameter
    p = subprocess.run(
        [
            "python", "main.py", "hill_climber",
            "--iterations", "50000", "--mutations", str(param),
            "--verbose", "--disable_auto_open"
        ],
        stdout=subprocess.PIPE,
        text=True
    )

    # print score
    for line in p.stdout.splitlines():
        if line.startswith("HillClimber highest score: "):
            print(line)
            break

    # move html file
    os.system(f"mv {default_output} {path}{filename}")



