# -*- coding: utf-8 -*-
"""
Created on Mon Sep 02 22:10:49 2013

@author: tamm
"""

# todo: Dialog und Frame vereinheitlichen

from psychopy import core, event, visual
import os
import uuid
import misc
from frame import Frame
from clock import Clock

# gesamtbildschirm (win.size) mit weißem Rechteck fuellen und opacity auf 0.1
# menurechteck setzen und groß zoomen oder opacity hochfahren und mit Text füllen
# Text per Maus und/oder Tasttur anwählbar
# bzw. Objekt uebergeben, dass im Dialogwidget dargestellt wird


# todo: Entwicklermode, der es erlaubt, per Wrapperfunktion auf Tastendruck die Elemente auf 
# dem Bildschirm hin- und herzuschieben. Dabei kann man vielleicht noch ein Rastergitter einblenden.
# Auf einen weiteren Knopfdruck hin werden dann die Koordinaten aller angezeigten Objekte 
# gespeichert und in eine Datei geschrieben, so dass man auf diesem Wege so etwas wie ein 
# GUI-Designer erhält.

# todo: add option: background='screenshot',color (=Farbe angeben)
#       bei Sicherheitsktisichen Applikationen dann ohne screenshot arbeiten

# todo: Koordinatensystem Frame ueberdenken + units (im Moment Mix aus 'norm' und 'pix')
# based on Frame
class Dialog(object):
    """
    Achtung: Dialog-Objekt erst erzeugen, wenn es benoetigt wird. Beim Erzeugen wird
    ein Screenshot von win angelegt und der passt sonst eventuell nicht mehr zum
    Kontext.

    Nicht bei sicherheitskritischen Applikationen einsetzen: Im Moment der Dialogerstellung
    koennte der Hintergrund z.B. ein Passwort enthalten, dass dann im Screenshot kurzzeitig gespeichert ist.

    """
    # todo: Koordinatensystem fuer pos ueberdenken!!!
    def __init__(self, win=None, parentwin=None, win_background=None,
                pos=(0, 0), width=300, height=300, roundness=9, units='pix'):

        # todo: win_background color + opacity setzen lassen + soll screenhot ja oder nein angezeigt werden
        # todo: Funktion um dialogspezifische relative Screencoord. zu erzeugen

        # todo: win und parentwin-parameter, um gegebenenfalls auch komplett neues
        #   Fenster oeffnen zu koennen?

        self._win = win # Usually (but not necessarily) the parent window.
        if parentwin is None:
            self._parentwin = self._win
        # todo: if not win: raise Exception

        self._win_background = win_background
        if self._win_background == 'screenshot':
            # create Screenshot from parent window
            # (maybe in future we could use BufferImageStim)
            self._fname = '{0}.png'.format(str(uuid.uuid4()))
            self._parentwin.getMovieFrame(buffer='front')
            self._parentwin.saveMovieFrames(self._fname)
            self._winback = visual.ImageStim(self._win, image=self._fname) # todo: choose better name
            try:
                os.remove(self._fname) # aus sicherheitsgruenden bild sofort wieder loeschen
            except:
                pass
            self._background = visual.Rect(self._win, width=2, height=2, pos=(0, 0), fillColor='lightgrey', lineColor='lightgrey', opacity=0.4, units='norm')
        elif self._win_background is None:
            self._winback = None
            self._background = visual.Rect(self._win, width=2, height=2, pos=(0, 0), fillColor='lightgrey', lineColor='lightgrey', opacity=0.4, units='norm')
        else:
            # fill win background with color
            self._winback = None
            self._background = visual.Rect(self._win, width=2, height=2, pos=(0, 0), fillColor=win_background, lineColor=win_background, units='norm')


        # dialog rect
        self._dialog = Frame(win=self._win, shape='rect', roundness=roundness,  pos=pos, width=width, height=height,
                                   fillColor='#4660fd', lineColor='#4660fd', units=units)

        # shadow rect
        self._dialog2 = Frame(win=self._win, shape='rect', roundness=roundness,  pos=(pos[0]+8., pos[1]-6.), width=width, height=height,
                                    fillColor='#5c5757', lineColor='#5c5757', units=units, opacity=0.3)

        # todo: autodraw-Events aus win austragen und nach rückkehr aus Dialog wieder eintragen
        # todo: function pre und post definieren, so dass per Callbacks pre und post-Operationen vom Anwender ausgeführt werden können


    def add(self, item):
        self._dialog.add(item)
        return item 

    def remove(self, name):
        self._dialog.remove(name)
        
    def draw(self):
        """Use draw() if you want external control over dialog box."""
        if self._winback: self._winback.draw()
        self._background.draw()
        self._dialog2.draw()
        self._dialog.draw()
            

    def show(self, max_wait_time=None):
        # todo: Ok + Cancel-key angeben
        if max_wait_time:
            runtime = Clock()
                

        while 1:
            if max_wait_time and runtime.getTime() >= max_wait_time:
                return 'OK'
            
            self._draw()
            self._win.flip()
                    
            key = event.waitKeys()[-1]
            if key: #in ('escape', 'q'):
                return 'OK'

 #####################################################

# Dialog based on visual.rect
class Dialog_old(object):
    """
    Achtung: Dialog-Objekt erst erzeugen, wenn es benoetigt wird. Beim Erzeugen wird 
    ein Screenshot von win angelegt und der passt sonst eventuell nicht mehr zum
    Kontext.
    
    Nicht bei sicherheitskritischen Applikationen einsetzen: Im Moment der Dialogerstellung 
    koennte der Hintergrund z.B. ein Passwort enthalten, dass dann im Screenshot kurzzeitig gespeichert ist.

    """

    def __init__(self, win=None, parentwin=None, win_background=None,
                 topleft=(-0.3, 0.4), bottomright=(0.3, -0.4), roundness=0.02):
        # todo: win_background color + opacity setzen lassen + soll screenhot ja oder nein angezeigt werden
        # todo: Funktion um dialogspezifische relative Screencoord. zu erzeugen

        # todo: win und parentwin-parameter, um gegebenenfalls auch komplett neues
        #   Fenster oeffnen zu koennen?
    
        self._win = win # Usually (but not necessarily) the parent window.
        if parentwin is None:
            self._parentwin = self._win
        # todo: if not win: raise Exception
        
        self._buffer = []
        self._win_background = win_background

        if self._win_background == 'screenshot':
            # create Screenshot from parent window
            # (maybe in future we could use BufferImageStim)
            self._fname = '{0}.png'.format(str(uuid.uuid4()))
            self._parentwin.getMovieFrame(buffer='front')
            self._parentwin.saveMovieFrames(self._fname)
            self._winback = visual.ImageStim(self._win, image=self._fname)  # todo: choose better name
            try:
                os.remove(self._fname) # aus sicherheitsgruenden bild sofort wieder loeschen
            except:
                pass
            self._background = visual.Rect(self._win, width=2, height=2, pos=(0,0), fillColor='lightgrey', lineColor='lightgrey', opacity=0.4)
        elif self._win_background is None:
            self._winback = None
            self._background = visual.Rect(self._win, width=2, height=2, pos=(0,0), fillColor='lightgrey', lineColor='lightgrey', opacity=0.4)
        else:
            # fill win background with color
            raise Warning('Background color not yet implemented.')


        # dialog rect
        left = topleft[0]
        right = bottomright[0]
        top = topleft[1]
        bottom = bottomright[1]
        vert = misc.rect_vertices(roundness=roundness, topleft=(left, top), bottomright=(right, bottom))
        self._dialog = visual.ShapeStim(win=self._win, vertices=vert, fillColor='#bcd5ef', lineColor='#bcd5ef')

        # shadow rect
        left += 0.02
        right += 0.02
        top -= 0.02
        bottom -= 0.02
        vert = misc.rect_vertices(roundness=roundness, topleft=(left, top), bottomright=(right, bottom))
        self._dialog2 = visual.ShapeStim(win=self._win, vertices=vert, fillColor='#5c5757', lineColor='#5c5757', opacity=0.3)

        # todo: autodraw-Events aus win austragen und nach rückkehr aus Dialog wieder eintragen
        # todo: function pre und post definieren, so dass per Callbacks pre und post-Operationen vom Anwender ausgeführt werden können
        

        # todo: pos in Koordinaten rel. zu Dialogfenster
        
    def add(self, item):
        if not isinstance(item, visual._BaseVisualStim):
            return

        self._buffer.append(item)


    def show(self):
        if self._winback: self._winback.draw()
        self._background.draw()
        self._dialog2.draw()
        self._dialog.draw()
        for item in self._buffer:
            item.draw()
        self._win.flip()
        
        while 1:
            key = event.waitKeys()[-1]
            if key in ('escape', 'q'):
                return 'OK'
            
    def _dlgpos2winpos(self, pos):
        """Returns pos in windows coordinates.
        
        Note: Only for rel. coordinates!         
        """
        #print(self._parentwin.pos)
        
        
# ----------------------
if __name__ == '__main__':
    MODE = 'new' # 'old', 'new'

    if MODE == 'old':    
        win = visual.Window()
        dummy1 = visual.TextStim(win, text="Dummy text", pos=(0.5,0))
        dummy2 = visual.TextStim(win, text="Another text", pos=(0.5,-0.3))
    elif MODE == 'new':
        win = visual.Window(units='pix')
        dummy1 = visual.TextStim(win, text="Dummy text", pos=(300,0), units='pix')
        dummy2 = visual.TextStim(win, text="Another text", pos=(300,-100), units='pix')

    while 1:
        dummy1.draw()
        dummy2.draw()
        win.flip()

        key = event.waitKeys()
        if key[0] in ('escape', 'q'):
            break

        if MODE == 'old':
            mydlg = Dialog_old(win, roundness=0)  #
            mydlg.add(visual.TextStim(win, text="Menu", pos=(0, 0.3)))

        elif MODE == 'new':
            mydlg = Dialog(win, roundness=9, win_background='screenshot', pos=(100,100), width=300, height=200)  # Wichtig: Beim Erzeugen wird ein Screenshot angefertigt!
            mydlg.add(visual.TextStim(win, text="Menu", pos=(0., 0.), units='pix', height=30))

        # simulate dialog usage
        ret = mydlg.show()
        if ret == 'OK':
            pass # todo: wie setze ich auf win auf draw-Zustand vor Aufruf von mydlg zurueck?

        #import pdb; pdb.set_trace()

    win.close()
    core.quit()
