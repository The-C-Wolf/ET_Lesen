# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:31:03 2013

@author: tamm
"""

"""
Thaler, L., Schütz, A. C., Goodale, M. A., & Gegenfurtner, K. R. (2013). What is the best fixation target? The effect of target shape on stability of fixational eye movements. Vision Research, 76, 31–42. doi:10.1016/j.visres.2012.10.012

Psychopy setzt PIL und matplotlib voraus, d.h. ich kann eines von beiden verwenden, um 
ein Bitmap des gewuenschten calibration targets zu erzeugen.
Die Verwendung der visual-Routinen von PsychoyPy erscheint mir nicht als sinnvoll,
weil ich dann entweder in ein bestehendes Window zeichnen muss oder ein neues Window aufmachen 
(geht nur mit Pyglet) usw.
Deshalb lieber eine von Psychopy unabaengige Variante
""" 

# momentan nur Graulevel-Kalibrationsicon moeglich
# todo: abmessungen an Sehwinkel ausrichten; momentan Werte genommen, die vergleichbar zum Paper 
# aussehen. 

from PIL import Image, ImageDraw 

# (0,0) = links oben
# todo: create transparent bitmap und lege nur frontcolor fest

class CalibrationTarget:
    def __init__(self, size=(100,100)):
        self.size = (210,210)
        self.cX, self.cY = (self.size[0]/2, self.size[1]/2)
        self.img = Image.new('LA', self.size, color='white') # 'L' = 8 Bit grey um bei resize antialiasing effect zu bekommen 
         
        draw = ImageDraw.Draw(self.img)
        draw.ellipse(((0,0), self.size), fill='black')
        draw.line([(0,self.cY), (self.size[0],self.cY)], width=60, fill='white')
        draw.line([(self.cX,0), (self.cX,self.size[1])], width=60, fill='white')
        draw.ellipse([(self.cX-32,self.cY-32), (self.cX+32,self.cY+32)], fill='black')
        self.img1 = self.img.resize((30,30), Image.ANTIALIAS)        
        
        #Apply the threshold using the point function
        mask = self.img1.split()[0] # get L channel
        mask = mask.point(lambda p: abs(p-255)) #0 if p==255 else 255)
        self.img1.putalpha(mask)
        
        
    def show(self):
        self.img1.show()
    
    def save(self):
        self.img1.save('calibtarget.png')

    
if __name__ == '__main__':
    ct = CalibrationTarget()
    ct.save()
    