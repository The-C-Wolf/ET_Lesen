# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 11:26:15 2013

@author: ocunostics
"""

from psychopy import visual
from oculib.misc import warning
import numpy
import misc

# see also psychopy Bufferstim for generating "static" frames

# todo: Frame.add: set parent of added object to self (i.e. Frame)

# todo: circle/ellipse als shape implemtieren


# todo: Frame resize ueber width und height oder ueber size ermoeglichen

# todo: change _items from list to dict, so you can use the name?

# todo: works only with 'pix' --> handle 'norm' etc.

# todo: Achtung: roundness ist abhaengig von unit!!! (z.B. 'norm': 0.02, 'pix': 5)


class Frame(visual.ShapeStim):
    """
    Relative Eigenschaften von Frame-Items (pos, size, ori, opacity) bleiben (bis an den
    Definitionsgrenzen) immer erhalten.
    
    todo: Die Parameter shape, width, height, vertices sind nicht unabhaengig voneinander.
    Logik noch mal ueberdenken. (brauche evtl noch relWidth, relHeight); TextStim hat nur height
    ShapeStim hat setScale, Rect hat setSize???
    todo: setContrast

    """

    def __init__(self, win=None, shape='rect', roundness=0, pos=(0., 0.), size=(1., 1.), ori=0.0, units='pix',
                 width=100, height=100, fillColor=None, lineColor=None, opacity=1.,
                 alignHoriz='center'):
        if shape in ('rect', 'rectangle'):
            whalf = width/2.
            hhalf = height/2.
            top = hhalf
            bottom = -hhalf
            if alignHoriz == 'center':
                left = -whalf
                right = whalf
            elif alignHoriz == 'left':
                left = 0
                right = width
            elif alignHoriz == 'right':
                left = -width
                right = 0
            else:
                raise Exception('Unknown alignment parameter: {0}'.format(alignHoriz))
            # Achtung: vertices werden fuer pos=(0,0) berechnet und pos wird dann unten gesetzt!!!
            vertices = misc.rect_vertices(roundness=roundness, topleft=(left, top), bottomright=(right, bottom))
            #vertices = ( (-whalf,-hhalf), (whalf,-hhalf), (whalf,+hhalf), (-whalf,+hhalf) )

        elif shape == 'triangle':
            whalf = width/2.
            hhalf = height/2.
            vertices = ( (-whalf,-hhalf), (0.,hhalf), (whalf,-hhalf) )
        else:
            raise Exception('Not implemented shape: {0}'.format(shape))

        visual.ShapeStim.__init__(self, win=win, vertices=vertices, units=units, size=size) 
        # Bug: Die direkte Uebergabe aller sonstigen moeglichen 
        # ShapeStim-Parameter klappt in PsychoPy 1.78 nicht. Diese muessen 
        # momentan im Nachgang gesetzt werden (insbesondere pos)  
        visual.ShapeStim.setPos(self, pos) # same thing as with __init__ (see above)
        visual.ShapeStim.setSize(self, size)
        visual.ShapeStim.setOri(self, ori)
        visual.ShapeStim.setFillColor(self, fillColor)
        visual.ShapeStim.setLineColor(self, lineColor)
        visual.ShapeStim.setOpacity(self, opacity)
        # visual.ShapeStim(self, ...) referenziert auf eigene Base class!!!
        
        self._items = [] 

    def add(self, item):
        if not hasattr(item, 'draw'):
            raise TypeError('Item has no draw() method.')
        
        if not hasattr(item, 'ori'):
            warning('Item has no orientation attribute. Added fake attribute.')
            item.ori = 0.
        if not hasattr(item, 'opacity'):
            warning('Item has no opacity attribute. Added fake attribute.')
            item.opacity = 1.
        
        item.relPos = numpy.array(item.pos) # item position is spezified relative to frame position
        # item.pos might already be a numpy array. In that case, item.relPos = item.pos
        # would be a reference, not a copy of the data!  
        try: 
            item.pos = self._item_winpos(item.relPos)
        except: 
            item.setPos( self._item_winpos(item.relPos) )  # set item position relative to windows coordinate system
        
        # RatingScale has no ori attribute so far, so we add a fake one
        if isinstance(item, visual.RatingScale):
            item.ori = 0.
        
        item.relOri    = self.ori - item.ori        
        if isinstance(item, visual.TextStim):
            item.relOpacity = self.opacity - item._pygletTextObj.color[3]
            item.relHeight  = self.size[1] - item.height 
        else:
            item.relOpacity = self.opacity - item.opacity
            item.relSize       = self.size - numpy.array(item.size)
         
        self._items.append(item)
        
        return item
      
    # todo: change to pop und erlaube index oder namen
    def remove(self, name):
        for i, item in enumerate(self._items):
            if item.name == name:
                self._items.pop(i)
                break

    def draw(self):
        visual.ShapeStim.draw(self)  # todo: switch on/off
        for item in self._items:
            item.draw()

    def setPos(self, pos):
        # eigentlich ueber setter fuer pos, aber um Konsistenz mit PsychoyPy zu wahren
        if hasattr(pos, 'getPos'): # pos = mouse handler
            pos = pos.getPos()        
        try:
            delta_pos = (pos[0]-self.pos[0], pos[1]-self.pos[1])         
        except:
            raise TypeError('Wrong parameter type: pos')
        
        visual.ShapeStim.setPos(self, pos)
        self._update_pos(delta_pos)
        
    def setRelPos(self, pos):
        # todo: via flag 'abs'|'rel' into setPos
        visual.ShapeStim.setPos(self, (self.pos[0]+pos[0], self.pos[1]+pos[1]))
        self._update_pos(pos)
    

    def setOri(self, ori):
        try:
            delta_ori = (ori-self.ori)
        except:
            raise TypeError('Wrong parameter type: ori')
        
        visual.ShapeStim.setOri(self, ori)        
        self._update_ori(delta_ori)

    def setRelOri(self, ori):
        pass

    def setScale(self, scale):
        pass

    def setOpacity(self, opacity):
        if opacity < 0. or opacity > 1.:
            return
        
        # ---Don't change line order ---
        visual.ShapeStim.setOpacity(self, opacity) 
        self._update_opacity(opacity)

        
    def __len__( self ):
        return len(self._items)

    def __getitem__(self, key):
        return self._items[key]

    def _update_pos(self, delta_pos):
        for item in self._items:
            newpos = (item.pos[0]+delta_pos[0], item.pos[1]+delta_pos[1])
            try:  # new way
                item.pos = newpos
            except:  # old way
                item.setPos( newpos )

    def _update_ori( self, delta_ori ):
        for item in self._items:
            # --- item rotation on the spot
            new_ori = item.ori+delta_ori
            try:
                item.ori = new_ori
            except:
                item.setOri( new_ori )
                    
            # --- item rotation arround frame center
            # old parameter
            x,y = self._item_framepos(item.pos)
            if x == y == 0.:
                continue # items in frame center only need to be rotatet on the spot
            
            if y == 0.:
                if x > 0.:
                    ori = 90.
                elif x < 0.:
                    ori = 270.
            else:
                ori = numpy.degrees(numpy.arctan2(x,y))
            mag = numpy.sqrt(x*x + y*y)
            
            # calculate new parameter
            ori = ori + delta_ori
            x = mag * numpy.sin(numpy.radians(ori))
            y = mag * numpy.cos(numpy.radians(ori))
            
            newpos = self._item_winpos( (x,y) )
            try: 
                item.pos = newpos
            except:
                item.setPos( newpos )

    def _update_opacity( self, opacity ):
        for item in self._items:
            if isinstance(item, visual.TextStim):
                # In Psychopy 1.78 TextStim.setOpacity() shows no effect, so we 
                # have to work around this issue.
                color = list(item._pygletTextObj.color)
                newopacity = item.relOpacity + opacity                
                if newopacity<0.:
                    color[3] = 0.
                elif newopacity>1.:
                    color[3] = 1.
                else:
                    color[3] = newopacity
                
                item._pygletTextObj._set_color(color)
            else:
                newopacity = item.relOpacity + opacity
                if newopacity < 0.:
                    newopacity = 0.
                elif newopacity > 1.:
                    newopacity = 1.
            
                try:
                    item.opacity = newopacity
                except:
                    item.setOpacity( newopacity )

    def _item_winpos( self, framepos ):
        """
        Calculate item windows position from item frame position.

        """
        return numpy.array(framepos) + self.pos  # self.pos = frame origin

    def _item_framepos( self, winpos ):
        """
        Calculate item frame position from item window position.

        """
        return numpy.array(winpos) - self.pos  # self.pos = frame origin

# ----------------------
if __name__ == '__main__':
    from psychopy import core, event
    
    MODE = 3
    
    win = visual.Window(size=(800,600), units='pix') # Frame lauft momentan nur
    # mit 'pix'
    
    stim = visual.TextStim(win, "Hallo",units='pix')
    img = visual.ImageStim(win, image='_ocu.jpg', pos=(66,66))
    
    frame = Frame(win, shape='rectangle',pos=(100,100), roundness=9)
    frame.add(stim)
    frame.add(visual.Rect(win, pos=(30,30), width=30, height=30, units='pix'))
    frame.add(img)    
    
    if MODE == 1:
        frame.draw()
        win.flip()
    
        event.waitKeys()

        frame.setPos((60,60))
        frame.draw()
        win.flip()

        event.waitKeys()
            
        win.close()
        core.quit()
    
    elif MODE == 2:
        mouse = event.Mouse(win)
        is_pressed = False
        while 1:
            frame.draw()
            win.flip()
            
            if is_pressed:
                if not mouse.isPressedIn(frame, buttons=[0]):
                    is_pressed = False
                    continue
                else:
                    print(mouse.getRel(), mouse.mouseMoved())
                    frame.setRelPos(mouse.getRel())
                    
            else:   
                #import pdb; pdb.set_trace()
                if mouse.isPressedIn(frame, buttons=[0]): # left click
                    is_pressed = True
                    mouse.getPos() # reset mouse 
                
    elif MODE == 3:
        mouse = event.Mouse(win)
        while 1:
            frame.draw()
            win.flip()
            
            
            if frame.contains(mouse):
                if any(mouse.getPressed()):
                    #frame.setRelPos(mouse.getRel()) # synchronisiert nicht korrekt
                    
                    frame.setPos(mouse)
                    # todo: rel. Position Maus beim Klicken relativ zu Frame
                    # beruecksichtigen und nach Neupositionierung wieder herstellen
                    
            keys = event.getKeys()
            for key in keys:
                if key=='r':
                    frame.setOri(frame.ori+1.)
                elif key=='t':
                    frame.setOpacity(frame.opacity-0.1)
                elif key=='o':
                    frame.setOpacity(frame.opacity+0.1)
                elif key=='q':
                    win.close()
                    core.quit()
                    break
                
    elif MODE == 4:
        run = True
        while run:
            for ori in numpy.arange(0.,359.,1.):
                frame.setOri(ori)                
                frame.draw()
                win.flip()
                
                keys = event.getKeys()
                for key in keys:
                    if key=='q':
                        run = False
                        win.close()
                        core.quit()
                        break
                    
    elif MODE == 5:
        mouse = event.Mouse(win)
        run = True
        while run:
            for ori in numpy.arange(0.,359.,1.):
                frame.setOri(ori)                
                frame.draw()
                win.flip()
                
                if frame.contains(mouse):
                    if any(mouse.getPressed()):
                        #frame.setRelPos(mouse.getRel()) # synchronisiert nicht korrekt
                        
                        frame.setPos(mouse)
                        # todo: rel. Position Maus beim Klicken relativ zu Frame
                        # beruecksichtigen und nach Neupositionierung wieder herstellen                
                
                keys = event.getKeys()
                for key in keys:
                    if key == 'q':
                        run = False
                        win.close()
                        core.quit()
                        break
        
                        
                