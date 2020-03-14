"""
Bewertet einen Test/Arbeit

Verwendung:
    in den entsprechenden Ordner gehen und das Programm aufrugen. Alle wichtigen Informationen
    müssen in meta.txt gespeichert sein

Zu jeder Punktzahl wird in der Spalte nebenan die Note eingetragen.
Die Note wird berechnet, indem mit den Fixpunkten (1,eins) und (4,vier) ein linearer Notenwert
berechnet und auf viertelnoten gerundet wird, wobei man keine schlechtere Note wie 6 und keine
bessere wie 1 erhalten kann.
"""

import configparser
import csv
import re
try:
    import my_stat
except ModuleNotFoundError:
    from bewerte import my_stat

class Schriftlich:
    """
    Die Klassen bruacht folgende Ordnerstruktur bei "pfad":
        pfad/messungrc
        pfad/punkte.csv

    In der Metadatei muss die Art der Leistungsmessung, die Nummer, das Datum der Durchfuehrung,
    die Notenskala, die Anzahl der Zwischennoten, die maximal erreichbare Punktzahl, sowie die
    Punktzahl, mit der man eine 1 bzw. eine 4 kriegen soll.
    """

    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.

    def __init__(self):
        """ Init Klasse """
        self.config = configparser.ConfigParser()
        self.noten = []
        self.tabelle = []
        self.noten_tabular_align = "ll"
        self.noten_tabular_head = "Vorname & Nachname"
        self.liste = []
        self.head = []
        self.eins = 0
        self.vier = 0
        self.schritte = 0
        self.tabular_align = ""
        self.max_punkte = []

    def read_config_files(self, defaultrc, klasserc, messungrc):
        """ Lese die Konfigdateien ein """
        self.config.read(defaultrc)
        self.config.read(klasserc)
        self.config.read(messungrc)

    def bestimme_werte(self):
        """ Bestimme die maximale Punktzahl"""
        if self.config['noten']['punkte'] == 'master':
            maxp = float(self.tabelle[0][-1])
            self.max_punkte = self.tabelle[0]
            del self.tabelle[0]
        else:
            maxp = float(self.config['noten']['punkte'])

        # Bestimme die benötigten für ein und vier.
        if self.config['noten']['eins'][-1] == "%":
            self.eins = float(self.config['noten']['eins'][:-1]) * maxp / 100
        else:
            self.eins = float(self.config['noten']['eins'])

        if self.config['noten']['vier'][-1] == '%':
            self.vier = float(self.config['noten']['vier'][:-1]) * maxp / 100
        else:
            self.vier = float(self.config['noten']['vier'])

        self.schritte = int(self.config['noten']['notenschritte'])

    def read_punkte(self, pfad):
        """ Lese die Punktedatei ein """
        with open(pfad+'/punkte.csv', encoding='utf-8', mode='r') as tabelle:
            data = csv.reader(tabelle, delimiter=',')
            for row in data:
                self.tabelle.append(row)
            self.head = self.tabelle[0]
            del self.tabelle[0]

    def liste_gesamt(self):
        """ Erstelle eine Liste mit den Orten der Gesamtpunkte """
        for index, val in enumerate(self.head):
            if re.match('A[0-9]$', val.strip()):
                self.tabular_align += ">{\\bfseries}"
                self.noten_tabular_align += "l"
                self.noten_tabular_head += " &" + self.head[index]
                self.liste.append(index)
            self.tabular_align += "l"

    def write_noten(self):
        """ Schreibe die Noten in die Datei noten.csv """
        with open('noten.csv', encoding='utf-8', mode='w') as tabelle:
            writer = csv.writer(tabelle, delimiter=',')
            self.head.append("Note")
            writer.writerow([self.head[val] for val in [0, 1] + self.liste + [-2, -1]])
            for row in self.tabelle:
                if len(row) > 4:
                    writer.writerow([row[val] for val in [0, 1] + self.liste + [-2, -1]])
                else:
                    writer.writerow([row[val] for val in [0, 1]])

    def bewerte(self):
        """ Ordnet jeder Punktzahl eine Note zu und erstellt die Datei noten.csv.  """
        ausnahmen = self.config['ausnahmen']['namen'].split(',')
        bonuspunkte = self.config['ausnahmen']['bonuspunkte'].split(',')
        for row in self.tabelle:
            if len(row) >= 3:
                name = row[0].strip() + " " + row[1].strip()
                if not name in ausnahmen:
                    wertung = 0
                    wertung = my_stat.note(
                        float(row[-1]),
                        self.eins,
                        self.vier,
                        self.schritte)
                    row.append(wertung)
                else:
                    bonus = float(bonuspunkte[ausnahmen.index(name)])
                    print("Mache eine Ausnahme für", name, "mit", str(bonus), "Bonuspunkten")
                    wertung = 0
                    eins = self.eins - bonus
                    vier = self.vier/self.eins * eins
                    wertung = my_stat.note(float(row[2]), eins, vier, self.schritte)
                    row.append(wertung)
            elif len(row) == 2:
                row.append("")
                row.append("")
            else:
                print("Falsche Zeilenbreite")
            self.noten.append(row)

    def aufgaben_stat(self):
        """Berechnet die Schwierigkeit und die Streuung einer Aufgabe"""
        schwierigkeit = "&Schwierigkeit"
        streuung = "&Streuung"
        for index, max_punkt in enumerate(self.max_punkte):
            if max_punkt[0].isdigit():
                punkte = []
                for row in self.tabelle:
                    if len(row) > index and row[index]:
                        punkte.append(float(row[index]))
                mean_punkte = sum(punkte)/len(punkte)
                punkteq = []
                for row in self.tabelle:
                    if len(row) > index and row[index]:
                        punkteq.append((float(row[index]) - mean_punkte)**2)
                mean_punkteq = sum(punkteq)/(len(punkteq)-1)
                if float(max_punkt) != 0:
                    schwierigkeit += "&" + str(round(mean_punkte/float(max_punkt), 2))
                    streuung += "&" + str(round(mean_punkteq/float(max_punkt), 2))
                else:
                    schwierigkeit += "&" + str(round(mean_punkte, 2))
                    streuung += "&" + str(round(mean_punkteq, 2))
        return schwierigkeit + "\\\\\\midrule\n" + streuung

    def totex(self):
        """ Erstelle eine pdf-Datei """
        # Speichere in noten die Noten der SchülerInnen, die eine Note erhalten erhaben
        noten = []
        for val in self.noten:
            if val[3]: # Wenn val[3] existiert, dann wurde eine Note vergeben
                noten.append(float(val[-1])) # Die Note steht im letzten Eintrag

        # Bestimme alle Werte für einen Boxplot
        [minimum, uquan, median, mean, oquan, maximum] = my_stat.stat(noten)
        # Schreibe die Werte in die Datei stat.txt.
        with open('stat.txt', encoding='utf-8', mode='w') as datei:
            datei.write("Minimum  " + str(minimum) + "\n")
            datei.write("u. Quar. " + str(uquan) + "\n")
            datei.write("Median   " + str(median) + "\n")
            datei.write("Schnitt  " + str(mean) + "\n")
            datei.write("o. Quar. " + str(oquan) + "\n")
            datei.write("Maximum  " + str(maximum) + "\n")
            print("Minimum  ", minimum)
            print("u. Quar. ", uquan)
            print("Median   ", median)
            print("Schnitt  ", mean)
            print("o. Quar. ", oquan)
            print("Maximum  ", maximum)

        # Öffne die Datei './auswertung.tex' im Schreibmodus, um die Daten einzutragen
        with open('./auswertung.tex', mode='w') as latex:
            # Öffne die Datei 'Auswertung_schriftliche_Arbeit.tex' im Schreibmodus, um den Inhalt zu übernehmen.
            # An den Stellen, bei denen die Escapesequen "<key>" steht, werden Zeilen eingefügt.
            with open("/home/ac/Projekte/NotenManager/tex/Auswertung_schriftliche_Arbeit.tex", mode='r') as text:
                for line in text:
                    if line == "\t<Notentabelle hier einfuegen>\n": # Die Notentabelle wird eingefügt
                        # Die Umgebung tabular wird aufgerufen
                        latex.write("\\begin{tabular}{" + self.noten_tabular_align +"l>{\\bfseries}l}\n")
                        latex.write(self.noten_tabular_head + "& Gesamt & Note\\\\\\toprule\n")

                        # Es folgen die Zeilen
                        for row in self.tabelle:
                            latex.write(str(row[0]) + "&" + str(row[1]) + "&") # Name
                            for val in self.liste:
                                # Wenn Punkte eingetragen wurden, weden die Gesamtpunkte pro Aufgabe eingetragen.
                                # Ansonsten wird ein " &" eingefügt.
                                if len(row) > val:
                                    latex.write(str(row[val]) + "&")
                                else:
                                    latex.write("" + "&")

                            # Die erreichte Punktzahl steht an der Stelle [-2] und die Note an der Stelle [-1]
                            latex.write(str(row[-2]) + "&" + str(row[-1]) + "\\\\\\midrule\n")

                        # Das Ende der Umgebung wird geschrieben.
                        latex.write("\\end{tabular}\n")

                    else:
                        # Was wo eingetragen wird ist selbsterklärend
                        line = line.replace("<Klasse>", self.config['basics']['klasse'])
                        line = line.replace("<Art>", self.config['basics']['art'])
                        line = line.replace("<Nummer>", self.config['basics']['nummer'])
                        line = line.replace("<MW>", str(mean))
                        line = line.replace("<MD>", str(median))
                        line = line.replace("<Min>", str(minimum))
                        line = line.replace("<Max>", str(maximum))
                        line = line.replace("<OQ>", str(oquan))
                        line = line.replace("<UQ>", str(uquan))
                        latex.write(line)

if __name__ == "__main__":
    TEST = Schriftlich()
    TEST.read_config_files('/home/ac/Projekte/NotenManager/config/defaultrc',
                           '../../klasserc', 'messungrc')
    TEST.read_punkte('./')
    TEST.bestimme_werte()
    TEST.bewerte()
    TEST.liste_gesamt()
    TEST.totex()
    TEST.write_noten()
