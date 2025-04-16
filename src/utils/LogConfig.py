import logging
from datetime import datetime

class LoggerConfig:
    @staticmethod
    def setup_logger(name):
        now = datetime.now()


        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logging.basicConfig(
            filename='logfile{0}.log'.format(now.strftime("%Y%m%d_%H%M%S")),  # Name of the log file
            level=logging.DEBUG,  # Set the minimum logging level
            format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
            # datefmt="%H:%M:%S"
        )
        return logger