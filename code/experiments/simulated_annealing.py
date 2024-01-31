import os
import subprocess
import numpy as np

temperatures = list(map(np.exp, np.linspace(start=-2, stop=0, endpoint=False, num=8)))
temperatures += list(map(np.exp, np.arange(start=0, stop=10, step=1)))

path = "code/experiments/simulated_annealing/"

# check if simulated annealing output directory exists
if not (os.path.exists(path) and os.path.isdir(path)):
    os.mkdir(path)

for temperature in temperatures:
    # status message
    print(f"Running parameter: temperature = {temperature}")

    # set filename
    filename = f"simulated_annealing_temp_{temperature}.html"

    # default html file location
    default_output = "output/iter_to_score.html"

    # run simulated_annealing algorithm
    p = subprocess.run(
        [
            "python", "main.py", "simulated_annealing",
            "--iterations", "50000",
            "--start_temperature", str(temperature),
            "--verbose", "--disable_auto_open"
        ],
        stdout=subprocess.PIPE,
        text=True
    )

    # print score
    for line in p.stdout.splitlines():
        if line.startswith("SimulatedAnnealing highest score: "):
            print(line)
            break

    # move html file
    os.system(f"mv {default_output} {path}{filename}")



