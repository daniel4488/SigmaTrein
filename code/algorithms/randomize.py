from code.classes.trajectory import Trajectory
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

        # initialize empty trajectory
        random_trajectory = Trajectory()
        
        # choose a random station to depart from
        random_departure_station = random.choice(list(self.stations.keys()))
        random_departure_station_object = self.stations[random_departure_station]

        # add departure station to the trajectory
        random_trajectory.add_station_to_trajectory(random_departure_station)

        # add stations to trajectory as long as its duration is less than 120 mins,
        # and there are still possible connections
        while random_trajectory.duration <= 120 and random_departure_station_object.possible_connections:
            
            # choose random connection number from possible connections at departure station
            random_connection = random.choice(random_departure_station_object.possible_connections)

            # get name of destination station from chosen connection 
            random_destination_station = self.connections[random_connection].get_destination_station(random_departure_station)

            # get destination station object
            random_destination_station_object = self.stations[random_destination_station]

            # remove created connection from destination and departure station's possible connections
            random_destination_station_object.remove_possible_connection(random_connection)
            random_departure_station_object.remove_possible_connection(random_connection)

            # add duration of created connection to duration of the trajectory
            random_trajectory.duration += self.connections[random_connection].duration

            # add station to trajectory if it fits within 120 mins
            if random_trajectory.duration <= 120:
                random_trajectory.add_station_to_trajectory(random_destination_station)
            else:
                break   

            # update departure station to the current station
            random_departure_station = random_destination_station
            random_departure_station_object = random_destination_station_object

        # create trajectory list of stations
        self.randomized_trajectory = random_trajectory.stations    
