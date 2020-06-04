

from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime
from traceback import format_exc as error
from os import popen
from os import system
from os import chdir
from random import shuffle
from os.path import abspath
from sys import argv



admin=['225847803','382227482']

#это обработчик ошибок. Сообщения идут в вк админам. Всё что ниже редактировать только в крайнем случае.

chdir('/'.join(abspath(argv[0]).split('/')[:-1]))
try:
 token=open('../kpml.bot.token').read()
except:
 token=''
while 1:
 system('git pull -q --no-edit')
 try:
  exec(open('./kpml.bot.py').read())
 except:
  print('kk')
  q=str(error())
  try:
   a=open('../kpml.bot.error').read()
  except:
   a=str(time()-400)+'\x08'
  bt=a.split('\x08')[0]
  if time()-float(bt)>100 or '\x08'.join(a.split('\x08')[1:]) != q:
   try:
    for w in admin:
     sleep(1/3)
     q=loads(urlopen('https://api.vk.com/method/messages.send?random_id='+str(time()).replace('.','0')+'&user_id='+str(w)+'&v=5.101&access_token='+token,data=('message='+q).encode()).read().decode())
     if 'response' not in q:
      print(q)
   except:
    print(q,error())
   q=str(q)
   open('../kpml.bot.error','w').write(str(time())+'\x08'+q)
