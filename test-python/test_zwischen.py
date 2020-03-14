"""Teste die Klasse Zwischen"""

import unittest
import tempfile
import shutil
import csv
import os
import bewerte.zwischen as zwischen

class TestZwischen(unittest.TestCase):
    """ Teste die Klasse Zwischen """
    def setUp(self):
        """Create a temporary directory"""
        self.tmpdir = tempfile.mkdtemp()
        with open(self.tmpdir + '/punkte.csv', 'w') as datei:
            writer = csv.writer(datei, delimiter=',')
            writer.writerow(['Vorname', 'Nachname', 'A1', 'A2', 'A3', 'A4'])
            writer.writerow(['Tom', 'Bombadil', '4', '4', '3', '3'])
            writer.writerow(['Frodo', 'Beutlin', '2', '2', '2', '1'])
            writer.writerow(['Samweis', 'Gamdschie', '4', '4', '3', '3'])
            writer.writerow(['Perigrin', 'Tuk', '3', '3', '2.5', '2'])
            writer.writerow(['Gimlie', 'Gloinson'])
            writer.writerow(['Merriadoc', 'Brandybok', '0', '0', '0', '0'])

    def tearDown(self):
        """Remove the directory after the test"""
        shutil.rmtree(self.tmpdir)

    def test_init(self):
        """ Werden alle erwarteten Größen angelegt? """
        stand = zwischen.Zwischen()
        self.assertEqual(stand.pfad, "./aufgaben.csv")
        self.assertEqual(stand.punkte, [])
        self.assertEqual(stand.namen, [])
        self.assertEqual(stand.noten, [])

    def test_read_punkte(self):
        """ Werden die Punkte richtig eingelesen? """
        # Erstelle eine Punktedatei
        stand = zwischen.Zwischen()
        stand.pfad = self.tmpdir+'/punkte.csv'
        stand.read_punkte()
        erwartung_namen = [
            ['Vorname', 'Nachname'],
            ['Tom', 'Bombadil'],
            ['Frodo', 'Beutlin'],
            ['Samweis', 'Gamdschie'],
            ['Perigrin', 'Tuk'],
            ['Gimlie', 'Gloinson'],
            ['Merriadoc', 'Brandybok']
        ]
        erwartung_punkte = [0, 14.0, 7.0, 14.0, 10.5, '', 0]

        self.assertEqual(stand.namen, erwartung_namen)
        self.assertEqual(stand.punkte, erwartung_punkte)

    def test_entnehme_infos(self):
        """Wird die erste Zeile richtig behandelt?"""
        stand = zwischen.Zwischen()
        stand.pfad = self.tmpdir+'/punkte.csv'
        stand.read_punkte()
        stand.entnehme_infos()
        erwartung_namen = [
            ['Frodo', 'Beutlin'],
            ['Samweis', 'Gamdschie'],
            ['Perigrin', 'Tuk'],
            ['Gimlie', 'Gloinson'],
            ['Merriadoc', 'Brandybok']
        ]
        erwartung_punkte = [7.0, 14.0, 10.5, '', 0]
        self.assertEqual(stand.namen, erwartung_namen)
        self.assertEqual(stand.punkte, erwartung_punkte)
        self.assertEqual(stand.max_punkte, 14)

if __name__ == '__main__':
    unittest.main()
