import os

basedir = os.path.abspath(os.path.dirname(__file__))


# Main configuration
class Config(object):
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

	#Database
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'nigdy-nie-zgadniesz'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False


# Heroku deployment
class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False
    LOG_TO_STDOUT = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

# Local postgres
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/lotdash_dev"


class TestingConfig(Config):
    TESTING = True