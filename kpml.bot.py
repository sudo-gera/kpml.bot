from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime

token=open('../kpml.bot.token').read()
db=loads(open('../kpml.bot.db.json').read())
rmo='января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split()
emo='jan feb mar apr may jun jul aug sep oct nov dec'.split()

def api(path,data):
 sleep(1/3)
 data=data.encode()
 global token
 return loads(urlopen('https://api.vk.com/method/'+path+'v=5.101&access_token='+token,data=data).read().decode())

def look(a=0):
 q=api('messages.getConversations?count=200&filter=unread&','')
 q=q['response']['items']
 q=[[w['conversation']['peer']['id'],w['last_message']['text'],w] for w in q if w['conversation']['can_write']['allowed']]
 if a==0:
  q=[w[:2] for w in q]
 q=[[str(w[0])]+w[1:] for w in q]
 return q

def send(id,text):
  q=api('messages.send?random_id='+str(int(time()*2**28))+'&user_id='+str(id)+'&','message='+text)
  if list(q.keys())!=['response']:
   print(q)

def next(q,w):
 q,w=int(q),int(w)
 l=[31,28,31,30,31,30,31,31,30,31,30,31]
 if q+1>l[w]:
  return '1 '+str(w%12+1)
 return str(q+1)+' '+str(w)

def parse():
 q=urlopen('http://xn--j1acc5a.xn--p1ai/pages/raspisanie/izmeneniya-v-raspisanii').read().decode()
 q=q.split('\n')
 q=[[len(w),w] for w in q]
 q=max(q)[1]
 q=q.replace('<','\n<').replace('>','>\n').replace('&nbsp;','')
 q=q.split('\n')
 q=[w for w in q if w and w[0] != '<']
 q=[[w,] for w in q]
 day=''
 for w in q:
  if w[0][:9].strip() == 'Изменения':
   w[0]=w[0].split('-')[1].split()[:2]
   w[0][1]=str(rmo.index(w[0][1].lower()))
   w[0]=' '.join(w[0])
   day=w[0]
   w[0]=''
  else:
   w[0]=day+' '+w[0]
 q=[w[0] for w in q if w[0]]
 t=asctime()
 t=t.split()[1:3]
 t[0]=t[0].lower()
 t[0]=emo.index(t[0])
 tn=next(t[1],t[0])
 t=str(t[1])+' '+str(t[0])
 q=['1 1 Изменения на сегодня, '+t.split()[0]+' '+rmo[int(t.split()[1])]+':']+[w for w in q if w[:len(t)]==t] + ['1 1 <=========================>','1 1 Изменения на завтра, '+tn.split()[0]+' '+rmo[int(tn.split()[1])]+':']+ [w for w in q if w[:len(tn)]==tn]
 q=[' '.join(w.split()[2:]) for w in q]
 q='\n'.join(q)
 return q

for q in look():
 if q[0] not in db.keys():
  db[q[0]]=dict()
 if q[1] == 'json':
  send(q[0],dumps(db))
 elif q[1]=='help':
  send(q[0],'для указания классов для получения изменений в расписани напиши class потом перечисли все классы через символ ;\n пример команды:\nclass 9А;10В;1Б\nдля указания времени оповещения введи time московское время через символ :\n пример команды:\ntime 20:00')
 elif q[1][:5]=='class':
  tmp=q[1][5:]
  tmp=tmp.upper()
  tmp=tmp.split(';')
  db[q[0]]['class']=[]
  se='вы подписались на изменения в расписании для классов:'
  for w in tmp:
   nu=[e for e in w if e in '01234567890']
   nu=''.join(nu)
   nu=int('1'+nu)-10**len(nu)
   nu=str(nu)
   le=[e for e in w if e in 'АБВГД']
   le=''.join(le)
   if nu and le:
    db[q[0]]['class']+=[nu+le]
    se+=' '+nu+le
  send(q[0],se)
 elif q[1][:4] == 'time':
  tmp=q[1][4:].strip()
  t=tmp.split(':')
  if len(t)==2 and t[0].isdigit() and t[1].isdigit() and 99<int('1'+'0'*(2-len(t[0]))+t[0])<124 and 99<int('1'+'0'*(2-len(t[1]))+t[1])<160:
   db[q[0]]['time']=t[0]*3600+t[1]*60
   send(q[0],'теперь автоматические оповещения будут приходить вам в '+tmp)
  else:
   send(q[0],'неправильный формат времени')
 elif q[1] == 'look':
  send(q[0],parse())
 else:
  send(q[0],'введи look')

for w if db.keys():
 if 'ls' not in db[w].keys():
  db[w]['ls']=0
 if abs(int(time())%(24*3600)-db[w]['time'])<300 and (int(time())-db[w]['ls'])>900:
  send(w,parse())
  db[w]['ls']=int(time())

open('../kpml.bot.db.json','w').write(dumps(db))
