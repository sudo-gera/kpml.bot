from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime

rmo='января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split()
emo='jan feb mar apr may jun jul aug sep oct nov dec'.split()

def parse(t):
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
 q=[w for w in q if w[:len(t)]==t]
 q=[' '.join(w.split()[2:]) for w in q]
 return q

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

print(get('9А','20 0'))  #20 января
print(get('10Б','1 9'))  #1 октября
print(get('1А','15 10')) #15 ноября
print(get('4В','4 11'))  #4 декабря
