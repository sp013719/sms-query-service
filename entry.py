import os
from dcsjira.app import create_app

app = create_app(config=os.environ.get('APP_SETTING', 'config.DevelopmentConfig'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    app.config['PORT'] = port

    app.run(host=app.config['HOST'], port=port, threaded=True)
