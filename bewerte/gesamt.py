"""
Gehe alle Schüler durch und erstelle eine Zusammenstellung der mündlichen Noten
"""

import configparser
import csv
import os
from statistics import mean
from note import endnote

class Klasse:
    """
    Jeder Schueler ist ein dictionary mit dem Namen als key und einem array als value
    """
    def __init__(self):
        """ Erstellt die Schuelerliste """
        self.schueler = dict()
        self.config = configparser.ConfigParser()
        self.config.read('~/Projekte/KlassenManager/config/defaultrc')
        self.config.read('klasserc')
        self.header = ["Vorname", "Nachname"]
        self.tabelle = [self.header]
        with open("./liste.csv", encoding='utf-8', mode='r') as datei:
            reader = csv.reader(datei, delimiter=',')
            count = False
            for row in reader:
                if count:
                    name = row[0].strip() + ", " + row[1].strip()
                    self.tabelle.append([row[0], row[1]])
                    self.schueler.update({name: dict()})
                else:
                    count = True

    def reihenfolge_art(self, kategorie, art):
        """ Sortiere die Arten in der richtigen Reiehnfolge """
        liste = []
        for messung in os.listdir(kategorie):
            pfad = "./"+kategorie+"/"+messung+"/"
            self.config.read(pfad+"messungrc")
            if self.config['basics']['art'] == art:
                liste.append([pfad, self.config['basics']['nummer']])

        for val in liste:
            print("reihenfolge",val)

    def gesamt_art(self, kategorie, art):
        """ Fuege bei jedem SuS den Eintrag {art: []} ein """
        print("\nStelle die Noten von", art, "zusammen.")
        for key in self.schueler:
            self.schueler[key].update({art: []})

        # Lese zu jeder Art von schriftlichen Noten die Noten aus
        liste = os.listdir(kategorie)
        for messung in liste:
            pfad = "./"+kategorie+"/"+messung+"/"
            self.config.read(pfad+"messungrc")
            if self.config['basics']['art'] == art:
                print("Bin in Pfad", pfad, "und das sollte nummer", self.config['basics']['nummer'],
                      "sein und öffne", pfad + "noten.csv")
                self.header.append(self.config.get('basics', 'nummer', fallback='NN'))
                with open(pfad+"noten.csv", encoding='utf-8', mode='r') as datei:
                    reader = csv.reader(datei, delimiter=',')
                    count1 = 0
                    count2 = 0
                    for row in reader:
                        count1 += 1
                        name = row[0].strip() + ", " + row[1].strip()
                        if name in self.schueler.keys():
                            if len(row) >= 3 and row[-1]:
                                self.schueler[name][art].append(float(row[-1].strip()))
                            else:
                                self.schueler[name][art].append("")
                            count2 += 1
                    print("Das öffnen hat geklappt und es wurden", count2, "SuS eingetragen.")
                    if not count1 == count2 + 1:
                        print("In", pfad, "wurden", count1-count2-1, "viele Namen ausgelassen")
        self.header.append("s"+art)

    def build_tabelle(self):
        """ Gibt alle momentan gespeicherten Infos zu den SuS aus """
        self.tabelle = []
        self.header.append("Gesamt")
        self.tabelle.append(self.header)
        for key, schueler in self.schueler.items():
            row = []
            row += key.split(',')
            for art in schueler:
                row += schueler[art]
                noten = [val for val in schueler[art] if val]
                if noten:
                    row.append(round(4*mean(noten), 0)/4)
                else:
                    row.append("")
            row.append(endnote(schueler, 'klasserc'))
            self.tabelle.append(row)

    def write_tabelle(self, ort):
        """ Schreibt die Tabelle an den vorgesehenen Ort """
        with open(ort, encoding='utf-8', mode='w') as tabelle:
            writer = csv.writer(tabelle, delimiter=',')
            for row in self.tabelle:
                writer.writerow(row)

    def to_string(self):
        """ Gibt alle momentan gespeicherten Infos zu den SuS aus """
        for key, value in self.schueler.items():
            print(key)
            for art in value:
                print(art, "\t", value[art])

    def process(self):
        """ Gehe alle Kategorien durch """
        kategorien = [val.strip() for val
                      in self.config.get("basics", "Kategorien",
                                         fallback="schriftlich, muendlich").split(",")]
        for kategorie in kategorien:
            for eintrag in self.config["arten"]:
                if self.config["arten"][eintrag] == kategorie:
                    self.gesamt_art(kategorie, eintrag)
        self.build_tabelle()
        self.write_tabelle('info.csv')

if __name__ == "__main__":
    KLASSE = Klasse()
    KLASSE.process()
    # KLASSE.reihenfolge_art('schriftlich', 'arbeit')
