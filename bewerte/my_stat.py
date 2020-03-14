""" Stelle statistikfunktionen bereit """
import statistics
import math

def mittelwert(noten):
    """ Berechnet den Mittelwert der Liste noten auf 2 Stellen genau """
    mean = round(sum(noten)/len(noten), 2)
    return mean

def median(noten):
    """ Berechnet den Median der Liste noten auf 2 Stellen genau """
    noten.sort()
    n_noten = len(noten)
    if n_noten % 2 == 0:
        median = round((noten[int(n_noten/2)-1] + noten[int(n_noten/2)]) / 2, 2)
    else:
        median = round(noten[int((n_noten-1)/2)], 2)
    return median

def quartile(noten):
    """ Berechnet das untere Quartil auf 2 Stellen genau """
    noten.sort()
    n_noten = len(noten)
    if n_noten % 2 == 0:
        untere_noten = noten[:int(n_noten/2)]
        obere_noten = noten[int(n_noten/2):]
    else:
        untere_noten = noten[:int((n_noten-1)/2)]
        obere_noten = noten[int((n_noten+1)/2):]
    unteres_quartil = median(untere_noten)
    oberes_quartil = median(obere_noten)
    return [unteres_quartil, oberes_quartil]

def stat(noten):
    """ Berechne Mittelwert, Median, min, max, oberes und unteres Quantil """
    minimum = round(min(noten), 2)
    maximum = round(max(noten), 2)
    _median = median(noten)
    _mittelwert = mittelwert(noten)
    [unteres_quartil, oberes_quartil] = quartile(noten)
    return [minimum, unteres_quartil, _median, _mittelwert, oberes_quartil, maximum]

def note(gesamt, eins, vier, feinheit):
    """
    Berechnet die Note zu einer gegebenen Punktzahl
    """
    steigung = 3./(vier-eins)
    achsenab = 4 - steigung * vier
    notenwert = steigung * gesamt + achsenab
    if notenwert <= 1:
        return 1
    if notenwert >= 6:
        return 6
    return round(round(notenwert*feinheit, 0)/feinheit, 2)
