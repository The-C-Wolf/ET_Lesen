# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 13:57:02 2016

@author: tamm
"""


# todo: iViewXAPI.h fuer automatisches Interface mit swig?


import iview_structures as ivx_struct
import ctypes as ct

ivx = ct.windll.LoadLibrary("iViewXAPI.dll")


class REDM(object):
     
    def __init__(self):
        self.config = _Config()
        self.geometry = _Geometry(tracker=self)
        # falls nutzer ueber iViewServer Einstellungen aendert, wird es hier nicht upgedatet!!
        
    def get_accuracy(self, visualization=0):
        """Accuracy values are only available, when the validation has been performed within the same
        Python process!
        """
        if visualization not in (0,1):
            raise ValueError()
            
        cobj = ivx_struct.CAccuracy(0, 0, 0, 0)
        ret = ivx.iV_GetAccuracy(ct.byref(cobj), ct.c_int(visualization))
        print(ret)
        if ret == 103:
            # todo: define Tracker not validated exception and handle via error propagation
            raise Exception('Not yet validatet.')
        elif ret != 1:
            raise Exception('Error: {0}'.format(ret))
        else:
            pass
        
    def validate(self):        
        ret = ivx.iV_Validate()
        print(ret)
        
        

class _Config(object):
    def __init__(self):
        pass


# todo Geometry:
# Umschreiben: setter duerfen von außen gar nicht zugängig sein. Man kann profile anlegen, editieren, loeschen und 
# parameter des aktuelle profils ausgeben lassen. Schnittstelle so umschreiben!
class _Geometry(object):
    """Wrapper to REDGeometry functions.
    
    If cgeom (=CGeometry struct) is given, all other arguments are ignored.

    name: 265 char
    angle: deg
    others: mm

    """
    def __init__(self, tracker=None, cgeom=None, name='init_empty', red_angle=20,
                 red_dist_depth=40, red_dist_height=0,
                 screen_width=300, screen_height=200):
        
        self._tracker = tracker  # todo: handle empty tracker        
        
        # !!!Don't use self._cgeom directly. It's just a temp object to allow the communication
        # between Python and the underlying C-API!!!
        if cgeom is None:
            redGeometry = 1  # iViewXAPI.h: 0 = monitor integrated, 1 = standalone
                         # RED-m is always standalone!!!
            monitorSize = 0  # RED only
            setupName = b""  # char * 256
            stimX = 0
            stimY = 0
            stimHeightOverFloor = 0  # RED only
            redHeightOverFloor = 0  # RED only
            redStimDist = 0  # RED only
            redInclAngel = 0
            redStimDistHeight = 0
            redStimDistDepth = 0

            self._cgeom = ivx_struct.CGeometry(
            redGeometry,
            monitorSize,
            setupName,
            stimX,
            stimY,
            stimHeightOverFloor,
            redHeightOverFloor,
            redStimDist,
            redInclAngel,
            redStimDistHeight,
            redStimDistDepth,
            )
            
            self.name = name
            self.red_angle = red_angle
            self.red_dist_depth = red_dist_depth
            self.red_dist_height = red_dist_height
            self.screen_width = screen_width
            self.screen_height = screen_height
        else:
            self._cgeom = cgeom
            

    #--- getter and setter
    @property
    def name(self):
        return self._cgeom.setupName

    @name.setter
    def name(self, name):
        # todo: erlaube nur ansi-zeichen + ziffern
        if len(name)<1 or len(name)>256:
            raise Exception('len(name) not in range 1...256')
        else:
            self._cgeom.setupName = name

    @property
    def screen_width(self):
        """Screen width in mm.
        """
        return self._cgeom.stimX

    @screen_width.setter
    def screen_width(self, width):
        if width<1:
            raise Exception('Screen width >=1 expected.')
        else:
            self._cgeom.stimX = width

    @property
    def screen_height(self):
        """Screen height in mm.
        """
        return self._cgeom.stimY

    @screen_height.setter
    def screen_height(self, height):
        if height<1:
            raise Exception('Screen width >=1 expected.')
        else:
            self._cgeom.stimY = height

    @property
    def red_dist_depth(self):
        """Distance between tracker and monitor in mm.
        """
        return self._cgeom.redStimDistDepth

    @red_dist_depth.setter
    def red_dist_depth(self, val):
        if val<1:
            raise Exception('Eyetracker cannot be behind the screen.')
        else:
            self._cgeom.redStimDistDepth = val

    @property
    def red_dist_height(self):
        """Height between tracker and monitor in mm.
        """
        return self._cgeom.redStimDistHeight

    @red_dist_height.setter
    def red_dist_height(self, val):
        self._cgeom.redStimDistHeight = val

    @property
    def red_angle(self):
        return self._cgeom.redInclAngel

    @red_angle.setter
    def red_angle(self, val):
        self._cgeom.redInclAngel = val


    #--- methods
    def get_profile(self, name=None):
        """Get profile settings from profile with name=name or from current profile if name is empty.
        """
        if name is None:     
            # update self._cgeom and return profile values
            ret = ivx.iV_GetCurrentREDGeometry(ct.byref(self._cgeom))
        else:
            profiles = self.get_profiles()
            if name not in profiles:
                raise Exception('Profile with name {0} not available.'.format(name))
            else:
                ret = ivx.iV_GetREDGeometry(ct.c_char_p(name), ct.byref(self._cgeom))
    
        return self

    def add_profile(self, geometry):
        # todo: set_geometry implicitly selects this geometry or only added to available geometries
        # where are geometries saved?
        raise NotImplementedError()
    
    def get_profiles(self):
        buffer_size = 50
        max_buffer = 2000
        ret = -1
        while buffer_size<=max_buffer:
            profiles = ' '.ljust(buffer_size-1)
            ret = ivx.iV_GetGeometryProfiles(ct.c_int(len(profiles)), ct.c_char_p(profiles))
            if ret == 112:  # ERR_WRONG_PARAMETER
                buffer_size += 50
                continue
            elif ret == 1:  # RET_SUCCESS
                break
            else:
                raise Exception('Error: {0}'.format(ret))
        if ret != 1:  # buffer_size>max_buffer and ret !=1
            raise Exception('Error: {0}'.format(ret))


        profiles = profiles.replace('\x00', '')  # get rid of empty buffer parts
        return profiles.split(';')

    def delete_profile(self, name):
        raise NotImplementedError()

    def select_profile(self, name):
        profiles = self.get_geometry_profiles()
        if name not in profiles:
            raise Exception('Profile with name {0} not available.'.format(name))

        ret = ivx.iV_SelectREDGeometry(ct.c_char_p(name))
        if ret !=1:
            raise Exception('Error: {0}'.format(ret))
    

#-------------------------------
if __name__ == '__main__':
    # res = ivx.iV_SetLogger(ct.c_int(1), ct.c_char_p("iViewXSDK_Python_GazeContingent_Demo.txt"))
    res = ivx.iV_Connect(ct.c_char_p('127.0.0.1'), ct.c_int(4444), ct.c_char_p('127.0.0.1'), ct.c_int(5555))
    print(res)
