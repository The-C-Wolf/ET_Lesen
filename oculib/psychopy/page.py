# -*- coding: utf-8 -*-
"""
Created on Sat May 16 22:08:42 2015

@author: tamm
"""

from oculib.psychopy import Frame

class Page(Frame):
    def __init__(self, win, mouse=None, name=None, *args, **kwargs):
        Frame.__init__(self, win, *args, **kwargs)
        
        self.win = win
        self.mouse = mouse
        self.name = name
        
        self._pages = None  # set to hosting pages object by pages.add() 
        
class Pages(object):
    '''Manage page objects.
    index: page number starting with 1
    '''
    def __init__(self):
        self._pages = []
        self._current_index = 0
        
    def add(self, page=None):
        if not isinstance(page, Page):
            raise Exception('Expectect page to be instance of Page class.')
        
        page._pages = self
        self._pages.append(page)
        
    def insert(self, pagenr=None, page=None):
        if not isinstance(page, Page):
            raise Exception('Expectect page to be instance of Page class.')
        
        index = self._pagenr2index(pagenr)
        if index<0: 
            index=0
        elif index>=self.count():
            index=self.count()
        self._pages.insert(index, page)
            
    def remove(self, pagenr=None):
        self._pages.remove(self._pagenr2index(pagenr))
        
    def count(self):
        return len(self._pages)
                
    def draw(self):
        self._pages[self._current_index].draw()
    
    def next(self):
        if self._current_index < self.count()-1:
            self._current_index +=1
    
    def prev(self):
        if self._current_index > 0:
            self._current_index -=1
     
    @property
    def page(self):
        """
        Return (nr, page) of current page
        
        Warning: Return interface will change in future.
        """
        return self._index2pagenr(self._current_index), self._pages[self._current_index]
        
    @page.setter
    def page(self, pagenr):
        index = self._pagenr2index
        if index < 1:
            index = 1
        elif index >= self.count():
            index = self.count()
        self._current_index = index
        
    def _index2pagenr(self, index):
        return index+1
        
    def _pagenr2index(self, pagenr):
        return pagenr-1
