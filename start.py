

from urllib.request import urlopen
from json import loads
from time import sleep
from time import time
from traceback import format_exc as error
from os import system
from os import chdir
from os.path import abspath
from sys import argv


# сюда нужно вписать id страниц вк тех, кто должен принимать сообщения об
# ошибках
admin = ['225847803', '382227482']

# это обработчик ошибок. Сообщения идут в вк админам. Всё что ниже редактировать только в крайнем случае.
# считается, что этот код рабоатет, если его не трогать. Поэтому если код работает - не трогать.
# в файле kpml.bot.py содержится основной исполняемый текст. В случае ошибки, программа ниже обработает это и сообщит об ошибке админам.
# Об ошибке , которая произошла в коде, который ниже, никто никогда не узнает, но бот перестанет работать.
# Поэтому сохраняйте этот код без изменений. Это гарант того, что в
# основном файле можно делать любые ошибки и это не смертельно.

chdir('/'.join(abspath(argv[0]).split('/')[:-1]))
try:
    token_vk = open('../kpml.bot.token_vk').read()
except BaseException:
    token_vk = ''
while True:
    system('git pull --no-edit')
    try:
        exec(open('./kpml.bot.py').read())
        q = ''
    except BaseException:
        q = str(error())
    if q:
        try:
            a = open('../kpml.bot.error').read()
        except BaseException:
            a = str(time() - 400) + '\x08'
        try:
            bt = float(a.split('\x08')[0])
        except BaseException:
            bt = time() - 400
        if time() - float(bt) > 100 or '\x08'.join(a.split('\x08')[1:]) != q:
            try:
                for w in admin:
                    sleep(1 / 3)
                    url = 'https://api.vk.com/method/messages.send?random_id='
                    url += str(time()).replace('.', '0')
                    url += '&user_id=' + \
                        str(w) + '&v=5.101&access_token=' + str(token_vk)
                    data = ('message=' + str(q)).encode()
                    q = loads(urlopen(url, data=data).read().decode())
                    if 'response' not in q:
                        print(q)
            except BaseException:
                print(q, error())
            q = str(q)
            open('../kpml.bot.error', 'w').write(str(time()) + '\x08' + q)
