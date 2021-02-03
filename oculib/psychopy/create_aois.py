# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 11:41:40 2014

@author: ocunostics
"""

from psychopy import visual, event, gui
from oculib.psychopy.frame import Frame

# todo: Aois in einer Gruppe zusammenfassen fuer radiobutton etc?

# todo: stop minipunkt nach verschieben von aoi

# todo: vertices mueesen fuer aois mitgespeichert werden

image = gui.fileOpenDlg()[0]
#import pdb; pdb.set_trace()

#image = '../../../StartScreen.png'
#image = './Stimuli/Folie16.png'
#image = './Stimuli/Folie18.png'
#image = './Stimuli/Folie22_TextWarnstreik.png'
#image = './Stimuli/Folie25_GedTest.png'

win = visual.Window(fullscr=True, units='pix')
mouse = event.Mouse(win)
img = visual.ImageStim(win, image=image, units='pix')

winw, winh = win.size

f_info = Frame(win, pos=(winw/2.-50,winh/2.-25), width=100, height=50, 
               roundness=6, lineColor='#2d69e0', fillColor='#2d69e0')
f_pos = visual.TextStim(win, text='0;0', pos=(0,10), color='white', 
                        height=12, units='pix')
f_width_height = visual.TextStim(win, text='w: 0; h: 0', pos=(0,-10), color='white',
                                 height=12, units='pix')
f_info.add(f_pos)
f_info.add(f_width_height)
f_info.opacity = 0.5

aois = []

# todo: aoi-draw separieren
def draw():
    img.draw()
    f_info.draw()    
    for aoi in aois:
        aoi.draw()
        
run = 1
while run:
    draw() 
    win.flip()
    buttons = mouse.getPressed()
    if buttons[0] == 1:  # left button:
        mouse_in_aoi = False
        for aoi in aois:
            if mouse.isPressedIn(aoi, buttons=[0]) == 1:
                mouse_in_aoi = True  # todo: leave loop wenn fertig
                delta = aoi.pos - mouse.getPos()
                aoi.setLineColor('blue')  
                draw()
                aoi.draw()
                win.flip()
                while mouse.isPressedIn(aoi, buttons=[0]) == 1:
                    aoi.setPos(mouse.getPos()+delta)
                    draw()
                    aoi.draw()
                    win.flip()
                
                aoi.setLineColor('red')
                draw()
                aoi.draw()  # kann weg?
                win.flip()
                
            
        if mouse_in_aoi is False:  
            pos1 = mouse.getPos()
            f_pos.setText(text='{0};{1}'.format(*pos1))
            aoi = visual.ShapeStim(win, pos=pos1, vertices=((0,0), (1,0), (1,1), (0,1)), closeShape=True,
            size=3, units='pix', lineColor='red')  # rect with mouse point bottom right
            aoi.name = len(aois)
            while mouse.getPressed()[0] == 1:
                width = mouse.getPos()[0]-pos1[0]
                height = mouse.getPos()[1]-pos1[1]
                aoi.setSize((width, height))
                f_width_height.setText(text='w: {0}; h: {1}'.format(width, height))
                draw()
                aoi.draw()
                win.flip()
            aois.append(aoi)
    elif buttons[2] == 1:  # reight button
        if mouse.isPressedIn(aoi, buttons=[2]) == 1:
                # right mouse: add/correct name
                pass             
    
    keys = event.getKeys()
    if keys:
        keys = keys[0]
        if keys == 's':
            # save aois
            # pickl aoi object (wegen vertex etc.)
            with open(image[:-4]+'_aois.txt', 'w') as fout:
                for nr, aoi in enumerate(aois,1):
                    fout.write('{nr};{x};{y};{width};{height}\n'.format(nr=nr,
                               x=aoi.pos[0], y=aoi.pos[1], 
                               width=aoi.size[0], height=aoi.size[1]))
            run = 0 

win.close()   
   
    
    
    
       
            
            