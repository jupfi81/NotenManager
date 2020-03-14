""" Teste punkte.py"""

import unittest
import tempfile
import csv
import bewerte.punkte as punkte 

class TestPunkte(unittest.TestCase):
    """ Teste PunkteZaehler """
    def test_init(self):
        """ Teste die Funktion __init__ """
        messung = punkte.PunkteZaehler()
        self.assertEqual(messung.tabelle, [])
        self.assertEqual(messung.zeilen, [])
        self.assertEqual(messung.head, [])
        self.assertEqual(messung.aufgabenListe, [])

    def test_addiere_punkte_1(self):
        """ Teste die Funktion addiere_punkte """
        messung = punkte.PunkteZaehler()
        messung.tabelle = [
            ['Vorname', 'Nachname', 'A1', 'A2'],
            ['Frodo', 'Beutlin', '2', '2'],
            ['Samweis', 'Gamdschie', '1', '4'],
            ['Perigrin', 'Tuk', '2', '4'],
            ['Merriadoc', 'Brandybok', '3', '4']
        ]
        ergebnis = [
            ['Vorname', 'Nachname', 'Punkte'],
            ['Frodo', 'Beutlin', 4],
            ['Samweis', 'Gamdschie', 5],
            ['Perigrin', 'Tuk', 6],
            ['Merriadoc', 'Brandybok', 7]
        ]
        messung.addiere_punkte()
        self.assertEqual(ergebnis, messung.zeilen)

    def test_addiere_punkte_2(self):
        """ Teste die Funktion addiere_punkte """
        messung = punkte.PunkteZaehler()
        messung.head = ['Vorname', 'Nachname', 'A1', 'A2']
        messung.tabelle = [
            ['Frodo', 'Beutlin'],
            ['Samweis', 'Gamdschie'],
            ['Perigrin', 'Tuk', '2', '4'],
            ['Merriadoc', 'Brandybok', '3', '4']
        ]
        ergebnis = [
            ['Vorname', 'Nachname', 'Punkte'],
            ['Frodo', 'Beutlin'],
            ['Samweis', 'Gamdschie'],
            ['Perigrin', 'Tuk', 6],
            ['Merriadoc', 'Brandybok', 7]
        ]
        messung.addiere_punkte()
        self.assertEqual(ergebnis, messung.zeilen)

    def test_addiere_punkte_einzeln1(self):
        """ Teste die Funktion addiere_punkte """
        messung = punkte.PunkteZaehler()
        messung.aufgabenListe = ['A1a', 'A1b', 'A2']
        messung.tabelle = [
            ['Frodo', 'Beutlin', ''],
            ['Samweis', 'Gamdschie'],
            ['Perigrin', 'Tuk', '2', '2', '4'],
            ['Merriadoc', 'Brandybok', '3', '3', '4']
        ]
        ergebnis = [
            ['Frodo', 'Beutlin'],
            ['Samweis', 'Gamdschie'],
            ['Perigrin', 'Tuk', 2, 2, 4, 4, 8],
            ['Merriadoc', 'Brandybok', 3, 3, 6, 4, 10]
        ]
        messung.addiere_punkte_einzeln()
        self.assertEqual(ergebnis, messung.zeilen)

    def test_addiere_punkte_einzeln2(self):
        """ Teste die Funktion addiere_punkte """
        messung = punkte.PunkteZaehler()
        messung.aufgabenListe = ['A1', 'A2a', 'A2b']
        messung.tabelle = [
            ['Frodo', 'Beutlin', ''],
            ['Samweis', 'Gamdschie'],
            ['Perigrin', 'Tuk', '2', '2', '4'],
            ['Merriadoc', 'Brandybok', '3', '3', '4']
        ]
        ergebnis = [
            ['Frodo', 'Beutlin'],
            ['Samweis', 'Gamdschie'],
            ['Perigrin', 'Tuk', 2, 2, 4, 6, 8],
            ['Merriadoc', 'Brandybok', 3, 3, 4, 7, 10]
        ]
        messung.addiere_punkte_einzeln()
        self.assertEqual(ergebnis, messung.zeilen)

    def test_make_head(self):
        """ Teste die Funktion make_head """
        messung =punkte.PunkteZaehler()
        messung.head = ['Vorname', 'Nachname', 'A1', 'A2a', 'A2b', 'A3a', 'A3b']
        messung.make_head()
        ergebnis = ['Vorname', 'Nachname', 'A1', 'A2a', 'A2b', 'A2', 'A3a', 'A3b', 'A3', 'Gesamt']
        self.assertEqual(ergebnis, messung.head)

    def test_read_file(self):
        """ Teste das Einlesen einer Datei """

        # Erstelle die einzulesende Datei
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(tmpdir+'/eintrag.csv', 'w') as datei:
                writer = csv.writer(datei, delimiter=',')
                writer.writerow(['Vorname', 'Nachname', 'A1', 'A2'])
                writer.writerow(['Frodo', 'Beutlin', ''])
                writer.writerow(['Samweis', 'Gamdschie', '1', '4'])
                writer.writerow(['Perigrin', 'Tuk', '2', '4'])
                writer.writerow(['Merriadoc', 'Brandybok', '3', '4'])
                writer.writerow(['Gollum', 'Smeagol'])

            # Lese die Datei ein
            messung = punkte.PunkteZaehler()
            with open(tmpdir+'/eintrag.csv', 'r') as datei:
                messung.read_file(datei)
        ergebnis = [
            ['Frodo', 'Beutlin'],
            ['Samweis', 'Gamdschie', '1', '4'],
            ['Perigrin', 'Tuk', '2', '4'],
            ['Merriadoc', 'Brandybok', '3', '4'],
            ['Gollum', 'Smeagol']
        ]
        self.assertEqual(messung.tabelle, ergebnis)
        ergebnis = ['Vorname', 'Nachname', 'A1', 'A2']
        self.assertEqual(messung.head, ergebnis)

if __name__ == '__main__':
    unittest.main()
