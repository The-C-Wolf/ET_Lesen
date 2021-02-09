# -*- coding: utf-8 -*-
"""
Created on Sun Aug 09 11:10:30 2015

@author: tamm


Changed on Fri Mar 29 13:38:18 2019
@author: culemann
"""


ET          = 0
FULLSCREEN  = 1

########################################
from psychopy import visual, core, event
#from oculib.misc import Struct
#from oculib.psychopy import Clock, UserQuit
from psychopy.core import Clock
from userquit import UserQuit

from smi.et_smi import RedM
from logfile import Logfile
from subject import Subject

#from oculib.hardware import RedM, Logfile
#from misc import Subject
import parameters as param
from multiplechoice import MultipleChoice
#from likertskala import LikertSkala
from LikertSkala_phq import LikertSkala
import pandas as pd
from ctypes import *
from smi.iViewXAPI import  *

from win32api import GetSystemMetrics

import os
import sys

screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

    
class TextLesen(object):
    # --- log ---
    sep = ';'
    header = ('sid', 'age', 'sex', 'lang', 'glass','trial', 'exptime', 'item')
              
    def __init__(self, win=None, et=RedM(), 
                 sess=dict(sid='999', group='1'), 
                 fname_log=None, expclock=Clock(), vp_id = "999"):
        self.win = win
        self.et = et

        self.sess = sess
        self.vp_id = vp_id
        
        self.expclock = expclock
        # --- logfile + et-file ---
        if fname_log is None:
#            self.fname = os.path.join(param.fpath_results,
#                                      'vp_{0}_{1}.txt'.format(self.sess.sid, self.sess.group))
            self.fname = os.path.join(param.fpath_results,
                                      'vp{0}.txt'.format(self.sess.sid))
        else: self.fname = fname_log 
        self.et_fname = '{0}'.format(self.fname[:-4])
      
        self.idf_path = os.path.abspath(param.fpath_results)  # smi sdk can only handle absolute path information
        self.log = Logfile()
        
        
    def calibrate(self,win=None, et=None, toDraw=None, img="dummy.jpg", userquit=None):
        event.clearEvents()
        if toDraw:
            for item in toDraw:
                item.setImage(os.path.join(param.fpath_instructions, img))
                item.draw()
                win.flip()
                core.wait(0.2)
            #if img=="calibration_zw.png":
            #    self.waitFixation(et=self.et, time=1,fixpos=[screen_width,screen_height/2], xdist=100, ydist=screen_height/2,toDraw=toDraw, userquit=userquit)
            #else:
            self.waitFixClick(mouse=mouse, button=[1,0,0], toDraw=toDraw, userquit=userquit, et=et, time=1,fixpos=[screen_width,screen_height/2], xdist=100, ydist=screen_height/2)
    
        white = visual.ImageStim(win, image=os.path.join(param.fpath_instructions, "whitescreen.png"), pos=(0.0, 0.0), units='pix')
        win.winHandle.set_fullscreen(False)
        win.winHandle.maximize()
        white.draw()
        win.flip()
        ac = 0.5
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
        
    def waitMouseClick(self,mouse=None, button=[1,0,0],toDraw=None, userquit=None):#, log=log, et=et, sess=sess, fname=fname):
        but = mouse.getPressed()
        while but != button:
            ret = userquit.check()
            if ret == 'Quit':
                self._on_quit()
            but = mouse.getPressed()
            if toDraw:
                for item in toDraw:
                    item.draw()
            win.flip()
        event.clearEvents()
#==============================================================================
#             if but == button:
#                 event.clearEvents()
#                 core.wait(0.2)
#                 break
#==============================================================================

    def waitFixation(self,et=None, time=2,fixpos=[240,160], xdist=50, ydist=50,toDraw=None, userquit=None):
        #rect = visual.Rect(win,width=100,height=100, pos=(0,0), lineColor="black", units="pix")
        #pos_txt = visual.TextStim(win, pos=(0,0), text="NA",height=30, color="black")
        if et:
            timer = core.CountdownTimer(time)
            while timer.getTime() > 0:
                ret = userquit.check()
                if ret == 'Quit':
                    self._on_quit()
                res = et._iViewXAPI.iViewXAPI.iV_GetSample(byref(sampleData))
                if res == 1:
                    x = ((sampleData.rightEye.gazeX < (fixpos[0]+xdist)) and (sampleData.rightEye.gazeX > (fixpos[0]-xdist)))
                    y = ((sampleData.rightEye.gazeY < (fixpos[1]+ydist)) and (sampleData.rightEye.gazeY > (fixpos[1]-ydist)))
                    cur_pos= (int((sampleData.rightEye.gazeX-screen_width/2)),int(-1*(sampleData.rightEye.gazeY-screen_height/2)))
                    #rect.setPos(cur_pos)
                    #pos_txt.setPos(cur_pos)
                    #pos_txt.setText(str(cur_pos))
                    if toDraw:
                        for item in toDraw:
                            item.draw()
                        #rect.draw()
                        #pos_txt.draw()
                        win.flip()
                    if x == True and y == True:
                        continue
                        #print("fixed")
                    else:
                        timer.reset(time)
            event.clearEvents()
                        
    def waitFixClick(self,et=None,mouse=None, button=[1,0,0], time=2,fixpos=[0,0], xdist=50, ydist=50,toDraw=None, userquit=None):
        but = mouse.getPressed()
        rect = visual.Rect(win,width=100,height=100, pos=(0,0), lineColor="black", units="pix")
        pos_txt = visual.TextStim(win, pos=(0,0), text="NA",height=30, color="black")
        if et:
            timer = core.CountdownTimer(time)
            while timer.getTime() > 0 and but == [0, 0, 0]:
                but = mouse.getPressed()
                ret = userquit.check()
                if ret == 'Quit':
                    self._on_quit()
                res = et._iViewXAPI.iViewXAPI.iV_GetSample(byref(sampleData))
                if res == 1:
                    x = ((sampleData.rightEye.gazeX < (fixpos[0]+xdist)) and (sampleData.rightEye.gazeX > (fixpos[0]-xdist)))
                    y = ((sampleData.rightEye.gazeY < (fixpos[1]+ydist)) and (sampleData.rightEye.gazeY > (fixpos[1]-ydist)))
                    cur_pos= (int((sampleData.rightEye.gazeX-screen_width/2)),int(-1*(sampleData.rightEye.gazeY-screen_height/2)))
    #==============================================================================
    #                 gazeX = sampleData.rightEye.gazeX
    #                 gazeY = sampleData.rightEye.gazeY
    #                 rect.setPos(cur_pos)
    #                 pos_txt.setPos(cur_pos)
    #                 pos_txt.setText(str(gazeX)+"_"+str(gazeY))
    #==============================================================================
                    if toDraw:
                        for item in toDraw:
                            item.draw()
                        #rect.draw()
                        #pos_txt.draw()
                        win.flip()
                    if x == True and y == True:
                        continue
                        #print("fixed")
                    else:
                        timer.reset(time)
                if but == button:
                    event.clearEvents()
                    core.wait(0.2)
                    break
            event.clearEvents()
    

    def run(self, maxtrials=None):
        win = self.win
        
        # gl_info = win.winHandle.context.get_info()
        # print(gl_info)
        # import pdb;pdb.set_trace()
        # if not gl_info.have_version(2,0,0):
        #     raise RuntimeError(
        #         "PsychoPy requires OpenGL 2.0+, exiting.")
        
        
        
        et = self.et
        et_fname = self.et_fname
        
        
        userquit = UserQuit(win, on_quit=self._on_quit, logfiles=(self.log, self.et))  
        
        log = self.log
        log.open(self.fname, mode='w', header=self.header, sep=self.sep)
           
        # --- visual stimuli --------------
        msg_img = visual.ImageStim(win, image=None, pos=(0.0, 0.0), units='pix')
        fixcross = visual.ImageStim(win, image = os.path.join(param.fpath_stimuli, 'Fixcross.png'))
        
        stim = visual.ImageStim(win, image=None)
        # --------------------------------

        trial_list = []
#==============================================================================
        for i in range(6): #50
            trial_list.append("./Stimuli/Seite_"+str(i)+".png")
            
#==============================================================================
        
        n_page_calib1 = [12,22,37]#,58,71,79,91,107,117,129] # [12,22,37,49,58,71,79,91,107,117,129]


        #todo: umblättern Ecke rechts unten
        #-------start------------
        
        mouse.setVisible(0)
        
        
        msg_img.setImage(os.path.join(param.fpath_instructions, 'start.png'))
        self.waitMouseClick(mouse, button=[1,0,0], toDraw=[msg_img], userquit=userquit)
        event.clearEvents()
        msg_img.setImage(os.path.join(param.fpath_instructions, "calibration.png"))
        #----------------------------------------------------------------------------

        #--------------------------------------------------------------------------------
        self.et.start_recording(str(et_fname+'_1'))###give set number for having separate log files
        if et._iViewXAPI:  
            ret = et._iViewXAPI.iViewXAPI.iV_StartRecording()

        if ET:
            cal_res = []
            c= self.calibrate(win=win, et=et, toDraw=[msg_img], img="calibration.png", userquit=userquit)
            cal_res.append(c)
        
        
         # --- instructions -----
        msg_img.setImage(os.path.join(param.fpath_instructions, 'instruction1.png'))
        self.waitFixation(et=self.et, time=1,fixpos=[screen_width,screen_height/2], xdist=100, ydist=screen_height/2,toDraw=[msg_img], userquit=userquit)

        ####--------show Beispieltext #---------------------------
        userquit_et = UserQuit(win, on_quit=self._on_quit, logfiles=(self.log, self.et), on_calib=self.calibrate, userquit=userquit)
        self.waitFixation(et=self.et, time=0.5,fixpos=[330,90], xdist=100, ydist=100, toDraw=[fixcross], userquit=userquit_et)
        stim.setImage("./Beispiel.png")
        stim.draw()
        win.flip()
        self.waitFixation(et=self.et, time=1,fixpos=[screen_width,screen_height/2], xdist=100, ydist=screen_height/2,toDraw=[stim], userquit=userquit_et)
        #self.waitFixClick(mouse=mouse, button=[1,0,0], toDraw=[stim], userquit=userquit_et, et=self.et, time=1,fixpos=[screen_width,screen_height/2], xdist=100, ydist=screen_height/2)

        msg_img.setImage(os.path.join(param.fpath_instructions, 'instruction2.png'))
        self.waitFixation(et=self.et, time=1,fixpos=[screen_width,screen_height/2], xdist=100, ydist=screen_height/2,toDraw=[msg_img], userquit=userquit_et)
        # -----------------------
        
        # --- Start recording and run trials ---
#==============================================================================
#         self.et.start_recording(str(et_fname+'_1'))###give set number for having separate log files
#         if et._iViewXAPI:  
#             ret = et._iViewXAPI.iViewXAPI.iV_StartRecording()
#==============================================================================
        
        
        rtclock = Clock()

        for trial_id, trial in enumerate(trial_list[:maxtrials], start=1):
            userquit_et = UserQuit(win, on_quit=self._on_quit, logfiles=(self.log, self.et), on_calib=self.calibrate, userquit=userquit)  
            self.waitFixation(et=self.et, time=0.5,fixpos=[345,100], xdist=100, ydist=100, toDraw=[fixcross], userquit=userquit_et)
            event.clearEvents()
            
            log.add_row()
            log['sid'] = self.sess.sid
            log['age'] = self.sess.age
            log['sex'] = self.sess.sex
            log['lang'] = self.sess.lang
            log['glass'] = self.sess.glass
            #log['group'] = self.sess.group
            log['trial'] = trial_id
            log['exptime'] = self.expclock.getTime()
            log['item'] = trial
    
            
            stim.setImage(trial)
            #print(trial)
            stim.draw()

            win.flip()
            rtclock.reset()
                                
            et.write('MSG:START:TRIAL{0}:IMAGE:{1}'.format(trial_id, os.path.basename(trial))) 
            if et._iViewXAPI: et._iViewXAPI.iViewXAPI.iV_SendImageMessage(os.path.basename(trial).lower())  # s. BeGaze p. 107 
            #self.waitFixation(et=self.et, time=1,fixpos=[screen_width,screen_height/2], xdist=100, ydist=screen_height/2,toDraw=[stim], userquit=userquit_et)
            self.waitFixClick(mouse=mouse, button=[1,0,0], toDraw=[stim], userquit=userquit_et, et=self.et, time=1,fixpos=[screen_width,screen_height/2], xdist=100, ydist=screen_height/2)
            event.clearEvents()

            et.write('MSG:STOP:TRIAL{0}:IMAGE:{1}'.format(trial_id, os.path.basename(trial))) 
            if et._iViewXAPI: et._iViewXAPI.iViewXAPI.iV_SendImageMessage('dummy.jpg')  # s. BeGaze p. 107 
            log.write_row()
            if trial_id-1 in n_page_calib1:
                x = int(n_page_calib1.index(trial_id-1))+1
                c= self.calibrate(win=win, et=et, toDraw=[msg_img], img="zw_"+str(x)+".png", userquit=userquit_et)
                cal_res.append(c)
                event.clearEvents()

        #-------Stop ET Recording
        self.et.stop_recording()
        if self.et._iViewXAPI:
            res = self.et._iViewXAPI.iViewXAPI.iV_StopRecording()
            res = self.et._iViewXAPI.iViewXAPI.iV_SaveData(os.path.join(self.idf_path, os.path.splitext(os.path.basename(self.fname))[0]+'.idf'),str('vp'+str(self.sess.sid)+str("_1")),str(''),1)
        msg_img.setImage(os.path.join(param.fpath_instructions, 'pause.png'))
        core.wait(3)
        self.waitMouseClick(mouse, button= [0,0,1], toDraw=[msg_img], userquit=userquit)        
        
    
    def _on_quit(self):
        self.log.write('ProgramQuit')
        self.log.close()
        self.et.write('MSG:Quit')
        self.et.stop_recording()
        if self.et._iViewXAPI:
            res = self.et._iViewXAPI.iViewXAPI.iV_StopRecording()
            res = self.et._iViewXAPI.iViewXAPI.iV_SaveData(os.path.join(self.idf_path, os.path.splitext(os.path.basename(self.fname))[0]+'.idf'),str('vp'+str(self.sess.sid)),str(''),1)
        self.et.close()
        core.wait(0.5)  # give time to close files properly
        self.win.close()
        sys.exit()  # Achtung: sys.exit() darf nie in einem try-Block stehen - dann wird es nicht ausgefuehrt!

########################
if __name__ == '__main__':
   
    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)
    
    maxtrials = 5
    
    sess = Subject(result_dir=param.fpath_results)
    
    res, vp_id, age, glass, lang, sex = sess.show(title=u'VP-Info') ###returns 1 and vp-nummer
    print(age)
    print(glass)
    vp_info = pd.DataFrame([])
    vp_info["VP-Code"] = vp_id
    vp_info["Alter"] = age
    vp_info["Geschlecht"] = sex
    vp_info["MuSpr"] = lang
    vp_info["Sehhilfe"] = glass
    f_info = param.fpath_results + "/info_"+str(vp_id) + ".csv"
    print(vp_info)
    vp_info.to_csv(f_info, encoding="utf-8")
    
    if res == 0:
        sys.exit()
    
    win = visual.Window(fullscr=FULLSCREEN, size= [screen_width,screen_height], color='white', units='pix',winType='pygame')  #size= [1300,900] #,winType='pyglet'
    mouse = event.Mouse(visible=True)

    et = RedM()
    if ET:
        et.mode = 'normal'
    et.open()
    
    result=dict()
    
#    flow = list()
#
#    instr_block = Block(name="instructions",order="consecutive")
#    for img in ["instr_1.png","instr_2.png","instr_3.png"]:
#        new_trial = ReadingTrial(name = img,
#                                 stimfile = img,
#                                 events = {"keyboard":                  ##"left":"previous_trial", #"space":"show_mw"
#                                               {"right":"end_trial",
#                                                "esc":"show_userquit",}
#                                               })
#        instr_block.add_trial(new_trial)
#    flow.append(instr_Block)
#
#           
#    
#    
#    flow = [instr_block,text1,text2,end_block]
    
    ws = TextLesen(win, et=et, sess=sess, vp_id = vp_id)
    ws.run(maxtrials=maxtrials)
    

    
    et.close()         
    win.close()
    sys.exit()
   