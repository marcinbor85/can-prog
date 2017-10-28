import logging

from canprog import __appname__

def get_log(name):
    log = logging.getLogger(name)
    h = logging.StreamHandler()
    formatter = logging.Formatter('[%(module)-8s] [%(asctime)s,%(msecs)03d] [%(levelname)-8s] - %(message)s',datefmt='%H.%M.%S')
    h.setFormatter(formatter)
    log.addHandler(h)    
    return log

log = get_log(__appname__)

def set_level(level):
    log.setLevel(level)
    for h in log.handlers:
        h.setLevel(level)

set_level(logging.INFO)

