# Wetterstation Client-Skript
Dieses Skript läuft auf den einzelnen Wetterstationen.
Dabei werden die Daten von den Sensoren ausgelesen und auf dem Server hochgeladen.

## Installation
### Herunterladen des Repositories
Zur Installation ist es zuerst erforderlich den Source Code des Servers auf den eigenen Rechner oder die virtuelle Machine herunterzuladen.

Dazu wird das verteilte Versionsverwaltung-Programm [Git](https://de.wikipedia.org/wiki/Git) benutzt. Dieses lässt sich für Windows unter https://git-scm.com/downloads installieren und unter Linux, falls nicht vorinstalliert, mit dem integrierten Paket-Manager (z.B. bei Debian/Ubuntu `sudo apt-get install git`).

Das Repository kann man dann mit `git clone https://github.com/lmg-anrath/weatherstation-client.git wetter` in das Verzeichnis "wetter" clonen.

### Installieren der Python Requirements
Zur Verwendung wird Python 3 verwendet. Dieses ist standardmäßig auf einem Raspberry Pi vorinstalliert, daher wird in dieser Anleitung nicht mehr weiter darauf eingegangen.

Die benötigten Pakete werden mit dem Python Package-Manager PIP installiert: `pip3 install -r requirements.txt`.

## Einrichtung
Damit der Wetterstations-Client funktionstüchtig agieren kann, muss die `config.example.json` kopiert oder unbenannt werden in `config.json`.
Dort wird die Station-ID und der Access-Token vom Server sowie die Server-URL eingetragen.

## Verwendung
Das Skript wird mit `python3 index.py` ausgeführt. Dadurch werden die aktuellen Sensor-Daten auf den Server hochgeladen.

Dies kann mit Crontab automatisiert werden: https://bktapan.medium.com/how-to-schedule-a-python-script-crontab-with-virtualenv-96bd6fcaa56a
