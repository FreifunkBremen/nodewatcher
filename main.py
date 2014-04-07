#!/usr/bin/python3

import os
import re
os.chdir(os.path.dirname(os.path.realpath(__file__)))
from NotifierManager import NotifierManager
from SourceManager import SourceManager

if __name__ == '__main__':
    s = SourceManager()
    s.update_database()
    s.quit()
    n = NotifierManager()
    n.notify_down()
    n.quit()
