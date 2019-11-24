	from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime
from traceback import format_exc as fo

nokey=''


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

token=open('../kpml.bot.token').read()
db=loads(open('../kpml.bot.db.json').read())
rmo='января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split()
emo='jan feb mar apr may jun jul aug sep oct nov dec'.split()
rdw='понедельник вторник среда четверг пятница суббота воскресенье'.split()
edw='mon tue wed thu fri sat sun'.split()
admin='225847803'

def api(path,data):
 sleep(1/9)
 print(path,data)
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

def send(text,id=None,key=''):
  global q
  gg=[]
  if type(id)==type(gg) and key=='':
   key=id[:]
   id=q[0]
  if id==None:
   id=q[0]
  global d
  global defkey
  if key=='':
   key=defkey[:]
  else:
   key=key[0]
  key='{"buttons":['+','.join(['['+','.join(['{"color":"'+d[e.split('×')[0]]+'","action":{"type":"text","label":"'+e.split('×')[1]+'"}}' for e in w.split('|')]) +']' for w in key.split('\n') if w])+']}'
  key='&keyboard='+key
  text=str(text)
  sleep(5)
  qq=api('messages.send?random_id='+str(int(time()*2**28))+'&user_id='+str(id)+'&','message='+text+key)
  print(qq)
  r=1
  if list(qq.keys())!=['response']:
   if 'error' in qq.keys():
    if qq['error']['error_code']==901:
     r=0
   if r:
    raise KeyError(str(qq))


def log(q):
 send(str(q),admin,[defkey])

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
  if ss[:26] == 'Изменения в расписании на ' and ' - ' in ss and ss.split(' - ')[1].strip().split()[0].strip().isdigit():
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

def work():
 q,w,e,dw=today()
 t=str(q)+' '+str(w)
 tn=next(q,w,e)
 tn=str(tn[0])+' '+str(tn[1])
 if int(time())%(24*3600)<12*3600 or int(time())%(24*3600)>21*3600:
  q=['Изменения на сегодня, '+t.split()[0]+', '+rmo[int(t.split()[1])]+' '+rdw[dw]+':']+ parse(t) + ['<=========================>','Изменения на завтра, '+tn.split()[0]+', '+rmo[int(tn.split()[1])]+' '+rdw[(dw+1)%7]+':']+parse(tn)
 else:
  q=['Изменения на завтра, '+tn.split()[0]+', '+rmo[int(tn.split()[1])]+' '+rdw[(dw+1)%7]+':']+parse(tn)
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
  return 1
 return 0

def istm(q):
 q=''.join(q.split())
 if '.' not in q:
  return 0
 w=q.split('.')[0]
 if not w.isdigit():
  return 0
 q=q[len(w)+1:]
 if q.isdigit()
  return 1
 return 0

try:
 tn=time()
 for w in db.keys():
  if w.isdigit():
   if 'ls' not in db[w].keys():
    db[w]['ls']=0
   if 'time' not in db[w].keys():
    db[w]['time']=[]
   if 'class' not in db[w].keys():
    db[w]['class']=[]
   if 'empty' not in db[w].keys():
    db[w]['empty']=1
   for e in db[w]['time']:
    if 0<int(tn)%(24*3600)-int(e)<300 and (int(tn)-db[w]['ls'])>=300:
     send(work(),w,[defkey])
     db[w]['ls']=int(time())


 wai=look()

 if wai == []:
  sleep(0.1)
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
  elif q[1] == 'ad':
   send('ad',[adefkey])
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
  elif q[1] == 'увеличить кол-во оповещений в день':
   send('Будет добавлено ещё одно оповещение. Введите время для него в формате ЧЧ:ММ')
  elif q[1] == 'отмена':
   send('отменено')
  elif q[1] == 'получить изменения':
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
   send('выберите дату (сегодня '+str(w)+' '+rmo[e]+')',[kb])
  elif q[1] == 'сообщение об ошибке':
   send('напишите сообщение об ошибке, начните его с символа $',backey)
  elif q[1][0] == '$':
   log('сообщение об ошибке\nавтор vk.com/id'+q[0]+'\n'+q[1][1:])
   send('сообщение отправлено администрации, с вами скоро свяжутся')
  elif q[1] == 'faq':
   send('частые ошибки, которые мешают пользоваться ботом:\nдля команд class и time убедитесь, что элементы разделены символом ; а не пробелом\nдля команды class убедитесь, что буквы классов русские, а не латинские\nдля команды lookall день, убедитесь, что сначала написали число, потом номер месяца, и между ними пробел. Введи help и проверь, что команда написана верно')
  elif q[1] == 'lookall':
   send(work(),[defkey])
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
     qq,w,e=next(qq,w,e)
    send('Изменения вперёд на '+tmp[0][1:]+' дней:\n'+'\n'.join(parse(str(qq)+' '+str(w))))
   elif len(tmp)==1 and tmp[0][0]=='>' and tmp[0][1:].isdigit():
    send('слишком далеко')
   else:
    send('не удалось распознать день')
  elif istm(q[1]):
   ms=q[1]
   q[1]=q[1].split(':')
   q[1]=(int(q[1][0])-3)%24*3600+int(q[1][1])%60*60
   if q[1] in db[q[0]]['time']:
    db[q[0]]['time']=[w for w in db[q[0]]['time'] if w != q[1]]
    send('количество оповещений в день уменьшено временем '+ms)
   else:
    db[q[0]]['time']+=[q[1]]
    send('количество оповещений в день увеличено временем '+ms)
  elif q[1]=='изменить кол-во оповещений в день':
   ts=db[q[0]]['time'][:]
   ts=[str((w//3600+3)%24)+':'+str(w%3600//60) for w in ts]
   ts='\n'.join(ts)
   if ts:
    ts='Сейчас вам приходят оповещения по этому расписанию:\n'+ts+'''
введите интересующее вас время,
если оно в расписании, то оно будет убрано от туда,
если его там нет, то добавлено.
Бот не способен оповещать чаще, чем раз в 5 минут
'''
   else:
    ts='Сейчас вам не приходят оповещения, введите время для оповещения'
   send(ts,[backey])
  elif isdt(q[1]):
   tla='lookall '+q[1].split('.')[0]+' '+q[1].split('.')[1].split(',')[0]
   wai+=[[q[0],tla]]
  elif iscl(q[1]):
   q[1]=q[1].upper()
   ms=q[1]
   if q[1] in db[q[0]]['class']:
    db[q[0]]['class']=[w for w in db[q[0]]['class'] if w != q[1]]
    send('количество отслеживаемых классов уменьшено классом '+ms)
   else:
    db[q[0]]['class']+=[q[1]]
    send('количество отслеживаемых классов увеличено классом  '+ms)
  elif q[1]=='изменить кол-во отслеживаемых классов':
   ts=db[q[0]]['class'][:]
   ts='\n'.join(ts)
   if ts:
    send('Сейчас вы подписаны на классы:\n'+ts+'\n Введите класс, который вас интересует, если вы подписаны на него, то будете отписаны, если подписаны не были, то будете подписаны. Вводить класс следует узазав номер и букву без пробела, если в параллели один класс, то это класс "а". Используйте только русские буквы, а не их латинские аналоги',[backey])
   else:
    send('Сейчас вы не подписаны ни на один из классов. Введите класс, на который хотите подписаться.  Вводить класс следует узазав номер и букву без пробела, если в параллели один класс, то это класс "а". Используйте только русские буквы, а не их латинские аналоги',[backey])
  elif q[1] == 'nokey':
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
для получения изменений по всем классам введи lookall
для просмотра изменений на произвольный день введи lookall день
примеры:
lookall 23 7
для просмотра на несколько дней вперёд введи lookall >дни
пример:
lookall >2
есть вопросы - введи faq
Бот работает не так как надо? напиши сюда сообщение об ошибке, начав его с символа $
''')
  else:
   send('''Привет, это бот-оповещатель об изменениях в расписании.
Бота надо настроить, чтобы он знал, в каком вы классе и во сколько вас оповещать.
Для этого укажи, сколько раз в день тебе сообщать об изменениях, и за изменениями для каких классов ты хочешь следить.
Клавиатура поможет тебе в этом.
если твоё приложение не поддерживает работу с клавиатурами, то напиши мне команду nokey
''')
except:
 log(fo())

open('../kpml.bot.db.json','w').write(dumps(db))


