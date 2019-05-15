import pytest
import os
import sys

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)

if PARENT not in sys.path:
    sys.path.insert(0, PARENT)
if HERE not in sys.path:
    sys.path.insert(0, HERE)
