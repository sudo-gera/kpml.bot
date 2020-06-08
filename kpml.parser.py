

rmo='января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split()
emo='jan feb mar apr may jun jul aug sep oct nov dec'.split()
rdw='понедельник вторник среда четверг пятница суббота воскресенье'.split()
edw='mon tue wed thu fri sat sun'.split()
beg='Изменения в расписании на '
#некоторые константы

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
  q=open('../kpml.bot.html').read()
 except:
  q=str(time()-400)+'\x01'
 bt=q.split('\x01',1)[0]
 oq=q.split('\x01',1)[1]
 if time()-float(bt)>300:
  try:
   q=urlopen('http://kpml.ru/pages/raspisanie/izmeneniya-v-raspisanii').read().decode()
   if q!=oq:
    log('site changed')
   open('../kpml.bot.html','w').write(str(time())+'\x01'+q)
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
def view(day=None,mon=None,profile=None):
 if profile==None and day != None and mon != None:
  del(profile)
  global profile
 try:
  if day==None and mon==None:
   parsed=out()
  else:
   parsed=''
   for w in profile['class']:
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
def work(profile,empty=0):
 q,w,e,dw=today()
 td=view(q,w,profile)
 if td or empty==0:
  td='Изменения на сегодня, '+str(q)+' '+rmo[int(w)]+' '+rdw[dw]+':\n'+ td
 r,t,y,dw=next(q,w,e,dw)
 tn=view(r,t,profile)
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

