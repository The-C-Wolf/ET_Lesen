# -*- coding: utf-8 -*-

# todo: Filter fuer pursuit etc. ueber open() bzw. __init__() setzen lassen

# __init__() ist immer noch geraeteunabhaengig und per default als dummy-mode; erst mit open() wird
# geraet tatsaechlich geoffnet.

from ..device import EyeTracker

# todo: diesen try block ueberall uebernehmen um plattformspezifische module abzufangen
try:
    import pylink
    import EyeLinkCoreGraphicsPsychoPy as nfeye
except ImportError:
    pass  # todo: add handling


class SRResearchEyeTracker(EyeTracker):
    def __init__(self):
        super(SRResearchEyeTracker, self).__init__()

        self._et = None
        self._win = None
        self.fname = None

    def open(self, win):
        """todo: At the moment, win is needed to display the calibration target etc.;
         --> an Loesung bei SMI zur eigenen Darstellung anpassen und open()-Interface vereinheitlichen

        """
        self._win = win
        if self._win.units != 'pix':
            raise Exception('Sorry! For now EyeLinkCoreGraphicsPsychoPy can only handle win "pix" units.')
        self._et = pylink.EyeLink("100.1.1.1.")
        genv = nfeye.EyeLinkCoreGraphicsPsychoPy(win, self._et)
        pylink.openGraphicsEx(genv)
        # eigentlich -1 fuer simulation; scheint aber auf 65636 gesetzt zu sein
        #self._et.isConnected()==1:

        self._et.setCalibrationType('HV9') #HV3,5,9
        self._et.setPupilSizeDiameter('yes') # record diameter
        self._et.sendCommand( "file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON" )
        self._et.sendCommand( "file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS")

        self._et.setSaccadeVelocityThreshold(30)
        #Sets velocity threshold of saccade detector: usually 30 for cognitive research, 22 for pursuit and neurological work.
        #Parameters: vel  minimum velocity (°/sec) for saccades.

        self._et.setAccelerationThreshold(9500)
        #Sets acceleration threshold of saccade detector: usually 9500 for cognitive research, 5000 for pursuit and neurological work.
        #Parameters:  accel  minimum acceleration (°/sec/sec) for saccades.

        self._et.setMotionThreshold(0.15)
        #Sets a spatial threshold to shorten saccades. Usually 0.15 for cognitive research, 0 for pursuit and neurological work.
        #Parameters: deg  minimum motion (degrees) out of fixation before saccade onset allowed.

        self._et.setPursuitFixup(60)
        #Sets the maximum pursuit velocity accommodation by the saccade detector. Usually 60.
        #Parameters: maxvel  maximum pursuit velocity fixup (°/sec).

    def close(self):
        if self._mode == 'dummy':
            return

        if self._recording is True:
            self.stop_recording()

        self._et.sendCommand("record_status_message 'DONE'")

        self._et.closeDataFile()
        #self._et.receiveDataFile(param['SAVE_PATH_REMOTE'] + fname +".EDF",param['SAVE_PATH_LOCAL'] + fname + ".edf")
        self._et.close()

    def calibrate(self, validate=True):
        self._et.doTrackerSetup(self._win.width, self._win.height)

    def start_recording(self, fname=None):
        # todo: check if et is connected

        #Opens the EDF file.
        self.fname = fname
        pylink.getEYELINK().openDataFile(self.fname)

        self._et.startRecording(1, 1, 0, 0)
        self._et.sendCommand('record_status_message "Task started"')
        self._recording = True

    def stop_recording(self):
        if self.mode == 'dummy' or self._recording is False:
            return

        self._et.sendCommand('record_status_message "Task finished"')
        self._et.stopRecording()
        self._recording = False

    def write(self, message):
        if self._mode == 'dummy':
            return  # return without argument = return None
        elif not self._recording:
            raise Exception('Recording not started.')

        self._et.sendMessage(message)


class Eyelink1000(SRResearchEyeTracker):
    """
        todo:

         self._tracker.sendCommand( "record_status_message 'Saccade task' " )
        self._tracker.sendMessage( "Saccade task start" )
    """
    def __init__(self):
        super(Eyelink1000, self).__init__()
