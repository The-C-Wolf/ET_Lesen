# -*- coding: utf-8 -*-
###############################
### Version 06.10.2010
###############################

try:
    import pylink # pylink nach psychopy gibt dll-Ladefehler???
    from psychopy import *
    from psychopy import sound
    from psychopy import gui
except ImportError:
    # todo: implement error handling
    pass

import sys
import array # image handling

# Faustregel fuer Win.flip():
# In der Regel immer als self.Win.flip(clearBuffer=False) verwenden!

ET=0

class EyeLinkCoreGraphicsPsychoPy(pylink.EyeLinkCustomDisplay):
    def __init__(self,win, tracker):
        """win: PsychoPy window

        """
        pylink.EyeLinkCustomDisplay.__init__(self)
        
        if ET: print('init')
        
        self.width = win.width
        self.height = win.height
        self.x0 = round(self.width/2,3) # todo: flexibler; im Moment fuer Koordinatenursprung im Zentrum
        self.y0 = round(self.height/2,3)

        self.default_text_color = [-1,-1,-1]
        self.default_font_size = 24
        self.fonts = ['Arial','Helvetica','Verdana'] #use the first font found on this list
        
        # todo
        # mouse invisible
        # sound:
        self.beep = sound.SoundPygame(value='C', secs=0.5)
        #self.__target_beep__ = pygame.mixer.Sound("type.wav")
        #self.__target_beep__done__ = pygame.mixer.Sound("qbeep.wav")
        #self.__target_beep__error__ = pygame.mixer.Sound("error.wav")
        #self.imagebuffer = array.array('l')
        
        # todo: Test auf None!
        self.Win = win
        self.cal_target= visual.TextStim(self.Win,text='+',pos=(0.0,0.0),antialias=True,units='pix',font=self.fonts,height=self.default_font_size,color = self.default_text_color)
        # todo: evtl. durch Kreis oder Ring ersetzen
        self.line = visual.ShapeStim(self.Win,units='pix',lineWidth=1.0,interpolate=True,pos=(0.0,0.0),vertices=((0.0,0.0)),closeShape=False)
        
        # # Handle eye image
        # self.imagebuffer = array.array('l') # kleines L
        # self.pal = None
        # self.size=(0,0)
        # self.fimg = open('etimage1','wb') # speicher Kamerabild
        # # test
        # #self.writeimg=True
        # self.writeimg=False
        
    def setTracker(self, tracker):
        if ET: print('setTracker')
        
        self.tracker = tracker
        self.tracker_version = tracker.getTrackerVersion()
        if(self.tracker_version >=3):
            self.tracker.sendCommand("enable_search_limits=YES")
            self.tracker.sendCommand("track_search_limits=YES")
            self.tracker.sendCommand("autothreshold_click=YES")
            self.tracker.sendCommand("autothreshold_repeat=YES")
            self.tracker.sendCommand("enable_camera_position_detect=YES")
            
    def setup_cal_display (self):
        if ET: print('setup_cal_display')
        
        
        self.Win.clearBuffer()
        self.Win.flip()
        
    def exit_cal_display(self):
        if ET: print('exit_cal_display')
        self.clear_cal_display()
     
        
    def record_abort_hide(self):
        pass
        
    def clear_cal_display(self):
        if ET: print('clear_cal_display')
        self.Win.clearBuffer()
        self.Win.flip()
    
    def erase_cal_target(self):
        if ET: print('erase_cal_target')
        self.Win.clearBuffer()
        self.Win.flip()
        
    def draw_cal_target(self, x, y):
        if ET: print('draw_cal_target',x,y)
        
        # todo auf korrekte Werte
        my_x = x-self.x0
        my_y = self.y0-y
        
        self.cal_target.setPos((my_x,my_y))
        self.cal_target.draw()
        self.Win.flip(clearBuffer=False)
        
    def play_beep(self,beepid):
        if ET: print('play_beep')
        self.beep.play()
        # todo: Beeps s.u. implementieren
        
#        if beepid == pylink.DC_TARG_BEEP or beepid == pylink.CAL_TARG_BEEP:
#            self.__target_beep__.play()
#        elif beepid == pylink.CAL_ERR_BEEP or beepid == pylink.DC_ERR_BEEP:
#            self.__target_beep__error__.play()
#        else:#  CAL_GOOD_BEEP or DC_GOOD_BEEP
#            self.__target_beep__done__.play()

    def draw_line(self,x1,y1,x2,y2,colorindex):
        if ET: print('draw_line')
        #self.line.pos(0.0,0.0)
        self.line.vertices((x1,y1),(x2,y2))
        
        if colorindex   ==  pylink.CR_HAIR_COLOR:          color = (1,1,1)
        elif colorindex ==  pylink.PUPIL_HAIR_COLOR:       color = (1,1,1)
        elif colorindex ==  pylink.PUPIL_BOX_COLOR:        color = (0,1,0)
        elif colorindex ==  pylink.SEARCH_LIMIT_BOX_COLOR: color = (1,0,0)
        elif colorindex ==  pylink.MOUSE_CURSOR_COLOR:     color = (1,0,0)
        else: color =(0,0,0,0)
        
        self.line.setLineColor(color)
        self.line.draw()
        self.Win.flip(clearBuffer=False)

# Keyboard-Abfrage ueber pygame (s. pylink-Hilfe)
#    def get_input_key(self):
#        ky = []
#        v = pygame.event.get()
#        if v !=[]: print(v)
#        for key in v:
#            if key.type != KEYDOWN:
#                continue
#            keycode = key.key
#            print(keycode)
#            if keycode == K_F1:  keycode = pylink.F1_KEY
#            elif keycode ==  K_F2:  keycode = pylink.F2_KEY
#            elif keycode ==   K_F3:  keycode = pylink.F3_KEY
#            elif keycode ==   K_F4:  keycode = pylink.F4_KEY
#            elif keycode ==   K_F5:  keycode = pylink.F5_KEY
#            elif keycode ==   K_F6:  keycode = pylink.F6_KEY
#            elif keycode ==   K_F7:  keycode = pylink.F7_KEY
#            elif keycode ==   K_F8:  keycode = pylink.F8_KEY
#            elif keycode ==   K_F9:  keycode = pylink.F9_KEY
#            elif keycode ==   K_F10: keycode = pylink.F10_KEY
#            
#            elif keycode ==   K_PAGEUP: keycode = pylink.PAGE_UP
#            elif keycode ==   K_PAGEDOWN:  keycode = pylink.PAGE_DOWN
#            elif keycode ==   K_UP:    keycode = pylink.CURS_UP
#            elif keycode ==   K_DOWN:  keycode = pylink.CURS_DOWN
#            elif keycode ==   K_LEFT:  keycode = pylink.CURS_LEFT
#            elif keycode ==   K_RIGHT: keycode = pylink.CURS_RIGHT
#            
#            elif keycode ==   K_BACKSPACE:    keycode = ord('\b')
#            elif keycode ==   K_RETURN:  keycode = pylink.ENTER_KEY
#            elif keycode ==   K_ESCAPE:  keycode = pylink.ESC_KEY
#            elif keycode ==   K_TAB:     keycode = ord('\t')
#            elif(keycode==pylink.JUNK_KEY): keycode= 0
#            ky.append(KeyInput(keycode))
#        return ky
      
    # Keyboard-Abfrage ueber Psychopy
    def get_input_key(self):
        # todo: warum ist keypress hier immer [], aber nicht in testkeypress2.py?
        # Irgendjemand scheint den Buffer immer schon vorher abzugreifen???
        ky=[]
        keypress = event.getKeys(keyList=None)
        if keypress == []:
            return ky
        else:
            for keycode in keypress:
                if keycode == 'f1':  keycode = pylink.F1_KEY
                elif keycode ==  'f2':  keycode = pylink.F2_KEY
                elif keycode ==   'f3':  keycode = pylink.F3_KEY
                elif keycode ==   'f4':  keycode = pylink.F4_KEY
                elif keycode ==   'f5':  keycode = pylink.F5_KEY
                elif keycode ==   'f6':  keycode = pylink.F6_KEY
                elif keycode ==   'f7':  keycode = pylink.F7_KEY
                elif keycode ==   'f8':  keycode = pylink.F8_KEY
                elif keycode ==   'f9':  keycode = pylink.F9_KEY
                elif keycode ==   'f10': keycode = pylink.F10_KEY
    
                elif keycode ==   'pageup': keycode = pylink.PAGE_UP
                elif keycode ==   'pagedown':  keycode = pylink.PAGE_DOWN
                elif keycode ==   'up':    keycode = pylink.CURS_UP
                elif keycode ==   'down':  keycode = pylink.CURS_DOWN
                elif keycode ==   'left':  keycode = pylink.CURS_LEFT
                elif keycode ==   'right': keycode = pylink.CURS_RIGHT
    
                elif keycode ==   'backspace':    keycode = ord('\b')
                elif keycode ==   'return':  keycode = pylink.ENTER_KEY
                elif keycode ==   'escape':  keycode = pylink.ESC_KEY
                elif keycode ==   'tab':     keycode = ord('\t')
                #elif(keycode==pylink.JUNK_KEY): keycode= 0
                # Was ist pylink.JUNK_KEY? Jede sonstige Taste?
                ky.append(pylink.KeyInput(keycode))
                return ky


    def exit_image_display(self):
        if ET: print('exit_image_display')
        self.Win.clearBuffer()
        self.Win.flip()
        self.fimg.close()

    def alert_printf(self,msg):
        myDlg = gui.Dlg(title="Alert Message")
        myDlg.addText('msg')
        myDlg.show()#show dialog and wait for OK or Cancel
        
    def setup_image_display(self, width, height):
        if ET: print('setup_image_display')
        self.size = (width,height)
        self.clear_cal_display()
        self.last_mouse_state = -1
        
        return 1

    def image_title(self, threshold, text):
        pass
        # todo
#        text = text + " " +str(threshold)
#
#        sz = self.fnt.size(text[0])
#        txt = self.fnt.render(text,len(text),(0,0,0,255), (255,255,255,255))
#        surf = pygame.display.get_surface()
#        imgsz=(self.size[0]*3,self.size[1]*3)
#        topleft = ((surf.get_rect().w-imgsz[0])/2,(surf.get_rect().h-imgsz[1])/2)
#        imsz=(topleft[0]+imgsz[0]/2,topleft[1]+imgsz[1]+10)
#        surf.blit(txt, imsz)
#        pygame.display.flip()
#        surf.blit(txt, imsz)


# todo
    def draw_image_line(self, width, line, totlines,buff):
       # if ET: print('draw_image_line')
       # todo rausschreiben in Datei und schauen, ob man damit eigene eyetrackingalg. schreiben könnte
        
        if self.writeimg==False: return
        
        #print "draw_image_line", len(buff)
        i =0
        while i <width:
            #self.imagebuffer.append(self.pal[buff[i]])
            self.imagebuffer.append(buff[i])
            i= i+1

        if line == totlines:
            self.imagebuffer.tofile(self.fimg)
            self.imagebuffer = array.array('l') # kleines L
            self.writeimg=False # nur 1 Bild rausschreiben
            
            
           #imgsz = (self.size[0]*3,self.size[1]*3)
            #bufferv = self.imagebuffer.tostring()
            #img =Image.new("RGBX",self.size)
            #img.fromstring(bufferv)
            #img = img.resize(imgsz)


#            img = pygame.image.fromstring(img.tostring(),imgsz,"RGBX");
#
#            self.__img__ = img
#            self.draw_cross_hair()
#            self.__img__ = None
#            surf = pygame.display.get_surface()
#            surf.blit(img,((surf.get_rect().w-imgsz[0])/2,(surf.get_rect().h-imgsz[1])/2))
#            pygame.display.flip()
#            self.imagebuffer = array.array('l')
#
#
#
    def set_image_palette(self, r,g,b):
        return
        
        if ET: print('set_image_palette')
        self.imagebuffer = array.array('l')
        self.clear_cal_display()
        sz = len(r)
        i =0
        self.pal = []
        while i < sz:
            rf = int(b[i])
            gf = int(g[i])
            bf = int(r[i])
            self.pal.append((rf<<16) | (gf<<8) | (bf))
            i = i+1

#def get_mouse_state(self):
#		pos = pygame.mouse.get_pos()
#		state = pygame.mouse.get_pressed()
#		return (pos,state[0])	

#############################################################################################
# todo: automatisch per __name__ == __main__ starten, wenn direkt aufgerufen
# Beispielanwendung
#
#MODE = "TRACKING" #DEMO, TRACKING
#ET=-1
#
#if MODE=="DEMO":
#    tracker = pylink.EyeLink(None) #?was bringt das, wenn man dann doch alle Kommandos ausblenden muss?
#    ET = 0
#elif MODE=="TRACKING":
#    tracker = pylink.EyeLink("100.1.1.1.")
#    ET=1
#else: 
#    # todo: Warnung + Abbruch
#    none
#    
#dispwidth = 800
#dispheight = 600
#
#FULLSCREEN=0
#default_background_color = [(200/127.5)-1,(200/127.5)-1,(200/127.5)-1]   #rgb presentation (0,255)-> rgb-psychopy (-1,1)
#Win = visual.Window((dispwidth,dispheight),allowGUI=False,winType='pyglet', monitor='testMonitor', screen=0,units='pix',colorSpace='rgb',color=default_background_color,fullscr=FULLSCREEN)
#
#genv = EyeLinkCoreGraphicsPsychoPy(dispwidth,dispheight,tracker,Win) #  Größe des Displays auf dem Presentationsrechner
#pylink.openGraphicsEx(genv)
#currentDisplay = pylink.getDisplayInformation();
#print "Current display settings: ", currentDisplay.width, currentDisplay.height,currentDisplay.bits, currentDisplay.refresh
#tracker.doTrackerSetup(dispwidth,dispheight) # mit diesen Werten berechnet der Tracker, wo die Kalibrierungspunkte gesetzt werden
#print('Back from tracker setup')
#
