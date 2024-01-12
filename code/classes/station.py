class Station:
    """ Class voor station. """

    def __init__(self, naam: str, x: float, y: float):
        self.naam: str = naam
        self.x: float = x
        self.y: float = y
        self.verbindingen: dict[str, list[int]] = dict()
        self.mogelijke_verbindingen: list[int] = []

    def voeg_verbinding_toe(self, bestemmingsstation: str, duur: int, trajectnummer: int) -> None:
        """ Voeg nieuwe verbinding toe aan het station. """
        self.verbindingen[bestemmingsstation] = [duur, trajectnummer]

    def geef_verbinding(self, bestemmingsstation: str) -> list[int]:
        """ Laat verbinding zien naar station toe. """
        return self.verbindingen[bestemmingsstation]
    
    def maak_mogelijke_verbindingen(self) -> None:
        for count, key in enumerate(self.verbindingen):
            self.mogelijke_verbindingen.append(self.verbindingen[key][1])

    def verwijder_mogelijke_verbinding(self, verbinding_nummer: int) -> None:
        self.mogelijke_verbindingen.remove(verbinding_nummer)

    def __str__(self) -> str:
        return self.naam
