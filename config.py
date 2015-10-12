class Config(object):
    DEBUG = False
    TESTING = False

    # bulksms api
    SMS_API_URL = 'http://usa.bulksms.com/eapi/status_reports/get_report/2/2.0'
    HOST = '0.0.0.0'

    RESULT_FOLDER = 'results'
    PORTAL_API_URL = 'http://dcs-portal.trendmicro.com/TMPrivilege/dcsinterface'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '127.0.0.1'


class DevelopmentContainerConfig(DevelopmentConfig):
    HOST = '0.0.0.0'


class TestingConfig(Config):
    TESTING = True
