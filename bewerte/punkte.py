"""
Berechne die Gesamtpunktzahl und speichere sie in punkte.csv
"""

import csv

class PunkteZaehler:
    def __init__(self):
        """ Als erste stelle existiertst du """
        self.tabelle = []
        self.zeilen = []
        self.head = []
        self.aufgabenListe = []

    def read_file(self,read):
        """ schreibt die Zeilen aus read in self.tabelle """
        tabelle = csv.reader(read, delimiter=',')
        # Speichere den betreffenden Spalte in eintrag
        for row in tabelle:
            self.tabelle.append([eintrag.strip() for eintrag in row if not eintrag.strip() == ''])
        self.head = self.tabelle[0]
        del(self.tabelle[0])

    def addiere_punkte(self):
        """ Addiert die Punkte zusammen """
        self.zeilen.append(["Vorname", "Nachname", "Punkte"])
        for row in self.tabelle:
            gesamt = 0
            if not row[0].strip() == "Vorname":
                check = False
                for val in row:
                    if val.strip()[0].isdigit():
                        check = True
                        gesamt += float(val.strip())
                if check:
                    self.zeilen.append(row[0:2] +[gesamt])
                else:
                    self.zeilen.append(row[0:2])

    def write_file(self, write):
        """ schreibt die Zeilen von self.tabelle in write """
        tabelle = csv.writer(write, delimiter=',')
        tabelle.writerow(self.head)
        for row in self.zeilen:
            tabelle.writerow(row)

    def make_head(self):
        """ Erstelle die richtige Kopfzeile """
        # Erstelle die Kopfzeile
        self.aufgabenListe = self.head[2:]
        aufgabenCounter = 1
        head_neu = ['Vorname', 'Nachname']
        teilaufgabenCounter = 0
        for counter, teilaufgabe in enumerate(self.aufgabenListe):
            if not self.aufgabenListe[counter].strip()[1] == str(aufgabenCounter):
                if not teilaufgabenCounter == 1:
                    head_neu.append("A"+str(aufgabenCounter))
                aufgabenCounter += 1
                teilaufgabenCounter = 0
            head_neu.append(teilaufgabe.strip())
            teilaufgabenCounter += 1
        if not teilaufgabenCounter == 1:
            head_neu.append("A"+str(aufgabenCounter))
        head_neu += ["Gesamt"]
        self.head = head_neu

    def addiere_punkte_einzeln(self):
        """ Addiere die Aufgaben einzeln zusammen """
        for row in self.tabelle:
            row_neu = row[0:2]
            if len(row) > 2:
                if row[2]:
                    punkte = 0
                    gesamt = 0
                    aufgabenCounter = 1
                    teilaufgabenCounter = 0
                    for counter, val in enumerate(row[2:]):
                        if self.aufgabenListe[counter].strip()[1] == str(aufgabenCounter):
                            punkte += float(val.strip())
                        else:
                            if not teilaufgabenCounter == 1:
                                row_neu.append(punkte)
                            gesamt += punkte
                            punkte = float(val.strip())
                            aufgabenCounter += 1
                            teilaufgabenCounter = 0
                        row_neu.append(float(val.strip()))
                        teilaufgabenCounter += 1
                    if not teilaufgabenCounter == 1:
                        row_neu.append(punkte)
                    gesamt += punkte
                    row_neu.append(gesamt)
            self.zeilen.append(row_neu)

if __name__ == "__main__":
    messung = PunkteZaehler()
    with open("./aufgaben.csv", mode='r') as read:
        messung.read_file(read)
    messung.make_head()
    messung.addiere_punkte_einzeln()
    with open("./punkte.csv", mode='w') as write:
        messung.write_file(write)
