# todo: dict statt ueber self.row['entry'] direkt als object['entry'] und als object.entry ansprechbar 

# todo: logfile auch als device-Object

# generate timestamp (eigene clock oder beim Start clock uebergeben
# --> sync with other clocks)

import codecs

class Logfile(object):
    def __init__(self):
        self.fname = None
        self.header = None
        self.sep = None
        self.mode = None
        self._fout  = None
        
        self._not_open_warning = False
        
    def open(self, fname, mode='r', header=[], sep=';'):
        self._fout = codecs.open(fname, mode=mode, encoding='utf-8')
        self.mode = mode
        self.sep = sep
        if header is not None:
            self.header = header
            self._fout.write(self.sep.join(self.header) + '\n')
            self._pattern_out = [u'{{{0}}}'.format(item) for item in header]  # ('{vp}', '{trial_id}', ...) ;
            # If you need to include a brace character in the literal text, it can be escaped by doubling: {{ and }}.
 
    def close(self):
        if self._fout is None:
            return
            
        self._fout.close()
        
    def add_row(self):
        self._row = dict.fromkeys(self.header,'/')  # init log with '/'
        
    def write_row(self):
        self._fout.write(self.sep.join(self._pattern_out).format(**self._row) + '\n') 
    
    def write(self, message):
        if self._fout is None:
            if not self._not_open_warning:
                print('Warning: Attempt to write to not existing logfile! This message is given only once.')  # Hack to simulate dummy mode
                self._not_open_warning = True
            return
        self._fout.write(u'{0}\n'.format(message))
    
    def __getitem__(self, key):
        return self._row[key]
    
    def __setitem__(self, key, val):
        self._row[key] = val