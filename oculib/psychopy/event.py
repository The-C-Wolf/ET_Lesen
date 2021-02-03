# -*- coding: utf-8 -*-
"""
Created on Fri May 02 01:01:26 2014

@author: ocunostics
"""
from psychopy import visual, event
from oculib.psychopy import UserQuit, Clock
import sys

# psychopy.event.waitKeys: Fenster wird bei Verschieben etc. nicht oder nur 
# unter bestimmten Bedingungen neu gezeichnet


# todo: maxWait testen;
# bei escape: clock anhalten und dann wieder starten -> dafuer generische Funktion 
# clock. reset, die Logik von recognition_test Zeile 198 ff verwendet

# todo: waitKeys auch als wait() implementieren: angegebene Zeit warten, keine 
# Tasten akzeptieren außer ESC

def wait(win, toDraw=None, userQuit=None, maxWait=float('inf'), show_skip=False):
    if toDraw:
        if not isinstance(toDraw, (list, tuple)):
            toDraw = [toDraw]
                     
    if userQuit is None:
        userQuit = UserQuit(win=win, show_skip=show_skip)
        
    clock = Clock()
    while clock.getTime() < maxWait:
        ret = userQuit.check()
        if ret == 'Continue':
            pass
        
        if toDraw:        
            for item in toDraw:
                item.draw()
        win.flip()
    

def waitKeys(win, toDraw=None, userQuit=None, maxWait=float('inf'), keyList=None, 
             timeStamped=False, show_skip=False):
    """
    Replacement for PsychoPy event.waitKeys, which allows for 
    continous check of Escape button press and redrawing of the window
    while in waiting state.
    
    userQuit: None or UserQuit instance with optionally set on_continue, on_quit. 
        This way you can, for example, send triggers to a recording device 

    """    
    
    if toDraw:
        if not isinstance(toDraw, (list, tuple)):
            toDraw = [toDraw]
            
            
    if userQuit is None:
        userquit = UserQuit(win=win, show_skip=show_skip)
    else: userquit = userQuit
        
    clock = Clock()
    while clock.getTime() < maxWait:
        ret = userquit.check()
        if ret == 'Continue':
            pass
        elif ret == 'Quit':
            return 'Quit', None
        elif ret == 'Skip':
            return 'Skip', None
                
        keys = event.getKeys(timeStamped=timeStamped)
        if keys:
            if timeStamped is False:
                key = keys[0]
            else:
                key, rt = keys[0]
            
            if keyList is None or key in keyList:  # todo: eleganter
                if timeStamped is False:
                    return key, None
                else:
                    return key, rt
        
        if toDraw:
            for item in toDraw:
                item.draw()
        win.flip()
            
    return 'Timeout', None

            
#####################
if __name__ == '__main__':
    win = visual.Window()
    msg = visual.TextStim(win, text='Hallo Test')
    
    print(waitKeys(win, toDraw=msg))
    
    win.close()
    