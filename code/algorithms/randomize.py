from code.classes.traject import Trajectory
from code.classes.station import Station
from code.classes.connection import Connection

import random


class Randomize:
    """ Algorithm to generate a randomly chosen trajectory. """

    def __init__(self, stations: dict[str, Station], connections: dict[int, Connection]) -> None:
        """ Initiates the random algorithm. """

        self.stations: dict[str, Station] = stations
        self.connections: dict[int, Connection] = connections

        self.randomized_trajectory: list[str] = []

    def repopulate_possible_connections_for_all_stations(self) -> None:
        """ Prepare for the generation of a new trajectory. """
        for station in self.stations:
            self.stations[station].repopulate_possible_connections()

    def make_random_trajectory(self) -> None:
        """ Generates a randomly chosen trajectory. """
        
        self.repopulate_possible_connections_for_all_stations()

        random_trajectory = Trajectory()
        
        random_departure_station = random.choice(list(self.stations.keys()))
        random_departure_station_object = self.stations[random_departure_station]

        random_trajectory.add_station_to_trajectory(random_departure_station)

        while random_trajectory.duration <= 120 and random_departure_station_object.possible_connections:
            
            random_connection = random.choice(random_departure_station_object.possible_connections)

            random_destination_station = self.connections[random_connection].get_destination_station(random_departure_station)

            random_destination_station_object = self.stations[random_destination_station]

            random_destination_station_object.remove_possible_connection(random_connection)
            random_departure_station_object.remove_possible_connection(random_connection)

            random_trajectory.duration += self.connections[random_connection].duration

            if random_trajectory.duration <= 120:
                random_trajectory.add_station_to_trajectory(random_destination_station)
            else:
                break   

            random_departure_station = random_destination_station
            random_departure_station_object = random_destination_station_object
            
        self.randomized_trajectory = random_trajectory.stations    

            


            
    
