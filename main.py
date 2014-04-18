#!/usr/bin/python3

import os
import re
import logging
import argparse
os.chdir(os.path.dirname(os.path.realpath(__file__)))
from NotifierManager import NotifierManager
from SourceManager import SourceManager

if __name__ == '__main__':
    def log_level(level_string):
        return getattr(logging, level_string.upper())

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log-level', default=logging.WARNING, type=log_level, help='Set log level (DEBUG, INFO, WARNING, ERROR)')
    args = parser.parse_args()
    if args.log_level:
        logging.basicConfig(level=args.log_level)
    s = SourceManager()
    s.update_database()
    s.quit()
    n = NotifierManager()
    n.notify_down()
    n.quit()
