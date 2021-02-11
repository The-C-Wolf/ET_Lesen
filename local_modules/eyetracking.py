# -*- coding: utf-8 -*-
"""
Created on Thur Feb 11 14:05:56 2021

@author: Wolf Culemann
"""


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