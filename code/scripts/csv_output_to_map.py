from code.visualisation.map import PlotlyLoad
from code.classes.solution import Solution
from code.classes.trajectory import Trajectory
from code.classes.railNL import RailNL

import csv

class CSVToMap:
    """
    Class to build a map view from "output.csv".
    """

    def __init__(self) -> None:
        self.file_path = "output.csv"
        self.dataset = "nationaal"
        self.railNL = RailNL(dataset=self.dataset)
        self.solution = self.load_solution()
        self.visualize()

    def load_solution(self) -> Solution:

        # declare empty list of trajectories
        trajectories: list[Trajectory] = []

        # read file
        with open(self.file_path, "r") as file:
            # csv reader
            reader = csv.DictReader(file)

            for row in reader:
                # save score
                if row["train"] == "score":
                    score = row["stations"]
                    continue

                # get stations in trajectory
                trajectory_stations_string = row["stations"]

                # strip off [ and ]
                trajectory_stations_string = trajectory_stations_string.strip("[]")

                # make a list of stations
                trajectory_stations_list = trajectory_stations_string.split(", ")

                # trajectory object
                trajectory = Trajectory()

                # add list of stations to the trajectory
                trajectory.stations = trajectory_stations_list

                # add trajectory to list of trajectories
                trajectories.append(trajectory)

        # create solution object
        return Solution(trajectories=trajectories, is_valid=True, origin="Unknown")

    def visualize(self) -> None:
        plot_engine = PlotlyLoad(dataset=self.dataset)
        plot_engine.draw_graph(solution=self.solution, auto_open=True)


if __name__ == "__main__":
    CSVToMap()
