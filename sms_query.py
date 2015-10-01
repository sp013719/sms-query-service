import urllib
import subprocess
import time
from datetime import datetime
from flask import Flask
from flask import send_file
from flask import render_template
app = Flask(__name__)

message_code = {'10': 'Delivered upstream', '64': 'Queued for retry after temporary failure delivering, due to fault on handset (transient)', '24': 'Data validation failed', '25': 'You do not have sufficient credits', '26': 'Upstream credits not available', '27': 'You have exceeded your daily quota', '22': 'Internal fatal error', '23': 'Authentication failure', '28': 'Upstream quota exceeded', '29': 'Message sending cancelled', '70': 'Unknown upstream status', '11': 'Delivered to mobile', '33': 'Failed: censored', '32': "Blocked (probably because of a recipient's complaint against you)", '31': 'Unroutable', '56': 'Failed: remotely censored (typically due to content of message)', '51': 'Delivery to phone failed', '50': 'Delivery failed - generic failure', '53': 'Message expired', '52': 'Delivery to network failed', '55': 'Failed: remotely blocked (variety of reasons)', '54': 'Failed on remote network', '57': 'Failed due to fault on handset (e.g. SIM full)'}

@app.route('/get_image/<batch_id>')
def get_image(batch_id):
    filename = 'results/%s.png' % batch_id 
    url = 'http://localhost:5000/get_status/%s' % batch_id
    #url = 'http://www.google.com.tw'
    subprocess.call(['java', '-jar', 'libs/webvector-3.4.jar', url, filename, 'png'])
    #cmd = ['java', '-jar', '/vagrant/webvector-3.4.jar', url, filename, 'png']    
    #p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
    #                        stderr=subprocess.PIPE,
    #                        stdin=subprocess.PIPE)
    #out,err = p.communicate()
    #time.sleep(10)
    #print
    return send_file(filename, mimetype='image/png')

@app.route('/get_status/<batch_id>')
def get_status(batch_id):
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    url = "<your_api_url>"
    params = urllib.urlencode({'username': '<your_account>', 'password': '<your_password>', 'batch_id': batch_id})
    f = urllib.urlopen(url, params)
    s = f.readlines()

    if len(s) > 2:
    	s = s[2:]
    
    statuses = dict() 
   
    for tmp in s:
        tt = tmp.split('|')
        number = '+%s' % tt[0]
        sms_status = tt[1].replace('\n', '')
        statuses[number] = message_code[sms_status]
    
    return render_template('result.html', statuses=statuses, time_stamp=time_stamp)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, threaded=True)
