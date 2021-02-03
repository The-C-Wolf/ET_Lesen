# -*- coding: utf-8 -*-
"""
Created on Fri May 02 17:15:45 2014

@author: ocunostics
"""

from psychopy.core import Clock as _Clock
import types


class Clock(_Clock):
    """
    On some windows machines Clock.reset(newT) gives negative or 
    far to large values. This class checks the new time and tries to 
    deal with this problem.
    
    """
    def __init__(self, *args, **kwargs):
        _Clock.__init__(self, *args, **kwargs)  # _Clock is not derived from object, so super() does not work here
        
        self._reset = types.MethodType(_Clock.reset, self)
        
    def reset(self, newT=0.0):
        self._reset(newT=newT)
        if self.getTime() < newT or self.getTime() > newT+1:  # +1 is an arbitrary upper bound
            # to prevent reseted tmes like 33303.xxx 
            self._reset(newT=-newT)
            if self.getTime() < newT or self.getTime() > newT+1:            
                raise Exception('Timer problem when resetting Clock.')
 
               
###################
if __name__ == '__main__':
    print('--- New Clock---')    
    myclock = Clock()
    myclock.reset()
    print(myclock.getTime())

    myclock.reset(newT=10)
    print(myclock.getTime())

    myclock.reset(newT=-10)  
    print(myclock.getTime())    
    
    print('--- PsychoPy Clock---')
    myclock = _Clock()
    myclock.reset()
    print(myclock.getTime())

    myclock.reset(newT=10)
    print(myclock.getTime())

    myclock.reset(newT=-10)  
    print(myclock.getTime())    
    
""" Example output
    --- New Clock---
    1.03749116533e-05
    10.0000087538
    -9.99999189461
    --- PsychoPy Clock---
    2.59372609435e-06
    -9.99999675784
    10.0000032422
"""