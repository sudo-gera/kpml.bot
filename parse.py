from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime

rmo='января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split()
emo='jan feb mar apr may jun jul aug sep oct nov dec'.split()

def next(q,w):
 q,w=int(q),int(w)
 l=[31,28,31,30,31,30,31,31,30,31,30,31]
 if q+1>l[w]:
  return '1 '+str(w%12+1)
 return str(q+1)+' '+str(w)

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

