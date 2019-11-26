import logging
import logging.handlers as handlers
import time
from config.configure import Config

class LogManager:
    logger = None

    def __init__(self):
        if LogManager.logger != None:
            raise Exception("This class is a singleton!")
        else:
            config = Config()
            LogManager.logger = logging.getLogger('pgw2')
            LogManager.set_loglevel(config.log_level)

            if config.std == 'on':
                LogManager.add_stream_handler()
            
            if config.log_path is not None:
                LogManager.add_log_file_handler(config.log_path)

    @staticmethod
    def set_loglevel(log_level):
        LogManager.logger.setLevel(logging.getLevelName(log_level))

    @staticmethod
    def add_log_file_handler(log_path):
        if any([handler for handler in LogManager.logger.handlers if type(handler) == handlers.TimedRotatingFileHandler]):
            return
        logHandler = handlers.TimedRotatingFileHandler(log_path, when='MIDNIGHT', interval=1, backupCount=10)
        logformatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logHandler.setFormatter(logformatter)
        LogManager.logger.addHandler(logHandler)

    @staticmethod
    def del_log_file_handler():
        for handler in LogManager.logger.handlers:
            if type(handler) == logging.TimedRotatingFileHandler:
                LogManager.logger.removeHandler(handler)

    @staticmethod
    def add_stream_handler():
        # 중복 체크
        if any([handler for handler in LogManager.logger.handlers if type(handler) == logging.StreamHandler]):
            return
        stream_hander = logging.StreamHandler()
        stream_formatter = logging.Formatter('%(message)s')
        stream_hander.setFormatter(stream_formatter)
        LogManager.logger.addHandler(stream_hander)

    @staticmethod
    def del_stream_handler():
        for handler in LogManager.logger.handlers:
            if type(handler) == logging.StreamHandler:
                LogManager.logger.removeHandler(handler)
            

    @staticmethod
    def getInstance():
        if LogManager.logger == None:
            LogManager()
        return LogManager.logger
