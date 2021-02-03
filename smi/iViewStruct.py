# -*- coding: utf-8 -*-


from ctypes import *
from PIL import Image


#===========================================================

class SystemData( object ) :

    #=============================

    class _CSystemData( Structure ) :
        _fields_ = [ ( 'samplerate',       c_int ),
                     ( 'iV_MajorVersion',  c_int ),
                     ( 'iV_MinorVersion',  c_int ),
                     ( 'iV_Buildnumber',   c_int ),
                     ( 'API_MajorVersion', c_int ),
                     ( 'API_MinorVersion', c_int ),
                     ( 'API_Buildnumber',  c_int ),
                     ( 'iV_ETDevice',      c_int ) ]

    #=============================

    def __init__( self ) :
        self._CSystemData = SystemData._CSystemData( 0, 0, 0, 0, 0, 0, 0, 0 )

        for e in self._CSystemData._fields_ :
            setattr( self.__class__, e[ 0 ],
                     property( self._getter( e[ 0 ] ) ) )
 

    #=============================

    def _getter( self, what ) :
        def wrapped( self ) :
            return getattr( self._CSystemData, what )
        return wrapped


#===========================================================

class CalibrationData( object ) :

    #=============================

    class _CCalibrationData( Structure ) :
        _fields_ = [ ( 'method',               c_int ),
                     ( 'visualization',        c_int ),
                     ( 'displayDevice',        c_int ),
                     ( 'speed',                c_int ),
                     ( 'autoAccept',           c_int ),
                     ( 'foregroundBrightness', c_int ),
                     ( 'backgroundBrightness', c_int ),
                     ( 'targetShape',          c_int ),
                     ( 'targetSize',           c_int ),
                     ( 'targetFilename',       c_char * 256 ) ]


    #=============================

    def __init__( self ) :
        self._CCalibrationData = \
                  CalibrationData._CCalibrationData( 5, 1, 0, 0, 1, 20,
                                                     239, 1, 15, b'' )

        for e in self._CCalibrationData._fields_ :
            setattr( self.__class__, e[ 0 ],
                     property( self._getter( e[ 0 ] ),
                               self._setter( e[ 0 ] ) ) )
 

    #=============================

    def _getter( self, what ) :
        def wrapped( self ) :
            return getattr( self._CCalibrationData, what )
        return wrapped


    #=============================

    def _setter( self, what ) :
        def wrapped( self, value ) :
            setattr( self._CCalibrationData, what, value )
        return wrapped


#===========================================================

class CalibrationPoint( object ) :
    #=============================

    class _CCalibrationPoint( Structure ) :
        _fields_ = [ ( 'number',        c_int ),
                     ( 'positionX',     c_int ),
                     ( 'positionY',     c_int ) ]
                   
                   
    #=============================

    def __init__( self, data = None ) :
        if not data :
            self._CCalibrationPoint = CalibrationPoint._CCalibrationPoint( 0, 0, 0 )
        else :
            self._CCalibrationPoint = data

        for e in self._CCalibrationPoint._fields_ :
            setattr( self.__class__, e[ 0 ],
                     property( self._getter( e[ 0 ] ) ) )
 

    #=============================

    def _getter( self, what ) :
        def wrapped( self ) :
            return getattr( self._CCalibrationPoint, what )
        return wrapped


#===========================================================

class EyeData( object ) :

    #=============================

    class _CEyeData( Structure ) :
        _fields_ = [ ( 'gazeX',        c_double ),
                     ( 'gazeY',        c_double ),
                     ( 'diam',         c_double ),
                     ( 'eyePositionX', c_double ),
                     ( 'eyePositionY', c_double ),
                     ( 'eyePositionZ', c_double ) ]


    #=============================

    def __init__( self, data = None ) :
        if not data :
            self._CEyeData = EyeData._CEyeData( 0, 0, 0, 0, 0, 0 )
        else :
            self._CEyeData = data

        for e in self._CEyeData._fields_ :
            setattr( self.__class__, e[ 0 ],
                     property( self._getter( e[ 0 ] ) ) )
 

    #=============================

    def _getter( self, what ) :
        def wrapped( self ) :
            return getattr( self._CEyeData, what )
        return wrapped


#===========================================================

class SampleData( object ) :

    #=============================

    class _CSampleData( Structure ) :
        _fields_ = [ ( 'timestamp',   c_longlong ),
                     ( 'leftEye',     EyeData._CEyeData ),
                     ( 'rightEye',    EyeData._CEyeData ),
                     ( 'planeNumber', c_int ) ]


    #=============================

    def __init__( self ) :
        self._CSampleData = SampleData._CSampleData( 0,
                                                     EyeData( )._CEyeData,
                                                     EyeData( )._CEyeData,
                                                     0 )

        for e in ( 'timestamp', 'planeNumber' ) :
            setattr( self.__class__, e[ 0 ],
                     property( self._getter( e[ 0 ] ) ) )
 

    #=============================

    def _getter( self, what ) :
        def wrapped( self ) :
            return getattr( self._CSampleData, what )
        return wrapped


    #=============================

    @property
    def leftEye( self ) :
        return EyeData( self._CSampleData.leftEye )


    #=============================

    @property
    def rightEye( self ) :
        return EyeData( self._CSampleData.rightEye )


#===========================================================

class EventData( object ) :

    #=============================

    class _CEventData( Structure ) :
        _fields_ = [ ( 'eventType', c_char ),
                     ( 'eye',       c_char ),
                     ( 'startTime', c_longlong ),
                     ( 'endTime',   c_longlong ),
                     ( 'duration',  c_longlong ),
                     ( 'positionX', c_double ),
                     ( 'positionY', c_double ) ]


    #=============================

    def __init__( self ) :
        self._CEventData = EventData._CEventData( 'F', 'L', 0, 0, 0, 0, 0 )

        for e in self._CEventData._fields_ :
            setattr( self.__class__, e[ 0 ],
                     property( self._getter( e[ 0 ] ) ) )
 

    #=============================

    def _getter( self, what ) :
        def wrapped( self ) :
            return getattr( self._CEventData, what )
        return wrapped


#===========================================================

class AccuracyData( object ) :

    #=============================

    class _CAccuracyData( Structure ) :
        _fields_ = [ ( 'deviationLX', c_double ),
                     ( 'deviationLY', c_double ),                               
                     ( 'deviationRX', c_double ),
                     ( 'deviationRY', c_double ) ]
    

    #=============================

    def __init__( self ) :
        self._CAccuracyData = AccuracyData._CAccuracyData( 0, 0, 0, 0 )

        for e in self._CAccuracyData._fields_ :
            setattr( self.__class__, e[ 0 ],
                     property( self._getter( e[ 0 ] ) ) )
 

    #=============================

    def _getter( self, what ) :
        def wrapped( self ) :
            return getattr( self._CAccuracyData, what )
        return wrapped


#===========================================================

class MonitorAttachedGeometry( object ) :

    #=============================

    class _CMonitorAttachedGeometry( Structure ) :
        _fields_ = [ ( 'setupName',         c_char * 256 ),
                     ( 'stimX',             c_int ),
                     ( 'stimY',             c_int ),
                     ( 'redStimDistHeight', c_int ),
                     ( 'redStimDistDepth',  c_int ),
                     ( 'redInclAngel',      c_int ) ]


    #=============================

    def __init__( self ) :
        self._CMonitorAttachedGeometry = \
                  MonitorAttachedGeometry._CMonitorAttachedGeometry( b'', 0, 0,
                                                                     0, 0, 0 )

        for e in self._CMonitorAttachedGeometry._fields_ :
            setattr( self.__class__, e[ 0 ],
                     property( self._getter( e[ 0 ] ),
                               self._setter( e[ 0 ] ) ) )
 

    #=============================

    def _getter( self, what ) :
        def wrapped( self ) :
            return getattr( self._CMonitorAttachedGeometry, what )
        return wrapped


    #=============================

    def _setter( self, what ) :
        def wrapped( self, value ) :
            setattr( self._CMonitorAttachedGeometry, what, value )
        return wrapped


#===========================================================

class ImageData( object ) :

    #=============================

    class _CImageData( Structure ) :
        _fields_ = [ ( 'imageHeight', c_int    ),
                     ( 'imageWidth',  c_int    ),                               
                     ( 'imageSize',   c_int    ),
                     ( 'imageBuffer', c_void_p ) ]
    

    #=============================

    def __init__( self ) :
        self._CImageData = ImageData._CImageData( 0, 0, 0, None )

        for e in self._CImageData._fields_ :
            setattr( self.__class__, e[ 0 ],
                     property( self._getter( e[ 0 ] ) ) )
 

    #=============================

    def _getter( self, what ) :
        def wrapped( self ) :
            return getattr( self._CImageData, what )
        return wrapped


    #=============================

    def get( self ) :
        """
        Returns the image the data represent as a PIL Image class instance
        """

        if not self.imageBuffer :
            return None

        return Image.fromstring( 'RGB', ( self.imageWidth, self.imageHeight ),
                                 string_at( self.imageBuffer,
                                                   self.imageSize ) )
