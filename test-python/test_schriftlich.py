""" Teste die Module von my_stat.py"""

import unittest
import tempfile
import csv

import bewerte.schriftlich as schriftlich

class Testschriftlich(unittest.TestCase):
    """ Teste die Funktionen schriftlich.mittelwert """

    def test_init(self):
        """ Teste die __init__(self) Funktion. """
        test = schriftlich.Schriftlich()
        self.assertEqual(test.noten, [])
        self.assertEqual(test.tabelle, [])
        self.assertEqual(test.head, [])
        self.assertEqual(test.eins, 0)
        self.assertEqual(test.vier, 0)
        self.assertEqual(test.schritte, 0)
    
    def test_read_config_file(self):
        """ Teste die Instanz read_config_files """
        # Erstelle 3 configfiles
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(tmpdir+'/defaultrc', 'w') as defaultrc:
                defaultrc.write('[basics]\n')
                defaultrc.write('default=default\n')
                defaultrc.write('klasse=default\n')
                defaultrc.write('messung=default\n')
            with open(tmpdir+'/klasserc', 'w') as klasserc:
                klasserc.write('[basics]\n')
                klasserc.write('klasse=klasse\n')
                klasserc.write('messung=klasse\n')
            with open(tmpdir+'/messungrc', 'w') as messungrc:
                messungrc.write('[basics]\n')
                messungrc.write('messung=messung\n')
                messungrc.write('[noten]\n')
                messungrc.write('notenschritte=2\n')
                messungrc.write('eins=100%%\n')
                messungrc.write('vier=8\n')

            # Lasse die Dateien einlesen
            test = schriftlich.Schriftlich()
            test.read_config_files(
                tmpdir+'/defaultrc', tmpdir+'/klasserc', tmpdir+'/messungrc')
            self.assertEqual(test.config['basics']['default'], 'default')
            self.assertEqual(test.config['basics']['klasse'], 'klasse')
            self.assertEqual(test.config['basics']['messung'], 'messung')
            self.assertEqual(test.config['noten']['notenschritte'], '2')
            self.assertEqual(test.config['noten']['eins'], '100%')
            self.assertEqual(test.config['noten']['vier'], '8')

    def test_read_punkte1(self):
        """ Teste das Einlesen einer Punktedatei """
        # Erstelle eine Punktedatei
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(tmpdir+'/punkte.csv', 'w') as datei:
                writer = csv.writer(datei, delimiter=',')
                writer.writerow(['Vorname', 'Nachname', 'Gesamt'])
                writer.writerow(['Frodo', 'Beutlin', '4'])
                writer.writerow(['Samweis', 'Gamdschie', '5'])
                writer.writerow(['Perigrin', 'Tuk', '6'])
                writer.writerow(['Merriadoc', 'Brandybok', '7'])

            test = schriftlich.Schriftlich()
            test.read_punkte(tmpdir)
            erwartung = [
                ['Frodo', 'Beutlin', '4'],
                ['Samweis', 'Gamdschie', '5'],
                ['Perigrin', 'Tuk', '6'],
                ['Merriadoc', 'Brandybok', '7']
            ]

            self.assertEqual(test.tabelle, erwartung)
            self.assertEqual(test.head, ['Vorname', 'Nachname', 'Gesamt'])

    def test_read_punkte2(self):
        """ Teste das Einlesen einer Punktedatei """
        # Erstelle eine Punktedatei
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(tmpdir+'/punkte.csv', 'w') as datei:
                writer = csv.writer(datei, delimiter=',')
                writer.writerow(['Vorname', 'Nachname', 'A1', 'A2', 'Gesamt'])
                writer.writerow(['Frodo', 'Beutlin', '4', '2', '6'])
                writer.writerow(['Samweis', 'Gamdschie', '5', '3', '8'])
                writer.writerow(['Perigrin', 'Tuk'])
                writer.writerow(['Merriadoc', 'Brandybok', ''])

            test = schriftlich.Schriftlich()
            test.read_punkte(tmpdir)
            erwartung = [
                ['Frodo', 'Beutlin', '4', '2', '6'],
                ['Samweis', 'Gamdschie', '5', '3', '8'],
                ['Perigrin', 'Tuk'],
                ['Merriadoc', 'Brandybok', '']
            ]

            self.assertEqual(test.tabelle, erwartung)
            self.assertEqual(test.head, ['Vorname', 'Nachname', 'A1', 'A2', 'Gesamt'])

    def test_gesamtliste(self):
        test = schriftlich.Schriftlich()
        test.head = ['Vorname', 'Nachname', 'A1a', 'A1b', 'A1', 'A2', 'A3']
        test.liste_gesamt()
        erwarte = "llll>{\\bfseries}l>{\\bfseries}l>{\\bfseries}l"
        self.assertEqual(test.tabular_align, erwarte)

    def test_bestimme_werte_1(self):
        """ Teste das Bestimmen der wichtigsten Werte, wenn sie absolut gegeben sind """
        test = schriftlich.Schriftlich()
        test.config.add_section('noten')
        test.config.set('noten', 'punkte', '24')
        test.config.set('noten', 'eins', '24')
        test.config.set('noten', 'vier', '12')
        test.config.set('noten', 'notenschritte', '2')
        test.bestimme_werte()
        self.assertEqual(test.eins, 24)
        self.assertEqual(test.vier, 12)
        self.assertEqual(test.schritte, 2)

    def test_bestimme_werte_2(self):
        """ Teste das Bestimmen der wichtigsten Werte, wenn sie absolut gegeben sind """
        test = schriftlich.Schriftlich()
        test.config.add_section('noten')
        test.config.set('noten', 'punkte', '24')
        test.config.set('noten', 'eins', '100%%')
        test.config.set('noten', 'vier', '50%%')
        test.config.set('noten', 'notenschritte', '2')
        test.bestimme_werte()
        self.assertEqual(test.eins, 24)
        self.assertEqual(test.vier, 12)
        self.assertEqual(test.schritte, 2)

    def test_bewerte(self):
        """ Teste das Bewerten """
        test = schriftlich.Schriftlich()
        test.tabelle = [
                ['Frodo', 'Beutlin', '0'],
                ['Samweis', 'Gamdschie', '24'],
                ['Perigrin', 'Tuk', '12'],
                ['Merriadoc', 'Brandybok', '10']
        ]
        test.config.add_section('ausnahmen')
        test.config.set('ausnahmen','namen', 'Merriadoc Brandybok')
        test.config.set('ausnahmen','bonuspunkte', '4')
        test.schritte = 4
        test.eins = 24
        test.vier = 12
        test.bewerte()
        ergebnis = [
                ['Frodo', 'Beutlin', '0', 6],
                ['Samweis', 'Gamdschie', '24', 1],
                ['Perigrin', 'Tuk', '12', 4],
                ['Merriadoc', 'Brandybok', '10', 4]
        ]
        self.assertEqual(test.noten, ergebnis)
        
if __name__ == '__main__':
    unittest.main()
