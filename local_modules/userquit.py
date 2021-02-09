# -*- coding: utf-8 -*-
"""
Created on Thu May 01 21:41:58 2014

@author: ocunostics
"""
# todo: s. textinput: 
# nutze _on_text um Tasten differenzierter auswerten zu koennen?
# handle key press of letters and symbols
# (event.getKeys liefert modifier und Buchstaben getrennt; onText liefert direkt z.B. 'A'
# wenn Shift + 'a' gedrueckt wurden)
# self._win.winHandle.on_text = self._onText

from psychopy import visual, event
import sys

class UserQuit(object):
    """
    on_quit and on_continue provide callbacks to override the behavior when user
    pressed (F)ortsetzen or (Q)Beenden
    
    Standard behavior: return 'Quit'|'Continue'
    """
    def __init__(self, win=None, keylist=('escape',), on_quit=None, on_continue=None,
                 show_skip=False, logfiles=None, on_calib=None, userquit=None):
        self.win = win
        self.show_skip = show_skip
        self._calib = on_calib
        self.userquit=userquit
        if self.show_skip is True:        
            self._msg = visual.TextStim(win, text=u'Das Programm wurde unterbrochen.\n\n\nF = Fortsetzen\nS = Aufgabe überspringen\nQ = Beenden',
                               pos=(0.0, 0.0), units='pix', height=32, wrapWidth=800,
                               color='black')
        elif self._calib:        
            self._msg = visual.TextStim(win, text=u'Das Programm wurde unterbrochen.\n\n\nF = Fortsetzen\nC = Neu Kalibrieren\nQ = Beenden',
                               pos=(0.0, 0.0), units='pix', height=32, wrapWidth=800,
                               color='black')
        else:
            self._msg = visual.TextStim(win, text=u'Das Programm wurde unterbrochen.\n\n\nF = Fortsetzen\nQ = Beenden',
                               pos=(0.0, 0.0), units='pix', height=32, wrapWidth=800,
                               color='black')
        if on_quit is None:
            self._quit = self._on_quit
        else:
            self._quit = on_quit
                       
        if on_continue is None:
            self._continue = self._on_continue
        else:
            self._continue = on_continue
        
        self._skip = self._on_skip
        
        self.keylist = keylist     

        self.logfiles = logfiles              
        
    def check(self):
        ret = event.getKeys(keyList=self.keylist)  # keyList angeben, damit keine
                        # anderen Eingaben aus der event-qeue geloescht werden
        if ret:
            self._msg.draw()
            self.win.flip()

            if self.logfiles:
                for log in self.logfiles:
                    log.write('MSG:UserQuit:ProgramPaused')
                    if isinstance(log, file):  # braucht man nicht mehr, wenn log als device definiert ist
                        log.write('\n')

            while 1:
                if self.show_skip is True:
                    key = event.waitKeys(keyList=('f','q','s'))  # keyList angeben, damit keine
                        # anderen Eingaben aus der event-qeue geloescht werden
                    #if key: 
                        #import pdb; pdb.set_trace()
                    if key[0] in ['f', ]:
                        #self._continue
                        return self._continue()
                    elif key[0] in ['q', ]:
                        #self._quit
                        return self._quit()
                    elif key[0] in ['s', ]:
                        return self._skip()

                if self._calib:
                    key = event.waitKeys(keyList=('f','c','q'))  # keyList angeben, damit keine
                        # anderen Eingaben aus der event-qeue geloescht werden
                    #if key: 
                        #import pdb; pdb.set_trace()
                    if key[0] in ['f', ]:
                        #self._continue
                        return self._continue()
                    elif key[0] in ['q', ]:
                        #self._quit
                        return self._quit()
                    elif key[0] in ['c', ]:
                        return self._calib(win=self.win, et=self.logfiles[1], img="calibration_zw.png", userquit=self.userquit)
                else:
                    key = event.waitKeys(keyList=('f','q'))  # keyList angeben, damit keine
                        # anderen Eingaben aus der event-qeue geloescht werden
                    #if key: 
                        #import pdb; pdb.set_trace()
                    if key[0] in ['f', ]:
                        #self._continue
                        return self._continue()
                    elif key[0] in ['q', ]:
                        #self._quit
                        return self._quit()                      
                    
    def _on_quit(self):
        if self.logfiles:
            for log in self.logfiles:
                log.write('MSG:UserQuit:ProgramQuit')  
                if isinstance(log, file):  # braucht man nicht mehr, wenn log als device definiert ist
                        log.write('\n')

        return 'Quit'
        
    def _on_continue(self):
        if self.logfiles:
            for log in self.logfiles:
                log.write('MSG:UserQuit:ProgramContinued')
                if isinstance(log, file):  # braucht man nicht mehr, wenn log als device definiert ist
                        log.write('\n')

        return 'Continue'
        
    def _on_skip(self):
        if self.logfiles:
            for log in self.logfiles:
                log.write('MSG:UserQuit:ProgramSkiped')
                if isinstance(log, file):  # braucht man nicht mehr, wenn log als device definiert ist
                        log.write('\n')
     
        return 'Skip'
    def _on_calibrate(self):
        if self.logfiles:
            for log in self.logfiles:
                log.write('MSG:UserQuit:ProgramSkiped')
                if isinstance(log, file):  # braucht man nicht mehr, wenn log als device definiert ist
                        log.write('\n')
     
        return 'Skip'
        
##########################
if __name__ == '__main__':
    win = visual.Window(color='white')
    msg = visual.TextStim(win, text='Please press ESC', color='black')
    

    def on_quit():
        win.close()
        sys.exit()
    
    userquit = UserQuit(win=win)    
    while 1:
        ret=4
        ret = userquit.check()
        print(ret)
        if ret == 'Quit':
            win.close()
            sys.exit()
        msg.draw()
        win.flip()
        
    #userquit = UserQuit(win=win, on_quit=on_quit)
#    while 1:
#        ret = userquit.check()
#        if ret: print(ret)
#        #if ret == 'Quit':
#        #    win.close()
#        #    sys.exit()
#        msg.draw()
#        win.flip()
        

    

