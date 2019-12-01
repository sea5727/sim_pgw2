import logging
import logging.handlers as handlers
from pgw2memory import pgw2Config as config


class LogManager:
    logger = None

    def __init__(self):
        if LogManager.logger is not None:
            raise Exception("This class is a singleton!")
        else:
            LogManager.logger = logging.getLogger('pgw2')
            LogManager.set_loglevel(config.log_level)

            if config.log_stderr == 'on':
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
        # datefmt="%Y-%m-%d %H:%M:%S"
        logformatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(name)s - %(message)s')
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
        stream_formatter = logging.Formatter('[%(asctime)s]%(message)s')
        stream_hander.setFormatter(stream_formatter)
        LogManager.logger.addHandler(stream_hander)

    @staticmethod
    def del_stream_handler():
        for handler in LogManager.logger.handlers:
            if type(handler) == logging.StreamHandler:
                LogManager.logger.removeHandler(handler)

    @staticmethod
    def getInstance():
        if LogManager.logger is None:
            LogManager()
        return LogManager.logger


pgw2logger = LogManager.getInstance()
# log를 찍으려면 pgw2logger 를 사용,
# loglevel 등 설정을 변경하려면 LogManager 를 받아 사용.
# ex) 로거 예
# from logger import pgw2logger as logger
# logger.info('test')
# ex) 로그레벨 세팅 예
# from logger import LogManager as logManager
# logManager.set_loglevel('INFO')
