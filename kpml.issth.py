

#тут представлены функции, проверяющие, верно ли, что строка является каким-либо объектом

#классом
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

#датой
def isdt(q):
 ot=q
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
  ot=ot.split(',')[0].split('.')
  ot[1]=str(int(ot[1])-1)
  return ot
 return 0

#временем
def istm(q):
 q=''.join(q.split())
 if ':' not in q:
  return 0
 w=q.split(':')[0]
 if not w.isdigit():
  return 0
 q=q[len(w)+1:]
 if q.isdigit():
  return 1
 return 0

#классом, введённым с клавиатуры
def iskcl(q):
 q=q.strip()
 if q.count('\u2000')==1 and iscl(q.replace('\u2000','')):
  return 1
 return 0

#временем, ввудённым с клавиатуры
def isktm(q):
 q=q.strip()
 if q.count('\u205a')==1 and istm(q.replace('\u205a',':')):
  return 1
 return 0

