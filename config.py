class Config(object):
    DEBUG = False
    TESTING = False

    # bulksms api
    API_URL = 'http://usa.bulksms.com/eapi/status_reports/get_report/2/2.0'
    HOST = '0.0.0.0'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '127.0.0.1'


class DevelopmentContainerConfig(DevelopmentConfig):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
