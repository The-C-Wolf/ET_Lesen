# -*- coding: utf-8 -*-
"""
Created on Sun Aug 09 16:36:41 2015

@author: Ocunostics
"""

from psychopy import gui
import os


class Subject(object):
    def __init__(self, result_dir=''):
        self.sid = ''
        #self.group = ''
        self.result_dir = result_dir
        self.age = ''
        self.sex = ''
        self.glass = ''
        self.lang = ''
        self.fname = None

        if not os.path.isdir(self.result_dir):
            os.makedirs(self.result_dir)

    def show(self, title=''):
        while 1:
            myDlg = gui.Dlg(title=title)
            myDlg.addText('                        ')
            myDlg.addField(u'VP-Nummer', self.sid)
            myDlg.addField(u'Alter', self.age)
            myDlg.addField(u'Geschlecht', self.sex, choices=['',u'maennlich', u'weiblich',u'anderes'])
            myDlg.addField(u'Muttersprache', self.lang, choices=['deutsch',u'deutsch + andere', u'andere'])
            myDlg.addField(u'Sehhilfe', self.glass, choices=['keine',u'Brille', u'Kontaktlinsen'])
            #myDlg.addField(u'Gruppe', self.group, choices=['','1', '2','3','4'])
            myDlg.addText(' ')
            myDlg.show()
            if myDlg.OK:
                dummy = myDlg.data # list of data returned from each field added in order
                self.sid = str(dummy[0])  # save return values before any further check so that they become the new default values
                #self.group = str(dummy[1])
                self.age = str(dummy[1])
                self.sex = str(dummy[2])
                self.lang = str(dummy[3])
                self.glass = str(dummy[4])
                #self.group = str(dummy[5])
                if not all(dummy):  # equivalent to if dummy[0] == '' or dummy[1] == '' ...
                    continue                
                
                # todo: anpassen                
                #if self.id != '' and self.sess != '' and self.handedness != '':
                #    if self.handedness not in ('L', 'R'):
                #        self.handedness = ''
                #        continue

                #self.fname = os.path.join(self.result_dir, 'vp{0}_{1}.txt'.format(
                #        self.sid, self.group))
                self.fname = os.path.join(self.result_dir, 'vp{0}.txt'.format(
                        self.sid))
                                
                if os.path.isfile(self.fname):
                    warnDlg = gui.Dlg(title="Warning")
                    warnDlg.addText('                        ')
                    warnDlg.addText('Overwrite file {0}?'.format(self.fname))
                    warnDlg.addText(' ')
                    warnDlg.show()
                    if warnDlg.OK:
                        break
                    else:
                        continue
                else:
                    break
            else:
                return 0

        return 1, self.sid, self.age, self.glass, self.lang, self.sex


