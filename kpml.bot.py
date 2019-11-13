from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime
from traceback import format_exc as fo

print('\x1b[93m'+'█'*20+asctime()+'\x1b[0m')

token=open('../kpml.bot.token').read()
db=loads(open('../kpml.bot.db.json').read())
rmo='января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split()
emo='jan feb mar apr may jun jul aug sep oct nov dec'.split()
rdw='понедельник вторник среда четверг пятница суббота воскресенье'.split()
edw='mon tue wed thu fri sat sun'.split()
admin='225847803'

def api(path,data):
 sleep(1/3)
 data=data.encode()
 global token
 return loads(urlopen('https://api.vk.com/method/'+path+'v=5.101&access_token='+token,data=data).read().decode())

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

def send(id,text=None):
  global q
  if text==None:
   id,text=q[0],id
  text=str(text)
  qq=api('messages.send?random_id='+str(int(time()*2**28))+'&user_id='+str(id)+'&','message='+text)
  r=1
  if list(qq.keys())!=['response']:
   if 'error' in qq.keys():
    if qq['error']['error_code']==901:
     r=0
   if r:
    raise KeyError(str(qq))


def log(q):
 send(admin,str(q))

def hparse(t):
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
  ss=w[0]
  if ss[:12] == 'Изменения на' and ' - ' in ss and ss[ss.index(' - '):].strip().split()[0].strip().isdigit():
   w[0]=w[0].split('-')[1].split()[:2]
   w[0][1]=str(rmo.index(w[0][1].lower()))
   w[0][0]=str(int(w[0][0]))
   w[0]=' '.join(w[0])
   day=w[0]
   w[0]=''
  else:
   w[0]=day+' '+w[0]
 q=[w[0] for w in q if w[0]]
 t=t.split()
 t[0]=str(int(t[0]))
 t[1]=str(int(t[1]))
 t=' '.join(t)
 q=[w for w in q if w[:len(t)]==t]
 q=[' '.join(w.split()[2:]) for w in q]
 return q

def parse(t):
 try:
  return hparse(t)
 except:
  send('225847803',fo())
  return ['''При чтении изменений произошла ошибка, о которой админ бота уже оповещён. Текст ошибки:
Traceback (most recent call last):
  File "kpml.bot.py", line 1342, in <module>
    read('kpml.ru')
YambarError: Yambarysheva ohrenela
Для получения изменений в расписании перейдите по ссылке http://кфмл.рф/pages/raspisanie/izmeneniya-v-raspisanii''']

def next(q,w,e):
 q,w=int(q),int(w)
 if e%4==0 and e%100 or e%400:
  l=[31,29,31,30,31,30,31,31,30,31,30,31]
 else:
  l=[31,28,31,30,31,30,31,31,30,31,30,31]
 if q+1>l[w]:
  tn= '1 '+str(w%12+1)
 else:
  tn= str(q+1)+' '+str(w)
 return tn

def work():
 t=asctime()
 t=t.split()[0:5]
 dw=t[0].lower()
 t=t[1:]
 t[0]=t[0].lower()
 t[0]=emo.index(t[0])
 q,w,e=int(t[1]),int(t[0]),int(t[3])
 t=str(t[1])+' '+str(t[0])
 tn=next(q,w,e)
 tn=tn.split()
 tn=str(tn[0])+' '+str(tn[1])
 if int(time())%(24*3600)<12*3600 or int(time())%(24*3600)>21*3600:
  q=['Изменения на сегодня, '+t.split()[0]+', '+rmo[int(t.split()[1])]+' '+rdw[edw.index(dw)]+':']+ parse(t) + ['<=========================>','Изменения на завтра, '+tn.split()[0]+', '+rmo[int(tn.split()[1])]+' '+rdw[(edw.index(dw)+1)%7]+':']+parse(tn)
 else:
  q=['Изменения на завтра, '+tn.split()[0]+', '+rmo[int(tn.split()[1])]+' '+rdw[(edw.index(dw)+1)%7]+':']+parse(tn)
 q='\n'.join(q)
 return q



try:

 for w in db.keys():
  if 'ls' not in db[w].keys():
   db[w]['ls']=0
  if 'time' in db[w].keys():
   for e in db[w]['time']:
    if 0<int(time())%(24*3600)-int(e)<300 and (int(time())-db[w]['ls'])>900:
     send(w,work())
     db[w]['ls']=int(time())

 wai=look()

 if wai == []:
  sleep(5)
 for q in wai:
  added=0
  if q[0] not in db.keys():
   db[q[0]]=dict()
   added=1
  if q[1] == '':
   send('текстом, пожалуйста')
  elif q[1] == 'json':
   send(dumps(db))
  elif q[1] == 'len':
   send(len(db.keys()))
  elif q[1] == 'xg':
   send('\n'.join([str([w,db[w]]) for w in db.keys()]))
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
    elif w:
     send('не удалось разобрать фрагмент строки '+w+'. Введите help и внимательно всё перечитайте, должно помочь')
   if se=='вы подписались на изменения в расписании для классов:':
    send('вы не подписались ни на один класс')
   else:
    send(se+'\nвозможность получать оповещения только по выбранным классам появится скоро. Пока что вы считаетесь подписаными на все классы')
  elif q[1][:4] == 'time':
   tmp1=q[1][4:].strip()
   ts=''
   db[q[0]]['time']=[]
   tmp1=';'.join([tmp.strip() for tmp in tmp1.split(';')])
   tmp1=':'.join([tmp.strip() for tmp in tmp1.split(':')])
   for tmp in tmp1.split(';'):
    t=tmp.split(':')
    if len(t)==2 and t[0].isdigit() and t[1].isdigit() and 99<int('1'+'0'*(2-len(t[0]))+t[0])<124 and 99<int('1'+'0'*(2-len(t[1]))+t[1])<160:
     db[q[0]]['time']+=[(int(t[0])*3600+int(t[1])*60-3*3600)%(24*3600)]
     ts+=' '+tmp
     db[q[0]]['ls']=0
    elif tmp.split():
     send('не удалось разобрать фрагмент строки '+tmp+'. Введите help и внимательно всё прочитайте, должно помочь')
   if ts:
    send('теперь автоматические оповещения будут приходить вам в '+ts+'. Обратие внимание, что оповещение не содержит изменений, опубликованных позднее, чем оно пришло')
   else:
    send('теперь вам не будут приходить оповещения')
   che=db[q[0]]['time'][:]
   che.sort()
   chs=0
   for w in range(len(che)-1):
    if che[w]-che[w+1]>-900:
     chs=1
   if chs:
    send('бот не может отправлять автоматические оповещения чаще, чем раз в 15 минут')
  elif q[1] == 'look':
   ts='изменения классам, на которые вы подписаны:\n'
   if 'class' in db[q[0]].keys() and db[q[0]]['class']:
    ts+=work()
   if ts=='изменения классам, на которые вы подписаны:\n':
    send('вы не подписаны ни на один из классов. Если нужна помошь, введите help')
   else:
    send(ts)
  elif q[1] == 'faq':
   send('частые ошибки, которые мешают пользоваться ботом:\nдля команд class и time убедитесь, что элементы разделены символом ; а не пробелом\nдля команды class убедитесь, что буквы классов русские, а не латинские\nдля команды lookall день, убедитесь, что сначала написали число, потом номер месяца, и между ними пробел. Введи help и проверь, что команда написана верно')
  elif q[1] == 'lookall':
   send(work())
  elif q[1][:7] == 'lookall':
   tmp=q[1][7:].split()
   if len(tmp)>1 and tmp[0].isdigit() and tmp[1].isdigit():
    tmp=tmp[0]+' '+str(int(tmp[1])-1)
    tmp=parse(tmp)
    tmp='\n'.join(tmp)
    tmp='Изменения на '+q[1][7:]+':\n'+tmp
    send(tmp)
   elif len(tmp)==1 and tmp[0][0]=='>' and tmp[0][1:].isdigit() and int(tmp[0][1:]) < 60:
    t=asctime()
    t=t.split()[1:5]
    t[0]=t[0].lower()
    t[0]=emo.index(t[0])
    qq,w,e=int(t[1]),int(t[0]),int(t[3])
    for sw in ' '*int(tmp[0][1:]):
     qq,w=next(qq,w,e).split()
     if str(qq)=='1' and str(w)=='0':
      e+=1
    send('Изменения вперёд на '+tmp[0][1:]+' дней:\n'+'\n'.join(parse(str(qq)+' '+str(w))))
   elif len(tmp)==1 and tmp[0][0]=='>' and tmp[0][1:].isdigit():
    send('слишком далеко')
   else:
    send('не удалось распознать день')
  elif q[1][0].isdigit() and len(q[1].split())>1:
   tmp=q[1]
   tmp=tmp.split()
   wai+=[[q[0],'class '+tmp[0]]]
   wai+=[[q[0],'time '+tmp[1]]]
  elif q[1] == 'other':
   send('''
Вы можете изменить класс подписки или подписаться сразу на несколько
Чтобы подписаться на изменения напиши class потом перечисли все интересующие классы через символ ; Внимание: для указания буквы класса можно использовать только русские символы (не их латинские аналоги)
примеры команды:
class 9А;10В;1Б
class 10А
так же можно изменить время оповещений, или указать несколько раз в сутки
для указания времени, когда должны приходить оповещения напиши time потом введи московское время через символ : если несколько, то разделяй символом ; чтобы отписаться, напиши time не указав время. Важно: если не указать время, оповещения приходить не будут
примеры команды:
time 20:00
time 21:12;23:23
Чтобы получить изменения своих классов прямо сейчас напиши look
для получения изменений по всем классам введи lookall
для просмотра изменений на произвольный день введи lookall день
примеры:
lookall 23 7
для просмотра на несколько дней вперёд введи lookall >дни
пример:
lookall >2
есть вопросы - введи faq
Бот работает не так как надо? пиши @'+admin+' (админy)
''')
  elif added==0 and [w for w in q[1] if w in 'qawszedxrfctgvyhbujnikmolp']==[]:
   send('нужна помощь по боту - пиши help. Хочешь что-то сказать админу - напиши админу, а не сюда')
  else:
   send('''Привет, это бот-оповещатель об изменениях в расписании.
Бота надо настроить, чтобы он знал, в каком вы классе и во сколько вас оповещать.
Для этого введи свой класс и время.
примеры:
9А 18:00
10Б 19:30
4В 16:55
Вы всегда сможете отписаться.
Важно: буква класса должна быть русской, а не латинской.
чтобы увидеть остальные возможности бота введи other
''')
except:
 log(fo())

open('../kpml.bot.db.json','w').write(dumps(db))


