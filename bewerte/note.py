""" Modul, dass die Gesamtnote fuer einen Schueler bestimmt """

import configparser
from statistics import mean

def endnote(schueler, klasserc):
    """ Berechnet die Gesamtnote (klappt nur, wenn es nur schriftlich un mündlich gibt"""
    # Schritt 1: loesche in allen Listen die leeren Noten
    for art in schueler:
        noten = []
        for val in schueler[art]:
            if val:
                noten.append(val)
        schueler[art] = noten

    config = configparser.ConfigParser()
    config.read('~/Projekte/KlassenManager/config/defaultrc')
    config.read(klasserc)
    noten = dict()
    wichtungs_summe = dict()
    for kategorie in config['basics']['Kategorien'].split(','):
        noten.update({kategorie.strip() : []})
        wichtungs_summe.update({kategorie.strip() : 0})
    for art in schueler:
        if schueler[art]:
            if config['bewertungsart'][art] == "e":
                noten[config['arten'][art]] += [float(config['wichtung'][art])
                                                * val for val in schueler[art]]
                wichtungs_summe[config['arten'][art]] += (float(config['wichtung'][art])
                                                          * len(schueler[art]))
            elif config['bewertungsart'][art] == 'g':
                noten[config['arten'][art]].append(float(config['wichtung'][art])
                                                   * mean(schueler[art]))
                wichtungs_summe[config['arten'][art]] += float(config['wichtung'][art])

    if wichtungs_summe['muendlich']:
        muendlich = sum(noten['muendlich']) / wichtungs_summe['muendlich']
    else:
        print("note:", schueler)
        muendlich = 100
        print("Etwas mit der Wichtung dern muendlichen Noten stimmt nicht")
    if sum(noten['schriftlich']) == 0:
        schriftlich = 0
        wichtungs_summe['schriftlich'] = 0
        note = muendlich
    else:
        schriftlich = sum(noten['schriftlich']) / wichtungs_summe['schriftlich']
        note = ((float(config['wichtung']['schriftlich']) * schriftlich
                 + float(config['wichtung']['muendlich']) * muendlich) /
                (float(config['wichtung']['schriftlich']) + float(config['wichtung']['muendlich'])))
    return round(note, 2)
