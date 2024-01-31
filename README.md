# SigmaTrein
This case is called RailNL. The goal of the case is to create a train system through the Netherlands that is as efficient as possible. Before explaining the details, we describe the terminologu specific to this case:
- Station: a city in the Netherlands were the train can stop or pass by
- Connection: the train rail between two stations
- Trajectory: a consecutive number of connections
- Solution: multiple trajectories together

So the goal is to try to make the best solution possible. However, there are some restrictions that the solution must meet. The first restriction is that every trajectory can maximally take 180 minutes by train. The second restriction is that we can create at most 20 trajectories in one solution.

To measure how good our solution is, we have a formula:

$$ K = p \cdot 10,000 - (T \cdot 100 - Min) $$

where $p$ is the fraction included connections of the total connections, $T$ is the number of trajectories, and $Min$ is the sum of total duration of all trajectories.
This formula gives us score $K$, which needs to be maximised.

# Algorithms

### Randomize
The random algorithm chooses a random starting station. From there it randomly chooses a possible connection. From this next station onward, the same is done, until the maximum time of a trajectory is reached. In this way, a solution of multiple trajectories is made.

Our random algorithm can be made less random by setting two booleans to True. The first boolean is ```unique```. When ```unique=True```, our random algorithm only chooses a connection once in the same trajectory. The second boolean is ```prefixed```. When ```prefixed=True```, the algorithm will start at some priorly chosen stations, and run from there.

### Advanced Randomize
The advanced randomize algorithm gets steered by a simple heuristic. It chooses a random departure station and then chooses the connection which has been used the least in a particular solution. For example if a solution consists of 19 trajectories, it keeps track of how many times each connection has been used within these 19 trajectories. If a 20th trajectory is made it will then depart from a random station and chooses from it's possible connections which has been used the least by the other 19 trajectories. 

### Hill Climber
The Hill Climber algorithm starts by creating a solution from our random algorithm. Thereafter, it starts deleting a chosen number of trajectories, and checks if these solutions return better scores. If not, it makes random new solutions for every deleted trajectory. A solution with a higher score than the current one is accepted as the new current solution. This process is repeated for a given amount of iterations.

### Simulated Annealing

Simulated annealing originates and is inspired by the annealing process in metallurgy,
in which metal is heated to a high temperature and then gradually cooled down.
The algorithm of simulated annealing works in a similar way.
Simulated annealing falls in the class of iterative metaheuristic algorithms.
It starts with a very high temperature and gradually cools down.
While the temperature decreases it becomes less likely that it accepts worse solutions.
In that way, the algorithm ideally converges.
The difference with hill climber is that it not only makes improvements,
but also could accept downturns.
The idea behind this is that simulated annealing could escape from a local maxima,
where hill climber would end, and reach the global maxima.

Simulated annealing has a parameter that can be set which is the starting temperature.
There are also a number of ways how the cooling down could be implemented.
In this version, simulated annealing is implemented with the following cooling down schemes:
*   linear
*   exponential
*   root
*   constant

There is an option available to choose between the different cooling down schemes,
by default it is set to linear.

### Genetic
The Genetic algorithm creates a parent solution from our random algorithm. Then it creates new solutions, called children, by mutating the parent solution using the our Hill Climber algorithm. Next, it takes the child with the highest score, and that one becomes the new parent solution. This process is repeated till there are no higher scores found. The algorithm can be repeated multiple times, this means that it automatically starts again with a whole new random solution.

### Sigma
The Sigma algorithm is an algorithm that we created ourselves. The algorithm gets a few predetermined consecutive stations and connections. These are fixed routes where some trajectories must start with. A trajectory is then made starting either from a predetermined station or a random one. After the first departure has been chosen the algorithm starts choosing its path with the advanced randomize algorithm. Once it has found a valid solution, meaning that all connections have been used by the trajectories, a heuristic starts looking at what connections can be removed from the trajectories. Starting with the shortest trajectory, it checks if both ends of the trajectory have connections that are used by other trajectories as well. If this is the case it removes these connections. It stops checking if both ends are not double connections anymore, or the whole trajectory has been removed due to all connections being double connections. In that case the whole trajectory gets removed from the final solution. 

# Usage
This application has the best experience if it is used as a command line application by running ```main.py.```

Before running the ```main.py```, all packages in the ```requirements.txt``` must be installed in Python3. This can be done in one step by running in your Terminal: \
``` pip install -r requirements.txt ```

If all requirements have been satisfied, main.py can be started by running ```python3 main.py```.

Apart from this README, the command line application offers a help interface that can be called via the command line by running ```python3 main.py --help```.

```main.py``` requires at least one argument which is the ```algorithm``` that needs to be executed. This can be done using ```python3 main.py <algorithm>```. The following algorithms are available.

- advanced_random
- baseline
- genetic
- hill_climber
- randomize
- sigma
- simulated_annealing

After the process has finished, one or more windows will be opened, showing the outcomes of the chosen algorithm. The output files can be found in a folder called ```output``` within the project's directory.

In addition to the mandatory option ```algorithm``` there is a whole list of optional arguments that can be used when desired.

| **argument**          | **description**                                                                                   | **options**                                 | **default**                |
|-----------------------|---------------------------------------------------------------------------------------------------|---------------------------------------------|----------------------------|
| --help, -h            | shows the manual inside the command line                                                          |                                             |                            |
| --iterations, -i      | specifies the number of iterations for the chosen algorithm                                       | integer larger than zero                    | varying for each algorithm |
| --dataset             | specifies the dataset                                                                             | either holland or nationaal                 | nationaal                  |
| --verbose, -v         | shows detailed printing statements, useful for debugging purposes                                 |                                             |                            |
| --experiment          | runs an experiment for the chosen algorithm                                                       |                                             |                            |
| --visual_off          | does not generate the visualization                                                               |                                             |                            |
| --disable\_auto\_open | generates the visualization but does not automatically opens it                                   |                                             |                            |
| --mutations           | specifies the number of mutations at each hill climber iteration, only applicable to hill climber | integer larger than zero but smaller than 8 | 1                          |
| --start_temperature   | sets the starting temperature for simulated annealing                                             | integer or float larger than zero           | 10                         |
| --cooling_down        | sets the cooling down scheme for simulated annealing                                              | linear, exponential, root, constant         | linear                     |
| --alpha               | sets the alpha parameter of the exponential cooling down scheme                                   | float in (0, 1)                             | 0.99                       |
| --not_unique          | allows the random algorithm to choose a connection multiple times within a single trajectory      |                                             |                            |
| --prefixed            | restricts the random algorithm to choose a starting station from a list of preferred stations     |                                             |                            |

### Default Iterations
For each algorithm an appropriate number of ```iterations``` has been set by default. If the ```iterations``` have not been adjusted, this will be used as configuration.

| **algorithm**       | **iterations** |
|---------------------|----------------|
| advanced_random     | 1000           |
| baseline            | 100000         |
| genetic             | 2              |
| hill_climber        | 300000         |
| randomize           | 1              |
| sigma               | 1000           |
| simulated_annealing | 100000         |


**Note:** Genetic algorithm does not have a controllable number of iterations, as it automatically stops when it converges. Therefore, the number of ```repetitions``` is given in the table.

# Computation Time
The Apollo 11 space shuttle has sent people to the moon using a board computer with 4 KB of memory. But this was in 1969 and now we are running this project with 16 GB of RAM. However, there are still limitations in what a computer can do within a restricted amount of time.

We have measured and extrapolated for each algorithm how long it would take to run some number of iterations depending on the ```algorithm```. The results are shown in the table below. The number of iterations have been rounded. Any parameters for the algorithms will have the default configuration in this test.

| **algorithm**       |  **3 minutes**  |  **15 minutes**  |
|---------------------|:---------------:|:----------------:|
| advanced_random     |     410.000     |    2.050.000     |
| baseline            |     500.000     |    2.500.000     |
| genetic             |       34        |       170        |
| hill_climber        |     990.000     |    4.950.000     |
| randomize           |        -        |        -         |
| sigma               |     330.000     |    1.650.000     |
| simulated_annealing |     940.000     |    4.700.000     |

**Note:** Genetic algorithm does not have a controllable number of iterations, as it automatically stops when it converges. Therefore, the number of ```repetitions``` is given in the table.


# Experiments
Experiments are available for the algorithms hill_climber and simulated_annealing. 
The hill climber has a parameter mutations, this means how many changes are made at each iteration.
Each hill climber change is replacing a trajectory. This means mutations is an integer inbetween 1 and 7, endpoints included.

Simulated annealing has always a starting temperature (> 0) that can be adjusted.
The algorithm has a cooling down scheme that could be linear, exponential, root or constant.
The exponential cooling down scheme has a parameter alpha that is in (0, 1).

The experiments can be executed with main.py. <br>
For hill_climber: ``` python3 main.py hill_climber --experiment ``` <br>
For simulated_annealing: ``` python3 main.py simualted_annealing --experiment ```

# Authors
Daniël Frijns (12904724) \
Timo Nijkamp (1322608) \
Roos van der Neut (13273000)

# Specifications
All tests have been conducted on a MacBook Pro with a Apple M2 Chip, 16.00 GB RAM, and running macOS Sonoma 14.3.
