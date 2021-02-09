# -*- coding: utf-8 -*-

from psychopy import visual, core, event
import numpy as np
import pandas as pd
import os

PATH = os.path.dirname(os.path.abspath(__file__)) #gets source file location

#PARAMETERS
x_start_position = 350
y_start_position = 250 #180 #250
p_box_size = 16
box_distance = p_box_size + 28 #number is real box dist!
item_distance = p_box_size + 40 #number is approx. item dist

x_scale_distance = 800 #todo make dependent on len(items)
wrap_items = 720 #width for itemtext
wrap_dots = 800

instruction_textsize = 20 #also textsize for items
instruction_pos=(x_start_position-x_scale_distance,y_start_position+150)
instruction_color = 'navy'

scaletext_height = 16
#scaletext_pos=(x_start_position,y_start_position+100)

#button_position = (500,-450)#(400,-320) 
button_size = (80,40)


scaleunit_height = 20
scaletext_ori = -40
scaleunit_ori = 0



class LikertSkala:
    def __init__(self, win, mouse, df, start_pos=(350,250), button_pos=(500,-450)):
        textsize = instruction_textsize
        x_start = start_pos[0]
        y_start = start_pos[1]
        box_size = p_box_size
        box_dist = box_distance
        item_dist = item_distance
        x_scale_dist = x_scale_distance
        
        self.itemzahl = len(df["Items"])
        instruction = df["Instruktion"][0] #place of instruction in input file
        scaleunit = df["Skaleneinheit"][0].split(",") #place of text for ratingscale
        
# =============================================================================
#         rotate_unit = False
#         for u in scaleunit:
#             if len(u) > 2:
#                 rotate_unit = True
#         if rotate_unit == True:
# =============================================================================
        self.scaletext_ori = scaletext_ori
        self.scaleunit_ori = scaleunit_ori
        
        scaletext = df["Skalenbeschriftung"][0].split(",")
        itemtext = df.loc[0:self.itemzahl,"Items"] #Number of Items for each screen and respective column in input file
        self.headers = df.loc[0:self.itemzahl,"Header"]
        boxes = len(scaleunit) #width of ratingscale
        self.rescale = scaleunit[0]
        self.itemtext = itemtext
        self.box = list()
        self.boxes = boxes
        self.text = list()
        self.dots = list()
        self.unit = list()
        self.scaleunit = scaleunit
        self.scale = list()
        self.scaletext = scaletext
        self.rating = list()
        self.instruction = visual.TextStim(win, units = "pix", text = instruction , height = textsize, wrapWidth = 1000, color=instruction_color, bold=True, pos=instruction_pos, alignHoriz = "left")
        #self.scaletext = visual.TextStim(win, units = "pix", text = scaletext, height = scaletext_height, ori=scaletext_ori, color=(-1,-1,-1),bold=True, pos=scaletext_pos)
        self.button = [visual.Rect(win, units = "pix",width = button_size[0], height = button_size[1], pos = button_pos, lineColor="black", fillColor = [0.5,0.5,0.5]),visual.TextStim(win, units = "pix", text = "Weiter", height = 20, color=(-1,-1,-1),bold=True, pos=button_pos)]
        self.mouse = mouse
        self.win = win
        for j, item in enumerate(itemtext):
            self.box.append(list())
            self.rating.append(list())
            for i in range(boxes):
                self.box[j].append(visual.Rect(win, units = "pix",width = box_size, height = box_size, pos = (x_start+i*box_dist,y_start-j*item_dist), lineColor="black", fillColor = "White"))
                self.rating[j].append(0)
            self.text.append(visual.TextStim(win, units = "pix", text = item, height = textsize, color=(-1,-1,-1),wrapWidth = wrap_items,  pos=(x_start-x_scale_dist,y_start-j*item_dist), alignHoriz = "left"))
            scale_len = self.text[j].boundingBox[0]
            space = x_scale_dist - scale_len
            #frederics anpassung
            dotdot = "."
            self.dots.append(visual.TextStim(win, units="pix", text = dotdot, height = textsize, color = (-1,-1,-1), wrapWidth= wrap_dots, pos = (x_start-10,y_start-j*item_dist),alignHoriz="right"))
            sizeOfOneDot = self.dots[j].boundingBox[0]
            amountofneededDots = int((space-20 )/ sizeOfOneDot)
            dotsdots = "."*amountofneededDots + " "
            self.dots[j].setText(dotsdots)
            #dotdot = ".."
            #self.dots.append(visual.TextStim(win, units="pix", text = dotdot, height = textsize, color = (-1,-1,-1), wrapWidth= wrap_dots, pos = (x_start-10,y_start-j*item_dist),alignHoriz="right"))
            #while self.dots[j].boundingBox[0] < space-20:
            #    dotdot = dotdot + "."
            #    self.dots[j].setText(dotdot)
        for i in range(boxes):
            self.unit.append(visual.TextStim(win, units = "pix", ori=self.scaleunit_ori, alignHoriz="left", text = scaleunit[i], height = scaleunit_height, color=(-1,-1,-1), bold=True, pos=(x_start+i*box_dist,y_start+40)))
            self.scale.append(visual.TextStim(win, units = "pix", ori=self.scaletext_ori, alignHoriz="left", text = scaletext[i], height = scaletext_height, color=(-1,-1,-1), bold=True, pos=(x_start+i*box_dist,y_start+50)))
    def draw(self, name=""):
        while True:
            for j in range(len(self.itemtext)):
                for i in range(self.boxes):
                    if self.mouse.isPressedIn(self.box[j][i]):
                        self.box[j][i].fillColor = "Black"
                        self.rating[j][i] = 1
                        for k in np.delete(range(self.boxes),i):
                            self.box[j][k].fillColor = "White"
                            self.rating[j][k] = 0
                    self.box[j][i].draw()
                self.text[j].draw()
                self.dots[j].draw()
            for i in range(self.boxes):
                self.unit[i].draw()
                self.scale[i].draw()
            #self.scaletext.draw()
            self.instruction.draw()
            self.win.flip()
            ratinglist = self.getRating() #get a list with ratings for each item
            if "NA" not in ratinglist: #check for missing values
                self.button[0].draw() #show button, when all items have been rated
                self.button[1].draw()
                if self.mouse.isPressedIn(self.button[0]): #save ratings to respective items, when button is pressed
                    ratinglist = self.getRating()
# =============================================================================
                    if self.scaleunit_ori == 0:
                        z = int(self.scaleunit[0])
                    else:
                        z = 1
                    rescaledlist = [x+z for x in ratinglist] #rescale
# =============================================================================
                    result = pd.DataFrame(data=rescaledlist, index=self.headers).transpose() #data=ratinglist
                    #result = pd.DataFrame({"Items": self.itemtext, "Ratings": rescaledlist}).stack()
                    #result.to_csv(PATH+"\\data\\Ergebnis_LS_"+name+".csv", sep=';')
                    return result
                    break
            if event.getKeys(['escape']):
                quittext = "Willst du das Experiment wirklich beenden? Drücke: \n\n W Für Weiter \n\n B Für Beenden"
                quit_text = visual.TextStim(self.win, units = 'pix', height = 22, text=quittext , alignHoriz = 'center', font="Courier New",  wrapWidth = 1100, color=(-1,-1,-1), pos = (0,0))
                event.clearEvents()
                while True:
                    quit_text.draw()
                    self.win.flip()
                    if event.getKeys(['b']):
                        self.win.close()
                        core.quit()
                    elif event.getKeys(['w']):
                        break
    def getRating(self):
        ratinglist = list()
        for i in range(self.itemzahl):
            x = np.array(self.rating[i])
            if 1 not in x:
                y = [["NA"]]
            else:
                y = np.where(x==1)
            ratinglist.append(y[0][0])
        return ratinglist