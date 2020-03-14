"""
Berechnet den aktuellen zwischenstand

Hierfür muss unter dem Namen Leonard Euler die jeweilige Maximalpunktzahl der Aufgabe stehen
"""

import csv
try:
    import my_stat
except:
    from bewerte import my_stat

class Zwischen:
    """ Die Zwischen-Klasse """
    def __init__(self):
        """Init-Funktion"""
        self.pfad = "./aufgaben.csv"
        self.punkte = []
        self.namen = []
        self.noten = []

    def read_punkte(self):
        """Lese die Punktedatei ein und speichere sie"""
        # Oeffne die Datei
        with open(self.pfad, mode='r') as data:
            tabelle = csv.reader(data, delimiter=',')
        # Speichere den betreffenden Spalte in eintrag
            for row in tabelle:
                self.namen.append(row[0:2])
                if len(row) > 2:
                    zeile = 0
                    for val in row:
                        if val.strip()[0].isdigit():
                            zeile += float(val.strip())
                    self.punkte.append(zeile)
                else:
                    self.punkte.append('')

    def entnehme_infos(self):
        """Ignotiere die erste Reihe"""
        del self.punkte[0]
        del self.namen[0]
        # Jetzt steht in der oberen Zeile die Maximale Punktzahl
        self.max_punkte = float(self.punkte[0])
        del self.punkte[0]
        del self.namen[0]

    def berechne_note(self):
        """Berechne die Note und gebe sie aus:"""
        for count, name in enumerate(self.namen):
            print(name[0], name[1], "\tPunkte:", self.punkte[count], "\tNote:",
                  round(6-5*self.punkte[count]/max_punkte, 2))
            noten.append(round(6-5*self.punkte[count]/max_punkte, 2))

    def to_string(self):
        """Berechne die Standardabweichung und den Mittelwert"""
        print("Min, UQuan, Med, Mean, OQuan, Max")
        print(stat(self.noten))

if __name__ == "__main__":
    ZWISCHEN = Zwischen()
