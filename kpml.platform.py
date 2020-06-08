

#здесь описаны общие функции для работы с платформами

#универсальный класс для платформ, тут описаны общие методы
#описанием платформы является класс, который наследует от этого
class platform:
 def __init__(self):
  self.name=self.__class__.__name__
  self.token=self.loadtoken()
 def loadtoken(self):
  try:
   return open('../kpml.bot.token_'+self.name).read().strip()
  except:
   return ''
 def savetoken(self,token):
  open('../kpml.bot.token_'+self.name,'w').write(str(token).strip())

#для создания новой платформы достаточно создать класс, наследующий от platform и имеющий функции
#sendsometext(self,text,keyboard,id):
# отправка сообщения
# если платформа не поддерживает клавиатуры, параметр keyboard можно игнорировать
#lookforunread():
# получить список непрочитанных сообщений
#getlink(self,id):
# получение ссылки по id
#по мимо них могут содержаться любые вспомогательные функции
#первым аргументом всегда передаётся объект (self), его рекомендуется использовать для хранения токена: self.token

#создание словаря dplats, где будут содержаться информация обо всех платформах
dplats=dict()
#обращение к платформе должно происходить через функцию plats которая принимает строку с названием класса платформы в качестве аргумента и возвращает необходимый объект, или список названий платформ, если ничего не передать
#обращение напрямую к платформе рекомендуется делать только из этого файла, а в остальных использовать обие функции, описанные здесь
#функция plats записывает в словарь dplats экземпляры классов платформ, каждый экземпляр создаётся единожды за время работы программы
def plats(q=None):
 for w in platform.__subclasses__():
  if w not in dplats:
   dplats[w.__name__]=w()
 if q==None:
  return list(dplats.keys())
 else:
  return dplats[q]


#получить последние сообщения в формате [[id,сообщение,профиль],[id,сообщение,профиль],[id,сообщение,профль]]
def look():
 ext=[]
 for w in plats():
  ext+=[[e[0],e[1].lower(),w] for e in plats(w).lookforunread()]
 return ext

#функция отправки сообщений, аргументы: текст, клавиатура (по умолчанию: defkey), приниматель(если не указан и функция вызвана во время обработки входящих сообщений, получателем будет тот, чьё сообение обрабатывается
def send(text,key=None,_id=None,_platform=None):
 text=str(text)
 print(text)
 if _platform==None:
  global platform
 else:
  platform=_platform
 if _id==None:
  global id
 else:
  id=_id
 if key==None:
  key=defkey
 profile=db[platform][id]
 key=keygen(key,profile)
 plats(platform).sendsometext(text,key,id)

#отправка сообщения администрации (только в вк)
def log(q):
 print(q)
 for w in admin:
  send(str(q),defkey,w,'vk')

#создаёт ссылку на пользователя. Формат входа: [id,text,platform] где text не используется и может быть чем угодно
def getlink(id,platform):
 return plats(platform).getlink(id)


