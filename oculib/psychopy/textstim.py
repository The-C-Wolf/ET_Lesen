# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 16:39:38 2014

@author: tamm
"""

from psychopy import visual
import psychopy.misc
import numpy

class TextStim(visual.TextStim):
    """
    Implement method 'contains' for PsychoPy TextStim class.
    """
    # todo: Implement alignVert: top and bottom!!!

    def __init__(self, *args, **kwargs):
        visual.TextStim.__init__(self, *args, **kwargs)

    def contains(self, x, y=None):
        if self.alignVert != 'center':
            raise NotImplementedError("Sorry: Only alignVert='center' implemented at the moment.")

        # from visual._BaseVisualStim.contains()
        if hasattr(x, 'getPos'):
            x, y = x.getPos()
        elif type(x) in [list, tuple, numpy.ndarray]:
            x, y = x[0], x[1]

        # convert x, y to pix
        if self.units in ['deg','degs']:
            x, y = psychopy.misc.deg2pix(numpy.array((x, y)), self.win.monitor)
        elif self.units == 'cm':
            x, y = psychopy.misc.cm2pix(numpy.array((x, y)), self.win.monitor)
        if self.ori:
            oriRadians = numpy.radians(self.ori)
            sinOri = numpy.sin(oriRadians)
            cosOri = numpy.cos(oriRadians)
            x0, y0 = x-self._posRendered[0], y-self._posRendered[1]
            x = x0 * cosOri - y0 * sinOri + self._posRendered[0]
            y = x0 * sinOri + y0 * cosOri + self._posRendered[1]

        posx, posy = self._posRendered
        hw = self._pygletTextObj._layout.content_width/2.  # half width
        hh = self.height/2.  # half height

        if self.alignHoriz == 'center':
            poly = ((posx-hw,posy-hh), (posx+hw, posy-hh), (posx+hw, posy+hh), (posx-hw, posy+hh))
        elif self.alignHoriz == 'left':
            poly = ((posx,posy-hh), (posx+2*hw, posy-hh), (posx+2*hw, posy+hh), (posx, posy+hh))
        elif self.alignHoriz == 'right':
            poly = ((posx-2*hw,posy-hh), (posx, posy-hh), (posx, posy+hh), (posx-2*hw, posy+hh))
        else:
            raise ValueError("Unexpected value for 'alignHoriz': {0}".format(self.alignHoriz))

        return visual.pointInPolygon(x, y, poly)