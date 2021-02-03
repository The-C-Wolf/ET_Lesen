# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:53:20 2015

@author: tamm
"""

# scrollender Text ueber scrollenden Frame realisieren:
# langen Text einladen und y-Koordinate scrollen lassen;
# spaeter: Scrollbalken

from psychopy import visual, core, event

template = 'jlsjkdlskjd fklsajdfklasjl ksdjflskj df'
text = ''
for i in range(100):
    text += '{0}\n'.format(template)
    
win = visual.Window()
stim = visual.TextStim(win, text=text, pos=(0,0), units='pix',
                       color='black', height=24)
y = 0.
dy = 1.
t = 0.05
run = 1                       
while run:
    y = y + dy
    stim.setPos((0,y))
    stim.draw()
    win.flip()
    
    core.wait(t)
    
    keys = event.getKeys()
    if keys:
        key = keys[0]
        if key == 'up':
            dy = dy+1
        elif key == 'down':
            dy = dy-1
        elif key == 'q':
            run = False
        elif key == 'left':
            t = t - 0.01
        elif key == 'right':
            t = t + 0.01
            

win.close()