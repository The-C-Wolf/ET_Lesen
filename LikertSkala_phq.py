# -*- coding: utf-8 -*-

from psychopy import visual, core, event
import numpy as np
import pandas as pd
import os

PATH = os.path.dirname(os.path.abspath(__file__)) #gets source file location

class LikertSkala:
    def __init__(self, win, mouse, df):
        textsize = 20
        button_pos = (500,-450)#(400,-320) 
        x_start = 350
        y_start = 250#180 #250
        box_size = 15
        box_dist = box_size + 15 #not real box dist!
        item_dist = box_size + 40 #not real dist
        x_scale_dist = 910
        self.itemzahl = len(df["Items"])
        instruction = df["Instruktion"][0] #place of instruction in input file
        scaleunit = df["Skaleneinheit"][0].split(",") #place of text for ratingscale
        scaletext = df["Skalenbeschriftung"][0]
        itemtext = df.loc[0:self.itemzahl,"Items"] #Number of Items for each screen and respective column in input file
        self.headers = df.loc[0:self.itemzahl,"Header"]
        boxes = len(scaleunit) #width of ratingscale
        self.rescale = scaleunit[0]
        self.itemtext = itemtext
        self.box = list()
        self.boxes = boxes
        self.text = list()
        self.unit = list()
        self.scaleunit = scaleunit
        self.scaletext = list()
        self.rating = list()
        self.instruction = visual.TextStim(win, units = "pix", text = instruction.decode("utf-8"), height = textsize, wrapWidth = 700, color='navy', bold=True, pos=(x_start-x_scale_dist,y_start+100), alignHoriz = "left")
        self.scaletext = visual.TextStim(win, units = "pix", text = scaletext, height = 15, ori=0, color=(-1,-1,-1),bold=True, pos=(x_start,y_start+100))
        self.button = [visual.Rect(win, units = "pix",width = 80, height = 40, pos = button_pos, lineColor="black", fillColor = [0.5,0.5,0.5]),visual.TextStim(win, units = "pix", text = "Weiter", height = 20, color=(-1,-1,-1),bold=True, pos=button_pos)]
        self.mouse = mouse
        self.win = win
        for j, item in enumerate(itemtext):
            self.box.append(list())
            self.rating.append(list())
            for i in range(boxes):
                self.box[j].append(visual.Rect(win, units = "pix",width = box_size, height = box_size, pos = (x_start+i*box_dist,y_start-j*item_dist), lineColor="black", fillColor = "White"))
                self.rating[j].append(0)
            self.text.append(visual.TextStim(win, units = "pix", text = item, height = textsize, color=(-1,-1,-1),wrapWidth =890,  pos=(x_start-x_scale_dist,y_start-j*item_dist), alignHoriz = "left"))
        for i in range(boxes):
            self.unit.append(visual.TextStim(win, units = "pix", ori=0, alignHoriz="left", text = scaleunit[i], height = 15, color=(-1,-1,-1), bold=True, pos=(x_start+i*box_dist,y_start+40)))
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
            for i in range(self.boxes):
                self.unit[i].draw()
            self.scaletext.draw()
            self.instruction.draw()
            self.win.flip()
            ratinglist = self.getRating() #get a list with ratings for each item
            if "NA" not in ratinglist: #check for missing values
                self.button[0].draw() #show button, when all items have been rated
                self.button[1].draw()
                if self.mouse.isPressedIn(self.button[0]): #save ratings to respective items, when button is pressed
                    ratinglist = self.getRating()
# =============================================================================
                    z = int(self.scaleunit[0])
                    rescaledlist = [x+z for x in ratinglist] #rescale
# =============================================================================
                    result = pd.DataFrame(data=rescaledlist, index=self.headers)#.transpose() #data=ratinglist
                    #result = pd.DataFrame({"Items": self.itemtext, "Ratings": rescaledlist}).stack()
                    #result.to_csv(PATH+"\\data\\Ergebnis_LS_"+name+".csv", sep=';')
                    return result
                    break
            if event.getKeys(['escape']):
                quittext = "Willst du das Experiment wirklich beenden? Drücke: \n\n W Für Weiter \n\n B Für Beenden"
                quit_text = visual.TextStim(self.win, units = 'pix', height = 22, text=quittext.decode("utf-8"), alignHoriz = 'center', font="Courier New",  wrapWidth = 1100, color=(-1,-1,-1), pos = (0,0))
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