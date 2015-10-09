import urllib
import subprocess
import os
from datetime import datetime
from dcsjira.service.dcsportal import Dcsportal
from flask import Flask, send_file, render_template, current_app


app = Flask(__name__)

project_root_dir = os.path.dirname(os.path.realpath('__file__'))
account = os.environ.get('bulksms_acc')
password = os.environ.get('bulksms_pwd')
message_code = {'10': 'Delivered upstream',
                '64': 'Queued for retry after temporary failure delivering, due to fault on handset (transient)',
                '24': 'Data validation failed',
                '25': 'You do not have sufficient credits',
                '26': 'Upstream credits not available',
                '27': 'You have exceeded your daily quota',
                '22': 'Internal fatal error', '23': 'Authentication failure',
                '28': 'Upstream quota exceeded', '29': 'Message sending cancelled',
                '70': 'Unknown upstream status', '11': 'Delivered to mobile',
                '33': 'Failed: censored',
                '32': "Blocked (probably because of a recipient's complaint against you)",
                '31': 'Unroutable', '56': 'Failed: remotely censored (typically due to content of message)',
                '51': 'Delivery to phone failed', '50': 'Delivery failed - generic failure',
                '53': 'Message expired', '52': 'Delivery to network failed',
                '55': 'Failed: remotely blocked (variety of reasons)',
                '54': 'Failed on remote network',
                '57': 'Failed due to fault on handset (e.g. SIM full)'}


def create_app(config='config.DevelopmentConfig'):
    app.config.from_object(config)

    return app


@app.route('/get_image/<batch_id>/<group_id>')
def get_image(batch_id, group_id):
    url = 'http://%s:%s/get_status/%s/%s' % (app.config['HOST'], app.config['PORT'], batch_id, group_id)
    file_name = '%s/%s.png' % (app.config['RESULT_FOLDER'], batch_id)
    file_path = os.path.join(project_root_dir, file_name)

    try:
        cmd = ['java', '-jar', os.path.join(project_root_dir, 'libs/webvector-3.4.jar'), url, file_name, 'png']

        if subprocess.call(cmd) == 0:
            return send_file(file_path, mimetype='image/png')
        raise ValueError('execute command failed')
    except ValueError as ex:
        current_app.logger.error(ex.message)

        return render_template('error.html')


@app.route('/get_status/<batch_id>/<group_id>')
def get_status(batch_id, group_id):
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    params = urllib.urlencode({'username': account, 'password': password, 'batch_id': batch_id})
    res = urllib.urlopen(app.config['SMS_API_URL'], params)

    current_app.logger.debug('http response code: %d' % res.code)

    if res.code != 200:
        return render_template('error.html')

    content = res.readlines()
    api_result = content[0].split('|')

    current_app.logger.debug('api result: %s' % content[0])

    if int(api_result[0]) != 0:
        return render_template('error.html', error_msg=api_result[1])

    client = Dcsportal(app.config['PORTAL_API_URL'])
    group_detail = client.get_group_detail(group_id)
    statuses = []

    for line in content[2:]:
        tmp = line.split('|')
        number = '+%s' % tmp[0]
        display_name = group_detail.get(number, 'Unknown')
        sms_status = message_code.get(tmp[1].strip(), 'Unknown')

        statuses.append({'name': display_name, 'number': number, 'status': sms_status})

    return render_template('result.html', statuses=statuses, time_stamp=time_stamp, batch_id=batch_id)
