"""Logging module.

Author: Sagar Paudel
Date : 2020-09-25
Description : This is logging module.
"""

import logging
import os
from utils.variables import var
from datetime import datetime

log_dir = os.path.join(var.root_dir, "logs")
if not os.path.isdir(log_dir):
    os.mkdir(log_dir)

filename = datetime.today().strftime("%Y-%m-%d.log")
# Configuration file path
log_file_path = os.path.join(log_dir, filename)

if var["logging_level"].lower() == "debug":
    level = logging.DEBUG
elif var["logging_level"].lower() == "info":
    level = logging.INFO
elif var["logging_level"].lower() == "error":
    level = logging.ERROR
else:
    level = logging.INFO

logging_format = ("%(asctime)s.%(msecs)03d  %(module)s %(funcName)s %"
                  "(lineno)d %(process)d  %(levelname)-8s %(message)s")
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(filename=log_file_path, level=level,
                    format=logging_format,
                    datefmt=date_format, filemode='a')

# define a Handler which writes
# INFO messages or higher to the sys.stderr
logger = logging.StreamHandler()
if var["enable_screen_log"].lower() == "yes":
    logger.setLevel(level)

    # create formatter
    formatter = logging.Formatter(fmt=logging_format, datefmt=date_format)

    # add formatter to ch
    logger.setFormatter(formatter)

    # add the handler to the root logger
    logging.getLogger('').addHandler(logger)

    logger = logging.getLogger(__name__)
else:
    logger = logging
