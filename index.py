%*
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>редактор изменений в расписании</title>
<style>
body {
  height: 100%;
}


textarea {
  width: 95vw;
  height: 77vh;
}

button {
 font-family:courier;
}

#menu{
 position: absolute;
 top: 3%;
 height: 10%;
}

#head{
 position: absolute;
 top: 0;
 height: 3%;
}

#main{
 position: absolute;
 bottom: 0;
 height: 80%;
}

</style>
</head>
<body>
<div id="head"></div>
<div id="menu"></div>
<div id="main"></div>
<script>
function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}
*%
def show(q,w):
 document.getElementById(q).innerHTML=w
show('main','<form name="mainform"><textarea name="maintext" ></textarea></form>')
show('head','''
<button onclick="save()">save</button>
<button onclick="open_s()">open</button>
''')
def defch(q,w):
 if q==undefined:
  return w
 return q
x=0
y=0
cursorstart=0
cursorend=0
edit_a=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
edit_v=''
def edit():
 check()
 l='АБВ'
 ted='<table><tr>'
 cc=0
 for e<3:
  for 1=w<12:
   o=''
   o+=String(w)
   o+=l[e]
   ted+='<td><button onclick="edit_c('+String(cc)+');return false">'
   edit_a[cc]=o
   cc+=1
   ted+=o
   ted+='</button></td>'
  ted+='</tr><tr>'
 day=new Date()
 for w<11:
  o=''
  o+=String(day.getDate()).padStart(2,'0')+'.'
  o+=String(day.getMonth()+1).padStart(2,'0')
  ted+='<td><button onclick="edit_c('+String(cc)+')">'
  edit_a[cc]=o
  cc+=1
  ted+=o
  ted+='</button></td>'
  day.setDate(day.getDate()+1)
 ted+='</tr></table>'
 show('menu',ted)
 check()
def edit_c(q):
 t=edit_a[q]
 s=document.forms.mainform.elements.maintext.value.split('\n')[y]
 s=s.split(' <<< xxx >>> ')[0].split('|')
 for w<s.length:
  s[w]=s[w].trim()
 if s.indexOf(t)==-1:
  s.push(t)
 else:
  s=s.filter(function(v,i,a){return v!=t})
 s=s.join('|')
 s+=' <<< xxx >>> '+ document.forms.mainform.elements.maintext .value.split('\n')[y].split(' <<< xxx >>> ')[1]
 d=document.forms.mainform.elements.maintext.value.split('\n')
 d[y]=s
 document.forms.mainform.elements.maintext.value=d.join('\n')
 document.forms.mainform.elements.maintext.focus()
  document.forms.mainform.elements.maintext. setSelectionRange(cursorstart,cursorend)
 check()
 return false
def save():
 check()
 download('kpml.txt', document.forms.mainform.elements.maintext.value)
def open_s():
 show('menu','''<form name="openform" onchange="open_o();return false"><input type="file" name="opentext"/></form><button onclick="edit();return false">cancel</button>''')
 check()
def open_o():
 fileo=document.forms.openform.elements.opentext.files[0]
 if fileo:
  fileo.text().then(open_t)
def open_t(text):
 document.forms.mainform.elements.maintext.value=text
 check()
 edit()
def ret(q):
 a=document.forms.mainform.elements.maintext.value.split('\n')[y]
 a=a.split(' <<< xxx >>> ')[0].split('|')
 for w<a.length:
  a[w]=a[w].trim()
 s=a.slice()
 c2d=1
 for w<a.length:
  if a[w].indexOf('.')+1:
   s[w]=new Date()
   s[w].setDate(\
    (new Date(\
     (new Date()).getFullYear(),\
     Number(a[w].split('.')[0],10)-1,\
     Number(a[w].split('.')[0],10)\
    )).getDate()+q\
   )
   s[w]=String(s[w].getDate()).padStart(2,'0')\
   +'.'+String(s[w].getMonth()+1).padStart(2,'0')
  else:
   s[w]=s[w].replace('А','1').replace('Б','2').replace('В',3)
   s[w]=Number(s[w])+q
   if s[w]%10==0:
    s[w]-=7
   if s[w]%10==4:
    s[w]+=7
   s[w]=String(s[w])
   s[w]=s[w].slice(0,s[w].length-1)+'=АБВ'[Number(s[w][s[w].length-1])]
   if s[w]=='12А':
    s[w]='5А'
    c2d=0
   if s[w]=='4В':
    s[w]='11В'
    c2d=0
   if s[w]=='В':
    s[w]='11В'
    c2d=0
 for w<a.length:
  if c2d and 1+a[w].indexOf('.'):
   pass
  else:
   a[w]=s[w]
 a=a.join('|')
 s=a
 s+=' <<< xxx >>> '+ document.forms.mainform.elements.maintext .value.split('\n')[y].split(' <<< xxx >>> ')[1]
 d=document.forms.mainform.elements.maintext.value.split('\n')
 d[y]=s
 document.forms.mainform.elements.maintext.value=d.join('\n')
 document.forms.mainform.elements.maintext.focus()
 document.forms.mainform.elements.maintext. setSelectionRange(cursorstart,cursorend)
 check()
def key(q):
 if q.ctrlKey:
  if q.which==76:
   ret(1)
   return false
  if q.which==80:
   ret(-1)
   return false
edit()
def check():
 document.forms.mainform.elements.maintext.focus()
 a=document.forms.mainform.elements.maintext.value.split('\n')
 cursorstart=defch(this.selectionStart,cursorstart)
 cursorend=defch(this.selectionEnd,cursorend)
 x=cursorstart
 y=0
 for w<:w<a.length and x-a[w].length-1>=0:
  y+=1
  x-=a[w].length+1
 today=new Date()
 date=String(today.getDate()).padStart(2,'0')
 date+='.'+String(today.getMonth()+1).padStart(2,'0')
 date=[date]
 clas=['5А']
 o=40
 for e<a.length:
  s=a[e]
  if s.indexOf(' <<< xxx >>> ') != -1:
   s=s.split(' <<< xxx >>> ')
  elif s.indexOf(' <<< xxx >>>') != -1:
   s=s.split(' <<< xxx >>>')
  elif s.indexOf(' <<< xxx >>') != -1:
   s=s.split(' <<< xxx >>')
  elif s.indexOf(' <<< xxx >') != -1:
   s=s.split(' <<< xxx >')
  elif s.indexOf(' <<< xxx ') != -1:
   s=s.split(' <<< xxx ')
  elif s.indexOf(' <<< xxx') != -1:
   s=s.split(' <<< xxx')
  elif s.indexOf(' <<< xx') != -1:
   s=s.split(' <<< xx')
  elif s.indexOf(' <<< x') != -1:
   s=s.split(' <<< x')
  elif s.indexOf(' <<< ') != -1:
   s=s.split(' <<< ')
  elif s.indexOf(' <<<') != -1:
   s=s.split(' <<<')
  else:
   s=['',s]
  if s[0].length:
   s[0]=s[0].split('|')
  else:
   s[0]=[]
  for w<s[0].length:
   s[0][w]=s[0][w].trim()
  cdate=0
  cclas=0
  for w<s[0].length:
   if s[0][w].indexOf('.')==-1:
    cclas=1
   else:
    cdate=1
  if cdate:
   date=[]
  if cclas:
   clas=[]
  for w<s[0].length:
   if s[0][w].indexOf('.')==-1:
    if cclas:
     clas.push(s[0][w])
   else:
    if cdate:
     date.push(s[0][w])
  if cdate==0:
   s[0]=s[0].concat(date)
  if cclas==0:
   s[0]=s[0].concat(clas)
  s[0]=s[0].join('|')
  s[0]=s[0].padStart(40,' ')
  o=(s[0]+' <<< xxx >>> ').length
  s=s.join(' <<< xxx >>> ')
  a[e]=s
 a=a.join('\n')
 document.forms.mainform.elements.maintext.value=a
 if x<o:
  document.forms.mainform.elements.maintext.focus()
  document.forms.mainform.elements.maintext. setSelectionRange(cursorstart+o-x,cursorend+o-x)
setInterval(check,500)
document.onkeydown=key
document.forms.mainform.elements.maintext.onkeydown=check
document.forms.mainform.elements.maintext.onkeyup=check
document.forms.mainform.elements.maintext.onkeypress=check
document.forms.mainform.elements.maintext.onmousedown=check
document.forms.mainform.elements.maintext.onmouseup=check
document.forms.mainform.elements.maintext.onmousepress=check
%*
</script>
</body>
</html>
*%
