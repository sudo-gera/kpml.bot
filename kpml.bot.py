from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
def api(path,data):
 sleep(1/3)
 data=data.encode()
 return loads(urlopen('https://api.vk.com/method/'+path+'v=5.101&access_token=4a2843c76eb198b26ada0a77f1ffe56319f51a7e4b936226cabdb4060efaabc76177977ce585e91e30a5f',data=data).read().decode())

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

db=loads(open('../kpml.bot.db.json').read())

for q in look():
 if q[0] not in db.keys():
  db[q[0]]=dict()
 if q[1] == 'json':
  send(q[0],dumps(db))
 elif q[1]=='help':
  send(q[0],'для указания классов для получения изменений в расписани напиши class потом перечисли все классы через символ ;\n пример команды:\nclass 9А;10В;1Б')
 elif q[1][:5]=='class'
  tmp=q[1][5:]
  tmp=tmp.upper()
  tmp=tmp.split(';')
  db[q[0]]['class']=[]
  se='вы подписались на изменения в расписании для классов:'
  for w in tmp:
   nu=[e for e in w if e in '01234567890']
   nu=''.join(nu)
   nu=int('1'+nu)-10**len(nu)
   le=[e for e in w if e in 'АБВГД']
   le=''.join(le)
   db[q[0]]['class']+=[nu+le]
   se+=' '+nu+le
  send(q[0],se)
 else:
  send(q[0],'nothing to mention')

open('../kpml.bot.db.json','w').write(dumps(db))
