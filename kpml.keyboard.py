

#здесь описаны клавиатуры


#формат клавиатуры:
#
#скнопка+скнопка+скнопка
#скнопка+скнопка+скнопка
#скнопка+скнопка+скнопка
#
#где с это цвет из набора r - красный, g - зелёный, b - синий, w - белый
#цвета определены для пк версии в светлой теме без цветоискажающих программ. На телефоне могут отличаться
#все изменяющиеся кнопки, например, включить/отключить пустые сообщения, описаны внутри функции keygen
#пустые строки игнорируются
#изменяющиеся значения описываются в {} в формате тернарного оператора, который выглядит так:
#значение if условие else значение
#при этом значением тернарного оператора может быть тоже тернарный оператор в круглых скобках, таким образом, значений может быть больше чем 2



#клавиатура по умолчанию
defkey='''
gполучить изменения
wнастройки
rсообщение об ошибке
'''

#клавиатура быстрой настройки
optkey='''
gуказать класс
gуказать время
wрасширенные настройки
rотмена
{'rотключить рассылку' if db[prof][id]['need'] else 'gвключить рассылку'}
'''

#клавиатура настроек
setkey='''
bизменить кол-во оповещений в день
bизменить кол-во отслеживаемых классов
rотмена
{'gвключить пустые сообщения' if db[prof][id]['dis_empty'] else 'rотключить пустые сообщения'}
'''

#клавиатура отмены
backey='rотмена'

#клавиатура выбора класса
#символ '\u2000' похож на ' ', и служит отличителем того, ввёл пользователь время сам или нажал на кнопку
clskey='''
w11\u2000А+w10\u2000А+w9\u2000А+w8\u2000А+w7\u2000А
w11\u2000Б+w10\u2000Б+w9\u2000Б+w8\u2000Б+w7\u2000Б
w11\u2000В+w10\u2000В+w9\u2000В+w8\u2000В+w7\u2000В
w6\u2000А+w5\u2000А+w4\u2000А+w3\u2000А+w2\u2000А
w6\u2000Б+w5\u2000Б+w4\u2000Б+w3\u2000Б+w2\u2000Б
w6\u2000В+w5\u2000В+w4\u2000В+w3\u2000В+w2\u2000В
w1\u2000А+w1\u2000Б+w1\u2000В+rотмена'''

#клавиатура выбора времени
#символ '\u205a' похож на ':', и служит отличителем того, ввёл пользователь время сам или нажал на кнопку
timkey='''
w04\u205a00+w04\u205a30+w05\u205a00+w05\u205a30
w06\u205a00+w06\u205a30+w07\u205a00+w07\u205a30
w07\u205a00+w07\u205a30+w09\u205a00+w09\u205a30
w10\u205a00+w10\u205a30+w11\u205a00+w11\u205a30
w12\u205a00+w12\u205a30+w13\u205a00+w13\u205a30
w14\u205a00+w14\u205a30+w15\u205a00+w15\u205a30
w16\u205a00+w16\u205a30+w17\u205a00+w17\u205a30
w18\u205a00+w18\u205a30+w19\u205a00+w19\u205a30
w20\u205a00+w20\u205a30+w21\u205a00+w21\u205a30
w22\u205a00+w22\u205a30+w23\u205a00+rотмена
'''

#функция, которая обрабатывает все изменяемые объекты
def keygen(id,key,prof):
 #id - получатель, обязательный параметр, key - клавиатура, по умолчанию, defkey
 while '{' in key and '}' in key:
  key=key.split('{',1)[0]+eval(key.split('{',1)[1].split('}',1)[0])+key.split('}',1)[1]
 return key
