

from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime
from traceback import format_exc as fo
from os import popen
from random import shuffle


#формат клавиатуры:
#
#скнопка|скнопка|скнопка
#скнопка|скнопка|скнопка
#скнопка|скнопка|скнопка
#
#где с это цвет из набора r - красный, g - зелёный, b - синий, w - белый

defkey='''
wполучить изменения
bизменить кол-во оповещений в день
bизменить кол-во отслеживаемых классов
rсообщение об ошибке
'''
#клавиатура по умолчанию
backey='rотмена'
#клавиатура отмены

try:
 token=open('../kpml.bot.token').read()
except:
 token=''
#открытие файла с токеном, который нельзя встраивать в код работы бота, ибо код находится в открытом доступе
try:
 db=loads(open('../kpml.bot.db.json').read())
except:
 db=loads('{}')
#открытие базы данных с информацией кому что когда присылать
admin=['225847803','382227482']
#admin=['225847803']
#список id администрации, это люди, которые получают оповещения об ошибках. Дополнительных полномочий наличие в этом списке не даёт

path='..'
rmo='января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split()
emo='jan feb mar apr may jun jul aug sep oct nov dec'.split()
rdw='понедельник вторник среда четверг пятница суббота воскресенье'.split()
edw='mon tue wed thu fri sat sun'.split()
beg='Изменения в расписании на '
d={'w':'default','b':'primary','r':'negative','g':'positive'}
#некоторые константы

#keygen###################################################################
#функция, которая преобразует клавиатуру в формат вк
def keygen(id,key):
 global defkey, db,d
 if key==None:
  key=defkey
 if key==defkey:
  if db[id]['empty']:
   key+='g×включить пустые сообщения'
  else:
   key+='r×отключить пустые сообщения'
 key='{"buttons":['+','.join(['['+','.join(['{"color":"'+d[e[0]]+'","action":{"type":"text","label":"'+e[1:]+'"}}' for e in w.split('|')]) +']' for w in key.split('\n') if w])+']}'
 key='&keyboard='+key
 return key

#vkwork###################################################################
#функция обращения к вк, идеально работает, редактировать только в крайнем случае
def api(path,data=''):
 sleep(1/3)
 if path and path[-1] not in '?&':
  if '?' in path:
   path+='&'
  else:
   path+='?'
 data=data.encode()
 global token
 ret= loads(urlopen('https://api.vk.com/method/'+path+'v=5.101&access_token='+token,data=data).read().decode())
 return ret
 print(asctime())

#получить последние сообщения в формате [[id,сообщение],[id,сообщение],[id,сообщение]]
def look(a=0):
 q=api('messages.getConversations?count=200&filter=unread&','')
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
 q=q['response']['items']
 q=[[w['conversation']['peer']['id'],w['last_message']['text'],w] for w in q if w['conversation']['can_write']['allowed']]
 if a==0:
  q=[w[:2] for w in q]
 q=[[str(w[0])]+w[1:] for w in q]
 q=[[w[0],w[1].lower(),w[1]] for w in q]
 return q

def send(text,key=None,id=None):
  text=str(text)
  global q
  if id==None:
   id=q[0]
  while len(text)>4096:
   send(text[:4096],key,id)
   text=text[4096:]
  key=keygen(id,key)
  qq=api('messages.send?random_id='+str(time()).replace('.','')+'&user_id='+str(id)+'&','message='+text+key)
  print(qq)
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
def log(q):
 q=str(q)
 try:
  a=open(path+'kpml.bot.error').read()
 except:
  a=str(time()-400)+'\x08'
 bt=a.split('\x08')[0]
 if time()-float(bt)>300 or '\x08'.join(a.split('\x08')[1:]) != q:
  for w in admin:
   send(str(q),defkey,w)
  open(path+'kpml.bot.error','w').write(str(time())+'\x08'+q)

#dates########################################################
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

def parse():
 try:
  q=open('../kpml.bot.html').read()
 except:
  q=str(time()-400)+'\x01'
 bt=q.split('\x01')[0]
 if time()-float(bt)>300:
  q=urlopen('http://kpml.ru/pages/raspisanie/izmeneniya-v-raspisanii').read().decode()
  open('../kpml.bot.html','w').write(str(time())+'\x01'+q)
 else:
  q=q.split('\x01')[1]
 #opened
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


def out():
 q=parse()
 t='<===========>\n'+beg
 q=t+t.join(q)
 return q

def repa(day,mon):
 q=parse()
 q=[w.split(rmo[mon]) for w in q if rmo[mon] in w]
 q=[[w[0],rmo[mon].join(w[1:])] for w in q]
 for w in q:
  for e in w[0]:
   if not e.isdigit():
    w[0]=w[0].replace(e,'\0')
  w[0]=w[0].split('\0')
  w[0]=[int(e) for e in w[0] if e]
  if day not in w[0]:
   w[1]=''
 q=[w[1] for w in q if w[1]]
 q='\n'.join(q)
 return q


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

def attach(q):
 q=q.split('\x01')
 q=[[w] for w in q if w]
 for w in q:
  w[0]=uft(w[0],'img','src')
  w[0]=uft(w[0],'a','href')
 q=[w[0] for w in q if w and w[0][0]!='\x02']
 return q

def get(day,mon,clas):
 text=repa(int(day),int(mon))
 text='\n'.join([w for w in text.split('\n') if clas in w])
 return text


def view(day=None,mon=None,id=None):
 try:
  if day==None and mon==None and id==None:
   parsed=out()
  else:
   parsed=repa(day,mon)
   if parsed:
    parsed='Происходит тестирование алгоритма, находящего изменения для вашего класса. Предлагаем вам помогать находить ошибки. Сейчас вы подписаны на классы: '+' '.join(db[id]['class'])+'\nИзменения по всем классам:\n'+parsed+'\n<=========================>\n<===================>изменения по вашим классам\n'
    for w in db[id]['class']:
     parsed+=get(day,mon,w)+'\n'
  parsed=attach(parsed)
  if len(parsed)==1 and parsed[0].lower()=='изменений нет':
   parsed=[]
  return parsed
 except:
  log(fo())
  return ['''При чтении изменений произошла ошибка, о которой админ бота уже оповещён.
Для получения изменений в расписании перейдите по ссылке http://kpml.ru/pages/raspisanie/izmeneniya-v-raspisanii''']


def work(id,empty=0):
 q,w,e,dw=today()
 td=view(q,w,id)
 if td or empty==0:
  td=['Изменения на сегодня, '+str(q)+' '+rmo[int(w)]+' '+rdw[dw]+':']+ td
 r,t,y,dw=next(q,w,e,dw)
 tn=view(r,t,id)
 if tn or empty==0:
  tn=['Изменения на завтра, '+str(r)+' '+rmo[int(t)]+' '+rdw[dw]+':']+tn
 if int(time())%(24*3600)<12*3600 or int(time())%(24*3600)>21*3600:
  if td+tn:
   q=td+['<=====================>']+tn
  else:
   q=[]
 else:
  q=tn
 q=[w.strip() for w in q if w]
 q='\n'.join(q)
 return q

#inputparse######################################################33
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


try:
 wai=[]
#mainloop#########################################################
 while wai==[]:
  tn=int(time())
  for w in db.keys():
   if w.isdigit():
    for e in db[w]['time']:
     if 0 < tn % (24*3600) - int(e) < 300 and tn - db[w]['ls'] >= 300:
      worked=work(w,db[w]['empty'])
      if worked:
       send(worked,defkey,w)
       db[w]['ls']=int(time())
  wai=look()
  shuffle(wai)
#gotmess###########################################################
 for q in wai:
  added=0
  if q[0] not in db.keys():
   db[q]=dict()
   added=1
  if 'ls' not in db[w].keys():
   db[w]['ls']=0
  if 'time' not in db[w].keys():
   db[w]['time']=[]
  if 'class' not in db[w].keys():
   db[w]['class']=[]
  if 'empty' not in db[w].keys():
   db[w]['empty']=0
#logic###############################################################
  if q[1] == '':
   send('текстом, пожалуйста')
  elif q[1] == 'json':
   send(str(db).replace("'",'"'))
  elif q[1] == 'git':
   t=popen('git show').read()
   t=t.split('\n\n')[0]
   send(t)
  elif q[1] == 'len':
   send(len(db.keys()))
  elif q[1] == 'xg':
   send('\n'.join(['vk.com/id'+w+' '+str(db[w]) for w in db.keys()]))
  elif q[1] == 'отмена':
   send('отменено')
  elif q[1] in ['получить изменения','сейчас']:
   tmp=view()
   tmp='\n'.join(tmp)
   send(tmp)
  elif q[1] == 'отключить пустые сообщения' or q[1] == 'пусто' and db[q[0]]['empty']==0:
   db[q[0]]['empty']=1
   send('теперь вам не будут приходить автоматические оповещения, если они не содержат изменений. Обратите внимание, что иногда вам всё же будут приходить пустые оповещения, сообщайте о таких ошибках и они будут исправлены.')
  elif q[1] == 'включить пустые сообщения' or q[1] == 'пусто' and db[q[0]]['empty']==1:
   db[q[0]]['empty']=0
   send('теперь вам будут приходить автоматические оповещения строго по расписанию, даже если в них ничего нет.')
  elif q[1] == 'сообщение об ошибке':
   send('напишите сообщение об ошибке, начните его с символа $',backey)
  elif q[1][0] == '$':
   log('сообщение об ошибке\nавтор vk.com/id'+q[0]+'\n'+q[1][1:])
   send('сообщение отправлено администрации, с вами скоро свяжутся')
  elif q[1] == 'lookall':
   send(work(q[0]))
  elif isdt(q[1]):
   tmp=isdt(q[1])
   tmp=view(tmp[0],tmp[1])
   tmp='\n'.join(tmp)
   tmp='Изменения на '+q[1]+':\n'+tmp
   send(tmp)
  elif istm(q[1]):
   ms=q[1]
   q[1]=q[1].split(':')
   q[1]=(int(q[1][0])-3)%24*3600+int(q[1][1])%60*60
   if q[1] in db[q[0]]['time']:
    db[q[0]]['time']=[w for w in db[q[0]]['time'] if w != q[1]]
    t='количество оповещений в день уменьшено временем '+ms
   else:
    if len(db[q[0]]['time']) >= 256:
     t='вы не можете получать более чем 256 уведомлений в сутки'
    else:
     db[q[0]]['time']+=[q[1]]
     t='количество оповещений в день увеличено временем '+ms
   send(t+'. Обратие внимание, что оповещение не содержит изменений, опубликованных позднее, чем оно пришло')
  elif q[1] in ['изменить кол-во оповещений в день','время']:
   ts=db[q[0]]['time'][:]
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
   if q[1] in db[q[0]]['class']:
    db[q[0]]['class']=[w for w in db[q[0]]['class'] if w != q[1]]
    t='количество отслеживаемых классов уменьшено классом '+ms+'.'
   else:
    if len(db[q[0]]['class'])>=256:
     t='вы не можете подписаться более чем на 256 классов'
    elif len(q[1]) > 16:
     t='длина класса не может превышать 16 символов'
    else:
     db[q[0]]['class']+=[q[1]]
     t='количество отслеживаемых классов увеличено классом  '+ms+'.'
   send(t+' Система оповещения только по выбранным классам сейчас находится в разработке, поэтому вы будете получать оповещения по всем классам')
  elif q[1] in ['изменить кол-во отслеживаемых классов','класс']:
   ts=db[q[0]]['class'][:]
   lts=len(ts)
   ts='\n'.join(ts)
   if ts:
    send('Сейчас вы подписаны на '+str(lts)+' классов:\n'+ts+'\n Введите класс, который вас интересует, если вы подписаны на него, то будете отписаны, если подписаны не были, то будете подписаны. Вводить класс следует указав номер и букву без пробела, если в параллели один класс, то это класс "а". Используйте только русские буквы, а не их латинские аналоги',backey)
   else:
    send('Сейчас вы не подписаны ни на один из классов. Введите класс, на который хотите подписаться.  Вводить класс следует узазав номер и букву без пробела, если в параллели один класс, то это класс "а". Используйте только русские буквы, а не их латинские аналоги',backey)
  else:
   send('''Привет, это бот-оповещатель об изменениях в расписании.
Бота надо настроить, чтобы он знал, в каком вы классе и во сколько вас оповещать.
Для этого укажи, сколько раз в день тебе сообщать об изменениях, и за изменениями для каких классов ты хочешь следить.
Клавиатура поможет тебе в этом.
если твоё приложение не поддерживает работу с клавиатурами, то напиши мне команду help
''')
except:
 print(fo())
 log(fo())

open('../kpml.bot.db.json','w').write(dumps(db))


