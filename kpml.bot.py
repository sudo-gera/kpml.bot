

#основной код работы сервиса kpml.bot, для опнимания работы енкоторых компонентов следует почитать документацию вк, расположеннцю по адреcу https://vk.com/dev/manuals
if 'urlopen' in globals():
 pass
else:
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

path='../'
rmo='января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split()
emo='jan feb mar apr may jun jul aug sep oct nov dec'.split()
rdw='понедельник вторник среда четверг пятница суббота воскресенье'.split()
edw='mon tue wed thu fri sat sun'.split()
beg='Изменения в расписании на '
#некоторые константы


#формат клавиатуры:
#
#скнопка|скнопка|скнопка
#скнопка|скнопка|скнопка
#скнопка|скнопка|скнопка
#
#где с это цвет из набора r - красный, g - зелёный, b - синий, w - белый
#цвета определены для пк версии в светлой теме без цветоискажающих программ. На телефоне могут отличаться
#все изменяющиеся кнопки, например, включить/отключить пустые сообщения, описаны внутри функции keygen

#клавиатура по умолчанию
defkey='''
gполучить изменения
wнастройки
rсообщение об ошибке
'''

#клавиатура быстрой настройки
optkey='''
gуказать класс
gуказать время
wрасширенные настройки
rотмена
'''

#клавиатура настроек
setkey='''
bизменить кол-во оповещений в день
bизменить кол-во отслеживаемых классов
rотмена
'''

#клавиатура отмены
backey='rотмена'

#клавиатура выбора класса
#символ \u2000 похож на ' ', и служит отличителем того, ввёл пользователь время сам или нажал на кнопку
clskey='''
w11\u2000А|w10\u2000А|w9\u2000А|w8\u2000А|w7\u2000А
w11\u2000Б|w10\u2000Б|w9\u2000Б|w8\u2000Б|w7\u2000Б
w11\u2000В|w10\u2000В|w9\u2000В|w8\u2000В|w7\u2000В
w6\u2000А|w5\u2000А|w4\u2000А|w3\u2000А|w2\u2000А
w6\u2000Б|w5\u2000Б|w4\u2000Б|w3\u2000Б|w2\u2000Б
w6\u2000В|w5\u2000В|w4\u2000В|w3\u2000В|w2\u2000В
w1\u2000А|w1\u2000Б|w1\u2000В|rотмена'''

#клавиатура выбора времени
#символ \u205a похож на ':', и служит отличителем того, ввёл пользователь время сам или нажал на кнопку
timkey='''
w04\u205a00|w04\u205a30|w05\u205a00|w05\u205a30
w06\u205a00|w06\u205a30|w07\u205a00|w07\u205a30
w07\u205a00|w07\u205a30|w09\u205a00|w09\u205a30
w10\u205a00|w10\u205a30|w11\u205a00|w11\u205a30
w12\u205a00|w12\u205a30|w13\u205a00|w13\u205a30
w14\u205a00|w14\u205a30|w15\u205a00|w15\u205a30
w16\u205a00|w16\u205a30|w17\u205a00|w17\u205a30
w17\u205a00|w17\u205a30|w19\u205a00|w19\u205a30
w20\u205a00|w20\u205a30|w21\u205a00|w21\u205a30
w22\u205a00|w22\u205a30|w23\u205a00|w23\u205a30
'''
try:
 token=open(path+'kpml.bot.token').read()
except:
 token=''
#открытие файла с токеном, который нельзя встраивать в код работы бота, ибо код находится в открытом доступе
try:
 db=loads(open(path+'kpml.bot.db.json').read())
except:
 db=loads('{}')
#открытие базы данных с информацией кому что когда присылать
admin=['225847803','382227482']
#список id администрации, это люди, которые получают оповещения об ошибках. Дополнительных полномочий наличие в этом списке не даёт

#keygen###################################################################
#функция, которая преобразует клавиатуру в формат вк
def keygen_vk(id,key):
 prof='vk'
 #id - получатель, обязательный параметр, key - клавиатура, по умолчанию, defkey
 global defkey, db,d,optkey
 if key==None:
  key=defkey
 if key==setkey:
  if db[prof][id]['empty']:
   key+='\ngвключить пустые сообщения'
  else:
   key+='\nrотключить пустые сообщения'
 if key==optkey:
  if db[prof][id]['until']<time():
   key+='\ngвключить рассылку'
  else:
   key+='\nrотключить рассылку'
#до сюда генерация изменяемых кнопок клавиатуры, далее идёт преобразование, оно описано в документации
 d={'w':'default','b':'primary','r':'negative','g':'positive'}
 key='{"buttons":['+','.join(['['+','.join(['{"color":"'+d[e[0]]+'","action":{"type":"text","label":"'+e[1:]+'"}}' for e in w.split('|')]) +']' for w in key.split('\n') if w])+']}'
 key='&keyboard='+key
 return key

#vkwork###################################################################
#функция обращения к вк, идеально работает, редактировать только в крайнем случае
def api_vk(path,data=''):
 #аргумент path имеет формат method?arg1=val1&arg2=val2 где method это название метода, далее список аргуметов и их значений. Подробнее методы и значения описаны в документации
 #аргумент data может содержать ещё несколько аргуметов в том же формате, только без метода, отличие в том, что здесь нет ограничения на размер аргументов
 if path and path[-1] not in '?&':
  if '?' in path:
   path+='&'
  else:
   path+='?'
 data=data.encode()
 global token
 ret=loads(urlopen('https://api.vk.com/method/'+path+'v=5.101&access_token='+token,data=data).read().decode())
 sleep(1/3)
 return ret

#получить последние сообщения в формате [[id,сообщение,профиль],[id,сообщение,профиль],[id,сообщение,профль]]
#заметьте, что все переменные, которые начинаются с look_ воспринимаются как функции, поэтому используйте такие имена тоько для получения изменений с определённого сервиса

def look():
 ext=[]
 #vk
 t=look_vk()
 for w in t:
  w+=['vk']
 ext+=t
 #can be other service
 return ext

#функция для вк, подобные функции должны возвращать формат [[id,сообщение],[id,сообщение],[id,сообщение]]
#рекомендуется сообщение пропусаать через .lower() для упрощения взаимодействия без клавиатуры
def look_vk():
 q=api_vk('messages.getConversations?count=200&filter=unanswered&','')
 if 'response' not in q.keys():
  r=1
  try:
   if q['error']['error_code']in[10,5]:
    r=0
  except:
   pass
  if r:
   log(q)
  return []
 #в случае серьёзной ошибки при чтении сообщений, администрации придёт сообщение об этом
 q=q['response']['items']
 q=[[w['conversation']['peer']['id'],w['last_message']['text']] for w in q if w['conversation']['can_write']['allowed']]
 q=[[str(w[0])]+w[1:] for w in q]
 q=[[w[0],w[1].lower()] for w in q]
 #обработка полученных данных для возвращения в удобном виде
 return q


#настоящая функция отправки сообщений, аргументы: текст, клавиатура (по умолчанию: то, что описано по умолчанию в keygen), приниматель(если не указан и функция вызвана во время обработки входящих сообщений, получателем будет тот, чьё сообение обрабатывается
def send(text,key=None,id=None,prof=None):
 global q
 if prof==None:
  prof=q[2]
 if prof=='vk':
  return send_vk(text,key,id)

#функция отправки сообщений в вк, аргументы: текст, клавиатура (по умолчанию: то, что описано по умолчанию в keygen), приниматель(если не указан и функция вызвана во время обработки входящих сообщений, получателем будет тот, чьё сообение обрабатывается
def send_vk(text,key=None,id=None):
  text=str(text)
  global q
  if id==None:
   id=q[0]
  #если сообщение большое, его стоит порезать на части
  while len(text)>2048:
   send_vk(text[:2048],key,id)
   text=text[2048:]
  key=keygen_vk(id,key)
  #отправка сообщений
  if 1:
   text=str(text+key)
#отправка сообщения
   qq=api_vk('messages.send?random_id='+str(time()).replace('.','')+'&user_id='+str(id)+'&','message='+text)
#в случае серьёзной ошибки оповестить админа
   r=1
   if list(qq.keys())!=['response']:
    try:
     if qq['error']['error_code'] in [901,10,5]:
      r=0
    except:
     pass
    if r:
     log(qq)

#отправка сообщения администрации
def log(q=None):
 for w in admin:
  send(str(q),defkey,w,'vk')

#dates########################################################
#формат даты, который испоьзуется вовсей пограмме: день (число, как есть) месяц (число, нумеруются с 0, то есть от 0 до 11) год (число, как есть) день недели (не обязательно, число, нумеруются с 0, то есть от 0 до 6)

#по дню определяет следующий
def next(q,w,e,dw=None):
 q,w,e=int(q),int(w),int(e)
 if dw!=None:
  dw=int(dw)
 if e%4==0 and e%100 or e%400==0:
  l=[31,29,31,30,31,30,31,31,30,31,30,31]
 else:
  l=[31,28,31,30,31,30,31,31,30,31,30,31]
 if q+1>l[w]:
  if w+1==12:
   q=1
   w=0
   e+=1
  else:
   q=1
   w+=1
 else:
  q+=1
 if dw!=None:
  return [q,w,e,(dw+1)%7]
 return [q,w,e]

#узнать, какой день сегодня
def today():
 t=asctime()
 t=t.split()[0:5]
 dw=t[0].lower()
 dw=edw.index(dw)
 t=t[1:]
 t[0]=t[0].lower()
 t[0]=emo.index(t[0])
 q,w,e=int(t[1]),int(t[0]),int(t[3])
 return [q,w,e,dw]

#kpml######################################################################

#открытие и базовая обработка страницы
def parse():
 #предотвращение повторного открытия страницы, если она была открыта не давно
 try:
  q=open(path+'kpml.bot.html').read()
 except:
  q=str(time()-400)+'\x01'
 bt=q.split('\x01',1)[0]
 oq=q.split('\x01',1)[1]
 if time()-float(bt)>300:
  try:
   q=urlopen('http://kpml.ru/pages/raspisanie/izmeneniya-v-raspisanii').read().decode()
   if q!=oq:
    log('site changed')
   open(path+'kpml.bot.html','w').write(str(time())+'\x01'+q)
  except:
   log(error())
   q=oq
 else:
  q=oq
 #здесь старница открыта, далее базовая обработка
 q=q.replace('<','\x01\x02').replace('>','\x01').replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>').replace('&amp;','&').replace('&quot;','"').replace('&apos;',"'")
 q=q[:q.index('«Кировский')]
 q=q[q.index('\x01\x02body'):]
 q=q.replace('\x01\x02br ','\n\x01\x02br ')
 q=q.replace('\x01\x02br/\x01','\n')
 q=q.replace('\x01\x02br ','\n\x01\x02br ')
 q=q.replace('\x01\x02/p\x01','\x01\x02/p\x01\n')
 q=q.split('\x01')
 ''' q=[w if len(w) < 2 or w[0] != '\x02' else ('\x03'+w[2:] if w[:2] in ['\x02/','\x02!'] else ('\x04'+w[1:-1]+'\x04' if w[-1] == '/' else w))  for w in q]'''
 q=[w for w in q if w and( w[0] != '\x02' or w[0] == '\x02' and w[-1] == '/')]
 q=['\x01'+w+'\x01' if w[0] == '\x02' else w for w in q]
 q=[w for w in q if w]
 q=''.join(q)
 q=q.strip()
 q=q.split(beg)[1:]
 return q


#отправка всех изменений при нажатии кнопки "получить изменения"
def out():
 q=parse()
 if ''.join(q).strip():
  t='<===========>\n'+beg
  q=t+t.join(q)
  return q
 else:
  return 'изменений нет'

#выделение изменений, относящихся к нужной дате
def repa(day,mon):
 q=parse()
 q=[w.split(rmo[mon]) for w in q if rmo[mon] in w]
 q=[[w[0],rmo[mon].join(w[1:])] for w in q]
 for w in q:
  for e in w[0]:
   if e not in '1234567890-':
    w[0]=w[0].replace(e,'\0')
  w[0]=w[0].split('\0')
  w[0]=[e for e in w[0] if e]
  w[0]=[e.replace('-','\0-\0') for e in w[0]]
  w[0]='\0'.join(w[0])
  w[0]=w[0].split('\0')
  w[0]=[w[0][e] if e==0 or w[0][e-1]!='-' or w[0][e]!='-' else '' for e in range(len(w[0]))]
  w[0]=[e for e in w[0] if e]
  for e in range(1,len(w[0])-1):
   if w[0][e]=='-':
    w[0][e]='\0'.join(list(map(str,range(int(w[0][e-1]),int(w[0][e+1])))))
  if w[0][0]=='-':
   w[0]=w[0][1:]
  if w[0][-1]=='-':
   w[0]=w[0][:-1]
  w[0]='\0'.join(w[0])
  w[0]=w[0].split('\0')
  w[0]=[int(e) for e in w[0] if e]
  if day not in w[0]:
   w[1]=''
 q=[w[1] for w in q if w[1]]
 q='\n'.join(q)
 e=q
 q=q.strip()
 if q[:4]==str(today()[2]):
  q=q[4:]
  q=q.strip()
  if q[:4].lower()=='года':
   q=q[4:]
   e=e[e.index(q):]
 return e

#функция обработки каждого прикреплённого материала к изменениям в расписании
def uft(q,w,e):
  ee=e
  if q[:len(w)+2]=='\x02'+w+' ':
   t=q.split()
   t=[[e[len(ee)+1:]] for e in t if e[:len(ee)+1]==ee+'=']
   for e in t:
    if e[0][0]=='"':
     e[0]=e[0][1:]
    if e[0][-1]=='"':
     e[0]=e[0][:-1]
    if e[0][0]=='/':
     e[0]='http://kpml.ru'+e[0]
    if e[0][:7]!='http://' and e[0][:8]!='https://':
     e[0]='http://kpml.ru/pages/raspisanie/izmeneniya-v-raspisanii/'+e[0]
   t=[e[0] for e in t]
   return '\n'.join(t)
  else:
   return q

#функция обработки прикреплённых материалов
def attach(q):
 q=q.split('\x01')
 q=[[w] for w in q if w]
 for w in q:
  w[0]=uft(w[0],'img','src')
  w[0]=uft(w[0],'a','href')
 q=[w[0] for w in q if w and w[0][0]!='\x02']
 q=[w.strip() for w in q]
 q='\n'.join(q)
 return q

#вспомогательная функция для проверки наличия данного класса среди нескольких, если фрагмент ориентирован на несоклько классов
def isin(q,c):
 q=q.replace(' классы ',' ')
 q=q.strip()
 if q=='':
  return 0
 if ',' in q:
  return sum([isin(w,c) for w in q.split(',')])
 if ' и ' in q:
  return sum([isin(w,c) for w in q.split(' и ')])
 if q==c:
  return 1
 if q[-2:] == '-е':
  q=q[:-2]
  if [w for w in q if w not in '1234567890-']:
   return 0
  q=list(map(int,q.split('-')))
  for w in c:
   if not w.isdigit():
    c=c.replace(w,'')
  c=int(c)
  if min(q)<=c<=max(q):
   return 1
 return 0

#выделение изменений по нужному классу
def get(day,mon,clas):
 q=repa(int(day),int(mon))
 q=q.split('\n')
 q=[w.split(' - ') for w in q]
 q=[[w[0],' - '.join(w[1:])] for w in q]
 q=[w[1] for w in q if isin(w[0],clas)]
 q='\n'.join(q)
 return q


#функция чтения изменений, оболочка всех предыдущих
def view(day=None,mon=None,id=None,prof=None):
 if id==None and prof==None and day != None and mon != None:
  global q
  id=q[0]
  prof=q[2]
 try:
  if day==None and mon==None:
   parsed=out()
  else:
   parsed=''
   for w in db[prof][id]['class']:
    tj=get(day,mon,w)
    if tj:
     parsed+=w+': '+tj+'\n'
  parsed=attach(parsed)
  return parsed
 except:
  log(error())
  return '''При чтении изменений произошла ошибка, о которой админ бота уже оповещён.
Для получения изменений в расписании перейдите по ссылке http://kpml.ru/pages/raspisanie/izmeneniya-v-raspisanii'''

#обработчик генерации текста автоматического оповещения
def work(id,prof,empty=0):
 q,w,e,dw=today()
 td=view(q,w,id,prof)
 if td or empty==0:
  td='Изменения на сегодня, '+str(q)+' '+rmo[int(w)]+' '+rdw[dw]+':\n'+ td
 r,t,y,dw=next(q,w,e,dw)
 tn=view(r,t,id,prof)
 if tn or empty==0:
  tn='Изменения на завтра, '+str(r)+' '+rmo[int(t)]+' '+rdw[dw]+':\n'+tn
 if int(time())%(24*3600)<12*3600 or int(time())%(24*3600)>21*3600:
  if td.split()+tn.split():
   q=td+'<=====================>'+tn
  else:
   q=''
 else:
  q=tn
# q=[w.strip() for w in q if w]
# q='\n'.join(q)
 return q

#inputparse######################################################33
#тут представлены функции, проверяющие, верно ли, что строка является каким-либо объектом

#классом
def iscl(q):
 q=''.join(q.split())
 w=0
 if q.isdigit():
  return 0
 while w<len(q) and q[w] in '1234567890':
  w+=1
 d=w
 if d==0:
  return 0
 while w<len(q) and q[w] in 'йцукенгшщзфывапролхэюбьтимсчяёъдж':
  w+=1
 if w==len(q):
  return [q[:d],q[d:]]
 return 0

#датой
def isdt(q):
 ot=q
 if '.' not in q:
  return 0
 w=q.split('.')[0]
 if not w.isdigit():
  return 0
 q=q[len(w)+1:]
 if ', ' not in q:
  return 0
 w=q.split(', ')[0]
 if not w.isdigit():
  return 0
 q=q[len(w)+2:]
 if q in rdw:
  ot=ot.split(',')[0].split('.')
  ot[1]=str(int(ot[1])-1)
  return ot
 return 0

#временем
def istm(q):
 q=''.join(q.split())
 if ':' not in q:
  return 0
 w=q.split(':')[0]
 if not w.isdigit():
  return 0
 q=q[len(w)+1:]
 if q.isdigit():
  return 1
 return 0

#классом, введённым с клавиатуры
def iskcl(q):
 q=q.strip()
 if q.count('\u2000')==1 and iscl(q.replace('\u2000','')):
  return 1
 return 0

#временем, ввудённым с клавиатуры
def isktm(q):
 q=q.strip()
 if q.count('\u205a')==1 and istm(q.replace('\u205a',':')):
  return 1
 return 0

#userwork######################################################
definf={'until':time()+2**29,'class':[],'time':[],'ls':0,'empty':1,'lm':today()[2],'ban':0}
#список полей, которые должны содержаться в профиле каждого пользователя, а так же значения полей по умолчанию

if 'vk' not in db:
 tdb=dict(db)
 db=dict()
 db['vk']=tdb


#весь дальнейший код выполняется сам, поэтому его нужно заключить в конструкцию try except, для возможности оповещения админов в случае ошибки
if 1:
 tn=time()
 wai=[]
 #пройти по списку пользователей и обновить информацию профиля
 for cdb in db:
  #cdb - текущий профиль (например, вк)
  for w in [w for w in db[cdb] if w.isdigit()]:
   for e in definf:
    if e not in db[cdb][w]:
     db[cdb][w][e]=definf[e]
   if tn-db[cdb][w]['until']>2**25:
    delete(db[cdb][w])
   if today()[2]-db[cdb][w]['lm']>0 and today()[1]>5:
    f=[]
    for e in db[cdb][w]['class']:
     i=''
     while e and e[0].isdigit():
      i+=e[0]
      e=e[1:]
     i=str(int(i)+1)
     e=i+e
     f+=[e]
    send('теперь вы подписаны классы: \n'+' '.join(f)+'\nраньше вы были подписаны на классы: \n'+' '.join(db[cdb][w]['class'])+'\nЕсли вы завершили обучение в лицее, перейдите в настройки и отключите оповещения',defkey,w,cdb)
    db[cdb][w]['class']=f[:]
    db[cdb][w]['lm']=today()[2]
#mainloop#########################################################
#бот ходит по этому циклу, пока не получит соообщения
 while wai==[]:
  tn=int(time())
  for cdb in db:
   for w in db[cdb].keys():
    if w.isdigit() and 'time' in db[cdb][w] and 'until' in db[cdb][w].keys() and tn<db[cdb][w]['until']:
     for e in db[cdb][w]['time']:
      if 0 < tn % (24*3600) - int(e) < 300 and tn - db[cdb][w]['ls'] >= 300:
       worked=work(w,cdb,db[cdb][w]['empty'])
       if worked:
        if db[cdb]['until']-tn<2**19:
         worked+='\nобратите внимание, что вы были зарегистрированы очень давно, по этой причине через неделю вы будете отключены от рассылки. Если вы хотите продолжать получать уведомления, то зайдите в настройки и отключите, а затем включите рассылку'
        send(worked,defkey,w,cdb)
        db[cdb][w]['ls']=int(time())
  wai=look()
#gotmess###########################################################
#сообщене получено, сначала нужно проверить верность профиля пользователя
 shuffle(wai)
 for q in wai:
  print(q)
  added=0
  if q[0] not in db[q[2]].keys():
   db[q[2]][q[0]]=dict()
   added=1
  for w in definf:
   if w not in db[q[2]][q[0]]:
    db[q[2]][q[0]][w]=definf[w]
  if db[q[2]][q[0]]['ban']>0:
   db[q[2]][q[0]]['ban']-=1
   continue
#logic###############################################################
#теперь можно приступать к пониманию, чего хотел пользователь
  if q[1] == '':
   send('текстом, пожалуйста')
  elif q[1] == 'json':
   send(str(db).replace("'",'"'))
  elif q[1] == 'git':
   t=popen('git show').read()
   t=t.split('\n\n')[0]
   send(t)
  elif q[1] == 'len':
   send(len(db[q[2]].keys()))
  elif q[1] == 'sub':
   send(len([w for w in db[q[2]] if 'time' in db[q[2]][w] and db[q[2]][w]['time']]))
  elif q[1] == '.':
   send('&#13;'.join('''
 _______
< hello >
 -------
         \     ,-.      .-,
          \    |-.\ __ /.-|
           \   \  `    `  /
                /_     _ \
              <  _`q  p _  >
              <.._=/  \=_. >
                 {`\()/`}`\
                 {      }  \
                 |{    }    \
                 \ '--'   .- \
                 |-      /    \
                 | | | | |     ;
                 | | |.;.,..__ |
               .-"";`         `|
              /    |           /
              `-../____,..---'`'''))
  elif q[1] == 'gl':
   send(globals())
  elif q[1] == 'xg':
   send('\n'.join(['vk.com/id'+w+' '+str(db[q[2]][w]) for w in db[q[2]].keys()]))
  elif q[1] == 'sw':
   send('\n'.join(['vk.com/id'+w+' class: '+str(db[q[2]][w]['class'] if 'class' in db[q[2]][w] else 0)+' time: '+str([str(e//3600+3)+':'+str(e//60%60) for e in (db[q[2]][w]['time'] if 'time' in db[q[2]][w] else [])]) for w in db[q[2]].keys()]))
  elif q[1] == 'отмена':
   send('отменено')
  elif q[1] in ['получить изменения','сейчас']:
   tmp=view()
   tmp=tmp
   send(tmp)
  elif q[1] == 'отключить пустые сообщения' or q[1] == 'пусто' and db[q[2]][q[0]]['empty']==0:
   db[q[2]][q[0]]['empty']=1
   send('теперь вам не будут приходить автоматические оповещения, если они не содержат изменений. Обратите внимание, что иногда вам всё же будут приходить пустые оповещения, сообщайте о таких ошибках и они будут исправлены.')
  elif q[1] == 'включить пустые сообщения' or q[1] == 'пусто' and db[q[2]][q[0]]['empty']==1:
   db[q[2]][q[0]]['empty']=0
   send('теперь вам будут приходить автоматические оповещения строго по расписанию, даже если в них ничего нет.')
  elif q[1] == 'сообщение об ошибке':
   send('напишите сообщение об ошибке, начните его с символа $',backey)
  elif q[1][0] == '$':
   log('сообщение об ошибке\nавтор vk.com/id'+q[0]+'\n'+q[1][1:])
   send('спасибо за обращение. Именно благодаря вам этот сервис скоро станет лучше. сообщение отправлено администрации, с вами скоро свяжутся')
  elif q[1] == 'lookall':
   send(work(q[0],q[2]))
  elif isdt(q[1]):
   tmp=isdt(q[1])
   tmp=view(tmp[0],tmp[1],q[0],q[2])
   tmp='\n'.join(tmp)
   tmp='Изменения на '+q[1]+':\n'+tmp
   send(tmp)
  elif iskcl(q[1]):
   q[1]=q[1].replace('\u2000','')
   q[1]=q[1].upper()
   db[q[2]][q[0]]['class']=[q[1]]
   send('теперь вы подписаны на класс '+q[1])
  elif isktm(q[1]):
   q[1]=q[1].replace('\u205a',':')
   ms=q[1]
   q[1]=q[1].split(':')
   q[1]=(int(q[1][0])-3)%24*3600+int(q[1][1])%60*60
   db[q[2]][q[0]]['time']=[q[1]]
   send('теперь вы будете узнавать об изменениях в '+ms)
  elif istm(q[1]):
   ms=q[1]
   q[1]=q[1].split(':')
   q[1]=(int(q[1][0])-3)%24*3600+int(q[1][1])%60*60
   if q[1] in db[q[2]][q[0]]['time']:
    db[q[2]][q[0]]['time']=[w for w in db[q[2]][q[0]]['time'] if w != q[1]]
    t='количество оповещений в день уменьшено временем '+ms
   else:
    if len(db[q[2]][q[0]]['time']) >= 256:
     t='вы не можете получать более чем 256 уведомлений в сутки'
    else:
     db[q[2]][q[0]]['time']+=[q[1]]
     t='количество оповещений в день увеличено временем '+ms
   send(t+'. Обратие внимание, что оповещение не содержит изменений, опубликованных позднее, чем оно пришло')
  elif q[1] in ['изменить кол-во оповещений в день','время']:
   ts=db[q[2]][q[0]]['time'][:]
   ts=[str((w//3600+3)%24)+':'+str(w%3600//60) for w in ts]
   lts=len(ts)
   ts='\n'.join(ts)
   if ts:
    ts='Сейчас вам приходят оповещения '+str(lts)+' раз в день по этому расписанию:\n'+ts+'''
введите интересующее вас время,
если оно в расписании, то оно будет убрано от туда,
если его там нет, то добавлено.
Бот не способен оповещать чаще, чем раз в 5 минут
'''
   else:
    ts='Сейчас вам не приходят оповещения, введите время для оповещения'
   send(ts,backey)
  elif q[1]=='указать класс':
   send('выберите свой класс',clskey)
  elif q[1]=='указать время':
   send('выберите, когда вас оповещать. Обратите внимание, что оповещение не содержит измений, опубликованных позднее. Любое время, которого здесь нет можно указать через расширенные настройки',timkey)
  elif q[1]=='настройки':
   send('панель настроек поможет настроить бота под себя',optkey)
  elif q[1]=='расширенные настройки':
   send('панель настроек поможет более точно настроить бота под себя',setkey)
  elif q[1]=='help':
   send('''
чтобы изменить кол-во отслеживаемых классов напиши слово класс
чтобы изменить кол-во оповещений в день напиши слово время
чтобы получить изменения прямо сейчас напиши слово сейчас
чтобы включить или отключить пустые сообщения напиши слово пусто
чтобы сообщить об ошибке напиши сообщение, начав его с символа $
  ''')
  elif iscl(q[1]):
   q[1]=q[1].upper()
   ms=q[1]
   if q[1] in db[q[2]][q[0]]['class']:
    db[q[2]][q[0]]['class']=[w for w in db[q[2]][q[0]]['class'] if w != q[1]]
    t='количество отслеживаемых классов уменьшено классом '+ms+'.'
   else:
    if len(db[q[2]][q[0]]['class'])>=256:
     t='вы не можете подписаться более чем на 256 классов'
    elif len(q[1]) > 16:
     t='длина класса не может превышать 16 символов'
    else:
     db[q[2]][q[0]]['class']+=[q[1]]
     t='количество отслеживаемых классов увеличено классом  '+ms+'.'
   send(t)
  elif q[1] in ['изменить кол-во отслеживаемых классов','класс']:
   ts=db[q[2]][q[0]]['class'][:]
   lts=len(ts)
   ts='\n'.join(ts)
   if ts:
    send('Сейчас вы подписаны на '+str(lts)+' классов:\n'+ts+'\n Введите класс, который вас интересует, если вы подписаны на него, то будете отписаны, если подписаны не были, то будете подписаны. Вводить класс следует указав номер и букву без пробела, если в параллели один класс, то это класс "а". Используйте только русские буквы, а не их латинские аналоги',backey)
   else:
    send('Сейчас вы не подписаны ни на один из классов. Введите класс, на который хотите подписаться.  Вводить класс следует узазав номер и букву без пробела, если в параллели один класс, то это класс "а". Используйте только русские буквы, а не их латинские аналоги',backey)
  elif q[1]=='отключить рассылку':
   db[q[2]][q[0]]['until']=time()
   send('рассылка отключена, однако, вы всё ещё можете получать изменения по нажатии на кнопку. Если вы не включите её в течение года, информация о ваших настройках бота будет удаена')
  elif q[1]=='включить рассылку':
   db[q[2]][q[0]]['until']=time()+2**29
   send('рассылка включена')
  else:
   send('''Привет, это бот-оповещатель об изменениях в расписании.
Бота надо настроить, чтобы он знал, в каком вы классе и во сколько вас оповещать.
Для этого укажи, сколько раз в день тебе сообщать об изменениях, и за изменениями для каких классов ты хочешь следить.
Клавиатура поможет тебе в этом.
если твоё приложение не поддерживает работу с клавиатурами, то напиши мне команду help
''')
#запись базы данных после успешного завершения программы
open(path+'kpml.bot.db.json','w').write(dumps(db))


