

from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime
from traceback import format_exc as error
from os import popen
from random import shuffle
from os.path import abspath
from sys import argv



admin=['225847803','382227482']


#это обработчик ошибок. Сообщения идут в вк админам. Всё что ниже редактировать только в крайнем случае.
try:
 token=open('/'.join(abspath(argv[0]).split('/')[:-2])+'kpml.bot.token').read()
except:
 token=''
try:
 exec(open('/'.join(abspath(argv[0]).split('/')[:-1])+'/kpml.bot.py').read())
except:
 q=str(error())
 try:
  a=open('/'.join(abspath(argv[0]).split('/')[:-2])+'/kpml.bot.error').read()
 except:
  a=str(time()-400)+'\x08'
 bt=a.split('\x08')[0]
 if time()-float(bt)>100 or '\x08'.join(a.split('\x08')[1:]) != q:
  try:
   print('ll')
   for w in admin:
    sleep(1/3)
    q=loads(urlopen('https://api.vk.com/method/messages.send?random_id='+str(time()).replace('.','0')+'&user_id='+str(w)+'&v=5.101&access_token='+token,data=('message='+q).encode()).read().decode())
    if 'response' not in q:
     print(q)
  except:
   print(q,error())
  open('/'.join(abspath(argv[0]).split('/')[:-2])+'/kpml.bot.error','w').write(str(time())+'\x08'+q)
