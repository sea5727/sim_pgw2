import logging
import logging.handlers as handlers
import time

class LogManager:
    logger = None

    def __init__(self):
        if LogManager.logger != None:
            raise Exception("This class is a singleton!")
        else:
            LogManager.logger = logging.getLogger('pgw2')
            LogManager.logger.setLevel(logging.INFO)

            stream_hander = logging.StreamHandler()
            stream_formatter = logging.Formatter('%(asctime)s : %(message)s')
            stream_hander.setFormatter(stream_formatter)

            logHandler = handlers.TimedRotatingFileHandler('./log/pgw2.log', when='MIDNIGHT', interval=1, backupCount=10)
            logHandler.setLevel(logging.INFO)
            logformatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            logHandler.setFormatter(logformatter)

            LogManager.logger.addHandler(stream_hander)
            LogManager.logger.addHandler(logHandler)

    @staticmethod
    def getInstance():
        if LogManager.logger == None:
            LogManager()
        return LogManager.logger
