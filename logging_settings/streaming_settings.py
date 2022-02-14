import logging

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
streaming_logger = logging.getLogger("streaming logger")
streaming_logger.setLevel(logging.DEBUG)
logger_handler = logging.StreamHandler()
logger_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(module)s %(processName)s  %(levelname)s: %(message)s')
logger_handler.setFormatter(formatter)
streaming_logger.addHandler(logger_handler)
