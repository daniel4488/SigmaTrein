class Station:
    """ Class voor station. """

    def __init__(self, naam, x, y):
        self.naam = naam
        self.x = x 
        self.y = y 
        self.verbindingen: dict[int, int] = dict()
        self.mogelijke_verbindingen: list[int] = []

    def voeg_verbinding_toe(self, bestemmingsstation, duur, trajectnummer):
        """ Voeg nieuwe verbinding toe aan het station. """
        self.verbindingen[bestemmingsstation] = [duur, trajectnummer]

    def geef_verbinding(self, bestemmingsstation):
        """ Laat verbinding zien naar station toe. """
        return self.verbindingen[bestemmingsstation]
    
    def maak_mogelijke_verbindingen(self):
        for count, key in enumerate(self.verbindingen):
            self.mogelijke_verbindingen.append(self.verbindingen[key][1])

    def verwijder_mogelijke_verbinding(self, verbinding_nummer):
        self.mogelijke_verbindingen.remove(verbinding_nummer)

