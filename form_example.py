# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 10:23:05 2021

@author: Wolf Culemann
"""

import os
import sys
import pandas as pd
from psychopy import visual, core, event, gui
from local_modules.likertskala import LikertSkala
from local_modules.multiplechoice import MultipleChoice
from win32api import GetSystemMetrics

screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)


FULLSCREEN = 0
DEBUG = 1

EXP_TITLE = "Lesen"

QUEST_PATH = "./questionnaires/"
RES_PATH = "./Results/"



def showGui():
    guidict = dict()
    myDlg = gui.Dlg(title=EXP_TITLE)
    myDlg.addText('Probandeninfo')
    myDlg.addText('Bitte alle Felder ausfüllen!')
    myDlg.addField('Generierter Zuordnungscode:')
    myDlg.addField('Erster Buchstabe des Vornamens der Mutter:')
    myDlg.addField('Zweiter Buchstabe des Vornamens des Vaters:')
    myDlg.addField('Dritter Buchstabe des Familiennamens:')
    myDlg.addField('Vierter Buchstabe des Geburtsortes:')
    myDlg.addField('Monat des Geburtsdatums:',choices=["","01","02","03","04","05","06","07","08","09","10","11","12"])
    myDlg.addField('Alter:',choices=["","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33",
                                     "34","35","36","37","38","39","40","41","42","43","44",">44"])
    myDlg.addField('Geschlecht:',choices=["","weiblich","männlich","anderes"])
    myDlg.addField('Studiengang:')
    myDlg.addField('Ungefähre Körpergröße (in cm):')
    myDlg.addField('Ungefähres Körpergewicht (in kg):')
    ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
    if myDlg.OK:
        guidict["vp_code"]= ok_data[1]+ok_data[2]+ok_data[3]+ok_data[4]+ok_data[5]
        guidict["age"] = ok_data[6]
        guidict["sex"] = ok_data[7]
        guidict["course"] = ok_data[8]
        guidict["height"] = ok_data[9]
        guidict["weight"] = ok_data[10]
    else:
        print('user cancelled')
        core.quit()
    return guidict


def split_quest(fpath, last_item, shuffle=True):
    #questionnaire input
    if fpath.endswith(".csv"):
        df = pd.read_csv(fpath, sep=";")
    elif fpath.endswith(".xlsx"):
        df = pd.read_excel(fpath)
    else:
        raise Exception("no valid filetype - .csv or .xlsx expected")
    if shuffle:
        df = df.sample(frac=1)
    df = df.reset_index()
    df1 = df.loc[0:last_item,:]
    df1 = df1.reset_index()
    df2 = df.loc[last_item+1:,:]
    df2 = df2.reset_index()
    return [df1,df2]

########################################################################
#START


def main():
    
    #create window and mouse objects
    win = visual.Window(fullscr=FULLSCREEN, size= [screen_width,screen_height], color='white', units='pix',winType='pyglet',gammaErrorPolicy="warn") 
    mouse = event.Mouse(visible=True)
    
    #dataframe to store vp data
    vp_data = pd.DataFrame([])
    
    #minimze window and show gui
    win.winHandle.set_fullscreen(False)
    win.winHandle.minimize()
    vp_info = showGui()
    for v in vp_info.keys():
        vp_data.loc[0,v] = vp_info[v]
    win.winHandle.set_fullscreen(FULLSCREEN)
    win.winHandle.maximize()
    
    #load questionnaires
    dfs_meta = split_quest(os.path.join(QUEST_PATH,"Meta.xlsx"),last_item = 6)
    dfs_sgse = split_quest(os.path.join(QUEST_PATH,"SGSE_BFI.xlsx"),last_item = 9)
    
    #init questionnaires
    sgse1 = LikertSkala(win, mouse, dfs_sgse[0],button_pos=(400,-400))
    sgse2 = LikertSkala(win, mouse, dfs_sgse[1],button_pos=(400,-400))
    meta1 = MultipleChoice(win, mouse, dfs_meta[0], ["Metadaten1"],dist_param=90,startpos=(-300,400),button_pos=(400,-400))
    meta2 = MultipleChoice(win, mouse, dfs_meta[1], ["Metadaten2"],dist_param=90,startpos=(-300,100),button_pos=(400,-300))
    
    #show questionnaires
    df_res_meta1  = meta1.draw("Meta1")
    vp_data = pd.concat([vp_data,df_res_meta1],axis=1)
    df_res_meta2 = meta2.draw("Meta2")
    vp_data = pd.concat([vp_data,df_res_meta2],axis=1)
    
    #append questionnaire data to vp_code gui data
    df_res_sgse1 = sgse1.draw("SGSE1")
    vp_data = pd.concat([vp_data,df_res_sgse1],axis=1)
    df_res_sgse2 = sgse2.draw("SGSE2")
    vp_data = pd.concat([vp_data,df_res_sgse2],axis=1)
    
    #save data
    vp_data.to_csv(os.path.join(RES_PATH,"results.csv"))
    
    
    win.close()
    sys.exit()


if __name__ == "__main__":
    main()

