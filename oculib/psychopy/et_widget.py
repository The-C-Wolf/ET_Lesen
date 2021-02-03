# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 17:41:31 2013

@author: tamm
"""

from psychopy import visual
#from oculib.hardware import RedM as redm
import oculib.hardware._smi.iViewStruct as iViewStruct
import time

# todo: als decorator class fuer alle visual Komponenten von 
# PsychoPy implementieren


### todo: timer arbeitet mit time.clock(). Das funktioniert nur unter Windows!!!
### todo: contains fuer event data noch nicht implementiert!!!

### todo: bei Verwendung von textStim wird der Text nicht angezeigt???

### Deprecated ###
import oculib.psychopy.misc as misc
def screen2win(win, pos):
    """Deprecated. Use screen2win from oculib.psychopy.misc instead."""
    print('Warning: Deprecated. Use screen2win from oculib.psychopy.misc instead.')
    return misc.screen2win(win, pos)
    
def win2screen(win, pos):
    """Deprecated. Use win2screen from oculib.psychopy.misc instead."""
    print('Warning: Deprecated. Use win2screen from oculib.psychopy.misc instead.')
    return misc.win2screen(win, pos)
### End Deprecated ###



# prio to PsychoPy version 1.79
#class _AddInteractivity(visual._BaseVisualStim):
class _AddInteractivity(visual.BaseVisualStim):
    '''
    Funktioniert momentan nur mit units='pix'!!!
    '''
    def __init__(self, *args, **kwargs):
        #visual._BaseVisualStim.__init__(self, args[0])
        visual.BaseVisualStim.__init__(self, args[0])        
        # args[0] = win?
        
        self.mouseEnterDelay = 0.
        self.mouseLeaveDelay = 0.
        self.eyeEnterDelay   = 0.
        self.eyeLeaveDelay   = 0.
        
        
        self.targetEye = 'both'
        
        self._mouseEnterTime = None
        self._mouseLeaveTime = None
        self._eyeEnterTime   = None
        self._eyeLeaveTime   = None
        
        self._mouseSwitchCompleted = None
        self._eyeSwitchCompleted   = None        
        
        self._mouseActive  = False
        self._eyeActive    = False
        
    def setMouseDelay(self, enter=0., leave=0.):
        self.mouseEnterDelay = enter
        self.mouseLeaveDelay = leave
    
    def setEyeDelay(self, enter=0., leave=0., eye='either'):
        '''
            eye: 'left', 'right', 'both', 'either'
        '''
        self.eyeEnterDelay = enter
        self.eyeLeaveDelay = leave
    
    def mouseOver(self, x, y=None):
        inside = self.containsMouse(x, y)
        if inside:
            if self._mouseActive==True:
                completed = 2.                
                if self._mouseLeaveTime != None:
                    self._mouseLeaveTime = None
                    # mouse inside but outside process started without finishing yet
                    # todo: could be used to give smooth fade out
                    # (z.B. setze _mouseEnterTime auf _mouseLeaveTime und _mouseLeaveTime auf False ???)
            else: # self._mouseActive==False
                if not self._mouseEnterTime:
                    self._mouseEnterTime=time.clock()
                    
                if self.mouseEnterDelay<=0: 
                    completed = 1.
                    self._mouseActive=True
                else:
                    completed = (time.clock() - self._mouseEnterTime)/self.mouseEnterDelay
                    if completed>=1:
                        completed = 1.
                        self._mouseActive=True
        else: # not inside        
            if self._mouseActive==False:
                completed = 2.
                if self._mouseEnterTime != None:
                    self._mouseEnterTime = None                
                    # mouse outside but inside process started without finishing yet
                    # todo: could be used to give smooth fade out
                    # (z.B. setze _mouseLeveTime auf _mouseEnterTime und _mouseEnterTime auf False ???)                    
            else: # self._mouseActive==True
                if not self._mouseLeaveTime:
                    self._mouseLeaveTime=time.clock()
                    
                if self.mouseLeaveDelay<=0: 
                    completed = 1.
                    self._mouseActive=False
                else:
                    completed = (time.clock() - self._mouseLeaveTime)/self.mouseLeaveDelay
                    if completed>=1:
                        completed = 1.
                        self._mouseActive=False
        return(inside, completed)
                
    def eyeOver(self, x, y=None):
        inside = self.containsEye(x, y)
        if inside:
            if self._eyeActive==True:
                completed = 2.                
                if self._eyeLeaveTime != None:
                    self._eyeLeaveTime = None
                    # eye inside but outside process started without finishing yet
                    # todo: could be used to give smooth fade out
                    # (z.B. setze _eyeEnterTime auf _eyeLeaveTime und _eyeLeaveTime auf False ???)
            else: # self._eyeActive==False
                if not self._eyeEnterTime:
                    self._eyeEnterTime=time.clock()
                    
                if self.eyeEnterDelay<=0: 
                    completed = 1.
                    self._eyeActive=True
                else:
                    completed = (time.clock() - self._eyeEnterTime)/self.eyeEnterDelay
                    if completed>=1:
                        completed = 1.
                        self._eyeActive=True
        else: # not inside        
            if self._eyeActive==False:
                completed = 2.
                if self._eyeEnterTime != None:
                    self._eyeEnterTime = None                
                    # eye outside but inside process started without finishing yet
                    # todo: could be used to give smooth fade out
                    # (z.B. setze _eyeLeveTime auf _eyeEnterTime und _eyeEnterTime auf False ???)                    
            else: # self._eyeActive==True
                if not self._eyeLeaveTime:
                    self._eyeLeaveTime=time.clock()
                    
                if self.eyeLeaveDelay<=0: 
                    completed = 1.
                    self._eyeActive=False
                else:
                    completed = (time.clock() - self._eyeLeaveTime)/self.eyeLeaveDelay
                    if completed>=1:
                        completed = 1.
                        self._eyeActive=False
        return(inside, completed)
    
    def containsMouse(self, x, y=None):
        #return(self.contains(x, y))
        return(self.contains(x))    
        
    def containsEye(self, x, y=None):
        if isinstance(x, iViewStruct.SampleData):
            lpos = screen2win(self.win, (x.leftEye.gazeX, x.leftEye.gazeY))
            rpos = screen2win(self.win, (x.rightEye.gazeX, x.rightEye.gazeY))
        else: # for mouse simulation 
            if y: x = (x,y)
            lpos = screen2win(self.win, x)
            rpos = screen2win(self.win, x)            
            #raise Exception('Unknown eye data.')
            
        # SampleData or EventData                 
        linside = self.contains(lpos)
        rinside = self.contains(rpos)
         
        if self.targetEye == 'both':
            return(linside and rinside)
        elif self.targetEye == 'left':
            return(linside)
        elif self.targetEye == 'right':
            return(rinside)
        elif self.targetEye == 'either':
            return(linside or rinside)
        else:
            raise Exception('Invalid target eye parameter.')
              
class ImageStim(visual.ImageStim, _AddInteractivity):
    def __init__(self, *args, **kwargs):
        visual.ImageStim.__init__(self, *args, **kwargs)
        _AddInteractivity.__init__(self, *args, **kwargs)
                    
class TextStim(visual.TextStim, _AddInteractivity):
    def __init__(self, *args, **kwargs):
        visual.TextStim.__init__(self, *args, **kwargs)
        _AddInteractivity.__init__(self,  *args, **kwargs)            
        