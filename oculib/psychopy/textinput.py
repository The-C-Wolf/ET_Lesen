# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 00:38:28 2014

@author: ocunostics

todo:
- Zeilenumbruch
- setFillColor, setLineColor implementieren; 
 evtl. besser: TextInput ist abgeleitet von Frame?



Based on textStimuli_with_textResponse.py:
https://groups.google.com/forum/#!topic/psychopy-users/lE_bTMHUAoU

"""

### ACHTUNG: Momentan nur mit units='pix'!!!

from psychopy import visual, event
from oculib.psychopy import Frame, Clock, RadioButton  # RadioButton only imported for 
# hack to allow key up and down to switch between TextInput fields 
import types



# todo: warum ist Tippen von Buchstaben schneller als loeschen oder cursor bewegen???

# show() kann eigentlich weg?; bzw. show() verwenden, wenn ich wait_time oder wait bis press
# nicht extern kontrollieren moechte.
# todo: win.flip() - wait for sync abschalten!?
class TextInput(visual.TextStim):
    def __init__(self, win=None, parent=None, cursor='|', cursor_freq=2, stuff_to_draw=[],
                 max_char=None, fillColor=None, lineColor=None, width=60, frameHeight=None,
                 max_wait_time=None, **kwargs):
        """
        stuff_to_draw: Workaround to pass additional visual components. A better way would be to reimplement
        TextInput as a Frame with a textinput field???
        todo: stuff_to_draw besser zu show(stuff_to_draw)
        """
        # super(TextInput, self).__init__(*args, **kwargs)  # nicht von object abgeleitet
        visual.TextStim.__init__(self, win=win, **kwargs)
        self._clone = visual.TextStim(win=win, **kwargs)  # create clone
        
        self._win = win
        if 'text' in kwargs:
            self.setText(text=kwargs['text'])
        else:
            self.setText(text='')
         
        self.parent = parent 

        self._max_char = max_char            
            
        
        self._cindpos = 0  # cursor index position                
        pos = self._cpos()
   
        kwargs['text'] = cursor
        kwargs['pos'] = pos
        self._cursor = visual.TextStim(self._win, **kwargs)
        
        self._cursor_onoff_duration = 1./cursor_freq  # sec
        self._cursor_clock = Clock()
        self._show_cursor = True
        self._max_wait_time = max_wait_time
        self._stuff_to_draw = stuff_to_draw
        
        # Background and Frame
        # todo: wenn kein width angegeben, dann aus max_char per pygletTextObj._layout.content_width
        # mit entsprechender Anzahl an "M"s berechnen
       
        # set pos to left alignment
        border = 3
        pos = (self.pos[0]-border, self.pos[1]-border-3)
        if frameHeight is None:
            frameHeight = self.height+50
        self.frame = Frame(self._win, units='pix', pos=pos, alignHoriz='left',
                           width=width, height=frameHeight, roundness=3, 
                           lineColor=lineColor, fillColor=fillColor)
                           # todo: warum self.height+50 fuer frame???
        
            
        # handle key press of letters and symbols
        # (event.getKeys liefert modifier und Buchstaben getrennt; onText liefert direkt z.B. 'A'
        # wenn Shift + 'a' gedrueckt wurden)
        self._orig_onText = self._win.winHandle.on_text 
        self._win.winHandle.on_text = self._onText
        
        self._accept_input = True

        self._draw = types.MethodType(visual.TextStim.draw, self)
        
    @property 
    def accept_input(self):
        return self._accept_input
        
    @accept_input.setter
    def accept_input(self, status):
        self._accept_input = bool(status)
        if self._accept_input is False:
            self._win.winHandle.on_text = self._orig_onText
        else:
            self._win.winHandle.on_text = self._onText
            
    def contains(self, x, y=None):
        # Has to be implemented so that for example TextInput object can be used
        # as part of a RadioButton
        return self.frame.contains(x, y)
    
    def draw(self):
        """todo: auf nur ein draw() reduzieren"""
        if self.accept_input and self._cursor_clock.getTime() > self._cursor_onoff_duration:
            self._show_cursor = not self._show_cursor
            self._cursor_clock.reset()
        
            for key in event.getKeys():
                #print('1:', key)
                #quit at any point
                if key == 'escape':
                    pass
                    # todo: pause
                    #myWin.close()
                    #core.quit()
                elif key == 'return':
                    if self.parent and isinstance(self.parent, RadioButton):
                        self.parent.focus_next()
                    else:
                        self.accept_input = False
                        return self.text
                elif key == 'down':
                    if self.parent and isinstance(self.parent, RadioButton):
                        self.parent.focus_next()
                elif key == 'up':
                    if self.parent and isinstance(self.parent, RadioButton):
                        self.parent.focus_prev()
                elif key == 'delete':  # delete right character
                    try:
                        self.setText(text=self.text[:self._cindpos] + self.text[self._cindpos+1:])  
                    except IndexError:
                        pass
                elif key == 'backspace':  # delete left character
                    self.backspace()
                elif key == 'left':
                    if self._cindpos > 0:
                        self._cindpos -= 1
                        self._cursor.setPos(self._cpos())
                elif key == 'right':
                    if self._cindpos < len(self.text):
                        self._cindpos += 1
                        self._cursor.setPos(self._cpos())
            
        
        for item in self._stuff_to_draw:
            item.draw()

        # todo: Warum funktioniert hier 'if self.frame:' nicht???
        if self.frame is not None:
            self.frame.draw()
        
        self._draw()        
        if self.accept_input and self._show_cursor:
            self._cursor.draw()
        
    
    def show(self):
        """
        Keep tracking keyboard input until return key is pressed or max_wait_time is reached.
        
        """
        if self._max_wait_time:
            runtime = Clock()

        while 1:
            if self._max_wait_time and runtime.getTime() >= self._max_wait_time:
                return self.text
            
            ret = self.draw()
            if ret:
                return ret
            else:
                self._update()

    def _onText(self, key):
        """Handle ASCII input"""
        if self._max_char and (len(self.text) < self._max_char):
            if ord(key) > 31 :  # allow ascii codes starting with 32 = space
                self.setText(text=self.text[:self._cindpos] + key + self.text[self._cindpos:])
                self._cindpos += 1
                self._cursor.setPos(self._cpos())
         
    def _cpos(self):
        """Calculate cursor position from cursor index position."""
        #print(self._cindpos)        
        self._clone.setText(self.text[:self._cindpos])
        #print(self._clone.text)
        #import pdb; pdb.set_trace()
        
        #pos = (self._clone._pygletTextObj._layout.x, self._clone._pygletTextObj._layout.y) 
        pos = self._clone.pos
        #print(pos, self._clone._pygletTextObj._layout.content_width)        
        #print(pos[0]+self._clone._pygletTextObj._layout.content_width, pos[1])
        return(pos[0]+self._clone._pygletTextObj._layout.content_width, pos[1])
        
    def _update(self):    
        self._win.flip()
        
    def backspace(self):
        """
        Put in separate function so that this can be called from outside
        (e.g. to remove letter f after pressing "Forsetzen" in UserQuit.check()).

        """
        if self._cindpos > 0:
            try:
                self.setText(text=self.text[:self._cindpos-1] + self.text[self._cindpos:])
                self._cindpos -= 1
                self._cursor.setPos(self._cpos())
            except IndexError:
                pass  
                   
        
##################
# geht nur fuer alignHoriz = 'left'!!!!!        
# raise Exception wenn nicht Pyglet!!! (greife auf pyglet-calls zurueck!)
        
if __name__ == '__main__':
    # besser: bette textinput in key-event ein!!!
    # d.h. show() auslagern! --> testen
    # dann könnte man auf "stuff_to_draw()" verzichten    
    mode = 2
    
    if mode == 1:  # simple demo
        win = visual.Window((800,600), units='pix')
        stuff_to_draw = []
        stuff_to_draw.append(visual.TextStim(win, 'Bitte geben Sie einen Text ein.\nReturn beendet die Eingabe.',
                                          pos=(0.,0.8)))
        myinput = TextInput(win=win, pos=(-100.,50), stuff_to_draw=stuff_to_draw, wrapWidth=400, 
                            cursor='|', text='', units='pix', alignHoriz='left',
                            fillColor='green', lineColor='red', max_char=10, width=100, height=40)
        ret = myinput.show()
        print('Input: {0}'.format(ret))
        win.close()
    elif mode == 2:  # mouse clickable input fields (via radiobutton)
        def on_select(self):
            self.frame.setFillColor('lightblue')
            self.accept_input = True
        
        def on_deselect(self):
            self.frame.fillColor = 'green'
            self.accept_input = False

        win = visual.Window((800,600), units='pix')
        mouse = event.Mouse(win=win)
        mouse.setVisible(True)
        
        stuff_to_draw = []
        stuff_to_draw.append(visual.TextStim(win, 'Bitte geben Sie einen Text ein.',
                                          units='pix', pos=(0.,-200)))
        
       
             
        myinput1 = TextInput(win=win, pos=(-100.,120), wrapWidth=400, 
                            cursor='|', text='', units='pix', alignHoriz='left',
                            max_char=10, width=100, height=40)
        myinput1.on_select = types.MethodType(on_select, myinput1)
        myinput1.on_deselect = types.MethodType(on_deselect, myinput1)
        
        
        myinput2 = TextInput(win=win, pos=(100.,50), wrapWidth=400, 
                            cursor='|', text='', units='pix', alignHoriz='left',
                            max_char=10, width=100, height=40)
        myinput2.on_select = types.MethodType(on_select, myinput2)
        myinput2.on_deselect = types.MethodType(on_deselect, myinput2)
        
        rb = RadioButton(win, mouse, name='myname')  
        rb.add_item(myinput1, select=False)
        rb.add_item(myinput2, select=True)

        while 1:
            for item in stuff_to_draw:
                item.draw()
            rb.draw()
            win.flip()
            
      
        win.close()

########################################
########################################
#class TextInput_old(visual.TextStim):
#    def __init__(self, win=None, cursor='_', cursor_freq=2, stuff_to_draw=[],
#                 max_wait_time=None, **kwargs):
#        """
#        stuff_to_draw: Workaround to pass additional visual components. A better way would be to reimplement
#        TextInput as a Frame with a textinput field???
#        todo: stuff_to_draw besser zu show(stuff_to_draw)
#        # max_wait_time to show()
#        """
#        # super(TextInput, self).__init__(*args, **kwargs)  # nicht von object abgeleitet
#        visual.TextStim.__init__(self, win=win, **kwargs)
#        
#        self._win = win
#        
#        self._cursor = cursor
#        self._cursor_onoff_duration = 1./cursor_freq  # sec
#        self._cursor_clock = Clock()
#        self._show_cursor = True
#        self._max_wait_time = max_wait_time
#        self._stuff_to_draw = stuff_to_draw
#        if 'text' in kwargs:
#            self.setText(text=kwargs['text'])
#        else:
#            self.setText(text='')
#        
#    def show(self):
#        """
#        Keep tracking keyboard input until return key is pressed or max_wait_time is reached.
#        
#        """
#        if self._max_wait_time:
#            runtime = Clock()
#
#        while 1:
#            if self._max_wait_time and runtime.getTime() >= self._max_wait_time:
#                return self.text
#
#            for key in event.getKeys():
#                #print(key)
#                #quit at any point
#                if key == 'escape':
#                    pass
#                    # todo: pause
#                    #myWin.close()
#                    #core.quit()
#                elif key == 'return':
#                    return self.text
#                    
#                    # Return als Zeilenumbruch (dann muss ander Moeglichkeit 
#                    # zum Beenden der Eingabe gefunden werden): 
#                    # self.setText(text=self.text + '\n')
#                elif key == 'delete':  # delete right character
#                    try:
#                        self.setText(text=self.text[:-1])  
#                    except IndexError:
#                        pass  # empty string
#                elif key == 'backspace':  # delete left character
#                    pass
#                elif key == 'space':
#                    self.setText(text=self.text + ' ') 
#                elif key == 'period':
#                    self.setText(text=self.text + '.')
#                elif key == 'comma':
#                    self.setText(text=self.text + ',')
#                elif key == 'left':
#                    pass
#                elif key == 'right':
#                    pass
#                elif key in ('lshift','rshift'):
#                    pass #do nothing when some keys are pressed            
#                else:
#                    if len(key) > 1:
#                        pass  # ignore function keys etc.
#                    else:
#                        self.setText(text=self.text + key)
#            self._update()
#            
#    def _update(self):
#        if self._cursor_clock.getTime() > self._cursor_onoff_duration:
#            self._show_cursor = not self._show_cursor
#            self._cursor_clock.reset()
#        
#        if self._show_cursor:
#            self.setText(text=self.text + self._cursor)  # set cursor
#        else: 
#            self.setText(text=self.text + ' ')
#
#        for item in self._stuff_to_draw:
#            item.draw()
#        self.draw()
#        self._win.flip()
#        self.setText(text=self.text[:-1])  # remove cursor