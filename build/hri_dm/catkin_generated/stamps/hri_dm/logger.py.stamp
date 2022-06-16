import os
import logging
import logging.handlers

_logger = logging.getLogger('cal-tek_logger')

SYSLOG_ADDRESS = '/dev/log'

PRIORITIES = {
    'CRITICAL': 5,
    'ERROR': 3,
    'WARNING': 2,
    'DEBUG': 1,
    'INFO': 0
}

_levelId = None
handler = None

def initLog():
    ''' Sets _levelID and handler
    '''
    global _levelId, handler
    _levelId = -1

    if os.path.exists(SYSLOG_ADDRESS):
        handler = logging.handlers.SysLogHandler(address=SYSLOG_ADDRESS)
        _logger.addHandler(handler)
    else:
        handler = None

def Log(level, *args):
    ## \brief Logging function
    # \param Log Level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    # \param Logging data
    if PRIORITIES[level] >= _levelId:
        text = ""
        for arg in args:
            text = text + " " + str(arg)
        text = text[1:]
        if handler is not None:
            if level == 'CRITICAL':
                _logger.critical(text)
            elif level == 'ERROR':
                _logger.error(text)
            elif level == 'WARNING':
                _logger.warning(text)
        print(text)
