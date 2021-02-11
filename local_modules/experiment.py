# -*- coding: utf-8 -*-
"""
Created on Thur Feb 11 14:04:23 2021

@author: Wolf Culemann
"""

from psychopy import visual, event, core, gui
from collections import OrderedDict


MOUSE_BUTTONS = {"left_click":[1,0,0],"right_click":[0,0,1],"wheel_click":[0,1,0]}

def show_gui(exp_title):
 
    """show GUI for User Input before actual Exp starts"""
 
    guidict = dict()
    myDlg = gui.Dlg(title=exp_title)
    myDlg.addText('Probandeninfo')
    myDlg.addText('Bitte alle Felder ausfüllen!')
    myDlg.addField('Generierter Zuordnungscode:')
    myDlg.addField('Erster Buchstabe des Vornamens der Mutter:')
    myDlg.addField('Zweiter Buchstabe des Vornamens des Vaters:')
    myDlg.addField('Dritter Buchstabe des Familiennamens:')
    myDlg.addField('Vierter Buchstabe des Geburtsortes:')
    myDlg.addField('Monat des Geburtsdatums:',
                   choices=["","01","02","03","04","05","06","07","08","09","10","11","12"])
    myDlg.addField('Alter:',
                   choices=["","18","19","20","21","22","23","24","25","26","27","28","29","30",
                            "31","32","33","34","35","36","37","38","39","40","41","42","43","44",">44"])
    myDlg.addField('Geschlecht:',choices=["","weiblich","männlich","anderes"])
    myDlg.addField('Brille:',choices=["","nein","ja","Kontaktlinsen"])
    myDlg.addField('Muttersprache:',choices=["","Deutsch","Deutsch + Andere","andere"])
    myDlg.addField('Studiengang:')
    ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
    if myDlg.OK:
        guidict["vp_code"]= ok_data[1]+ok_data[2]+ok_data[3]+ok_data[4]+ok_data[5]
        guidict["age"] = ok_data[6]
        guidict["sex"] = ok_data[7]
        guidict["glass"] = ok_data[8]
        guidict["lang"] = ok_data[9]
        guidict["course"] = ok_data[10]
    else:
        print('user cancelled')
        core.quit()
    return guidict


class Experiment(object):
    
    def __init__(self, win, session, logger, exp_clock = core.Clock(), devices = dict()):
        
        self.win = win
        self.devices = devices
        self.session = session
        self.logger = logger
        self.exp_clock = exp_clock
        
        self._flow = OrderedDict()
        
        self.instructions = dict()
        self.questionnaires = dict()
        self.blocks = dict()
        self.misc = dict()
        
    @property
    def flow(self):
        return self._flow
    
    @flow.setter
    def flow(self, ordered_dict):
        self._flow = self.make_flow(ordered_dict)
        
    def make_flow(self, ordered_dict):
        flow = OrderedDict()
        for kind, name in ordered_dict.items():
            if kind == "instr":
                flow[name] = self.instructions[name]
            elif kind == "quest":
                flow[name] = self.questionnaires[name]
            elif kind == "block":
                flow[name] = self.blocks[name]
            elif kind == "misc":
                flow[name] = self.misc[name]
            else:
                raise NotImplementedError
            #create instances for each entry
        return flow
        
    def run(self):
        print("Run Experiment")
        self.exp_clock.reset()
        for element in self.flow:
            ret = element.run()
            print(element.name, "successfully ended")

class Block(object):
    """
    groups multiple Trials or Blocks
    """
    def __init__(self, name, contains, exp_clock):
        super(Block,self).__init__()
        self._name = name
        self._contains = contains
        self._n_max = len(contains)
        self._current_trial_no = None
        self._current_trial = None
        self._exp_clock = exp_clock
        self._start_time = 0
        self._end_time = 0
        self._duration = 0
        
    @property
    def duration(self):
        return self._duration
    
    @duration.setter
    def duration(self, dur):
        self._duration = dur #end_time - start_time
        
    def run(self):
        self._current_trial_no = 0
        self._start_time = self._exp_clock.getTime()
        while True:
            self._current_trial = self._contains[self._current_trial_no]
            ret = self._current_trial.run()
            if ret == "next":
                if self._current_trial_no+1 == self._n_max:
                    self._end_time = self._exp_clock.getTime()
                    self.duration = self._end_time - self._start_time
                    return "end"
                self._current_trial_no += 1
            elif ret == "previous":
                if self._current_trial_no == 0:
                    print("no previous entry!!! continue...")
                self._current_trial_no -= 1
            elif ret == "Quit":
                return ret


class Trial(object):
    """ 
    A Trial is a single unit in an experiment...
    
    e.g.
    event_dict = {"keyboard":{"space","ask_mw","right": "next", "left": "previous", "escape": "userquit"},
                    "mouse": {"left_click": "previous","right_click":"next"},
                    "et": {"some_thresh": "ask_mw"}}
    """
    def __init__(self, win, event_dict, exp_clock, content, userquit, mouse = None):
        
        self._win = win
        self._mouse = mouse
        
        self._exp_clock = exp_clock
        self._start_time = 0
        self._end_time = 0
        self._duration = 0
        
        self._content = content #list of objects to draw
        self._userquit = userquit
        self._event_dict = event_dict
        
    
    @property
    def duration(self):
        return self._duration
    
    @duration.setter
    def duration(self, dur):
        self._duration = dur #end_time - start_time
    
    @property
    def start_time(self):
        return self._start_time
    
    @start_time.setter
    def start_time(self, val):
        self._start_time = val
        
    @property
    def end_time(self):
        return self._end_time
    
    @end_time.setter
    def end_time(self, val):
        self._end_time = val
    
    def draw_content(self):
        for content in self._content:
            content.draw()
        self._win.flip()
        event.clearEvents()
    
    def run(self):
        self.start_time = self._exp_clock.getTime()
        
        while True:
            self.duration = self._exp_clock.getTime() - self.start_time
            
            if self.duration > self.t_min:
                
                if "keyboard" in self._event_dict:
                    pressed_keys = event.getKeys(keyList = self._event_dict["keyboard"])
                    if any([el for el in pressed_keys if el in self._event_dict["keyboard"]]):
                        return self._event_dict["keyboard"][pressed_keys[0]]
                
                if "mouse" in self._event_dict:
                    button = self._mouse.getPressed()
                    clickable = {name:MOUSE_BUTTONS[click] for name, click in self._event_dict["mouse"].items()}
                    for name, but in clickable:
                        if button == but:
                            return self._event_dict["mouse"][name]
               
            else:      
                self.draw_content()
            

class MindWanderProbe(Trial):
    """This probe consists of the blurred version of the text image, 
    presented in fullscreen mode and an overlay of MW question
    """
    def __init__(self, win, fpath_blurred, fpath_overlay, text_quest, t_min = 0,
                 keys_ans = {"1":"text","2":"other","3":"nothing"}):
        super(MindWanderProbe,self).__init__()
        self.win = win
        self.fpath_blurred = fpath_blurred
        self.overlay = visual.ImageStim(self.win, fpath_overlay)
        self.text = visual.TextStim(win = self.win, text = text_quest,
                                    color = "black", font = "RobotoMono-Regular.ttf")
        self.keys_ans = keys_ans
        self.t_min = t_min
        self._bg_image = None
        self.running_time = 0
        
    @property
    def bg_image(self):
        return self._bg_image
    
    @bg_image.setter
    def bg_image(self):
        self._bg_image = visual.ImageStim(self.win, self.fpath_blurred)
    
    def run(self):
        self.start_time = self._exp_clock.getTime()
        
        while True:
            pressed_keys = event.getKeys(keyList = self.keys_ans.append('escape'))
            self.running_time = self._exp_clock.getTime() - self.start_time
                    
            if self.running_time > self.t_min:
                match_list = [el for el in pressed_keys if el in self.keys_ans]
                if len(match_list) > 0:
                    self.duration = self._exp_clock.getTime() - self.start_time
                    #first matching key is the answer
                    answer = self.keys_ans[match_list[0]] 
                    return answer
            else:      
                self.bg_image.draw()
                self.overlay.draw()
                self.text.draw()
                self._win.flip()
                event.clearEvents()
            
            if self._enable_escape:
                if 'escape' in pressed_keys:
                    ret = self._userquit.check()
                    if ret == "Quit":
                        return ret
                    
class Questionnaire(Trial):
    """
    A LikertSkala or MultipleChoice
    """
    def __init__(self, fpath):
        super(Questionnaire,self).__init__()
        
        
