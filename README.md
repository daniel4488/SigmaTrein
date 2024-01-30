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

# Usage
Before running the ```main.py```, all packages in the ```requirements.txt``` must be installed in Python3. This can be done in one step by running in your Terminal: \
``` pip install -r requirements.txt ```

# Structure

# Authors
Daniël Frijns () \
Timo Nijkamp () \
Roos van der Neut (13273000)

# Specs
SA algorithm has been implemented using MATLAB using a desktop PC with Intel® Core ™ i7-2620M, 2.7 GHz, 16.00 GB RAM, and a 64-bit Operating System. The optimal solution has been obtained after running several runs with different markov chain length with sizes varying from 50 -100 and it takes around 4-6 hours for a run to converge.