# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 16:53:12 2021

@author: Wolf Culemann
"""

from psychopy import visual, core, event, gui
import pandas as pd

#import gc

import sys
import os

import parameters as param
from local_modules.multiplechoice import MultipleChoice
from local_modules.likertskala import LikertSkala
from local_modules.subject import Subject
from local_modules.logfile import Logfile

if param.ET == "Eyelink":
    from pylink import *
    from constants import *
    from eyelinkCoreGraphicsPsychopy.EyeLinkCoreGraphicsPsychopy import EyeLinkCoreGraphicsPsychopy
    from eyelinkcommunication import EyelinkCommunication
elif param.ET == "SMI":
    from smi.et_smi import RedM
    from ctypes import *
    from smi.iViewXAPI import  *


def show_gui():
 
    """show GUI for User Input before actual Exp starts"""
 
    guidict = dict()
    myDlg = gui.Dlg(title=param.EXP_TITLE)
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
                    clickable = {name:param.MOUSE_BUTTONS[click] for name, click in self._event_dict["mouse"].items()}
                    for name, but in clickable:
                        if button == but:
                            return self._event_dict["mouse"][name]
               
            else:      
                self.draw_content()

class Calibration(object):
    
    def __init__(self, win, et, eye = "both", accuracy = 0.5, to_draw=None, userquit=None):
        super(Calibration,self).__init__()
        self.win = win
        self.et = et
        self.to_draw = to_draw
        self.accuracy = accuracy
        self.eye = eye #both, mean, one, l, r
        
    def run(self):   
        ac = 0.5
        if self.to_draw:
            for item in self.to_draw:
                #item.setImage(os.path.join(param.fpath_instructions, img))
                item.draw()
                self.win.flip()
                #core.wait(0.2)
            self.waitFixClick(mouse=mouse, button=[1,0,0], toDraw=toDraw, userquit=userquit, et=et, time=1,fixpos=[screen_width,screen_height/2], xdist=100, ydist=screen_height/2)
    
        white = visual.ImageStim(win, image=os.path.join(param.fpath_instructions, "whitescreen.png"), pos=(0.0, 0.0), units='pix')
        win.winHandle.set_fullscreen(False)
        win.winHandle.maximize()
        white.draw()
        win.flip()
        while True:
            dummy, calib_info, full_info = et.calibrate()
            cal_res = dict(calib_info)
            cal_full = dict(full_info)
            if float(cal_res["X:"])<=ac and float(cal_res["Y:"])<=ac:
                print("Calibrated"+str(cal_res))
                if ac ==0.5:
                    et.write('MSG:Calibrated_05:{0}'.format(cal_res))
                    et.write('MSG:Calibrated_05:{0}'.format(cal_full))
                else:
                    et.write('MSG:Calibrated_07:{0}'.format(cal_res))
                    et.write('MSG:Calibrated_07:{0}'.format(cal_full))
                break
            else:
                fail = visual.ImageStim(win, image=os.path.join(param.fpath_instructions, "calibration_fail.png"), pos=(0.0, 0.0), units='pix')
                self.waitFixClick(mouse=mouse, button=[1,0,0], toDraw=[fail], userquit=userquit, et=et, time=1,fixpos=[screen_width,screen_height/2], xdist=100, ydist=screen_height/2)
                ac=0.7
                et.write('MSG:Failed_Calibration_with:{0}'.format(cal_res))
                et.write('MSG:Failed_Calibration_with:{0}'.format(cal_full))
                print("Failed With"+str(cal_res))
                white.draw()
                win.flip()
        #white.draw()
        win.winHandle.set_fullscreen(True)
        event.clearEvents()
        return cal_res 
class Instruction(Trial):
    """An instruction consists of an image, that is presented
    in fullscreen mode and can be ended on an event
    """
    def __init__(self, fpath, keys_next, t_min):
        super(Instruction,self).__init__()
        self.fpath = fpath
        self.keys_next = keys_next
        self.t_min = t_min
        self._image = None
        self.running_time = 0
        
    @property
    def image(self):
        return self._image
    
    @image.setter
    def image(self):
        self._image = visual.ImageStim(self.win, self.fpath)
    
    def run(self):
        self.start_time = self._exp_clock.getTime()
        
        while True:
            pressed_keys = event.getKeys(keyList = self.keys_next.append('escape'))
            self.running_time = self._exp_clock.getTime() - self.start_time
                    
            if self.running_time > self.t_min:
                
                if any([el for el in pressed_keys if el in self.keys_next]):
                    self.duration = self._exp_clock.getTime() - self.start_time
                    break
            else:      
                self.image.draw()
                self._win.flip()
                event.clearEvents()
            
            if self._enable_escape:
                if 'escape' in pressed_keys:
                    self._userquit.check()

class PageReading(Trial):
    def __init__(self, win, fpath_image, t_min = 0,
                 keys_ans = {"right":"next","left":"previous","space":"instance_of_mind_wander_probe"}):
        super(PageReading, self).__init__()
        self.win = win
        self.fpath_image = fpath_image
        
        
    @property
    def text_image(self):
        return self._text_image
    
    @text_image.setter
    def text_image(self, img):
        self._text_image = img #visual.ImageStim(self.win, self.fpath_image)
        
        
class MindWanderProbe(Trial):
    """This probe consists of the blurred version of the text image, 
    presented in fullscreen mode and an overlay of MW question
    """
    def __init__(self, win, fpath_blurred, fpath_overlay, text_quest, t_min = 0,
                 keys_ans = {"1":"text","2":"other","3":"nothing"}):
        super(Instruction,self).__init__()
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

        

class Questionnaire(Trial):
    """
    A LikertSkala or MultipleChoice
    """
    def __init__(self, fpath):
        super(Questionnaire,self).__init__()

    
class Experiment(object):
    # --- log ---
    sep = ';'
    header = ('sid', 'age', 'sex', 'lang', 'glass','trial',
              'exptime','trackertime', 'item') 
              
    def __init__(self, win=None, mouse=None,et=None,ec = None,
                 et_fname=None, sess=None, fname_log=None, 
                 expclock=core.Clock(), vp_code = "999"):
        self.win = win
        self.mouse = mouse
        self.et = et
        self.ec = ec
        #self.edf_name = edf_name
        self.et_fname = et_fname
        self.sess = sess
        self.vp_code = vp_code
        self.expclock = expclock  
        self.fname = fname_log
        self.et_fname = '{0}'.format(self.fname[:-4])
        self.log = Logfile()
        self.log.open(self.fname,mode='w',header=self.header,sep=self.sep)
        
        self.quests = dict()
        
    
    def show_instruction(self,pic=None):
        
        if pic:
            slide = visual.ImageStim(win=self.win, image=param.fpath_instruction+pic)
            slide.draw() 
            self.win.flip()
        key = event.waitKeys(keyList=["space","escape"])
        if key[0] == "escape":
            self.endTrial(win=self.win,et=self.et,edf=self.edf_name)
        elif key[0] =="space":
            return 0
        else:
            return 1
    
    #def make_instructions(self, nested_dict)
    
    def make_questionnaires(self, nested_dict,button_pos=(400,-400)):
        
        """takes specified nested_dict structure
        returns dict with name - instance of LikertSkale or Multiple Choice - pairs"""
        
        for name, quest in nested_dict:
            
            self.quests[name] = []
            
            fpath = os.path.join(param.QUEST_PATH,quest["file"])
            #questionnaire input
            if fpath.endswith(".csv"):
                df = pd.read_csv(fpath, sep=";")
            elif fpath.endswith(".xlsx"):
                df = pd.read_excel(fpath)
            else:
                raise Exception("no valid filetype - .csv or .xlsx expected")
            
            if quest["shuffle"]:
                df = df.sample(frac=1)
                df = df.reset_index()
                
            #split into pages    
            if quest["split"]:
                if type(quest["split"]) == int:
                    last_item = quest["split"]
                    df1 = df.loc[0:last_item,:]
                    df1 = df1.reset_index()
                    df2 = df.loc[last_item+1:,:]
                    df2 = df2.reset_index()
                    df_list = [df1,df2]
                elif type(quest["split"]) == list:
                    df_list = []
                    #n_splits = len(quest["split"])
                    df_tail = df
                    for split in quest["split"]:
                        df_head = df_tail[:split]
                        df_list.append(df_head)
                        df_tail = df_tail[split:]
                    df_list.append(df_tail)
                else:
                    raise Exception("unknown splitting type - None, int or list expected")
            else:
                df_list = [df]
            #create instance for each page
            if quest["kind"] == "LS":
                for df in df_list:
                    self.quests[name].append(
                            LikertSkala(self.win, self.mouse, df ,button_pos))
            elif quest["kind"] == "MC":
                for df in df_list:
                    self.quests[name].append(
                            MultipleChoice(self.win, self.mouse, df, [name],dist_param=90,startpos=(-300,400),button_pos))
    
    def show_result(self,win=None,t_fix=[0]):
        
        n_fix = len(t_fix)
        mean_fix = round(pd.Series(t_fix).mean(),2)
        sd_fix = round(pd.Series(t_fix).std(),2)
        text = "Anzahl der Fixationen: {0} \n\n Mittlere Fixationsdauer: {1} \n\n Standardabweichung Fixationsdauer: {2}".format(n_fix,mean_fix,sd_fix)
        result = visual.TextStim(win=win, color="black",text=text, height=50)
        result.draw()
        win.flip()
        key = event.waitKeys(keyList=["space","escape"])
        if key[0] == "escape":
            self.endTrial()
        elif key[0] =="return":
            return 0
        else:
            return 1
    
    def run_example_trials(self,slide=None,max_dur=None,max_slides=None):
        
        """presents one slide for reading and returns list with fixation durations"""
        
        ec = self.ec
        et = self.et
        win = self.win
        edf = self.edf_name
        log = self.log
        img = visual.ImageStim(win, None)
        sample = None
        DURATION = max_dur
        t_fix = []
        gaze = 0
        
        ######################
        et.setOfflineMode()
        msecDelay(50)
        error = et.startRecording(1,1,1,1) #1,1,0,1 -- 0 means send events only through link
        if error:
            print("Error after trying to start Recording...")
            print(error)
            return error
        #begin the realtime mode
        beginRealTimeMode(100)
        #clear tracker display to black
        et.sendCommand("clear_screen 0")
        startTime = currentTime()
        try: 
            et.waitForBlockStart(100,1,0) 
        except RuntimeError: 
            if getLastError()[0] == 0: # wait time expired without link data 
                self.endTrial()
                print ("ERROR: No link samples received!") 
                return TRIAL_ERROR 
            else: # for any other status simply re-raise the exception 
                raise
        eye_used = et.eyeAvailable() #determine which eye(s) are available 
        if eye_used == param.RIGHT_EYE:
            et.sendMessage("EYE_USED 1 RIGHT")
        elif eye_used == param.LEFT_EYE or eye_used == param.BINOCULAR:
            et.sendMessage("EYE_USED 0 LEFT")
            eye_used = param.LEFT_EYE
        elif eye_used == param.BINOCULAR:
            et.sendMessage("EYE_USED 2 BINOCULAR")
        else:
            print("Error in getting the eye information!")
            return TRIAL_ERROR
        
        et.flushKeybuttons(0)
        
        ####################################
        img.setImage(param.fpath_stimuli+slide)
        img.draw()
        self.win.flip()
        et.sendMessage("SHOW PRE SLIDE "+slide)
        last_draw_time = currentTime()
        log.add_row()
        log['sid'] = self.sess.sid
        log['age'] = self.sess.age
        log['sex'] = self.sess.sex
        log['lang'] = self.sess.lang
        log['glass'] = self.sess.glass
        log['trial'] = i
        log['exptime'] = self.expclock.getTime()
        log['trackertime'] = self.et.trackerTime()
        log['item'] = slide
        while 1:
            error = et.isRecording()  # First check if recording is aborted 
            if error!=0:
                print("End Trail because of Error...")
                self.endTrial()
                return error
            ltype = et.getNextData()
            if ltype == param.ENDFIX: #elif
                et.sendMessage("fixEnd")
                ldata = et.getFloatData()
                if ldata.getEye() == param.eye_calc:
                    gaze = ldata.getAverageGaze()
                    t_start = ldata.getStartTime()
                    t_end = ldata.getEndTime()
                    dur = t_end-t_start + 1 # see manual - to compute duration subtract times and add 1 msec
                    t_fix.append(dur)
            keylist = event.getKeys()
            if keylist == ['space']:
                print("spacebar pressed...continue..")
                break
        log.write_row()
        ret_value = et.getRecordingStatus()
        endRealTimeMode()
        et.sendMessage("TRIAL OK")
        return t_fix #list with fixation durations
        
    def run_other_trials(self,slides=None,max_dur=None,max_slides=None,t_fix=[0],mw_break = 0):
        
        """presents for reading, asks for mindwandering if pupil or fixation is over thresholds or random mw is activated"""
        
        ec = self.ec
        et = self.et
        win = self.win
        edf = self.edf_name
        log = self.log
        img = visual.ImageStim(win, None)
        sample = None
        DURATION = max_dur
        n_fix = len(t_fix)
        mean_fix = round(pd.Series(t_fix).mean(),2)
        sd_fix = round(pd.Series(t_fix).std(),2)
        fix_max = (param.dur_factor_mean*mean_fix)+(param.dur_factor_sd*sd_fix)
        print("fix_max")
        print(fix_max)
        mw_dict = {}
        n_event = 0
        pupil = 1
        pupil_timer = core.Clock()
        mw_delay_timer = core.Clock()
        gaze = 0
        
        #############
        et.setOfflineMode()
        msecDelay(50)
        error = et.startRecording(1,1,1,1) #1,1,0,1 -- 0 means send events only through link
        if error:
            print("Error after trying to start Recording...")
            print(error)
            return error
        #begin the realtime mode
        beginRealTimeMode(100)
        #clear tracker display to black
        et.sendCommand("clear_screen 0")
        startTime = currentTime()
        try: 
            getEYELINK().waitForBlockStart(100,1,0) 
        except RuntimeError: 
            if getLastError()[0] == 0: # wait time expired without link data 
                self.endTrial()
                print ("ERROR: No link samples received!") 
                return TRIAL_ERROR 
            else: # for any other status simply re-raise the exception 
                raise
        eye_used = et.eyeAvailable() #determine which eye(s) are available 
        if eye_used == param.RIGHT_EYE:
            et.sendMessage("EYE_USED 1 RIGHT")
        elif eye_used == param.LEFT_EYE or eye_used == param.BINOCULAR:
            et.sendMessage("EYE_USED 0 LEFT")
            eye_used = param.LEFT_EYE
        elif eye_used == param.BINOCULAR:
            et.sendMessage("EYE_USED 2 BINOCULAR")
        else:
            print("Error in getting the eye information!")
            return TRIAL_ERROR
        
        et.flushKeybuttons(0)
        ###################
        
        if slide in param.ask_random:
            mw_random = True
        else:
            mw_random = False
        et.resetData() #reset buffer
        slide_event = 0 # reset event counter
        img.setImage(param.fpath_stimuli+slide)
        img.draw()
        self.win.flip()
        et.sendMessage("SHOW MAIN SLIDE "+slide)
        last_draw_time = currentTime()
        mw_delay_timer.reset()
        log.add_row()
        log['sid'] = self.sess.sid
        log['age'] = self.sess.age
        log['sex'] = self.sess.sex
        log['lang'] = self.sess.lang
        log['glass'] = self.sess.glass
        log['trial'] = i
        log['exptime'] = self.expclock.getTime()
        log['trackertime'] = self.et.trackerTime()
        log['item'] = slide
        while 1:
            error = et.isRecording()  # First check if recording is aborted 
            if error!=0:
                print("End Trail because of Error...")
                self.endTrial()
                return error
            ltype = et.getNextData()
            if ltype == param.ENDFIX: #elif
                #et.sendMessage("fixEnd") ###ANGELA
                ldata = et.getFloatData()
               # if ldata.getEye() == param.eye_calc:  #ACHTUNGANGELA
                if (ldata.getEye() == param.eye_calc) or (ldata.getEye() != param.eye_calc):
                    #gaze = ldata.getAverageGaze()
                    t_start = ldata.getStartTime()
                    t_end = ldata.getEndTime()
                    dur = t_end-t_start + 1 # see manual - to compute duration subtract times and add 1 msec
                    if (dur > fix_max) and (slide_event == 0) and (mw_break == 0) and (mw_delay_timer.getTime() > param.delay):
                        self.et.sendMessage("MW_FIX")  ###ANGELA                        
                        exptime = self.expclock.getTime()
                        trackertime = et.trackerTime()
                        n_event += 1
                        print(dur)
                        print("Sehr lange Fixation...frage nach!")
                        ans, rt = self.askWandering(slide=slide)
                        et.resetData()
                        slide_event +=1
                        pupil_timer.reset()
                        mw_dict[n_event] = {}
                        mw_dict[n_event]["kind"] = "fixation"
                        mw_dict[n_event]["ans"] = ans
                        mw_dict[n_event]["RT"] = rt
                        mw_dict[n_event]["img"] = slide
                        mw_dict[n_event]["trackertime"] = trackertime
                        mw_dict[n_event]["exptime"] = exptime
                        mw_random = False
                        mw_break = param.mw_break
            gaze, pupil = ec.getGazePupil(et,param.eye_calc)
            if pupil != 0.0:
                pupil_timer.reset()
            if (pupil_timer.getTime() > param.pupil_max) and (slide_event == 0) and (mw_break == 0)and (mw_delay_timer.getTime() > param.delay):
                exptime = self.expclock.getTime()
                trackertime = et.trackerTime()
                n_event += 1
                print("Pupillengroesse zu lange auf 0...frage nach!")
                ans, rt = self.askWandering(slide=slide)
                et.resetData()
                slide_event += 1
                mw_dict[n_event] = {}
                mw_dict[n_event]["kind"] = "pupil"
                mw_dict[n_event]["ans"] = ans
                mw_dict[n_event]["RT"] = rt
                mw_dict[n_event]["img"] = slide
                mw_dict[n_event]["trackertime"] = trackertime
                mw_dict[n_event]["exptime"] = exptime
                #mw_dict[n_event]["time"] = currentTime()
                mw_random = False
                mw_break = param.mw_break
            keylist = event.getKeys()
            if keylist == ['space']:
                #ask for mw random!
                self.et.sendMessage("LEERTASTE")  ###ANGELA! self.et.sendMessage("BLA") 
                if (mw_random == True) and (mw_break == 0):
                    self.et.sendMessage("MW_RANDOM")  ###ANGELA!
                    exptime = self.expclock.getTime()
                    trackertime = et.trackerTime()
                    n_event += 1
                    print("Slide war für random eingestellt, Sleep nicht aktiviert...frage nach!")
                    ans, rt = self.askWandering(slide=slide,trial_end=True)
                    et.resetData()
                    slide_event += 1
                    mw_dict[n_event] = {}
                    mw_dict[n_event]["kind"] = "random"
                    mw_dict[n_event]["ans"] = ans
                    mw_dict[n_event]["RT"] = rt
                    mw_dict[n_event]["img"] = slide
                    mw_dict[n_event]["trackertime"] = trackertime
                    mw_dict[n_event]["exptime"] = exptime
                    #mw_dict[n_event]["time"] = currentTime()
                    mw_break = param.mw_break
                if slide_event == 0: #keine MW-Abfrage
                    mw_break -= 1
                print("spacebar pressed...continue..")
                break
        log.write_row()
        ret_value = et.getRecordingStatus()
        endRealTimeMode()
        et.sendMessage("TRIAL OK")
        return mw_dict,mw_break,mean_fix,sd_fix,fix_max

    def ask_wandering(self,slide,ans_keys=[param.key_yes,param.key_no],trial_end=False):
        
        """shows blurred version of the slide,
        opens up rectangle with question if subject mindwandered
        returns ans_key and reaction time"""
        
        event.clearEvents()
        ans = 2
        img = visual.ImageStim(self.win, param.fpath_stimuli+"blurred_"+slide)
        rect = visual.Rect(self.win, width=800,height=200,fillColor="grey", lineColor="black",opacity=0.7)
        quest = visual.TextStim(self.win, text=param.question_wandering, color="black", height=25, wrapWidth=300)
        quest_timer = core.Clock()
        quest_timer.reset()
        self.et.sendMessage("MW_Start") ###ANGELA
        while True:
            keylist = event.getKeys(keyList=ans_keys)
            img.draw()
            rect.draw()
            quest.draw()
            self.win.flip()
            if keylist == list(ans_keys[0]):
                ans = 1
                rt = quest_timer.getTime()
                if not trial_end:
                    img.setImage(param.fpath_stimuli+slide)
                img.draw()
                self.win.flip()
                break
            elif keylist == list(ans_keys[1]):
                ans = 0
                rt = quest_timer.getTime()
                if not trial_end:
                    img.setImage(param.fpath_stimuli+slide)
                img.draw()
                self.win.flip()
                break
        self.et.sendMessage("MW_End")  ###ANGELA
        return ans, rt
                
    def end_trial(self):
        
        self.log.write('ProgramQuit')
        self.log.close()
        self.ec.onEnd() #eyelinkcommunication
        self.win.close()
        sys.exit()



def main():
    
    # change current directory to the one where this code is located 
    spath = os.path.dirname(sys.argv[0])
    if len(spath) !=0: os.chdir(spath)
    
    #show gui and get data
    vp_data = show_gui()
    #create window and mouse objects
    win = visual.Window(fullscr=FULLSCREEN, size= [screen_width,screen_height], color='white', units='pix',winType='pyglet',gammaErrorPolicy="warn") 
    mouse = event.Mouse(visible=True)
 
    if param.ET == "Eyelink":
        #set EDF name
        et_fname = vp_data["vp_code"] + ".EDF"
        #init eyetracker
        ec = EyelinkCommunication(address=param.TRACKER, et_fname=et_fname,
                                  screen_width=param.SCREEN_WIDTH,screen_height=param.SCREEN_HEIGHT,
                                  win=win)    
        et = ec.trackerSetup() #eyelinkcommunication
        ec.sendInitCommands() #send initial commands and set edf file contents
        if(et.isConnected() and not et.breakPressed()):
            print("Tracker is connected, start Experiment ...")
            
    elif param.ET == "SMI":
        #set IDF name
        et_fname = vp_data["vp_code"] + ".IDF"
        et = RedM()
        et.mode = 'normal'
        et.open()
        ec = None
    else:
        print("no Eyetracker in Use")
        et_fname = None
        et = None
        ec = None
    
    
    #create experiment instance
    exp = Experiment(
            et = et,
            ec = ec,
            win = win,
            sess = sess,
            et_fname = et_fname,
            vp_code = vp_data["vp_code"],
            mouse = mouse,
            fname_log = log_fname)#,screen_size=[param.SCREEN_WIDTH,param.SCREEN_HEIGHT])
    
    #create questionnaire objects
    exp.make_questionnaires(
            nested_dict =
            {
            "demographics":
                {"file": "demograph.xlsx",
                 "kind": "MC",
                 "split": [6],
                 "shuffle": False},
                 
             "between-text":
                 {"file": "between_text.xlsx",
                  "kind": "MC",
                  "split": None,
                  "shuffle": False},
                  
              "final-ratings":
                  {"file": "final_ratings.xlsx",
                   "kind": "LS",
                   "split": [6,11],
                   "shuffle": True}
              })
    
    exp.make_instructions(
            nested_dict =
            {
            "introduction":
                {"file": "Folie_1.PNG",
                 "key_next": ["space"],
                 "t_min": 3},
             "eyetracker":
                 {"file": "Folie_2.PNG",
                  "key_next": ["space"],
                  "t_min": 3},
              "demographics":
                 {"file": "Folie_3.PNG",
                  "key_next": ["space"],
                  "t_min": 3},
                    }
            )
    
    exp.make_blocks(
            nested_dict =
            {
            "read_text_1":
                {}})
    
    #kinds of trials: instr, quest, misc, trial, block
    exp.create_flow = [
            {"instr":"introduction"},
            {"instr":"eyetracker"},
            {"misc":"calibration"},
            {"instr":"demographics"},
            {"quest":"demographics"},
            {"instr":"mw_intro"},
            {"instr":"mw_instr"},
            {"block":"read_text_1"},
            {"block":"read_text_2"},
            {"instr":"ratings_intro"},
            {"quest":"final_ratings"},
            {"instr":"end"}
            ]
    
    
        
        
        
        exp.showInstruction(pic="Folie1.png") #Willkommen
      #  exp.showInstruction(pic="Folie2.png") #Instruktion
        
        #present slides for getting baseline fixation list
        fix_list = []
        slides = param.example_slides
        for i, slide in enumerate(slides[:param.max_pretrial_slides]):
            t_fix = exp.runExampleTrials(slide=slide)
            fix_list.extend(t_fix)

        #remove outlier from raw fixation baseline list
        raw_fix = fix_list #for baseline log
        fix_list = removeOutlier(fix_list)
        
        #present slides for mw query
        mw_list = []
        slides = param.main_slides
        mw_br = param.init_mw_break
        trial_dict = {}
        for i, slide in enumerate(slides[:param.max_main_slides]):
            if (i >= param.init_mw_break) and (trial_dict == {}):
                mw_br = 0
            trial_dict,mw_br,mean_fix,sd_fix,fix_max = exp.runOtherTrials(slides=param.main_slides,t_fix=fix_list,mw_break=mw_br)
            mw_list.append(pd.DataFrame(trial_dict).transpose())
        
        print("send Trial RESULT message to et")
        #TRIAL_RESULT message defines the end of a trial for the EyeLink Data Viewer. 
        #This is different than the end of recording message END that is logged when the trial recording ends. 
        #Data viewer will not parse any messages, events, or samples that exist in the data file after this message. 
        et.sendMessage("TRIAL_RESULT %d"%(0))
        
        df_mw = pd.concat(mw_list)
        df_mw.to_csv(param.fpath_results+param.FNAME_VP_INFO+vp_id+"_mindwander.csv")
        
        #writing baseline logfile
        df_base = saveBaselineLog(raw_fix,fix_list,mean_fix,sd_fix,fix_max)
        df_base.to_csv(param.fpath_results+param.FNAME_VP_INFO+vp_id+"_baseline.csv")


        exp.showInstruction(pic="Folie3.png") #Instruktion
        
        #present multiple choice questions
        mouse.setVisible(1)
        df1_1 = mc_wiss1.draw("wiss1")
        df1 = df1_1
        df1.to_csv(param.fpath_results+param.FNAME_VP_INFO+vp_id+"_wissen.csv",encoding="utf-8")
       # df1_2 = mc_wiss2.draw("wiss2")
       # df1 = pd.concat([df1_1,df1_2],axis=1)
        #df1.to_csv(param.fpath_results+param.FNAME_VP_INFO+vp_id+"_wissen.csv",encoding="utf-8")
        mouse.setVisible(0)
        
       # exp.showInstruction(pic="Folie3.png") #Instruktion
        
        #present likertskala questions
        mouse.setVisible(1)
        df2_1 = ls_int1.draw("int1")
        df2 = df2_1
        df2.to_csv(param.fpath_results+param.FNAME_VP_INFO+vp_id+"_interesse.csv",encoding="utf-8")
        #df2_2 = ls_int2.draw("int2")
        #df2 = pd.concat([df2_1,df2_2],axis=0)
        #df2.to_csv(param.fpath_results+param.FNAME_VP_INFO+vp_id+"_interesse.csv",encoding="utf-8")
        mouse.setVisible(0)
        
        exp.showInstruction(pic="Folie4.png") #Ende
        
        #ends experiment, closes logfiles, gets EDF etc...
        exp.endTrial()
    else:
        print("Tracker is not connected or break is pressed...terminate Experiment...!")
        win.close()
        sys.exit()

########################
if __name__ == '__main__':
    print("Start Experiment with Eyetracker:",param.ET, "and Parallel Port:",param.PARALLEL)
    main()
