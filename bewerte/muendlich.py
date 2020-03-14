"""Berechnet die mündliche Note"""

import csv

with open('bewertung.csv', encoding='utf-8', mode='r') as bewertung:
    TABELLE = []
    DATA = csv.reader(bewertung, delimiter=',')
    for row in DATA:
        TABELLE.append([element.strip() for element in row])
    OUTPUT = [TABELLE[0] + ["Note"]]
    del TABELLE[0]

    for row in TABELLE:
        if len(row) > 3:
            note = 20*float(row[2]) + 20*float(row[3]) + 40*float(row[4]) + 20*float(row[5])
            note = round(note/25, 0)/4
            row = row + [note]
        OUTPUT.append(row)
    with open('note.csv', encoding='utf-8', mode='w') as safe:
        WRITER = csv.writer(safe, delimiter=',')
        for row in OUTPUT:
            WRITER.writerow(row)
