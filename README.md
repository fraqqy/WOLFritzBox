# WOLFritzBox

Basiert auf Python 2.7
Die Bibliotheken:
requests
hashlib
json
sys
lxml
requests.exceptions
requests.packages.urllib3.exceptions
müssen vorhanden sein.

wakeup.config muss wie folgt aussehen:
IPADRESSE des Routers
PORT des Routers
BENUTZERNAME
PASSWORT # Falls Passwort abgefragt werden soll hier - eingeben
MACADRESSE der Rechner die geweckt werden sollen

BEISPIEL:
192.168.152.1
443
TestNutzer
testpasswort
EC:F4:BB:6E:D6:8F
E5:C2:AA:8E:E9:7B

Die Configdatei muss sich im selben Ordner befinden.
Gestartet wird über wakeup.py -Parameter, wobei Parameter für den Rechner steht der
gestartet werden soll. Beispiel: wakeup.py -2 für die 2. Macadresse.
Wird keine Parameter angegeben geht der Befehl an Defaultmacadresse Nr.1.