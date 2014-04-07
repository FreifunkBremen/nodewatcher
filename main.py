#!/usr/bin/python3

import re
from NotifierManager import NotifierManager
from SourceManager import SourceManager

if __name__ == '__main__':
    s = SourceManager()
    s.update_database()
    s.quit()
    n = NotifierManager()
    n.notify_down()
    n.quit()
