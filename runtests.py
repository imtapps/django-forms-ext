#!/usr/bin/env python
import sys
import os

def runtests(*test_args, **kwargs):
    current_dir = os.path.dirname(__file__)
    manage_file = os.path.abspath(os.path.join(current_dir, "example", "manage.py"))

    os.system("python %s test forms_ext" % manage_file)
    os.system("python %s harvest -a sample -S" % manage_file)
    sys.exit()