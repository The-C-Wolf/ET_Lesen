import sys

# todo: _device.py als Baseclass und vendor specific code in entsprechenden subfolder?
# s. psychopy basestim.py (oder zumindest etwa dort), wie man durch zugriff auf Modul-Directory Funktionen und Items
# fuer den Nutzer ausblenden kann.

"""
if a package __init__.py code defines a list named __all__, it is taken to be the list of module names that should
be imported when from package import * is encountered. It is up to the package author to keep this
list up-to-date when a new version of the package is released. Package authors may also decide not to support it, if
they dont see a use for importing * from their package. For example, the file sound/effects/__init__.py could contain
the following code:

__all__ = ["echo", "surround", "reverse"]
"""

# __init__() ist immer noch geraeteunabhaengig und per default als dummy-mode; erst mit open() wird
# geraet tatsaechlich geoffnet.

# Systemspezifischen Code wie folgt kapseln und
# bei versuch zu oeffnen unter linux etc. Warning: Device only verfuegbar im demo-mode
#
#try:
#    import pylink
#    import EyeLinkCoreGraphicsPsychoPy as nfeye
#except ImportError:
#    abc

# if sys.platform.startswith('win'):
# 	# todo: from _smi.redm import ...
#

# Eyelink
#from _srresearch.et_srresearch import Eyelink1000

# SMI
from _smi.et_smi import RedM
from _smi.et_smi import IviewX

# Misc
from device import ParallelPort
from device import SerialPort

# Screen
from screen import Screen

# Logfile
from logfile import Logfile