from code.classes.traject import Traject

import random


class Randomize:
    def __init__(self, stations: dict, connections: dict):
        self.stations = stations
        self.connections = connections
        
        self.randomized_trajectory = []

    def repopulate_possible_connections_for_all_stations(self):
        for i in self.stations:
            self.stations[i].repopulate_possible_connections()

    def make_random_trajectory(self):
        
        self.repopulate_possible_connections_for_all_stations()

        random_trajectory = Traject()
        
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

            


            
    
