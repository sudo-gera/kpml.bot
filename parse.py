from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime

rmo='января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split()
emo='jan feb mar apr may jun jul aug sep oct nov dec'.split()
beg='Изменения в расписании на '


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
 q=q.replace('<','\x01\x02').replace('>','\x01').replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>').replace('&amp;','&').replace('&quot;','"').replace('&apos;',"'")
 q=q[:q.index('«Кировский')]
 q=q[q.index('\x01\x02body'):]
 q=q.replace('\x01\x02br ','\n\x01\x02br ')
 q=q.replace('\x01\x02br/\x01','\n')
 q=q.replace('\x01\x02br ','\n\x01\x02br ')
 q=q.replace('\x01\x02/p\x01','\x01\x02/p\x01\n')
 q=q.split('\x01')
# q=[w if len(w) < 2 or w[0] != '\x02' else ('\x03'+w[2:] if w[:2] in ['\x02/','\x02!'] else ('\x04'+w[1:-1]+'\x04' if w[-1] == '/' else w))  for w in q]
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



def get(clas,day,mon):
 day=int(day)
 mon=int(mon)
 text=repa(day,mon)
 '''

.∧＿∧
( ･ω･｡)つ━☆・*。
⊂. ノ ...・゜+.
しーＪ...°。+ *´¨)
..........· ´¸.·*´¨) ¸.·*¨)
..........(¸.·´ (¸.·'* ☆  your code ☆

 '''
 return text

print(get('9А','20','0'))  #20 января
print(get('10Б','1','9'))  #1 октября
print(get('1А','15','10')) #15 ноября
print(get('4В','4','11'))  #4 декабря
print(get('4В','27','0'))  #4 декабря
