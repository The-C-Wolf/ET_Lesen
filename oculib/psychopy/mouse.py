# -*- coding: utf-8 -*-
"""
Created on Sun Jun 07 12:54:38 2015

@author: tamm
"""
# todo: add clickedIn()?
# or provide only clickedIn() and default is clickedIn(win) to catch
# all clicks?

# Is isPressedIn(win) equivalent to get_pressed()? 


from psychopy import event
import numpy as np


class Mouse(event.Mouse):
    def __init__(self, *args, **kwargs):
        event.Mouse.__init__(self, *args, **kwargs)
        self._wasReleased = True
        self._getPressed = event.Mouse.getPressed
        
    def getPressed(self, getTime=False, blocked_until_release=False):
        """Wrap original get_pressed and add option
        to block mouse until mouse button was released.
        Return None after first press until all buttons are released.
        
        Important: Default values for getTime and blocked_until_release have to be set to False.
        Otherwise internal psychopy funcions could be influenced in an unpredictable manner.
        
        Example:
        mouse.clickReset()  # if your are interested  in reaction times
        while 1:
            button, rt = mouse.getpressed(getTime=True, blocked_until_release=True)
        
        button: [1,0,0]
        rt: [1.23., 0, 0]
        """
        if getTime:
                bt, rt = self._getPressed(self, getTime=True)
        else:
            bt = self._getPressed(self, getTime=False)
        
        if blocked_until_release and not self._wasReleased:
            if np.sum(bt) == 0: self._wasReleased = True  # no button pressed
            return None, None
        
        if np.any(bt): 
            self._wasReleased = False  # at least one button is pressed
        
        if getTime:
            return bt, rt
        else:
            return bt
    
    def clicked(self, getTime=False):
        pass # todo: same as get_pressed, but only after release of mouse
 
       
#########################
if __name__ == '__main__':
    from psychopy import visual
    import sys
    
    win = visual.Window(color='white')
    mouse = Mouse()
    
    # Pattern to check if mouse was pressed within a shape
    # if mouse.pressedIn(shape) and np.any(mouse.getPressed(blocked_until_release=True)):
    # do something
    
    
    mouse.clickReset()  # reset click timer
    while 1:
        bt, rt = mouse.getPressed(getTime=True, blocked_until_release=True)
        if np.any(bt):
            print(bt, rt)
        
        keys = event.getKeys()
        if keys:
            break
    
    win.close()
    sys.exit()
    