#!/usr/bin/env python
#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from handler.operationserver import CreateStream
from handler.operationserver import GetStream

url = [
    (r'/createstream', CreateStream),
    (r'/getstream', GetStream),
]
