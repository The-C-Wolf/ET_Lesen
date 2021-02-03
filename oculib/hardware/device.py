# -*- coding: utf-8 -*-

# todo: dummy-Verhalten per Dekorator festlegen!!!
# todo: logfile unabhaengig von EEG-Port schalten koennen - auch bei ET: bei dummy-Mode in file schreiben koennen;
# erst nach practice aktivieren usw.

from psychopy import parallel  # todo: Diese Abhängigkeiten schrittweise entfernen!!!
from oculib.psychopy import Clock
import os
import time
import thread  # todo: replace with threading
import threading


# Gibt es eine Möglichkeit, ein Dummy-Objekt zu erzeugen, welches passiv jede aufgeführte Funktion "leer"
# aufruft?
# z.B. http://stackoverflow.com/questions/2704434/intercept-method-calls-in-python
#
# Something like this? This implictly adds a decorator to your method (you can also make an explicit decorator based on this if you prefer that):
#
# class Foo(object):
#     def __getattribute__(self,name):
#         attr = object.__getattribute__(self, name)
#         if hasattr(attr, '__call__'):
#             def newfunc(*args, **kwargs):
#                 print('before calling %s' %attr.__name__)
#                 result = attr(*args, **kwargs)
#                 print('done calling %s' %attr.__name__)
#                 return result
#             return newfunc
#         else:
#             return attr
#
# when you now try something like:
#
# class Bar(Foo):
#     def myFunc(self, data):
#         print("myFunc: %s"% data)
#
# bar = Bar()
# bar.myFunc(5)
#
# You'll get:
#
# before calling myFunc
# myFunc:  5
# done calling myFunc

################################################
# Base class
# open, close: Implementieren notwendige Operationen, um eine Verbindung
# zum Device herzustellen
# Achtung: __init__() darf keine Abhaengigkeiten von einem Geraet haben!!!
# Beim Initialisieren werden alle Geraete automatisch auf 'dummy' gesetzt.
# Erst durch open() wird das Geraet aktiv --> dann werden auch erst geraeteabhaengige libraries geladen!!!
# Zwischendurch kann man das Geraet (ohne close) auf 'dummy' setzen, dann wird
# fuer diese Zeit das Geraet ignoriert.
# open im dummy mode oder auch nach Oeffnen in Dummymode versetzen:
# Daten werden nicht zum Geraet geschrieben oder gelesen, aber simuliert
# mode: dummy = pass
# mode: emulate = schreibe in file, generiere daten
# mode: normal: normale arbeistweise
# normal + emulate koennen gemischt werden
# silent + andere Option wirft Fehler auf
class _Device(object):
    def __init__(self):
        self._mode = 'dummy'
        self._closed = True

    def write(self, *args, **kwargs):
        if self._mode == 'dummy':
            return  # return without argument = return None

        raise NotImplementedError()

    def read(self, *args, **kwargs):
        if self._mode == 'dummy':
            return

        raise NotImplementedError()

    def open(self):
        if self._mode == 'dummy':
            return

        raise NotImplementedError()

    @property
    def closed(self):
        return self._closed

    def close(self):
        if self._mode == 'dummy':
            return

        raise NotImplementedError()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, val):
        allowed = ('normal', 'emulate', 'dummy')

        if not isinstance(val, (list, tuple)):
            val = (val,)

        if len(val) > 1 and 'dummy' in val:
            raise ValueError('Dummy mode cannot be mixed with other mode options.')

        unknown = [item for item in val if item not in allowed]
        if unknown:
            raise ValueError('Unknown device mode(s): {0}'.format(unknown))

        if len(val) == 1:
            self._mode = val[0]
        else:
            self._mode = val


# todo: implementiere Klassen counter und wenn es
# z.B. schon ein Parallel _device gibt, pruefe ob gleicher port verwendet werden soll
# falls ja - Fehlermeldung werfen


class EyeTracker(_Device):
    """
    open, close: Kontakt zum Gerät herstellen/unterbrechen
    start_recording, stop_recording: Datei fuer write oeffnen; Modus idf oder raw
    """
    def __init__(self):
        super(EyeTracker, self).__init__()

        self._calibrated = False  # todo: wenn moeglich dynamisch ueber Geraete API abfragen;
                                  # Dann kann man in Programmen nacheinander der Tracker ohne Uebergabe eines
                                  # Trackerobjekts nutzen ohne jedesmal neu tracken zu muessen
        self._recording = False  # set flag via start_recording, stop_recording
                                 # todo: _recording automatisch auf False setzen, wenn mode auf dummy gesetzt wird???

    def close(self):
        if self._mode == 'dummy':
            return

        if self.recording:
            self.stop_recording()
        super(EyeTracker, self).close()

    def calibrate(self, validate=True):
        if self._mode == 'dummy':
            return

        raise NotImplementedError()

    def validate(self):
        if self._mode == 'dummy':
            return

        raise NotImplementedError()

    @property
    def recording(self):
        return self._recording

    def start_recording(self):
        if self._mode == 'dummy':
            return

        raise NotImplementedError()
        # set self._recording = True

    def stop_recording(self):
        if self._mode == 'dummy':
            return

        raise NotImplementedError()
        # set self._recording = False


class ParallelPort(_Device):
    # todo: hold time; Nullwert etc. einstellen lassen
    def __init__(self, address=0x0378, logfile=None, clock=None,
                 mode='dummy'):
        super(ParallelPort, self).__init__()

        self._address = address
        
        self._mode = mode
        if self._mode == 'dummy':  # parallel.ParallelPort wird
            # von Psychopy parallel nur bereitgestellt, wenn der Computer
            # ueber einen Parallelport verfuegt.
            # --> Workaround um den Dummy-Mode + flog-File schreiben auf allen Rechnern zu ermoeglichen.
            # (s. auch rewrite von mode
            self._port = None
        else:
            self._port = parallel.ParallelPort(address=self._address)
            self._port.setData(0)  # reset port

        # todo check: if timer != timer.time or Clock() ...

        self._log = None
        self._flog = None
        self._timestamp = None

        if logfile:
            self.open_log(logfile=logfile, clock=clock)

    def _writeport_on(self, data):
        self._port.setData(int(data))

    def _writeport_off(self):
        self._port.setData(0)

    def write(self, data, msg=''):
        if self._mode != 'dummy':
            pt = threading.Timer(0.01, self._writeport_off)  # set marker for 10 ms
            self._writeport_on(data)
            pt.start()

        if self._flog:
            self._flog.write(';'.join((str(self._timestamp.getTime()), str(data), msg))+'\n')


    #    ## future
    #    # self._devices = None
    def open_log(self, logfile=None, clock=None):
        if self._log:
            raise Warning('Logfile already open.')
            return

        self._log = logfile
        self._flog = open(self._log, 'w')
        if clock:
            self._timestamp = clock
        else:
            self._timestamp = Clock()

    def close_log(self):
        if self._flog:
            self._flog.close()

    # todo: wie ruft man property der Basisklasse auf, wenn diese ueber
            # Dekorator definiert wurde?
    #@property
    #def mode(self):  # muss property immer vor @setter stehen?
    #    super(ParallelPort, self).mode
    #
    #@mode.setter
    #def mode(self, mode):
    #    super(ParallelPort, self).mode = mode
    #
    #    if self.mode == 'normal':  # todo: mit __init__ verheiraten
    #        self._port = parallel.ParallelPort(address=self._address)
    #        self._port.setData(0)  # reset port

#==============================================================================
#     def mode(self, mode):  # ersetzen durch Aufruf der Basismethode
#         allowed = ('normal', 'emulate', 'dummy')
# 
#         if not isinstance(mode, (list, tuple)):
#             mode = (mode,)
# 
#         if len(mode) > 1 and 'dummy' in mode:
#             raise ValueError('Dummy mode cannot be mixed with other mode options.')
# 
#         unknown = [item for item in mode if item not in allowed]
#         if unknown:
#             raise ValueError('Unknown device mode(s): {0}'.format(unknown))
# 
#         if len(mode) == 1:
#             self._mode = mode[0]
#         else:
#             self._mode = mode
# 
#         if self.mode == 'normal':  # todo: mit __init__ verheiraten
#             self._port = parallel.ParallelPort(address=self._address)
#             self._port.setData(0)  # reset port
#==============================================================================



class SerialPort(_Device):
    def __init__(self):
        super(SerialPort, self).__init__()

    # s. Parameter fuer seriell port
    # abgeleitete Klassen fuer Nexus, ETG-4000 setzen dann schon die richtigen Startparameter
    # und haben Wertebereichcheck (ETG 'A'-'H'?) etc.


class LogFile(_Device):
    # todo: new_entry() erzeugt neue Spalte (evtl. mit defaults belegt
    # per ['col']os oder logfile.col = xyz koennen Werte gesetzt werden
    # logfile.write() schreibt raus
    # oder diese Variante:
     # fout.write(sep.join(pattern_out).format(vp=vp_name,
        #                                            trial_id=trial.trial_index,
        #                                            exp_time=trial.exp_time,
        #                                            stim=trial.stim,
        #                                            category=trial.category,
        #                                            portcode=trial.portcode,
        #                                            delta_val=trial.rating['xstop'] - trial.rating['xstart'].values[0],
        #                                            delta_arous=trial.rating['ystop'] - trial.rating['ystart'].values[0]))
        #

    def __init__(self, header=None, sep=';'):
        super(LogFile, self).__init__()

        self._sep = sep
        self._header = header

        self._pattern_out = ['{{{0}}}'.format(item) for item in self._header] + ['\n'] # ('{vp}', '{trial_id}', ...) ;
            # If you need to include a brace character in the literal text, it can be escaped by doubling: {{ and }}.

        # todo: open and close file
        # flog = codecs.open(subject.fname, 'w', 'utf-8')

    def write(self):
        pass

        # fout.write(sep.join(pattern_out).format(vp=vp_name,
        #                                            trial_id=trial.trial_index,
        #                                            exp_time=trial.exp_time,
        #                                            stim=trial.stim,
        #                                            category=trial.category,
        #                                            portcode=trial.portcode,
        #                                            delta_val=trial.rating['xstop'] - trial.rating['xstart'].values[0],
        #                                            delta_arous=trial.rating['ystop'] - trial.rating['ystart'].values[0]))
        #

        # default_ret = dict.fromkeys(header,'/')
        # fout.write(sep.join(pattern_out).format(**default_ret))











#################################################

### todo integrieren ###
# ### todo: Entwickle generische Loesung, um
# ### beliebige Geraetekombinationen zusammen betreiben zu koennen.
# ### Problem: Wie gehet man damit um, dass BrainAmp per Parallelport
# ### 255 Trigger unterscheiden kann; ET Klartext verarbeitet, Nexus
# ### Werte seriell, Parport 0,1 und ETG4000 8 Werte kennt?
# class _RecordingDevice(object):
#     device_types = ('brainamp', 'redm', 'iviewx_hispeed1250', 'eyelink1000',
#                     'nexus10', 'etg4000')
#
#     implemented_devices = {'brainamp', 'redm'}
#
#     def __init__(self, name=None, device=None):
#         if name is None:
#             raise Exception('Missing name for recording device.')
#         else:
#             self.name = None
#
#         if device is None:
#             raise Exception('Missing type of recording devices.')
#         elif device not in self.device_types:
#             raise Exception('Unknown device: {0}'.format(device))
#         elif device not in self.implemented_devices:
#             raise Exception('Sorry! Device type {0} is not yet implemented.'.format(device))
#         else:
#             self.device = device
#
#
# class RecordingDeviceManager(object):
#     def __init__(self):
#         """
#         Wichtig: parallel.setPortAddress(0x378) muss ausserhalb der Klasse aufgerufen werden!
#         setPortAddress setzt globale Variable PORT, die sonst nicht verfuegabr ist.
#         """
#
#         self._EEG = 0
#         self._REDM = 0
#         self._REDM_IDF = 0
#         self._HISPEED = 0
#         self._HISPEED_IDF = 0
#         self._ET = 0
#
#         self._eeg_port = None
#
#     @property
#     def EEG(self):
#         return self._EEG
#
#     @EEG.setter
#     def EEG(self, value):
#         self._EEG = bool(value)
#         self._init_eeg()
#
#     @property
#     def REDM(self):
#         return self._REDM
#
#     @REDM.setter
#     def REDM(self, value):
#         self._REDM = bool(value)
#
#     @property
#     def REDM_IDF(self):
#         return self._REDM_IDF
#
#     @REDM_IDF.setter
#     def REDM_IDF(self, value):
#         self._REDM_IDF = bool(value)
#
#     @property
#     def HISPEED(self):
#         return self._HISPEED
#
#     @HISPEED.setter
#     def HISPEED(self, value):
#         self._HISPEED = bool(value)
#
#     @property
#     def HISPEED_IDF(self):
#         return self._HISPEED_IDF
#
#     @HISPEED_IDF.setter
#     def HISPEED_IDF(self, value):
#         self._HISPEED_IDF = bool(value)
#
#     @property
#     def ET(self):
#         return any((self.REDM, self.REDM_IDF, self.HISPEED, self.HISPEED_IDF))
#
#     def _writeport_on(self, data):
#         self._eeg_port.setData(data)
#
#     def _writeport_off(self):
#         self._eeg_port.setData(0)
#
#     def writeport(self, data, msg=''):
#         if self._EEG:
#             pt = threading.Timer(0.01, self._writeport_off) # set marker for 10 ms
#             self._writeport_on(data)
#             pt.start()
#         else:
#             self.f_triggerlog.write(';'.join((str(self.timestamp.getTime()), str(data), msg))+'\n')
#
#     def _init_eeg(self):
#         # todo: Umstellen auf z.B.: 0 = nichts; 1=EEG; 2=File; 3=EEG und File
#         if self._EEG:
#             try:
#                 self.f_triggerlog.close()
#             except:
#                 pass
#             self.f_triggerlog = None
#             #self._eeg_port = parallel.ParallelPort(address=0x0378)
#             self._eeg_port = parallel.ParallelPort(address=0x2040)
#             self._eeg_port.setData(0)  # sets all pins low
#         else:
#             self.f_triggerlog = open('./Results/'+'eeg'+'_trigger.log','w')
#             self.timestamp  = Clock()
#
#         ## future
#         # self._devices = None
#
#     ### future ###
#     # def add_device(self, name=None, device=None):
#     #     pass
#     #
#     # def remove_device(self, name):
#     #     pass
#     #
#     # @property
#     # def devices(self):
#     #     pass


