from code.classes.solution import Solution
from code.classes.trajectory import Trajectory
from code.classes.railNL import RailNL


import pytest
import csv


@pytest.fixture()
def parse_output_csv():
    """ Function to load and parse output.csv. """

    RailNL(dataset="nationaal")

    def load_connections() -> tuple[dict[tuple[str, str], float], dict[tuple[str, str], int]]:
        connections: dict[tuple[str, str], float] = {}
        connection_to_number: dict[tuple[str, str], int] = {}
        connection_number = 0
        with open("data/nationaal/ConnectiesNationaal.csv", "r") as file:
            # csv reader
            reader = csv.DictReader(file)

            for row in reader:
                connection = tuple(sorted([row["station1"], row["station2"]]))
                distance = float(row["distance"])

                connections[connection] = distance
                connection_to_number[connection] = connection_number
                connection_number += 1
        return connections, connection_to_number

    def calculate_trajectory_duration(stations: list[str]) -> tuple[float, list[int]]:
        connections_csv, connection_to_number = load_connections()
        # assert len(self.connections) > 0
        # assert self.stations is not None
        connections = list(map(lambda x: tuple(sorted(x)), zip(stations, stations[1:])))
        connection_numbers: list[int] = []
        distance = 0.0
        for connection in connections:
            distance += connections_csv[connection]
            connection_numbers.append(connection_to_number[connection])
        return distance, connection_numbers

    trajectories: list[Trajectory] = []
    with open("tests/output.csv", "r") as file:
        # csv reader
        reader = csv.DictReader(file)

        # iterate over csv file
        for row in reader:
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

            # set trajectory duration
            trajectory.duration, trajectory.connections = calculate_trajectory_duration(stations=trajectory_stations_list)

            # add trajectory to list of trajectories
            trajectories.append(trajectory)
    return trajectories, score


def test_solution(parse_output_csv) -> None:
    # assert self.stations is not None
    # assert len(self.trajectories) > 0
    # assert self.score != -1e9

    trajectories, score = parse_output_csv

    solution = Solution(
        trajectories=trajectories,
        is_valid=True
    )
    assert solution.score == float(score)
