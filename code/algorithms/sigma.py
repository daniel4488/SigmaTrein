from code.classes.trajectory import Trajectory
from code.classes.solution import Solution
from code.classes.output import Output
from code.algorithms.advanced_random import AdvancedRandom
from code.classes.write_file import ScoreFile
from code.visualisation.map_class import MapVisualization
from code.classes.railNL import RailNL
from code.classes.station import Station
from code.visualisation.baseline import visualize_baseline, visualize_iterations_to_score

import copy


class Sigma(AdvancedRandom, MapVisualization):
    """
    Algorithm following our custom Sigma algorithm.

    This algorithm gets a few predetermined consecutive stations and connections. 
    These are fixed routes where some trajectories must start with. 
    A trajectory is then made starting either from a predetermined station or a random one. 
    After the first departure station has been chosen the algorithm starts choosing its 
    path with the advanced randomize algorithm. Once it has found a valid solution, 
    meaning that all connections have been used by the trajectories, a heuristic starts 
    looking at what connections can be removed from the trajectories. 
    Starting with the shortest trajectory, it checks if both ends of the trajectory have 
    connections that are used by other trajectories as well. If this is the case it 
    removes these connections. It stops checking if both ends are not double connections 
    anymore, or the whole trajectory has been removed due to all connections being 
    double connections. In that case the whole trajectory gets removed from the final solution. 

    Sigma takes the AdvancedRandom class as a parent. Furthermore it has a list
    with prefixed routes and a list with corresponding connections. 
    """

    def __init__(self, dataset: str):

        super().__init__(dataset=dataset)

        # Create and prepare score files
        self.score_file = ScoreFile("sigma.csv")
        self.highest_score_file = ScoreFile("sigma_highest.csv")

        # list with pre-fixed routes that start a trajectory
        self.standard_stations = [["Maastricht", "Sittard", "Heerlen", "Sittard", "Roermond", "Weert", "Eindhoven"],
                                       ["Venlo", "Helmond", "Eindhoven"], ["Vlissingen", "Roosendaal"],
                                       ["Den Helder", "Alkmaar"], ["Enschede", "Hengelo", "Almelo"], ["Lelystad Centrum", "Almere Centrum"]
                                       , ["Zwolle", "Assen", "Groningen", "Leeuwarden", "Heerenveen", "Steenwijk", "Zwolle"]]
        
        # list with corresponding connection numbers to the prefixed routes,
        # in each list the last number represents the trajectory duration
        self.standard_connections = [[76, 77, 77, 78, 79, 80, 91], 
                                                  [81, 82, 39], [75, 63], [71, 36], 
                                                  [88, 72, 17], [73, 14],
                                                  [74, 83, 84, 86, 85, 87, 146]]
        
        # empty lists where copies of the lists above can be stored
        self.standard_stations_copy = []
        self.standard_connections_copy = []
        
        # Set is valid parameter to False
        self.is_valid = False

    def choose_predetermined_first_departure_station(self, trajectory: Trajectory):
        """ Prefixed list of stations and connections are added to a trajectory,
            from there a random connection to a departure station is chosen. The
            departure station is returned. """

        # if there are still standard trajectories
        if self.standard_stations_copy:
            departure_station = self.process_standard_routes(trajectory)

        # if there are no more predetermined stations, choose a random next one
        else:
            # set a random departure station
            departure_station = self.choose_station(list(self.stations.keys()))

            # add random departure station to the trajectory
            trajectory.add_station(departure_station[0])

        return departure_station
    
    def process_standard_routes(self, trajectory: Trajectory) -> Station:
        # select stations and connections lists from standard list
        stations: list[str] = self.standard_stations_copy.pop()
        connections: list[int] = self.standard_connections_copy.pop()

        # add duration of standard route to the trajectory
        trajectory.duration += connections.pop()

        # add all stations to the current trajectory
        for station in stations:
            trajectory.add_station(station)

        # add all connections to the current trajectory
        for connection in connections:
            trajectory.add_connection_number(connection)

        # set the correct predetermined departure station
        departure_station = (stations[-1], self.stations[stations[-1]])

        return departure_station


    def make_sigma_trajectory(self) -> Trajectory:
        """ Returns a trajectory that starts with a predetermined part, and
            is supplemented with random stations. """

        # initialize trajectory
        trajectory = Trajectory()

        # set departure station according to predetermined or random procedure
        departure_station = self.choose_predetermined_first_departure_station(trajectory)
        
        # create a trajectory with advanced randomize algorithm
        return self.make_advanced_trajectory(trajectory, departure_station)
    
    def create_solution(self):
        # create empty set for the trajectories
        trajectories = set()
        
        # create at most the allowed trajectories for a solution 
        for _ in range(int(self.constrictions.max_trajectories)):
            # make one trajectory
            current_trajectory = self.make_sigma_trajectory()

            # add the trajectory to set of trajectories
            trajectories.add(current_trajectory)

            # add the trajectory's connections to used_connections of this solution
            self.used_connections.update(current_trajectory.connections)

            # check if a solution is valid if all connections are used
            if len(self.used_connections) == RailNL.NUMBER_OF_CONNECTIONS:
                # set is_valid parameter to True if a valid solution is found
                self.is_valid = True

                # break for loop
                break
        
        return trajectories
    
    def run(self, iterations: int, visualize: bool, verbose: bool, auto_open: bool):
        """ Runs Sigma algorithm. """

        print("Running Sigma algorithm...")
        
        # prepare csv files
        self.score_file.prepare_file()
        self.highest_score_file.prepare_file()

        # set a parameter that keeps track of the highest score
        highest_score = 0 

        # set a parametere that keeps track of the amount of iterations
        i = 0
        try:
            for _ in range(iterations):
                # print iterations
                if i % 10000 == 0:
                    print(f"{i} iterations")

                # whilst a solution is not valid, i.e. all connections used by trajectories
                # keep looking for a valid solution
                while not self.is_valid:
                    # rest all used connections by previous solution
                    self.reset_used_connections_and_weight()

                    # repopulate the standard routes lists
                    self.standard_stations_copy = copy.deepcopy(self.standard_stations)
                    self.standard_connections_copy = copy.deepcopy(self.standard_connections)

                    # create a solution consisting of a set of trajectories
                    trajectories = self.create_solution()

                # Convert trajectories set to list for it to maintain order
                trajectories = list(trajectories)

                # create a solution, where it will strip double connections
                solution = Solution(trajectories, self.is_valid, self.__class__.__name__)

                # write the score after removing double connections to csv file
                self.score_file.write_score(solution.score)

                # check if a new highest score has been found
                if solution.score > highest_score:
                    highest_score = solution.score
                    highest_score_solution = solution

                # write current highest score to the highest score file
                self.highest_score_file.write_score(highest_score)

                # print statements
                if self.verbose:
                    print(f"Score: {solution.score}")

                # reset is_valid parameter
                self.is_valid = False
                # update iterations parameter
                i += 1
        except KeyboardInterrupt:
            pass

        # Create proper output for the highest solution found
        Output(highest_score_solution.trajectories, self.is_valid)

        # visualize results
        if visualize:
            self.visualize(solution=highest_score_solution, auto_open=auto_open)
            visualize_iterations_to_score("data/scores/sigma_highest.csv", auto_open=auto_open)
            visualize_baseline("data/scores/sigma.csv", title=self.__class__.__name__)
