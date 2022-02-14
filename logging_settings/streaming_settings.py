import logging

logging.basicConfig(encoding='utf-8', level=logging.WARNING)
streaming_logger = logging.getLogger("streaming logger")
streaming_logger.setLevel(logging.WARNING)
logger_handler = logging.StreamHandler()
logger_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s %(module)s %(processName)s  %(levelname)s: %(message)s')
logger_handler.setFormatter(formatter)
streaming_logger.addHandler(logger_handler)

if __name__ == '__main__':
    pass
