#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2014 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-03-29
#

"""
"""

from __future__ import print_function, unicode_literals

import os
import subprocess
from workflow import Workflow


def main(wf):
    cachepath = wf.cachefile('url')
    if os.path.exists(cachepath):
        with open(cachepath, 'rb') as file:
            url = file.read().strip()
            subprocess.call(['open', url])


if __name__ == '__main__':
    wf = Workflow()
    wf.run(main)
