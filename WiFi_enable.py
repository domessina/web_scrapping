#!/usr/bin/python3
import hashlib
import sys
import requests
import re

router_address = 'http://192.168.0.1'
username = 'voo'
password = 'Mthwftko1'
headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'X-CSRF-TOKEN': '', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://192.168.0.1/'}
session = requests.Session() # pour garder les cookies set par les reponses routeur

# LOGIN
salt_response = session.post(router_address+'/api/v1/session/login', headers=headers, data={'username': username, 'password': 'seeksalthash'}).json()
if (salt_response['error'] != 'ok'):
  print('{}');
  sys.exit(0)

# doPbkdf2NotCoded(DoPbkdf2NotCoded(password, salt), saltWebUI)
a = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), bytes(salt_response['salt'], 'utf-8'), 1000).hex()[:32]
b = hashlib.pbkdf2_hmac('sha256', bytes(a, 'utf-8'), bytes(salt_response['saltwebui'], 'utf-8'), 1000).hex()[:32]

response = session.post(router_address+'/api/v1/session/login', headers=headers, data={'username': 'voo', 'password': b})
#print(response.json())
token = re.search("[a-f0-9]{32}", response.headers['Set-Cookie']).group()
headers['X-CSRF-TOKEN'] = token

# pour set les cookies dans les headers et autres, necessaire
response = session.get(router_address+'/api/v1/session/menu', headers=headers)

# WIFI ENABLE
session.post(router_address+'/api/v1/wifi/1,WifiEnable', headers=headers, data={
    '1[SSID]': 'MayThe4thBeWithYou',
    '1[SSIDEnable]': 'true',
    '1[SSIDAdvertisementEnabled]': 'true',
    '1[ModeEnabled]': 'WPA2-Personal',
    '1[EncryptionMethod]': 'AES',
    '1[KeyPassphrase]': 'Mexico2011',
    '1[WPSEnable]': 'false',
    'WifiEnable': 'true',
})

