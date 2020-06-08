class vk(platform):
 def sendsometext(self,text,key,id):
  text=str(text)
  #если сообщение большое, его стоит порезать на части, иначе вк его не пропустит
  g=[]
  while text:
   g+=[text[:4096]]
   text=text[4096:]
  for text in g:
   #генерация клавиатуры
   d={'w':'default','b':'primary','r':'negative','g':'positive'}
   key='{"buttons":['+','.join(['['+','.join(['{"color":"'+d[e[0]]+'","action":{"type":"text","label":"'+e[1:]+'"}}' for e in w.split('+')]) +']' for w in key.split('\n') if w])+']}'
   key='&keyboard='+key
   #отправка сообщений
   text+=key
   key=''
   self.api('messages.send?random_id='+str(time()).replace('.','')+'&user_id='+str(id)+'&','keyboard='+key+'&message='+text)
 def lookforunread(self):
  q=self.api('messages.getConversations?count=200&filter=unanswered&','')
  if q==None:
   return []
  q=q['items']
  q=[[w['conversation']['peer']['id'],w['last_message']['text']] for w in q if w['conversation']['can_write']['allowed']]
  q=[[str(w[0])]+w[1:] for w in q]
  #обработка полученных данных для возвращения в удобном виде
  return q
 def api(self,path,data=''):
 #аргумент path имеет формат method?arg1=val1&arg2=val2 где method это название метода, далее список аргуметов и их значений. Подробнее методы и значения описаны в документации
 #аргумент data может содержать ещё несколько аргуметов в том же формате, только без метода, отличие в том, что здесь нет ограничения на размер аргументов
  print(path,data,time())
  if path and path[-1] not in '?&':
   if '?' in path:
    path+='&'
   else:
    path+='?'
  data=data.encode()
  sleep(1/3)
  ret=loads(urlopen('https://api.vk.com/method/'+path+'v=5.101&access_token='+self.token,data=data).read().decode())
  print(ret)
  if 'response' in ret:
   return ret['response']
  else:
   r=0
   try:
    if ret['error']['error_code'] in [10,5]:
     r=0
   except:
    pass
   if r:
    log(ret)
   return None
 def getlink(self,id):
  return 'https://vk.com/id'+id

