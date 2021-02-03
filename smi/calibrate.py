# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 19:47:07 2013

@author: ocunostics
"""

# todo: Trenne Calibration-prozedur und Anzeige/Rueckmeldemodule!

# todo: binoc->monoc->... umschalten, wenn Auge nicht trackbar

# "Wackelmaß" für Augenpos auch ohne Tracken möglich?

# todo: Esc bevor Kalibration beginnt bringt komischen Effekt


# Hat "schnell" und "langsam" im Calib auch Auswirkungen, wenn ich manuell und extern kalibriere?

# Click mouse einbauen etc. (s. Calib-Tests SMI)

# todo: speed parameter einbauen

# todo: fixtarget per encode("base64") 
# direkt in calibrate.py speichern

# todo: space fuer manuellen Mode einbauen (momentan 'e')
# pyglet behandelt spacebar anders als sonstige Tasten -->
# spacebar kann dauerhaft Signal liefern und muss deshalb gesondert 
# behandelt werden (s. event.py:
#def _onPygletText(text, emulated=False):
#    """handler for on_text pyglet events, or call directly to emulate a text
#    event.
#
#    S Mathot 2012: This function only acts when the key that is pressed
#    corresponds to a non-ASCII text character (Greek, Arabic, Hebrew, etc.). In
#    that case the symbol that is passed to _onPygletKey() is translated into a
#    useless 'user_key()' string. If this happens, _onPygletText takes over the
#    role of capturing the key. Unfortunately, _onPygletText() cannot solely
#    handle all input, because it does not respond to spacebar presses, etc.



# SMI
# cp.number-Sequenz fuer 5-Punkt-Kalibration:
        # -1, 1, 2, 3, 4, 5, -1 --> bei zweitem -1 Kalibration beenden
# core.wait(0.5) nach Calibrate(): # verhindere Startpunkt (-641.0, 513.0) = linke obere Ecke - SDK-Bug???

# autoaccept = True bereitet Probleme:
# Meine Tastenabfrage scheint mit Tastenabfrage fuer Start von Eyetracker zu "kollidieren"
# Frage ich Taste nicht ab, startet Eyetracker; frage ich Taste ab, ueberspringt er Punkte
# Ausweg waere: Startabfrage "vor" aktivieren der Kalibration zu legen

from psychopy import core, event, visual
#from oculib.hardware._smi import iView, iViewStruct
import ctypes
import numpy as np
from PIL import Image
from oculib.hardware import RedM
from oculib.psychopy import misc, Dialog

class Calibrate:
    def __init__( self, win, method=5, distance_limit=(50,70),
                 autotracking=True, accept='space',
                 target='standard', target_motion=True, target_size=20):
        self._win            = win
        self._method         = method
        self._distance_limit = distance_limit
        self._target         = target
        self._target_size    = target_size
        self._target_motion  = target_motion
        self._autotracking   = autotracking
        if not isinstance(accept, (list,tuple)):
            self._accept = (accept,) # [key] | 'mouse'
        else:
            self._accept = accept           
        
        if target == 'standard':
            self._target = visual.ImageStim(win, image='calibtarget.png',
                                            size = self._target_size, units='pix')


    def calibrate(self):
        ret = self._init_calibrate_validate(mode='calibrate')  # set calibration parameter
        if ret != 1:
            return ret

        ret = iView.iView._XAPI.iV_Calibrate()
        if ret != 1:
            raise Exception('Unexpected return value: {0}'.format(ret))
        core.wait(0.5)  # verhindere Startpunkt (-641.0, 513.0) = linke obere Ecke - SDK-Bug???

        ret = self._do_calibrate_validate(mode='calibrate')
        return ret
        
    def validate(self):
        #if self._isCalibrated is False:
        #    return

        #self._init_calibrate_validate()  # set validation parameter
        # nur noetig, wenn gegenueber Calibration etwas veraendert werden soll?
        # z.B. manuelle Validierung moeglich???

        # wieviele Punkte bei Validierung - woran erkenne ich das Ende?

        ret = iView.iView._XAPI.iV_Validate()
        if ret != 1:
            raise Exception('Unexpected return value: {0}'.format(ret))
        core.wait(0.5)  # verhindere Startpunkt (-641.0, 513.0) = linke obere Ecke - SDK-Bug???

        ret = self._do_calibrate_validate(mode='validate')
        return ret

    def show_accuracy( self ):
        #if self._isValidated is False:
        #    return

        ac = iViewStruct.AccuracyData()
        res = iView.iView._XAPI.iV_GetAccuracy(ctypes.byref(ac._CAccuracyData),0)

        w = 450
        h = 450
        mydlg = Dialog(self._win, roundness=9, win_background=None, pos=(0,0), width=w, height=h)
        mydlg.add(visual.TextStim(self._win, text='Validierung', pos=(0., 195), units='pix', height=30))

        x_ac = (ac._CAccuracyData.deviationLX+ac._CAccuracyData.deviationRX)/2.
        y_ac = (ac._CAccuracyData.deviationLY+ac._CAccuracyData.deviationRY)/2.
        mydlg.add(visual.TextStim(self._win, text='dx: {0}    dy: {1}'.format(x_ac, y_ac), pos=(0., 125.),
                                  units='pix', height=30))

        image = iViewStruct.ImageData()
        ret = iView.iView._XAPI.iV_GetAccuracyImage(ctypes.byref(image._CImageData))
        if ret:
            strimg = ctypes.string_at(image._CImageData.imageBuffer, image._CImageData.imageSize)
            myimg = Image.fromstring('RGB', (image._CImageData.imageWidth, image._CImageData.imageHeight), strimg)
            ac_image = visual.ImageStim(self._win, image=myimg, pos=(0,-50), size=(320,240), units='pix')
            mydlg.add(ac_image)

        ret = mydlg.show()
        if ret == 'OK':
            pass

    def _animate(self, pos1, pos2, msg, sd):
        step = 10
        xstart, xstop = pos1[0], pos2[0]
        ystart, ystop = pos1[1], pos2[1]

        if abs(xstop - xstart) >= abs(ystop - ystart):
            sign = (xstop-xstart)/abs(xstop-xstart)  # +1 or -1
            x = np.arange(xstart, xstop, sign*step)
            y = np.linspace(ystart, ystop, num=len(x))
        else:
            sign = (ystop-ystart)/abs(ystop-ystart)  # +1 or -1
            y = np.arange(ystart, ystop, sign*step)
            x = np.linspace(xstart, xstop, num=len(y))

        for xi, yi in zip(x, y):
            self._target.setPos((xi, yi))
            self._target.draw()

            self._show_distance(msg, sd)

            self._win.flip()
            core.wait(0.001)

    def _show_distance(self, msg, sd):
        iView.iView._XAPI.iV_GetSample(ctypes.byref(sd._CSampleData))
        msg.setText('Distance: {0}'.format(int(round(sd.leftEye.eyePositionZ))))
        msg.draw()

    def _init_calibrate_validate(self, mode=None):
        cd = iViewStruct.CalibrationData()
        cd.method = self._method  # calibration method (3 point,
        # 5 point,...)
        cd.visualization = 0  # 0: external; 1: SMI SDK
        cd.displayDevice = 0  # 0: primary device; 1: secondary device
        cd.speed = 0  # calibration/validation speed: 0: slow;
        # 1: fast
        if self._autotracking is True:
            cd.autoAccept = 1  # 0: manual; 1: auto
        else:
            cd.autoAccept = 0
        cd.foregroundBrightness = 20  # calibration/validation target
        #  brightness[0..255]
        cd.backgroundBrightness = 239  # calibration/validation background
        # brightness
        cd.targetShape = 2  # 0: image; 1: CIRCLE1; 2: CIRCLE2;
        # 3pos = misc.screen2win(win, (cp.positionX, cp.positionY)): CROSS
        cd.targetSize = self._target_size  # target size in pixels
        cd.targetFilename = b''  # used with targetShape = 0

        # Code gehört eigentlich _do_calibrate_validate (s. dort)

        if self._autotracking is True and mode == 'calibrate':
            msg = visual.TextStim(self._win, text='', units='pix')
            sd = iViewStruct.SampleData()
            pos = (0., 0.)
            self._target.setPos(pos)
            while 1:
                # wait for initial button press to start calibration/ validation
                self._target.draw()
                self._show_distance(msg, sd) # todo profiling: sd mitgeben oder in Unterfunktion neu erzeugen?
                self._win.flip()

                # todo: prevent repetition when space bar is pressed
                key = event.getKeys()
                if key:
                    key = key[0]
                    event.clearEvents()
                    # todo: ohne clearEvents scheint der Tracker bei autotracking=True
                    #   immer mehr als einen Punkt weiterzuspringen --> Interaktion mit irgendeiner event loop/Tastenabfrage von SMI?
                    if key in self._accept:
                        break
                    elif key == 'escape':
                        return 0

        ret = iView.iView._XAPI.iV_SetupCalibration(ctypes.byref(cd._CCalibrationData))
        if ret == 1: # todo: replace with SMI return code
            return 1
        else:
            return 0

    def _do_calibrate_validate(self, mode=None):
        """
        Return  0: Calibration/ Validation aborted
                1: Success

        """
        # todo: Man koennte auf mode verzichten, wenn man
        #   den namen der aufrufenden Funktion ermitteln koennte.
        #   Der Weg ueber das Inspect-Modul ist mir aber zu aufwendig.

        if mode == 'calibrate':
            npoints = self._method
        elif mode == 'validate':
            npoints = 4  # todo: Ist das beim Validieren immer der Fall?
        else:
            return 0

        msg = visual.TextStim(self._win, text='', units='pix')
        cp = iViewStruct.CalibrationPoint()
        sd = iViewStruct.SampleData()

        # Code gehört eigentlich hier her; momentan in _calibration_init() um bei autotracking=True
        # zu verhindern, dass am Anfang bei meinem Tastendruck zu viele Punkte übersprungen werden
        # (baue ich keine Tastenabfrage ein, startet Tracker sofort, baue ich Taste ein, scheint der Tracker diese
        #  auch noch mal auszuwerten).
        #if self._autotracking is True and mode != 'validate':
        #    pos = (0., 0.)
        #    self._target.setPos(pos)
        #    while 1:
        #        # wait for initial button press to start calibration/ validation
        #        self._target.draw()
        #        self._show_distance(msg, sd) # todo profiling: sd mitgeben oder in Unterfunktion neu erzeugen?
        #        self._win.flip()
        #
        #        # todo: prevent repetition when space bar is pressed
        #        key = event.getKeys()
        #        if key:
        #            key = key[0]
        #            event.clearEvents()
        #            # todo: ohne clearEvents scheitn der Tracker bei autotracking=True
        #            # immer mehr als einen Punkt weiterzuspringen --> Interaktion mit irgendeiner event loop/Tastenabfrage von SMI?
        #            if key in self._accept:
        #                break
        #            elif key == 'escape':
        #                iView.iView._XAPI.iV_AbortCalibration()
        #                return 0


        lastcp = None
        lastpos = None
        # calibration/ validation loop
        while 1:
            iView.iView._XAPI.iV_GetCurrentCalibrationPoint(ctypes.byref(cp._CCalibrationPoint))
            pos = misc.screen2win(self._win, (cp.positionX, cp.positionY))

            if lastcp == npoints and cp.number == -1:
                return 1 # calibration/validation successfully finished

            if pos != lastpos:
                if lastpos is not None and self._target_motion is True:
                    self._animate(lastpos, pos, msg, sd)
                lastpos = pos

            self._target.setPos(pos)
            self._target.draw()
            self._show_distance(msg, sd)
            self._win.flip()

            if cp.number is not lastcp:
                lastcp = cp.number

            # todo: prevent repetition when space bar is pressed
            key = event.getKeys()
            if key:
                key = key[0]
                event.clearEvents()
                if self._autotracking is False and key in self._accept:
                    ret = iView.iView._XAPI.iV_AcceptCalibrationPoint()
                elif key == 'escape':
                    iView.iView._XAPI.iV_AbortCalibration()
                    return 0

#################################
if __name__ == '__main__':
    eye = RedM()

    eye.mode = 'normal'
    eye.open()

    win = visual.Window(fullscr=True, color=(0.9, 0.9, 0.9) )

    cal = Calibrate(win, accept='e', autotracking=True)
    ret = cal.calibrate()
    if ret == 0:
        print('Calibration aborted')
    elif ret == 1:
        weg=''
        iView.iView._XAPI.iV_GetCalibrationStatus(ctypes.c_char_p(weg))
        import pdb; pdb.set_trace()
        ret = cal.validate()

        if ret == 0:
            print('Validation aborted')
        elif ret == 1:
            cal.show_accuracy()

    win.close()
    core.quit()