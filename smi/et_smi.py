# -*- coding: utf-8 -*-

from psychopy import gui
import os
import time
#underscore thread for python3
import _thread as thread  # todo: umstellen auf threading (fuer polling mode) 


# Sobald auf hardware/__init__.py zugegriffen und REDM geladen wird,
# sucht das System iViewXAPI. Daher kann man ein Programm auch im Dummymode 
# nur dann auf einem Rechner uasführen, wenn das SMI-SDK installiert ist. 
# Hier wird iViewXAPI auf None gesetzt und beim Umschalten von Dummy- auf
# Messmode geprueft, ob die DLL verfuegbar ist
#try:

from . import iViewXAPI  # iViewX library RED-m Eyetracker
#except:
#    iViewXAPI = None
    
import ctypes as ct
from .device import EyeTracker


class SmiEyeTracker(EyeTracker):
    """
        todo: replace with implementation by Jens
    """
    def __init__(self, samplingmode='polling'):
        """
        StartRecording(), StopRecording(): Wie kann ich testen, ob Gerät idf-Mode kann?

        write-Funktion mit idf-flag oder spezielle Funktion: new_trial --> setzt automatisch idf-kompatiblen Trenner

        """
        super(SmiEyeTracker, self).__init__()
        
        ### new 07052014 ###
        if samplingmode not in ('callback', 'polling'):
            samplingmode = 'callback'
        self.samplingmode = samplingmode


        # todo: calibrate und validate: nur per callback oder intern;
        # wenn callback: Anbindung fuer automatischen Trigger auf Parallel oder Serial (EEG, Nexus, ETG-4000)
        # einbauen; genauso fuer Validierung

        ### Code taken from local_redm.py --> todo: komplett Ueberarbeiten
        self.sampling_rate = None
        self.polling_interval = None
        self.polling_thread = None

        self.eye_distance = None
        self.sampledata = None
        self.eventdata = None

        self.fname = None
        self.fname_gaze = None
        self.fname_fix = None
        self._fgaze = None  # file handle
        self._ffix = None

        #self._stop = threading.Event( )
        self._stop = False

        self._recording = False
        # direct access to underlying API
        self._iViewXAPI = iViewXAPI

    def open(self):
        """Entspricht iViexAPI.connect()
        """
        if self._mode == 'dummy':
            return

        res = iViewXAPI.iViewXAPI.iV_SetLogger(ct.c_int(1), ct.c_char_p(b"tracker.log"))

        #res = iViewXAPI.iV_Connect(ct.c_char_p('160.45.120.146'), ct.c_int(4444), ct.c_char_p('160.45.120.194'), ct.c_int(5555))
        res = iViewXAPI.iViewXAPI.iV_Connect(ct.c_char_p(b'127.0.0.1'), ct.c_int(4444), ct.c_char_p(b'127.0.0.1'), ct.c_int(5555))
        if res == 1:
            pass  # ok
        elif res == 104:  # no SMI eye tracking application running
            raise RuntimeError('Could not connect to RED-m.')
        else:
            raise RuntimeError('RED-m error: {0}'.format(res))

        res = iViewXAPI.iViewXAPI.iV_GetSystemInfo(ct.byref(iViewXAPI.systemData))

        # Set device polling rate to 2*sampling_rate
        self.sampling_rate = iViewXAPI.systemData.samplerate # Hz
        
        if self.samplingmode == 'polling':
            self.polling_interval = 1./(2.*self.sampling_rate)
            self.polling_thread = None

    def close(self):
        """Entspricht iViewXAPI.disconnect()
        """
        if self._mode == 'dummy':
            return

        if self._recording:
            self.stop_recording()

        res = iViewXAPI.iViewXAPI.iV_Disconnect()

    @EyeTracker.mode.setter
    def mode(self, val):
        """Wrap device mode setter to handle dummy mode on 
           systems without SMI-SDK (i.e. iViewXAPI is None)
        """
        if str(val.lower()) != 'dummy' and iViewXAPI is None:
            raise Warning('iViewXAPI not found. Maybe SMI-SDK is not installed?\n'+
                'Still running in "dummy" mode.')
            return
        
        EyeTracker.mode.fset(self, val)
        
    def start_recording(self, fname=None, mode='raw'):
        # todo: check if et is connected
        # todo: implement raw vs. idf
        if self.mode == 'dummy':
            return
        
    
        # --- WINFUNCTYPE does not work with self? ---        
        @ct.WINFUNCTYPE(None, iViewXAPI.CSample)
        def _sample_callback(sample):
            """
            Callback function for gaze samples when recording via callback.
            
            """
            print('s')
            self.sampledata = sample
            self._write_gaze(self.sampledata)
        
        @ct.WINFUNCTYPE(None, iViewXAPI.CEvent)  
        def _event_callback(event):
            """
            Callback function for events when recording via callback.
         
            """
            print('e')
            self.eventdata = event
            self._write_fix(self.eventdata)
        # ------------------------------------------
        
        if self._recording is True:
            raise Warning('Tracker is still recording')
            return  # todo: Man koennte pruefen, ob alter Dateiname = neuer Dateiname etc.; wird aber sehr komplex
        else:
            self._stop = False  # reset stop signal for polling thread; 
            # ersetzen durch self.recording-flag???
        if fname is None:  
            if self.fname is None:   
                raise Exception('File name missing.')
            else:  # continue session paused with stop_recording
                self._fgaze = open(self.fname_gaze, 'a')
                self._ffix  = open(self.fname_fix, 'a')
                self.eye_distance = 0  # left eye distance (todo: right eye)  # wofuer gebraucht?
        else:  # fname given and tracker not recording: create new outputfile
            # todo: warning if file still exists?
            self.fname = fname        
            self.fname_gaze = '{0}_gaze.txt'.format(os.path.splitext(fname)[0])
            self.fname_fix  = '{0}_fix.txt'.format(os.path.splitext(fname)[0])
            self._fgaze = open(self.fname_gaze, 'w')
            self._ffix  = open(self.fname_fix, 'w')
            self.eye_distance = 0  # left eye distance (todo: right eye)
                
        if self.samplingmode == 'polling':
            self.polling_thread = thread.start_new_thread(self._poll_data, ())
        else:  # 'callback'
            res = iViewXAPI.iViewXAPI.iV_SetSampleCallback(_sample_callback)
            res = iViewXAPI.iViewXAPI.iV_SetEventCallback(_event_callback)
        
        self._recording = True

    def stop_recording(self):
        # todo: idf-mode
        if self.mode == 'dummy' or self._recording is False:
            return

        if self.samplingmode == 'polling':
            #self.polling_thread.exit()
            self._stop = True
            time.sleep(0.5)
            self.polling_thread = None
        else:  # 'callback'
            res = iViewXAPI.iViewXAPI.iV_SetSampleCallback(0)
            res = iViewXAPI.iViewXAPI.iV_SetEventCallback(0)
                        
        self._fgaze.close()
        self._ffix.close()

        self._recording = False

    def write(self, message):
        if self.mode == 'dummy':
            return
        elif self._recording is False:
            return
        #    raise Exception('Recording not started.')
        # if self.dummy:
        #     self.msglog.write('{0} {1}\n'.format(self.timestamp.getTime(), message))
        # else:

        self._fgaze.write('{0} {1}\n'.format(self.timestamp, message))
        self._ffix.write('{0} {1}\n'.format(self.timestamp, message))
        

    def _write_gaze(self, sampleData):
        if self.mode == 'dummy':
            return

        # if self.dummy:
        #     return
        # else:
            # check distance
            ## todo: right eye
            #if sampleData.leftEye.eyePositionZ > 700 or sampleData.leftEye.eyePositionZ < 500:
            #    self.out_of_range = True
            #else:
            #    self.out_of_range = False
        self.eye_distance = sampleData.leftEye.eyePositionZ
        self._fgaze.write(
                str(sampleData.timestamp)+" " +
                str(sampleData.leftEye.gazeX) + " " +
                str(sampleData.leftEye.gazeY) + " " +
                str(sampleData.leftEye.diam) + " " +
                str(sampleData.leftEye.eyePositionX) + " " +
                str(sampleData.leftEye.eyePositionY) + " " +
                str(sampleData.leftEye.eyePositionZ) + " " +
                str(sampleData.rightEye.gazeX) + " " +
                str(sampleData.rightEye.gazeY) + " " +
                str(sampleData.rightEye.diam) + " " +
                str(sampleData.rightEye.eyePositionX) + " " +
                str(sampleData.rightEye.eyePositionY) + " " +
                str(sampleData.rightEye.eyePositionZ) + "\n")

    def _write_fix(self, eventData):
        if self.mode == 'dummy':
            return

        # if self.dummy:
        #     return
        # else:
        self._ffix.write(
                str(eventData.eventType) + " " +
                str(eventData.eye) + " " +
                str(eventData.startTime) + " " +
                str(eventData.endTime) + " " +
                str(eventData.duration) + " " +
                str(eventData.positionX) + " " +
                str(eventData.positionY) + "\n")
                

    def get_tracking_monitor(self):
        if self.mode == 'dummy':
            return

        res = iViewXAPI.iViewXAPI.iV_GetTrackingMonitor(ct.byref(iViewXAPI.imageData))
        return iViewXAPI.imageData

    def _poll_data(self):
        """
        Thread reading gaze and fixation data from RED-m device.
        Device response codes:
            1: ok
            2: no new data available
            101: tracker disconnected
        """
        while self._stop is False:
            time.sleep(self.polling_interval) # theoretisch koennte man nur Restzeit "schlafen", wenn man einen Timer mitlaufen lässt

            # gaze data
            res = iViewXAPI.iViewXAPI.iV_GetSample(ct.byref(iViewXAPI.sampleData))
            if res == 1:
                self.sampledata = iViewXAPI.sampleData 
                self._write_gaze(self.sampledata)
            # todo:
            # elif res==101:
            #     self.stopPolling()

            # fixation data
            res = iViewXAPI.iViewXAPI.iV_GetEvent(ct.byref(iViewXAPI.eventData))
            if res == 1:
                # todo: wer schreibt hier? thread safe?
                self.eventdata = iViewXAPI.eventData
                self._write_fix(self.eventdata)
            # todo:
            # elif res==101:
            #    self.stopPolling()

    def calibrate(self, validate=True):
        """
        Calibration and validation
        """
        if self.mode == 'dummy':
            return

#==============================================================================
# 
# class CCalibration(Structure):
# 	_fields_ = [("method", c_int),
# 	("visualization", c_int),
# 	("displayDevice", c_int),
# 	("speed", c_int),
# 	("autoAccept", c_int),
# 	("foregroundBrightness", c_int),
# 	("backgroundBrightness", c_int),
# 	("targetShape", c_int),
# 	("targetSize", c_int),
# 	("targetFilename", c_char * 256)]
#==============================================================================
        calibrationData = iViewXAPI.CCalibration(5, 1, 0, 0, 2, 0, 255, 0, 25, b"calibtarget.png")
        #calibrationData = iViewXAPI.CCalibration(5,1,0,0,1,0,250,0,25, b'calibtarget.png')
        while 1:
            res = iViewXAPI.iViewXAPI.iV_SetupCalibration(ct.byref(calibrationData))
            res = iViewXAPI.iViewXAPI.iV_Calibrate()

            if validate:
                calib_info, res, full_info = self.validate()
                if res == 1:  # ok
                    return 1, calib_info, full_info
                elif res == -1:  # cancel
                    return -1
                elif res == 0:
                    continue

    def validate(self):
        while 1:
            res = iViewXAPI.iViewXAPI.iV_Validate()
            # todo: if res != 1:
                ###
            res = iViewXAPI.iViewXAPI.iV_GetAccuracy(ct.byref(iViewXAPI.accuracyData), 0)
            calib_info, dummy, full_info = self._showValidationResults(iViewXAPI.accuracyData)
            #if float(calib_info['X:']) < float(0.7) and (calib_info['Y:']) < float(0.7):
            #    dummy = 1
            #else:
            #    dummy = 0
                
            if dummy == 1: 
                return calib_info, 1, full_info  # ok
            elif dummy == 0:
                return 0  # calibrate again  # todo: zusaetzlich nur Validierung wiederholen anbieten!!!
            else: # -1 cancel
                return -1
                
        

    def _showValidationResults(self, acData):
        if self.mode == 'dummy':
            return
        full_info = {"left":{'X:':str(acData.deviationLX),'Y:':str(acData.deviationLY)},
        "right":{'X:':str(acData.deviationRX),'Y:':str(acData.deviationRY)}
        }
        info = {
        'X:':str((acData.deviationLX+acData.deviationRX)/2.),
        'Y:':str((acData.deviationLY+acData.deviationRY)/2.),
        }
        #print(info)
        return info, 1, full_info
# =============================================================================
#         infoDlg = gui.DlgFromDict(dictionary=info, title="Validation accuracy", fixed=['X:',  'Y:'])
#         if infoDlg.OK:
#             return(1)
#         else:
#             retryDlg = gui.Dlg(title="")
#             retryDlg.addText(' ')
#             retryDlg.addText('Retry calibration?')
#             retryDlg.addText(' ')
#             retryDlg.show()
#             if retryDlg.OK:
#                 return 0
#             else:
#                 return -1
# =============================================================================

#    @property
#    def sampledata(self):
#        res = iViewXAPI.iViewXAPI.iV_GetSample(ct.byref(iViewXAPI.sampleData))
#        if res == 1:
#            return iViewXAPI.sampleData
#        # else: implicitly returns None
#
#    @property
#    def eventdata(self):
#        res = iViewXAPI.iViewXAPI.iV_GetEvent(ct.byref(iViewXAPI.eventData))
#        if res == 1:
#            return iViewXAPI.eventData
#
    @property
    def timestamp(self):
        """
        Wrapper for the iViewXAPI iV_GetCurrentTimestamp() function, making
        the current eye-trackers timestamp a (read-only) attribute.
        """

        ts = ct.c_longlong(0)
        res = iViewXAPI.iViewXAPI.iV_GetCurrentTimestamp(ct.byref(ts))

        return ts.value

    def save_calibration(self, name='calib.txt'):
#        import ctypes
#        # os.path.dirname(os.path.abspath(name)))
#        out = 'T:\\000_Work\\2014\\Ocunostics\\Devel\\RemoteTracking\\weg\\calib1.txt'
#        res = iViewXAPI.iViewXAPI.iV_SaveCalibration(ctypes.c_char_p(out))
#        
#        out = '.\\weg\\calib2.txt'
#        res = iViewXAPI.iViewXAPI.iV_SaveCalibration(ctypes.c_char_p(out))                
#
#        #out = '.\weg\calib3.txt'
#        #res = iViewXAPI.iViewXAPI.iV_SaveCalibration(ctypes.c_char_p(out))
#                
#        out = './weg/calib4.txt'
#        res = iViewXAPI.iViewXAPI.iV_SaveCalibration(ctypes.c_char_p(out))
#        
        res = iViewXAPI.iViewXAPI.iV_SaveCalibration(name)
        if res != 1:
            raise Exception('IViewX error: {0}'.format(res))
            
    def load_calibration(self, name='calib.txt'):
        res = iViewXAPI.iViewXAPI.iV_LoadCalibration(name)
        if res != 1:
            raise Exception('IViewX error: {0}'.format(res))
            
    def set_resolution(self, width, height):
        # todo: catch empty values
        res = iViewXAPI.iViewXAPI.iV_SetResolution(width, height)
        if res != 1:
            raise Exception('IViewX error: {0}'.format(res))


class RedM(SmiEyeTracker):
    def __init__(self, *args, **kwargs):
        super(RedM, self).__init__(*args, **kwargs)


class IviewX(SmiEyeTracker):
    def __init__(self, *args, **kwargs):
        super(IviewX, self).__init__(*args, **kwargs)
