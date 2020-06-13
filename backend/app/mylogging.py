from app import mongo_settings

from mongolog.handlers import MongoHandler
import logging, os

logger = logging.getLogger('app')
# Send logs to mongodb
logger.setLevel(logging.DEBUG)

if os.environ['FLASK_ENV'] == 'production':
    logger.addHandler(
            MongoHandler.to(
                host = mongo_settings[os.environ['FLASK_ENV']]['hostname'],
                db   = mongo_settings[os.environ['FLASK_ENV']]['database'],
                collection = 'log'),
                )
