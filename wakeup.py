import requests
import hashlib
import json
import sys

from lxml import etree
from requests.exceptions import SSLError
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


CONFIG_FILENAME = 'wakeup.config'
config_list = []
mac_list = []
VERIFY_SSL = False


def error_exit(msg):
    print ("[error] {}".format(msg))
    sys.exit(1)


def ssl_error_exit():
    error_exit("SSL Zertifikat fehlt")


def get_sid():
    try:
        r = requests.get(URL_LOGIN, verify=VERIFY_SSL)
        t = etree.XML(r.content)
        challenge = t.xpath('//Challenge/text()')[0]
        response = '{}-{}'.format(challenge, hashlib.md5('{}-{}'.format(challenge, PASSWORD).encode('utf-16-le')).hexdigest())
        r = requests.get('{}?username={}&response={}'.format(URL_LOGIN, USERNAME, response), verify=VERIFY_SSL)
        t = etree.XML(r.content)
        return t.xpath('//SID/text()')[0]
    except SSLError:
        ssl_error_exit()


def get_uid(sid):
    try:
        payload = {'sid': sid, 'page': 'netDev'}
        r = requests.post(URL_DATA, data=payload, verify=VERIFY_SSL)
        devs = json.loads(r.content)
        for dev in devs['data']['passive']:
            if dev['mac'] == MAC:
                return dev['UID']
        for dev in devs['data']['active']:
            if dev['mac'] == MAC:
                return dev['UID']
        return ''
    except SSLError:
        ssl_error_exit()


def wake_up(sid, uid):
    try:
        payload = {'sid': sid, 'dev': uid, 'oldpage': 'net/edit_device.lua', 'btn_wake': ''}
        r = requests.post(URL_DATA, data=payload, verify=VERIFY_SSL)
        if '"pid": "netDev"' in r.content:
            return True
        else:
            return False
    except SSLError:
        ssl_error_exit()



if __name__ == '__main__':
    PASSWORD = ''
    if len(sys.argv) == 1:
        argument = 0
    else:
        argument = str(sys.argv[1])
        argument = str(argument[1:])
        argument = int(argument) - 1

    config = open(CONFIG_FILENAME, 'r')
    for line in config:
        config_line = line.strip()
        config_list.append(config_line)

    x = len(config_list)
    y = 0
    while y < x:
        if y == 0:
            HOST = config_list[y]
        elif y == 1:
            PORT = config_list[y]
        elif y == 2:
            USERNAME = config_list[y]
        elif y == 3:
            if config_list[y] == '-':
                PASSWORD = raw_input('Bitte geben Sie ein Passwort ein: ')
            else:
                PASSWORD = config_list[y]
        else:
            mac_list.append(config_list[y])
        y = y + 1
    config.close()

    SID_NOAUTH = '0000000000000000'
    URL_LOGIN = 'https://{}:{}/login_sid.lua'.format(HOST, PORT)
    URL_DATA = 'https://{}:{}/data.lua'.format(HOST, PORT)

    if argument > (len(mac_list) - 1) or argument < 0:
        print ('Falscher Parameter')
    else:
        MAC = mac_list[argument]
        print(MAC)
        sid = get_sid()
        if sid == SID_NOAUTH:
            error_exit("Login Daten falsch")
        else:
            uid = get_uid(sid)
            if uid:
                wake_up(sid, uid)
                print ("[success] wakeup gesendet {}".format(MAC))
            else:
                error_exit("Unbekannte MAC Adresse {}".format(MAC))
