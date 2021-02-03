# -*- coding: utf-8 -*-

import numpy as np


class Screen(object):
    """Screen device.

    """

    def __init__(self, width_cm=None, height_cm=None, distance_cm=None, width_pix=None, height_pix=None):
        # todo: pruefe, dass keine None uebergeben werden!!!
        self._width_cm = width_cm
        self._height_cm = height_cm
        self._distance_cm = distance_cm
        self._width_pix = width_pix  # todo: fuer Windows automatisch berechnen aus Systemfunktion
        self._height_pix = height_pix

    @property
    def width_cm(self):
        return self._width_cm

    @property
    def height_cm(self):
        return self._height_cm

    @property
    def distance_cm(self):
        return self._distance_cm

    @property
    def width_pix(self):
        return self._width_pix

    @property
    def height_pix(self):
        return self._height_pix

    @property
    def width_deg(self):
        return cm2deg(self.width_cm, self.distance_cm)

    @property
    def height_deg(self):
        return cm2deg(self.height_cm, self.distance_cm)

    def deg2pix_width(self, deg):
        return self.width_pix / self.width_deg * deg

    def deg2pix_height(self, deg):
        return self.height_pix / self.height_deg * deg

    def pix2deg_width(self, pix):
        return self.width_deg / self.width_pix * pix

    def pix2deg_height(self, pix):
        return self.height_deg / self.height_pix * pix

    def cm2pix_width(self, cm):
        return cm * self.width_pix / self.width_cm

    def cm2pix_height(self, cm):
        return cm * self.height_pix / self.height_cm

    def pix2cm_width(self, pix):
        return pix * self.width_cm / self.width_pix

    def pix2cm_height(self, pix):
       return pix * self.height_cm / self.height_pix



def cm2rad(cm, distance):
    """
    Statt cm ist jede beliebige Einheit moeglich, solange s und d die gleiche Einheit haben.
    """
    return 2.*np.arctan(cm/(2.*distance))


def cm2deg(cm, distance):
    """
    Statt cm ist jede beliebige Einheit moeglich, solange s und d die gleiche Einheit haben.
    """
    return 180./np.pi * cm2rad(cm, distance)
