from code.classes.trajectory import Trajectory
from code.classes.railNL import RailNL


class Solution:
    """
    Class describing all information containing a solution.
    Solution object contains a boolean describing if it is a valid
    solution, a list with the trajectory objects, and the score of the
    solution.
    """

    def __init__(self, trajectories: list[Trajectory], is_valid: bool,
                 origin: str = "", verbose: bool = False) -> None:

        self.verbose: bool = verbose
        self.is_valid: bool = is_valid
        self.trajectories: list[Trajectory] = trajectories
        if origin == "Sigma" and self.is_valid:
            self.remove_double_connections()
        self.score: float = self.calculate_score()
        self.write_score()

    def calculate_score(self) -> float:
        """
        Formula: K = p * 10000 - (T * 100 + Min)
        p: fraction of used connections
        T: number of trajectories
        Min: number of minutes used in all trajectories
        """

        T = len(self.trajectories)

        # initialize empty variables
        used_connections = set()
        Min = 0.0

        # count total connections and duration
        for traject in self.trajectories:
            used_connections.update(traject.connections)
            Min += traject.duration

        assert RailNL.NUMBER_OF_CONNECTIONS != -1

        # calculate score
        p = len(used_connections) / RailNL.NUMBER_OF_CONNECTIONS
        K = p * 10000 - (T * 100 + Min)

        # print score variables if verbose is True
        if self.verbose:
            print(f"T = {T}")
            print(f"Min = {Min}")
            print(f"p = {p}")

        return K

    def write_score(self) -> None:
        """ Write score to csv file. """

        with open("data/scores/random.csv", "a") as file:
            file.write(str(self.score))
            file.write("\n")

    def check_is_valid(self, new_trajectory: Trajectory) -> bool:
        """ Check if solution meets all restrictions. """

        if RailNL.DATASET == "holland":
            return len(self.trajectories) <= 7 and \
                   new_trajectory.duration <= 120
        else:
            return len(self.trajectories) <= 20 and \
                   new_trajectory.duration <= 180

    def remove_double_connections(self) -> None:
        """ Removes double connections if they are found at the end or beginning
            of a trajectory. """

        # sort trajectories on duration using a custom lambda function
        sorted_trajectories = sorted(self.trajectories,
                                     key=lambda trajectory: trajectory.duration)
        
        # iterate over all trajectories in a solution
        for i, trajectory in enumerate(sorted_trajectories):

            # put all connections from current trajectory we are looking at in a list
            connections = list(trajectory.connections)

            # create an empty set to be populated with al other used connections
            #  in a solution
            used_connections = set()
            # look at all used connections by the other trajectories
            for j, other_trajectory in enumerate(sorted_trajectories):
                if i != j:
                    # add used connections to set
                    used_connections.update(other_trajectory.connections)

            # start looking at the end of current trajectory for double connections
            for k in range(1, len(connections) + 1):
                # if double connection found at the end remove it
                if connections[-k] in used_connections:
                    # remove connection from current trajectory
                    trajectory.connections.remove(connections[-k])
                    # update duration of trajectory
                    trajectory.duration -= RailNL.CONNECTIONS[connections[-k]].duration
                    # set the removed connection in the list to -1 to indicate that this
                    #  connection has been removed
                    connections[-k] = -1
                    # remove station from the trajectory where the connection lead to
                    trajectory.stations.pop()
                else:
                    # break the for loop if the end was not a double connection
                    break

            # if there are still connections left in the current trajectory
            if trajectory.connections:
                # start looking at the other end of current trajectory for double connections
                for l in range(0, len(connections)):
                    # # if double connection found at the end remove it
                    if connections[l] in used_connections:
                        # remove connection from current trajectory
                        trajectory.connections.remove(connections[l])
                        # update duration of trajecto
                        trajectory.duration -= RailNL.CONNECTIONS[connections[l]].duration
                        # remove station from the trajectory where the connection lead to
                        trajectory.stations.pop(0)
                    else:
                        # break the for loop if the end was not a double connection
                        break

            # if there are no connections left in the current trajectory
            if not trajectory.connections:
                # remove trajectory
                self.trajectories.remove(trajectory)
