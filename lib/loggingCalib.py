# Created loggingCalib.py by histravelstories on 8:36 PM under Project6


import logging
def get_logger(name):
    log_format = '%(asctime)s  %(name)8s  %(levelname)5s  %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        filename='../logging/calibration.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)