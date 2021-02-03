# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 20:27:35 2014

@author: ocunostics
"""

# todo: radio button items von BaseVisualStim und RadioButtonItem ableiten
# RadioButtonItem: Definiert Interface:
# on_select, on_deselect: aufgerufen bei click
# init mit Option setze auf slected, deselected
# Achtung: Aufruf von on_deselect beim Initialisieren von RadioButton class
# ist schlecht, weil gegebenenfalls dann auch alles Aktionen ausgefuehrt werden,
# die bein einem Deselection Mausklick ausgefuehrt werden sollen (z.B
# RT wegschreiben und aehnliches)  
# Loesung momentan: neue Methode add_item_new und Kompatibilitaet mit altem 
# Code nicht zu gefaehrden

# todo: statt type um items mit Methoden on_select und on_deselect auszustatten,
# erzeuge subclass radio_button_item mit stubs fuer diese Funktionen (und Vorbelegung: Not implemented yet)
# (see examle sls.py BA Valentina 2015)
# Achtung: brauche eigene TextStim-Klasse, weil nur diese "contain" enthaelt
# todo: Braucht RadioButton ein pseudo- pos() Attribut?
# Ansonsten ist Page().add(RadioButton) momentan nicht moeglich

# todo: Wenn main in Demo-Beispiel (if __name__=='__main__)
# win.flip() weglaesst und Fenster mit der Maus bewegt, taucht trotzdem eine (wenn auch haessliche) Anzeige des
# Textes auf. Das duerfte eigentlich nicht sein und sieht nach einem Bug in Psychopy aus!!!


from psychopy import visual, event
from oculib.psychopy import TextStim

class RadioButton(object):
    """
    Manages BaseVisualStim items to mimic radio button functionality.
    """
    def __init__(self, win, mouse, name='MyRadioButton', 
                 deselect_when_click_on_selected=False):
        """
        
        """
        self._win = win
        self._mouse = mouse
        self._deselect_when_click_on_selected = deselect_when_click_on_selected

        self._items = []
        self._selected_item = None
        self._changed = False
        self.name = name
        
        if not hasattr(self._mouse, '_wasReleased'):
            self._mouse._wasReleased = True
            
    def add_item(self, obj, select=False):
        """Item has to be a child of BaseVisualStim.
            Last added item with select=True is selectd.  
            
        """
        if not isinstance(obj, visual.BaseVisualStim):
            raise Exception('Entry of radio button has to be a child of BaseVisualStim.')
        elif not (hasattr(obj, 'on_select') and hasattr(obj, 'on_deselect')): 
            raise Exception('Missing "on_select" and/or "on_deselect" methods for obj.')
            
        # todo: check if obj is already contained in self._items
        obj.parent = self  # register self as parent to obj (fuer tab weiterleitung usw.; s. Beispiel textinput.py)
        self._items.append(obj)
        if select is True:  
            self.select(self._items[-1])
        else:
            self._items[-1].on_deselect()  # init item with deselected state 
            
    def add_item_new(self, obj, select=False):
        """Item has to be a child of BaseVisualStim.
            Last added item with select=True is selectd.  
            
        """
        if not isinstance(obj, visual.BaseVisualStim):
            raise Exception('Entry of radio button has to be a child of BaseVisualStim.')
        elif not (hasattr(obj, 'on_select') and hasattr(obj, 'on_deselect')): 
            raise Exception('Missing "on_select" and/or "on_deselect" methods for obj.')
            
        # todo: check if obj is already contained in self._items
        obj.parent = self  # register self as parent to obj (fuer tab weiterleitung usw.; s. Beispiel textinput.py)
        self._items.append(obj)
        if select is True:  
            self.select(self._items[-1])
        else:
            #self._items[-1].on_deselect()  # init item with deselected state
            self._items[-1].init_deselect()  # init item with deselected state
                    
    def del_item(self, name):
        pass
    
    def changed(self, mouse):
        """Return True if radio button has been changed by mouse click and
           and set changed-Attribute to False.

        """
        ret = self._changed
        self._changed = False
        return ret
        
    
    @property
    def selected(self):
        return self._selected_item
        
    @property
    def selected_id(self):
        for i, item in enumerate(self._items, start=1):
            if item is self._selected_item:
                return i
    
    def focus_next(self):  # todo: eleganter
        # see textinput.py for an example
        #print('next')
        for i, item in enumerate(self._items):
            if item == self._selected_item:
                try:
                    self.select(self._items[i+1])
                except:
                    self.select(self._items[0])
                break
                    
    def focus_prev(self):  # todo: eleganter
        # see textinput.py for an example
        #print('prev')
        for i, item in enumerate(self._items):
            if item == self._selected_item:
                try:
                    self.select(self._items[i-1])
                except:
                    self.select(self._items[-1])
                break
            
    def select(self, obj):
        """obj can be name or object
        If no match is found, obj is ignored and ret=0
        """
        # 1. Check if self was selected and is again clicked
        self_handling = False        
        if isinstance(obj, str) and (self._selected_item.name == obj):
            self_handling = True
        elif isinstance(obj, visual.BaseVisualStim) and (obj is self._selected_item):
            self_handling = True
            
        if self_handling is True:
            if self._deselect_when_click_on_selected is True:
                self._selected_item.on_deselect()
                self._selected_item = None
            else:
                return 1  # nothing to do
            return
        
        # 2. Handle click on different obj
        if isinstance(obj, str):
            sel = [item for item in self._items if item.name == obj]
            if not sel:
                return 0
            else:
                sel = sel[0]
        elif isinstance(obj, visual.BaseVisualStim):               
            sel = [item for item in self._items if item is obj]
            if not sel:
                return 0
            else: 
                sel =sel[0]
            
        # found name and its not self._selected_item
        if self._selected_item:
            self._selected_item.on_deselect()
        self._selected_item = sel
        self._selected_item.on_select()
        
    # todo: mouse._wasReleased local speichern und nicht in global mouse?
    def draw(self):
        # update mouse status
        mouse_press = self._mouse.getPressed()[0]  # left button only
        if (self._mouse._wasReleased is False) and ( mouse_press == 0):
            self._mouse._wasReleased = True 
        
        # update items
        if mouse_press == 1:
            for item in self._items:
                if self._mouse.isPressedIn(item, buttons=[0]):  # left click only
                    if item is self._selected_item:
                        if self._deselect_when_click_on_selected is False:
                            pass  # mouse press in already selected item, so there is nothing to do
                        else:
                            # handle mouse click
                            if self._mouse._wasReleased is True:
                                self._mouse._wasReleased = False
                                self.select(item)
                            
                    else:
                        ## handle mouse over
                        #if not item._isSelected and item.contains(self.mouse):
                        #    item._isSelected = True
                        #    item.setColor('blue')
                        #    #item.setHeight(item._origHeight*1.2)
                        #elif not item.contains(self.mouse) and item._isSelected: # reset item size
                        #    item._isSelected = False
                        #    item.setColor(self.fontcolor)
                        #    #item.setHeight(item._origHeight)
            
                        # handle mouse click
                        if self._mouse._wasReleased is True:
                            self._mouse._wasReleased = False
                            self.select(item)
                    
        # draw            
        for item in self._items:            
            item.draw()
            

########################
if __name__ == '__main__':
    import types

    def on_select(self):
        self.color = 'green'
        
    def on_deselect(self):
        self.color = 'blue'

    win = visual.Window(units='pix')  # Achtung: units muss mit units der items ueberein stimmen!!! oder es geht 
                # wegen oculib.psychopy.TextStim.contains() im Moment nur 'pix'? 
    mouse = event.Mouse(win=win)
    item1 = TextStim(win, text='Choice 1', name='item1', pos=(0,-50), units='pix')
    item1.on_select = types.MethodType(on_select, item1)  # see http://stackoverflow.com/questions/972/adding-a-method-to-an-existing-object
    item1.on_deselect = types.MethodType(on_deselect, item1)
    
    item2 = TextStim(win, text='Choice 2', name='item2', pos=(0,-20), units='pix')
    item2.on_select = types.MethodType(on_select, item2)
    item2.on_deselect = types.MethodType(on_deselect, item2)
    
    
    # todo: per decorator on_select und on_deselct + name setzen!!!    
    
    item3 = TextStim(win, text='Choice 3', name='item3', pos=(0,10), units='pix')
    item3.on_select = types.MethodType(on_select, item3)
    item3.on_deselect = types.MethodType(on_deselect, item3)
    
    rb = RadioButton(win, mouse)
    rb.add_item(item1, select=True)
    rb.add_item(item2)
    rb.add_item(item3, select=True)
    

    while 1:
        rb.draw()
        win.flip()
        
    
