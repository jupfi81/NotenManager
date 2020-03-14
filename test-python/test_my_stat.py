""" Teste die Module von my_stat.py"""

import unittest
from bewerte import my_stat

class TestMittelwert(unittest.TestCase):
    """ Teste die Funktion my_stat.mittelwert """
    def test_ganze_Zahl(self):
        """ Wenn das Ergebnis eine ganze Zahl ergeben soll """

        noten = [2, 6]
        result = my_stat.mittelwert(noten)
        expected = 4
        self.assertEqual(result, expected)

    def test_gerundete_Zahl(self):
        """ Wenn das Ergebnis gerundet werden soll """

        noten = [1, 2, 2]
        result = my_stat.mittelwert(noten)
        expected = 1.67
        self.assertEqual(result, expected)

class TestMedian(unittest.TestCase):
    """ Teste die Funktion my_stat.median """

    def test_gerade_Anzahl(self):
        """ Wenn die Länge der Noten gerade ist """
        noten = [1, 2, 3, 4]
        result = my_stat.median(noten)
        expected = 2.5
        self.assertEqual(result, expected)

    def test_ungerade_Anzahl(self):
        """ Wenn die Länge der Noten ungerade ist """
        noten = [1, 2, 3, 4, 5]
        result = my_stat.median(noten)
        expected = 3
        self.assertEqual(result, expected)

    def test_gerundet(self):
        """ Wenn das Ergebnis gerundet werden muss """
        noten = [1.25, 1.5]
        result = my_stat.median(noten)
        expected = 1.38
        self.assertEqual(result, expected)

class TestQuartile(unittest.TestCase):
    """ Teste die Funktion my_stat.quartile """

    def test_gerade_Anzahl(self):
        """ Wenn die Länge der Noten gerade ist """
        noten = [1, 2, 3, 4]
        [result_uquart, result_oquart] = my_stat.quartile(noten)
        expected_uquart = 1.5
        expected_oquart = 3.5
        self.assertEqual(result_uquart, expected_uquart)
        self.assertEqual(result_oquart, expected_oquart)

    def test_ungerade_Anzahl(self):
        """ Wenn die Länge der Noten ungerade ist """
        noten = [1, 2, 3, 4, 5]
        [result_uquart, result_oquart] = my_stat.quartile(noten)
        expected_uquart = 1.5
        expected_oquart = 4.5
        self.assertEqual(result_uquart, expected_uquart)
        self.assertEqual(result_oquart, expected_oquart)

    def test_gerundet(self):
        """ Wenn das Ergebnis gerundet werden muss """
        noten = [1.25, 1.5, 3.25, 3.5]
        [result_uquart, result_oquart] = my_stat.quartile(noten)
        expected_uquart = 1.38
        expected_oquart = 3.38
        self.assertEqual(result_uquart, expected_uquart)
        self.assertEqual(result_oquart, expected_oquart)

class TestStat(unittest.TestCase):
    """ Teste die Funktion my_stat.stat """

    def test_gesamt(self):
        """ Ein einmaliger Test bei einer langen Liste """
        noten = [1, 2, 3, 4, 3.5, 6, 1.25, 3, 2.5, 2.5]
        [minimum, unteres_quartil, median, mittelwert, oberes_quartil, maximum] = my_stat.stat(noten)
        expected = [1, 2, 2.75, 2.88, 3.5, 6]
        self.assertEqual(minimum, expected[0])
        self.assertEqual(unteres_quartil, expected[1])
        self.assertEqual(median, expected[2])
        self.assertEqual(mittelwert, expected[3])
        self.assertEqual(oberes_quartil, expected[4])
        self.assertEqual(maximum, expected[5])

    def test_gesamt(self):
        """ Funktoniert es auch mit einer kurzen liste"""
        noten = [1,1,1,1]
        [minimum, unteres_quartil, median, mittelwert, oberes_quartil, maximum] = my_stat.stat(noten)
        expected = [1, 1, 1, 1, 1, 1]
        self.assertEqual(minimum, expected[0])
        self.assertEqual(unteres_quartil, expected[1])
        self.assertEqual(median, expected[2])
        self.assertEqual(mittelwert, expected[3])
        self.assertEqual(oberes_quartil, expected[4])
        self.assertEqual(maximum, expected[5])

    def test_gerundet(self):
        """ Wenn das Ergebnis gerundet werden muss """
        noten = [1.25, 1.5, 3.25, 3.5]
        [result_uquart, result_oquart] = my_stat.quartile(noten)
        expected_uquart = 1.38
        expected_oquart = 3.38
        self.assertEqual(result_uquart, expected_uquart)
        self.assertEqual(result_oquart, expected_oquart)

class TestNote(unittest.TestCase):
    """ Teste die Funktion my_stat.note """

    def test_nummer1(self):
        """ gesamt = [0, 5, 10, 15, 20] , eins = 20, vier = 10, feinheit=.25 """
        note1 = my_stat.note(0, 20, 10, 4)
        note2 = my_stat.note(5, 20, 10, 4)
        note3 = my_stat.note(10, 20, 10, 4)
        note4 = my_stat.note(15, 20, 10, 4)
        note5 = my_stat.note(20, 20, 10, 4)
        self.assertEqual(note1, 6)
        self.assertEqual(note2, 5.5)
        self.assertEqual(note3, 4)
        self.assertEqual(note4, 2.5)
        self.assertEqual(note5, 1)

    def test_ungerade_Anzahl(self):
        """ Wenn die Länge der Noten ungerade ist """
        noten = [1, 2, 3, 4, 5]
        [result_uquart, result_oquart] = my_stat.quartile(noten)
        expected_uquart = 1.5
        expected_oquart = 4.5
        self.assertEqual(result_uquart, expected_uquart)
        self.assertEqual(result_oquart, expected_oquart)

    def test_gerundet(self):
        """ Wenn das Ergebnis gerundet werden muss """
        noten = [1.25, 1.5, 3.25, 3.5]
        [result_uquart, result_oquart] = my_stat.quartile(noten)
        expected_uquart = 1.38
        expected_oquart = 3.38
        self.assertEqual(result_uquart, expected_uquart)
        self.assertEqual(result_oquart, expected_oquart)

if __name__ == '__main__':
    unittest.main()
