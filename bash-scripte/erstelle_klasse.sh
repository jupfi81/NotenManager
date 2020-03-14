#!/bin/bash

# Erstelle die Ordnerstruktur:
# KLASSE/
# KLASSE/schriftlich/
# KLASSE/muendlich/
# KLASSE/.klasserc/


if [ -n "$(ls -A ./)" ]; then
   echo "ERROR: Ordner ist nicht leer. Klasse kann nicht erstellt werden!"
   exit 1
fi

cp ~/Projekte/NotenManager/config/klasserc klasserc
mkdir schrifltich
mkdir schrifltich/gfs
mkdir muendlich
touch list.csv

echo "Trage in die Datei liste.csv alle SuS ein."
echo "Passe die Datei klasserc nach deinen Wünschen an und trage die Klasse und das Fach ein."
