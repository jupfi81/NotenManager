""" Erstellt eine Ordner für eine neue Messung und frägt hierzu alle wichtigen Teile ab """

import os
import sys

class Messung:
    """
    Messung hilft beim erstellen der "messungrc"-Datei
    """

    def __init__(self):
        """ Erstellt alle wichtigen Variablen """
        self.place = os.listdir("./")

    def toString(self):
        """ Gibt die Variablen aus. """
        return self.place

    def make(self, name):
        """ Erstelle die Messung name """

        # Überpeüfe, ob der name noch frei ist
        if name in self.place:
            # Wenn der Name nicht mehr frei ist, gebe eine Fehlermeldung aus
            # sys.exit("1")
            print("Kein Platz für", name)
        else:
            # Wenn der Platz frei ist, dann schreibe das auch
            print("Der Platz für", name, "ist noch frei")

if __name__ == "__main__":
    m = Messung()
    print("So sieht mein Platz aus", m.toString())
    m.make("test1")
    m.make("test2")
