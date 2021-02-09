# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 13:38:18 2019

@author: culemann
"""
from psychopy import visual, core, event
import numpy as np
import pandas as pd
import os

PATH = os.path.dirname(os.path.abspath(__file__)) #gets source file location

class MultipleChoice:
    def __init__(self, win, mouse, df, titel="",startpos=(-400,400), button_pos=(500,-450),dist_param=110):
        textsize = 20
        #button_pos = (500,-450) #fullscreen false: (400,-300)
        self.button = [visual.Rect(win, units = "pix",width = 80, height = 40, pos = button_pos, lineColor="black", fillColor = [0.5,0.5,0.5]),visual.TextStim(win, units = "pix", text = "Weiter", height = 20, color=(-1,-1,-1), pos=button_pos)]
        self.win = win
        self.mouse = mouse
        self.itemzahl = len(df["Items"])
        self.itemtext = df.loc[0:(self.itemzahl-1),"Items"] #Number of Items for each screen and respective column in input file
        self.answers = df.loc[0:(self.itemzahl-1),"Antworten"]
        self.headers = df.loc[0:(self.itemzahl-1),"Header"]
        self.answ_list = list()
        self.multi = ""
        for answer in self.answers:
            self.answ_list.append(answer.split('//'))
        self.mult_answ = df.loc[0:(self.itemzahl-1),"Mehrfachauswahl"]
        x_start = startpos[0]
        y_start = startpos[1]
        box_size = 15
        box_dist = box_size + 125 #not real box dist!
        item_dist = box_size + dist_param #not real dist
        #x_scale_dist = 500
        self.box = list() #going to be the list with rect objects for clicking the answers
        self.answer = list() #going to be the list of objects with answer options
        self.text = list() #going to be the list of objects with itemtexts
        self.rating = list() #going to be the list for ratings
        for j, item in enumerate(self.itemtext):
            self.box.append(list())
            self.answer.append(list())
            self.rating.append(list())
            for i, answer in enumerate(self.answ_list[j]):
                self.box[j].append(visual.Rect(win, units = "pix",width = box_size, height = box_size, pos = (x_start+i*box_dist,y_start-j*item_dist), lineColor="black", fillColor="White"))
                self.answer[j].append(visual.TextStim(win, units = "pix", text=answer, height = textsize-5, color=(-1,-1,-1), wrapWidth =90,alignHoriz = "left", pos = (x_start+box_size +i*box_dist,y_start-j*item_dist)))
            if "TITEL DES TEXTES 1 EINBLENDEN" in item:
                item = item.replace("TITEL DES TEXTES 1 EINBLENDEN",titel[0])
            self.text.append(visual.TextStim(win, units = "pix", text = item, height = textsize, color=(-1,-1,-1),wrapWidth =800,  pos=(x_start,y_start+50-j*item_dist), alignHoriz = "left"))
    def draw(self, name=""):
        while True:
            for j in range(len(self.itemtext)):
                for i, box in enumerate(self.box[j]):
                    if self.mult_answ[j] == "nein": # for all single choice items
                        if self.mouse.isPressedIn(self.box[j][i]):
                            self.box[j][i].fillColor = "Black"
                            self.rating[j] = i+1
                            for k in np.delete(range(len(self.box[j])),i):
                                self.box[j][k].fillColor = "White"
                    else:                                           #for multi choice items
                        self.multi = True
                        if self.mouse.isPressedIn(self.box[j][i]):
                            if self.box[j][i].fillColor == "Black":
                                self.box[j][i].fillColor = "White"
                                self.rating[j].remove(i+1)
                            else:
                                self.box[j][i].fillColor = "Black"
                                self.rating[j].append(i+1)
                            core.wait(0.1)
                    self.box[j][i].draw()
                    self.answer[j][i].draw()
                self.text[j].draw()
            self.win.flip()
            x = 1
            for i, el in enumerate(self.rating):
                if not self.rating[i]:
                    x +=1
            
            #------- add name to header ---
            column_names = self.headers.apply(lambda x: name+"_"+str(x)) ##############add text name to quest-column names
            if x == 1:
                self.button[0].draw() #show button, when all items have been rated
                self.button[1].draw()
                if self.mouse.isPressedIn(self.button[0]): #save ratings to respective items, when button is pressed
#                    ratinglist = self.getRating()
                    if self.multi == True:
                        result = pd.DataFrame([self.rating], columns=column_names)
                    else:
                        result = pd.DataFrame(data=self.rating, index=column_names).transpose() #{"Items": self.headers, "Ratings": self.rating}
                    #result.to_csv(PATH+"\\data\\Ergebnis_MC_"+name+".csv", sep=';')
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
