# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 11:01:04 2016

@author: tamm
"""

import ctypes as ct


class CGeometry(ct.Structure):
    _fields_ = [
        ("redGeometry", ct.c_int),   # iViewXAPI.h: 0 = monitor integrated, 1 = standalone
                                      # RED-m is always standalone!!!
        ("monitorSize", ct.c_int),  # RED only
        ("setupName", ct.c_char * 256),
        ("stimX", ct.c_int),
        ("stimY", ct.c_int),
        ("stimHeightOverFloor", ct.c_int),  # RED only
        ("redHeightOverFloor", ct.c_int),  # RED only
        ("redStimDist", ct.c_int),  # RED only
        ("redInclAngel", ct.c_int),
        ("redStimDistHeight", ct.c_int),
        ("redStimDistDepth", ct.c_int)]


class CSystem(ct.Structure):
    _fields_ = [
        ("samplerate", ct.c_int),
        ("iV_MajorVersion", ct.c_int),
        ("iV_MinorVersion", ct.c_int),
        ("iV_Buildnumber", ct.c_int),
        ("API_MajorVersion", ct.c_int),
        ("API_MinorVersion", ct.c_int),
        ("API_Buildnumber", ct.c_int),
        ("iV_ETDevice", ct.c_int)]  
        # iV_ETDevice:
        # 0: None
        # 1: RED
        # 2: REDm
        # 3: HiSpeed
        # 4: MRI
        # 5: HED
        # 7: Custom


class CCalibration(ct.Structure):
    _fields_ = [
        ("method", ct.c_int),
        ("visualization", ct.c_int),
        ("displayDevice", ct.c_int),
        ("speed", ct.c_int),
        ("autoAccept", ct.c_int),
        ("foregroundBrightness", ct.c_int),
        ("backgroundBrightness", ct.c_int),
        ("targetShape", ct.c_int),
        ("targetSize", ct.c_int),
        ("targetFilename", ct.c_char * 256)]
        
        
class CCalibrationPoint(ct.Structure):
    _fields_ = [
        ("number", ct.c_int),
        ("positionX", ct.c_int),
        ("positionY", ct.c_int)]


class CEye(ct.Structure):
    _fields_ = [
        ("gazeX", ct.c_double),
        ("gazeY", ct.c_double),
        ("diam", ct.c_double),
        ("eyePositionX", ct.c_double),
        ("eyePositionY", ct.c_double),
        ("eyePositionZ", ct.c_double)]


class CSample(ct.Structure):
    _fields_ = [
        ("timestamp", ct.c_longlong),
        ("leftEye", CEye),
        ("rightEye", CEye),
        ("planeNumber", ct.c_int)]


class CEvent(ct.Structure):
    _fields_ = [
        ("eventType", ct.c_char),
        ("eye", ct.c_char),
        ("startTime", ct.c_longlong),
        ("endTime", ct.c_longlong),
        ("duration", ct.c_longlong),
        ("positionX", ct.c_double),
        ("positionY", ct.c_double)]


class CAccuracy(ct.Structure):
    _fields_ = [
        ("deviationLX",ct.c_double),
        ("deviationLY",ct.c_double),
        ("deviationRX",ct.c_double),
        ("deviationRY",ct.c_double)]


class CImage(ct.Structure):
    _fields_ = [ 
        ("imageHeight", ct.c_int),
        ("imageWidth",  ct.c_int),
        ("imageSize",   ct.c_int),
        ("imageBuffer", ct.c_void_p)]
        # c_char_p funktioniert nicht: http://www.grulic.org.ar/~mdione/glob/posts/ctypes-and-buffers/


class CEyePosition(ct.Structure):
    _fields_ = [
        ("validity", ct.c_int),
        ("relativePositionX", ct.c_double),
        ("relativePositionY", ct.c_double),
        ("relativePositionZ", ct.c_double),
        ("positionRatingX", ct.c_double), 
        ("positionRatingY", ct.c_double),
        ("positionRatingZ", ct.c_double)]
 
       
class CTrackingStatus(ct.Structure):
    _fields_ = [
        ("timestamp", ct.c_longlong),
        ("leftEye", CEyePosition),
        ("rightEye", CEyePosition),
        ("total", CEyePosition)]

        
class CDate(ct.Structure):
    _fields_ = [
        ("day", ct.c_int),
        ("month", ct.c_int),
        ("year", ct.c_int)]
        
        
class CAOIRectangle(ct.Structure):
    _fields_ = [
        ("x1", ct.c_int),  # left border (px)
        ("x2", ct.c_int),  # right border (px)
        ("y1", ct.c_int),  # upper border (px)
        ("y2", ct.c_int)]  # lower border (px)


class CAOI(ct.Structure):
    _fields_ = [
        ("enabled", ct.c_int),
        ("aoiName", ct.c_char * 256),
        ("aoiGroup", ct.c_char * 256),
        ("position", CAOIRectangle),
        ("fixationHit", ct.c_int),  # 0: use raw data hit; 1: use fixation hit
        ("outputValue", ct.c_int),  # TTL output value
        ("outputMessage", ct.c_char * 256),
        ("eye", ct.c_char)]  # "l" | "r" 

    