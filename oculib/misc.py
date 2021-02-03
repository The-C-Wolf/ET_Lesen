# -*- coding: utf-8 -*-
"""
Created on Fri Jun 05 15:06:32 2015

@author: tamm
"""
from __future__ import print_function
import sys 

class Struct(object):
    """General purpose struct object.
    
    obj1 = Struct()
    obj1.a = 10
    obj1.b = 20
    
    obj2 = Struct(a=10, b=20)
    """
    
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def warning(*objs):
    """Print warning to stderr."""
    print("Warning: ", *objs, file=sys.stderr)