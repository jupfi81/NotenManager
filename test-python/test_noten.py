""" Teste note.py"""

import unittest
import tempfile

import bewerte.note as note

class Testschriftlich(unittest.TestCase):
    """ Teste die Funktionen schriftlich.mittelwert """

    def test_read_config_file(self):
        """ Teste die Instanz read_config_files """
        # Erstelle 3 configfiles
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(tmpdir+'/klasserc', 'w') as defaultrc:
                defaultrc.write('[wichtung]\n')
                defaultrc.write('schriftlich = 2\n')
                defaultrc.write('muendlich = 1\n')
                defaultrc.write('arbeit = 1\n')
                defaultrc.write('test = 1\n')
                defaultrc.write('monat = 1\n')
                defaultrc.write('\n[bewertungsart]\n')
                defaultrc.write('arbeit = e\n')
                defaultrc.write('test = g\n')
                defaultrc.write('monat = e\n')
                defaultrc.write('\n[arten]\n')
                defaultrc.write('arbeit = schriftlich\n')
                defaultrc.write('test = schriftlich\n')
                defaultrc.write('monat = muendlich\n')

            # Lasse die Dateien einlesen
            gimli = {'arbeit' : [2, 3, 3], 'test' : [2, 2], 'monat' : [1, 1, 1]}
            gloin = {'arbeit' : [2.5, 2.5, 3.25],
                     'test' : [3.0, 1.5, 1.0, 5.0, 5.0, 1.5, 3.5],
                     'monat' : [3.0, 2.5, 2.0, 2.0, 2.25]}
            self.assertEqual(note.endnote(gimli, tmpdir+'/klasserc'), 2)
            self.assertEqual(note.endnote(gloin, tmpdir+'/klasserc'), 2.65)

if __name__ == '__main__':
    unittest.main()
