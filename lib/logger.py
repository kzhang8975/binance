import logging
import datetime as dt

def get_logger(log_dir, name, date, level):
    logger    = logging.getLogger(name)
    
    handler   = logging.FileHandler("%s/%s.%s.log" % (log_dir, name, date))
    handler.setLevel(level) 
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(level)

    return logger
