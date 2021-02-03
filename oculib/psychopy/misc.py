# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 10:43:36 2013

@author: ocunostics
"""

from psychopy import visual


def screen2win(win, pos):
    """Transform full screen coordinates to window coordinates.
    
    Args:
        win: Psychopy window object
        pos: (x,y) screen coordinates
    
    Returns:
        (x,y) in window coordinates
    """
    if not isinstance(win, visual.Window):
        pass # todo
    (winX, winY)          = win.pos
    (winWidth, winHeight) = win.size
    (x, y)                = pos # x,y in screen coordinates
    return x-winX-winWidth/2., winHeight/2.-(y-winY)

def win2screen(win, pos):
    """Transform window coordinates to full screen coordinates.
    
    Args:
        win: Psychopy window object
        pos: (x,y) window coordinates
    
    Returns:
        (x,y) in screen coordinates
    """
    if not isinstance(win, visual.Window):
        pass # todo
    (winX, winY)          = win.pos
    (winWidth, winHeight) = win.size
    (x, y)                = pos # x,y in windows coordinates
    return x+winX+winWidth/2., y-winHeight/2.+winY


def rect_vertices(roundness=0, topleft=(-0.3,0.4), bottomright=(0.3,-0.4)):
    """
    From Psychopy RatingScale code.

    roundness: 0 = rectangle

    """

    delta = roundness
    delta2 = delta / 7.
    left = topleft[0]
    right = bottomright[0]
    top = topleft[1]
    bot = bottomright[1]
    boxvertices = [  # a rectangle with rounded corners; for square corners, set delta to 0
                  [left, top - delta], [left + delta2, top - 3 * delta2],
                  [left + 3 * delta2, top - delta2], [left + delta, top],
                  [right - delta, top], [right - 3 * delta2, top - delta2],
                  [right - delta2, top - 3 * delta2], [right, top - delta],
                  [right, bot + delta], [right - delta2, bot + 3 * delta2],
                  [right - 3 * delta2, bot + delta2], [right - delta, bot],
                  [left + delta, bot], [left + 3 * delta2, bot + delta2],
                  [left + delta2, bot + 3 * delta2], [left, bot + delta]]
    return boxvertices
