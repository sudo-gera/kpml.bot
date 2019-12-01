
from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime
from traceback import format_exc as fo
from os import popen

defkey='''
b×получить изменения
b×изменить кол-во оповещений в день
b×изменить кол-во отслеживаемых классов
r×сообщение об ошибке
'''
adefkey='''
b×получить изменения
'''
backey='''
r×отмена
'''
d={'w':'default','b':'primary','r':'negative','g':'positive'}
print('\x1b[93m'+asctime()+'\x1b[0m')

#token=urlopen('http://192.168.0.104:9002/0/kpml.bot.token').read().decode()
token=open('../kpml.bot.token').read()
try:
 db=loads(open('../kpml.bot.db.json').read())
except:
 db='{}'
rmo='января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split()
emo='jan feb mar apr may jun jul aug sep oct nov dec'.split()
rdw='понедельник вторник среда четверг пятница суббота воскресенье'.split()
edw='mon tue wed thu fri sat sun'.split()
admin=['225847803']

def api(path,data):
 sleep(1/10)
 print(path,data,time())
 data=data.encode()
 global token
 print(time())
 ret= loads(urlopen('https://api.vk.com/method/'+path+'v=5.101&access_token='+token,data=data).read().decode())
 print(path,data,time())
 return ret

def look(a=0):
 q=api('messages.getConversations?count=200&filter=unread&','')
 if 'response' not in q.keys():
  raise KeyError (str(q))
 q=q['response']['items']
 q=[[w['conversation']['peer']['id'],w['last_message']['text'],w] for w in q if w['conversation']['can_write']['allowed']]
 if a==0:
  q=[w[:2] for w in q]
 q=[[str(w[0])]+w[1:] for w in q]
 q=[[w[0],w[1].lower(),w[1]] for w in q]
 return q

def send(text,key='',id=None):
  text=str(text)
  global q
  if id==None:
   id=q[0]
  global d
  global defkey
  if key=='':
   key=defkey[:]
  while len(text)>4096:
   send(text[:4096],key,id)
   text=text[4096:]
  if key==defkey:
   if db[id]['empty']:
    key+='g×включить пустые сообщения'
   else:
    key+='r×отключить пустые сообщения'
  key='{"buttons":['+','.join(['['+','.join(['{"color":"'+d[e.split('×')[0]]+'","action":{"type":"text","label":"'+e.split('×')[1]+'"}}' for e in w.split('|')]) +']' for w in key.split('\n') if w])+']}'
  key='&keyboard='+key
  text=str(text)
  qq=api('messages.send?random_id='+str(time()).replace('.','')+'&user_id='+str(id)+'&','message='+text+key)
  print(qq)
  r=1
  if list(qq.keys())!=['response']:
   if 'error' in qq.keys():
    if qq['error']['error_code']==901:
     r=0
   if r:
    raise KeyError(str(qq))


def log(q):
 for w in admin:
  send(str(q),defkey,w)

def nparse(day,mon):
 day,mon=int(day),int(mon)
 q=urlopen('http://xn--j1acc5a.xn--p1ai/pages/raspisanie/izmeneniya-v-raspisanii').read().decode()
 q=q.split('''«Кировский''')[0]
 q=q.replace('<','\0<').replace('>','>\0')
 q=q.split('\0')
 q=[w.strip() for w in q]
 get=0
 new=[]
 mon+=100
 q=[w for w in q if w and not(w[0] == '<' and '=' not in w)]
 got=q[:]
 for q in got:
  if q[:25] == 'Изменения в расписании на':
   date=q[25:].lower()
   for w in range(12):
    date=date.replace(rmo[w],str('\0'+str(w+100)+'\0'))
   date=list(date)
   for w in range(len(date)):
    if not date[w].isdigit():
     date[w]='\0'
   date=''.join(date)
   date=[int(w) for w in date.split('\0') if w]
   if day in date and mon in date:
    get =1
   else:
    get=0
  elif get:
   new+=[q]
 new='\0'.join(new)
 new=new.replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>').replace('&amp;','&').replace('&quot;','"').replace('&apos;',"'")
 new=new.split('\0')
 new=[w for w in new if w and w[0]!='<']
 return new

def parse(day,mon):
 try:
  parsed=nparse(day,mon)
  if len(parsed)==1 and parsed[0].lower()=='изменений нет':
   parsed=[]
  return parsed
 except:
  log(fo())
  return ['''При чтении изменений произошла ошибка, о которой админ бота уже оповещён.
Для получения изменений в расписании перейдите по ссылке http://kpml.ru/pages/raspisanie/izmeneniya-v-raspisanii''']

def next(q,w,e):
 q,w,e=int(q),int(w),int(e)
 if e%4==0 and e%100 or e%400:
  l=[31,29,31,30,31,30,31,31,30,31,30,31]
 else:
  l=[31,28,31,30,31,30,31,31,30,31,30,31]
 if q+1>l[w]:
  tn= [1,w%12+1]
 else:
  tn= [q+1,w]
 return tn+[e]

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

def work(empty=0):
 q,w,e,dw=today()
 td=parse(q,w)
 if td or empty==0:
  td=['Изменения на сегодня, '+str(q)+' '+rmo[int(w)]+' '+rdw[dw]+':']+ td
 r,t,y=next(q,w,e)
 tn=parse(r,t)
 if tn or empty==0:
  tn=['Изменения на завтра, '+str(r)+', '+rmo[int(t)]+' '+rdw[(dw+1)%7]+':']+tn
 if int(time())%(24*3600)<12*3600 or int(time())%(24*3600)>21*3600:
  if td+tn:
   q=td+['<=====================>']+tn
  else:
   q=[]
 else:
  q=tn
 q='\n'.join(q)
 return q

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

#po0
try:
# if 'time' not in  db.keys():
#  db['time']=dict()
# db['time']=dict()
 wai=[]
 while wai==[]:
  tn=int(time())
  for w in db.keys():
   if w.isdigit():
    for e in db[w]['time']:
#     if e not in db['time'].keys():
#      db['time'][str(e)]=[]
#     if w not in db['time'][str(e)]:
#      db['time'][str(e)]+=[w]
     if 0 < tn % (24*3600) - int(e) < 300 and tn - db[w]['ls'] >= 300:
      worked=work(db[w]['empty'])
      if worked:
       send(worked,defkey,w)
       db[w]['ls']=int(time())
  wai=look()

 for q in wai:
  added=0
  if q[0] not in db.keys():
   db[q[0]]=dict()
   w=q[0]
   if 'ls' not in db[w].keys():
    db[w]['ls']=0
   if 'time' not in db[w].keys():
    db[w]['time']=[]
   if 'class' not in db[w].keys():
    db[w]['class']=[]
   if 'empty' not in db[w].keys():
    db[w]['empty']=0
   added=1
#po1
  if q[1] == '':
   send('текстом, пожалуйста')
  elif q[1] == 'json':
   send(str(db))
  elif q[1] == 'git':
   t=popen('git show').read()
   t=t.split('\n\n')[0]
   send(t)
  elif q[1] == 'len':
   send(len(db.keys()))
  elif q[1][:2] == 'np':
   dat=q[1][2:].split('.')
   dat[1]=int(dat[1])-1
   send('\n'.join(nparse(dat[0],dat[1])))
  elif q[1] == 'xg':
   send('\n'.join([str([w,db[w]]) for w in db.keys()]))
  elif q[1] == 'отмена':
   send('отменено')
  elif q[1] in ['получить изменения','сейчас']:
   w,e,r,dw=today()
   kb='w×'+str(w)+'.'+str(e+1)+', '+rdw[dw]
   w,e,r=next(w,e,r)
   kb+='|w×'+str(w)+'.'+str(e+1)+', '+rdw[(dw+1)%7]
   for t in range(4):
    w,e,r=next(w,e,r)
    kb+='\nw×'+str(w)+'.'+str(e+1)+', '+rdw[(dw+2+t*2)%7]
    w,e,r=next(w,e,r)
    kb+='|w×'+str(w)+'.'+str(e+1)+', '+rdw[(dw+3+t*2)%7]
   w,e,r,dw=today()
   send('выберите дату (сегодня '+str(w)+' '+rmo[e]+')',kb)
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
   send(work())
  elif isdt(q[1]):
   tmp=isdt(q[1])
   tmp=parse(tmp[0],tmp[1])
   tmp='\n'.join(tmp)
   tmp='Изменения на '+q[1]+':\n'+tmp
   send(tmp)
  elif istm(q[1]):
   ms=q[1]
   q[1]=q[1].split(':')
   q[1]=(int(q[1][0])-3)%24*3600+int(q[1][1])%60*60
   send([q[1]])
   send(db[q[0]]['time'])
   if q[1] in db[q[0]]['time']:
#    q[1]=str(q[1])
#    db['time'][q[1]]=[w for w in db['time'][q[1]] if w != q[0]]
#    if db['time'][q[1]]==[]:
#     del(db['time'][q[1]])
#    q[1]=int(q[1])
    db[q[0]]['time']=[w for w in db[q[0]]['time'] if w != q[1]]
    t='количество оповещений в день уменьшено временем '+ms
   else:
#    if q[1] not in db['time']:
#     db['time'][q[1]]=[]
#    db['time'][q[1]]+=[q[0]]
    db[q[0]]['time']+=[q[1]]
    t='количество оповещений в день увеличено временем '+ms
    send(t+'. Обратие внимание, что оповещение не содержит изменений, опубликованных позднее, чем оно пришло')
  elif q[1] in ['изменить кол-во оповещений в день','время']:
#   ts=[int(w) for w in db['time'] if q[0] in db['time'][w]]
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
    db[q[0]]['class']+=[q[1]]
    t='количество отслеживаемых классов увеличено классом  '+ms+'.'
   send(t+' Система оповещения только по выбранным классам сейчас находится в разработке, поэтому вы будете получать оповещения по всем классам')
  elif q[1] in ['изменить кол-во отслеживаемых классов','класс']:
   ts=db[q[0]]['class'][:]
   lts=len(ts)
   ts='\n'.join(ts)
   if ts:
    send('Сейчас вы подписаны на '+str(lts)+' классов:\n'+ts+'\n Введите класс, который вас интересует, если вы подписаны на него, то будете отписаны, если подписаны не были, то будете подписаны. Вводить класс следует узазав номер и букву без пробела, если в параллели один класс, то это класс "а". Используйте только русские буквы, а не их латинские аналоги',backey)
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


