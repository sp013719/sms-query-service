import urllib
import subprocess
import time

batch_id = '765877541'
filename = '%s.png' % batch_id 
url = 'http://localhost:5000/get_status/%s' % batch_id
subprocess.call(['java', '-jar', '/vagrant/webvector-3.4.jar', url, filename, 'png'])

