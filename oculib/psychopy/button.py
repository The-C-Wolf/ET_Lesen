# -*- coding: utf-8 -*-
"""
Created on Sat May 16 22:12:30 2015

@author: tamm
"""

from psychopy import visual
from oculib.psychopy import Frame

# todo: provide: isPressed, isClicked (=isPressed and Released in Button), isReleased 
# todo: reset mouseclick (im  Moment on_click permanent waerend eines Klicks aufgerufen)
# besser: on_press, on_release?

###
# Achtung: Alle Elemente auf units='pix' setzen
### sonst: andere units nachimplementieren!
class Button(Frame):
    def __init__(self, win=None, text='Button', pos=(0,0), name=None, textColor='black', textHeight=24,
                 fillColor='lightblue', lineColor='red', units='pix',
                 mouse=None, *args, **kwargs):
        Frame.__init__(self, win=win, pos=pos, fillColor=fillColor, lineColor=lineColor, units=units, 
                       *args, **kwargs)
        self._win = win
        self._mouse = mouse
        self._name = name
        
        self._text = self.add(visual.TextStim(win, text=text, 
                                         height=textHeight, color=textColor,
                                         units='pix'))
    
        self._mouse_is_over = False
        self._mouse_is_clicked = False
        
    def on_click(self):
        """Override"""
        if not self._mouse_is_clicked:
            self._mouse_is_clicked is True
        
        
    def on_mouse_over(self):
        """Override"""
        if not self._mouse_is_over:
            self._mouse_is_over = True
            self.setFillColor('green')
        
        
    def draw(self):
        if self._mouse:
            if (self._mouse_is_clicked is False) and (self._mouse.getPressed()[0]==1) and self.contains(self._mouse):  # start left mouseclick
                self.on_click()
            
            if self._mouse_is_clicked is True and self._mouse.getPressed()[0]==0: 
                if self.contains(self._mouse):  # mouse released within button: start button action
                    self.on_click()
                
            if self.contains(self._mouse.getPos()):
                self.on_mouse_over()
            else: 
                if self._mouse_is_over is True:
                    self._mouse_is_over = False
                    self.setFillColor('lightblue')
        
        Frame.draw(self)