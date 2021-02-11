# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 16:59:27 2021

@author: Wolf Culemann
"""

EXP_TITLE = "Lesen"

ET = None #"SMI" #"Eyelink"
PARALLEL = None #adress ...

QUEST_PATH = "./questionnaires/"

FULLSCREEN = True

#Bildschirmgröße anpassen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1024

MOUSE_BUTTONS = {"left_click":[1,0,0],"right_click":[0,0,1],"wheel_click":[0,1,0]}

#wenn MAX_FIX überschritten wird nachgefragt, nach Formel: MAX_FIX = dur_factor_mean*MEAN + dur_factor_sd*SD
dur_factor_mean = 2
dur_factor_sd = 2

#pupil_max gibt an, ab wann nachgefragt wird, wenn Pupille weg ist
pupil_max = 1

#delay gibt an, für wie viele Sekunden nach dem Umblättern (Erscheinen der neuen Seite) keine MW-Abfrage möglich ist
delay = 2

#quantiles for removing outliers from fix-list for calculation mean_fix
lower_quantile = 0.15
higher_quantile = 0.85

# positions for asking MW after Slide only if not already asked because of long fixation or lost pupil
ask_random = ["Folie7.png","Folie9.png","Folie10.png","Folie13.png","Folie15.png","Folie18.png","Folie21.png","Folie23.png"] 

#wie lange nicht mehr nachgefragt wird, nachdem eine MW-Abfrage kam
init_mw_break = 0 #1 = auf erster Folie, die für MW-Abfragen genutzt wird, poppt keine Abfrage auf, 0 = auf erster Folie kann schon gefragt werden
mw_break = 1 # 0 means mw can be shown on next slide, 1,2 means sleep for one, two slide(s)...

#Folien für die die Mean-Fixation (und SD) berechnet wird
example_slides = ["Folie1.png","Folie2.png"]

#Folien für die MW-Abfragen angezeigt werden, wenn Fix zu lang, Pupille zu lange weg oder Random-Abfrage zutrifft
main_slides = ["Folie3.png","Folie4.png","Folie5.png","Folie6.png","Folie7.png","Folie8.png","Folie9.png","Folie10.png","Folie11.png","Folie12.png","Folie13.png","Folie14.png","Folie15.png","Folie16.png","Folie17.png","Folie18.png","Folie19.png","Folie20.png","Folie21.png","Folie22.png","Folie23.png"]

#Text der bei MW-Abfrage angezeigt wird
#Tasten individuell einstellbar, Achtung: dann auch in dem Text ändern...
key_yes = "z"
key_no = "m"
#angezeigter Text/Frage:
question_wandering = "Haben Sie den Text gerade\n aufmerksam gelesen?\n\n linke Taste --> ja\n rechte Taste --> nein"
#question_wandering = "Haben Sie den Text jetzt gerade\n aufmerksam gelesen?\n\n linke Taste --> ja\n rechte Taste --> nein"
#question_wandering_page = "Haben Sie diese Seite\n aufmerksam gelesen?\n\n linke Taste --> ja\n rechte Taste --> nein"

# eye for calculation of mean fixation 1 = right, 0 = left
eye_calc = 1
max_pretrial_slides = 99#2 #for demo purpose
max_main_slides = 99#7#for demo purpose
FNAME_VP_INFO = "VP_"

#Ordner für Stimuli, Ergebnisse usw.
fpath_results = "./Results/"
fpath_stimuli = "./Stimuli/"
fpath_instruction = "./Instructions/"

RIGHT_EYE = 1
LEFT_EYE = 0
BINOCULAR = 2
ENDFIX = 8
TRACKER = "100.1.1.1"#None # default = "100.1.1.1" or None