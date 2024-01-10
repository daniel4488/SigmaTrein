from station import Station
from traject import Traject
from verbinding import Verbinding
import random

class RailNL:
    def __init__(self):
        # Dict met de naam van het station als key en een bijbehordend object
        self.stations: dict[str, Station] = {}
        # Dict met het trajectnummer als key en een bijbehordend object
        self.verbindingen: dict[int, Verbinding] = {}
        # Dict met de trajectnaam als key en een bijbehordend object
        self.trajecten: list[Traject] = []

        # Laad de stations in
        self.laad_stations()
        # Laad de verbindingen in
        self.laad_verbindingen()

    def laad_stations(self):
        # Open StationsHolland.csv
        with open("../../data/holland/StationsHolland.csv", "r") as file:
            # Remove header
            _ = file.readline()

            # Iterate over rest of the file
            for line in file:
                # Remove newline character at the end
                line = line.strip()

                # Split line based on a comma
                station, y, x = line.split(",")
                
                self.stations[station] = Station(station, x, y)

    def laad_verbindingen(self):

        with open("../../data/holland/ConnectiesHolland.csv", "r") as file:
            # Remove header
            _ = file.readline()

            traject_nummer = 0

            for line in file:
                # Remove newline character
                line = line.strip()

                # Split line
                station_1, station_2, duur = line.split(",")

                # Convert van string naar integer
                duur = int(duur)

                # Voeg verbinding toe voor beide stations
                self.stations[station_1].voeg_verbinding_toe(station_2, duur, traject_nummer)
                self.stations[station_2].voeg_verbinding_toe(station_1, duur, traject_nummer)

                # Voeg verbinding toe 
                self.verbindingen[traject_nummer] = (Verbinding(station_1, station_2, duur, traject_nummer))  

                # Houd bij welk trajectnummer dit was
                traject_nummer += 1
                

    def maak_traject(self):

        # Zorg ervoor dat de mogelijke verbindingen weer correct zijn voor een nieuw traject
        for i in self.stations:
            self.stations[i].maak_mogelijke_verbindingen()

        # Variabele om de totale tijd van een traject bij te houden
        totale_tijd = 0 
        geen_verbindingen_mogelijk = False

         # Maak een nieuw traject object aan
        traject = Traject()

        # Voeg het traject toe aan de dictionary met trajecten
        self.trajecten.append(traject)
        
        # Kies een willekeurig station uit de stations dictionary
        random_station = random.choice(list(self.stations.keys()))

        # Voeg station toe
        traject.voeg_station_toe(random_station)

        # Verkrijg het desbetreffende station die bij de willikeurige key hoort
        random_station_object = self.stations[random_station]

        # Leg nieuwe verbindingen aan zolang trajectduur korter is dan 120 en er verbindingen mogelijk zijn
        while totale_tijd <= 120 and geen_verbindingen_mogelijk == False:
            # Als de verbinding nog niet is gebruikt voeg de verbinding toe aan het traject
            if random_station_object.mogelijke_verbindingen:

                # Kies een random bestemming station
                random_verbinding = random.choice(random_station_object.mogelijke_verbindingen)

                # Kijk vanuit waar de verbinding vertrekt
                if self.verbindingen[random_verbinding].station_1 == random_station:
                    random_bestemming_station = self.verbindingen[random_verbinding].station_2
                elif self.verbindingen[random_verbinding].station_2 == random_station:
                    random_bestemming_station = self.verbindingen[random_verbinding].station_1

                # Vind het desbetreffende object bij het bestemmings station
                random_bestemming_station_object = self.stations[random_bestemming_station]

                # Kijk welke verbinding is gebruitkt
                gebruikte_verbinding = random_station_object.verbindingen[random_bestemming_station][1]

                # Verwijder deze verbinding als mogelijke verbinding die nog gebruikt kan worden voor bestemmingsstation
                random_bestemming_station_object.verwijder_mogelijke_verbinding(gebruikte_verbinding)

                # Verwijder deze verbinding als mogelijke verbinding die nog gebruikt kan worden voor het huidige station
                random_station_object.verwijder_mogelijke_verbinding(gebruikte_verbinding)

                # Update de totale tijdsduur van het traject met de tijd van de gelegde verbinding
                totale_tijd += self.verbindingen[gebruikte_verbinding].duur
                
                if totale_tijd <= 120:
                    # Voeg station toe aan traject als het binnen tijdslimiet valt
                    traject.voeg_station_toe(random_bestemming_station)
                    traject.trajectduur = totale_tijd

                # Zet bestemmingsstation naar het huidige station
                random_station = random_bestemming_station

                # Zo ook voor het object
                random_station_object = random_bestemming_station_object

                # Kies een random bestemming station
                random_bestemming_station = random.choice(list(random_bestemming_station_object.verbindingen.keys()))

                # Vind bijbehorende object
                random_bestemming_station_object = self.stations[random_bestemming_station]
            else:
                # Als de gekozen verbinding al gebruikt is toggle dubbel_traject naar True
                geen_verbindingen_mogelijk = True


if __name__ == "__main__":
    # Initialize raiLNL
    railNL = RailNL()

    # Maak een traject
    railNL.maak_traject()

    # Print traject
    railNL.trajecten[0].print_traject()
    print("tijd = ", end="")
    railNL.trajecten[0].print_trajectduur()
    print()
            

