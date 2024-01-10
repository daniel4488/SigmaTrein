class Station():
    """ Class voor station. """

    def __init__(self, naam):
        self.naam = naam
        self.verbindingen = dict()

    def maak_verbinding(self, station, tijd):
        """ Voeg nieuwe verbinding toe aan het station. """
        self.verbindingen[station] = tijd

    def geef_verbinding(self, station):
        """ Laat verbinding zien naar station toe. """
        return self.verbindingen[station]
