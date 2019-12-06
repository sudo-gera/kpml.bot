from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime

rmo='января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split()
emo='jan feb mar apr may jun jul aug sep oct nov dec'.split()


def parse():
 q=urlopen('http://kpml.ru/pages/raspisanie/izmeneniya-v-raspisanii').read().decode()
 q=q.replace('<','\x01\x02').replace('>','\x01').replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>').replace('&amp;','&').replace('&quot;','"').replace('&apos;',"'")
 q=q.split('''«Кировский''')[0]
 t=beg
 q=q.split(t)[1:]
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
 q=[w[1] for w in q]
 q='\n'.join(q)
 return q


def get(clas,day,mon):
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
