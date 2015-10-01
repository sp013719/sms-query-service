import urllib
import subprocess
import time

batch_id = '765877541'
filename = '%s.png' % batch_id 
url = 'http://www.google.com.tw'
subprocess.call(['java', '-jar', 'libs/webvector-3.4.jar', url, filename, 'png'])

