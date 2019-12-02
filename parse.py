from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime

rmo='января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split()
emo='jan feb mar apr may jun jul aug sep oct nov dec'.split()


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

def get(clas,day):
 text=parse(day)
 '''

.∧＿∧
( ･ω･｡)つ━☆・*。
⊂. ノ ...・゜+.
しーＪ...°。+ *´¨)
..........· ´¸.·*´¨) ¸.·*¨)
..........(¸.·´ (¸.·'* ☆  your code ☆

 '''
 return text

print(get('9А','20 8'))  #20 января
print(get('10Б','1 9'))  #1 октября
print(get('1А','15 10')) #15 ноября
print(get('4В','4 11'))  #4 декабря
