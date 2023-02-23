import tkinter as tk
import pandas as pd
import glob
from tkinter import filedialog

class analyzer:
    def __init__(self, fname):
        self.filename = fname
        self.df = self.formatCSV(fname)
        self.values = {
            '# Detected particles' : {'row':None,'val':None},
            '# Detection stddev'   : {'row':None,'val':None},
            '# Background'         : {'row':None,'val':None},
            '# Limit of detection' : {'row':None,'valCounts':None,'valKg':None},
            '# Mean'               : {'row':None,'valCounts':None,'valKg':None}
        }
        self.out = {
            'File name' : None,
            'Detected particles' : None,
            'Detection stddev' : None,
            'Background (counts)' : None,
            'Limit of detection (counts)' : None,
            'Limit of detection (kg)' : None,
            'Mean (counts)' : None,
            'Mean (kg)' : None
        }
        self.massKg = None

    def formatCSV(self,fname):
        '''Standardizes the input CSV so that all files are compatible'''
        f = open(fname,'r')
        lines = [l.strip() + ','*(3-l.count(',')) for l in f.readlines()]
        df = pd.DataFrame(l.split(',') for l in lines)
        return df

    def getValues(self):
        for name, info in self.values.items():
            idx = self.df.index[self.df[0]==name][0]
            self.values[name]['row'] = idx
            val = self.df.iloc[idx,1]
            self.values[name]['val'] = val
            if (len(info) > 2):
                self.values[name]['valCounts'] = val
                valkg = self.df.iloc[idx+1,1]
                self.values[name]['valKg'] = valkg
            # Logic for fillint output dict
            self.out['File name'] = self.filename
            if 'Detected particles' in name:
                self.out['Detected particles'] = val
            if 'stddev' in name:
                self.out['Detection stddev'] = val
            if 'Background' in name:
                self.out['Background (counts)'] = val
            if 'Limit' in name:
                self.out['Limit of detection (counts)'] = val
                self.out['Limit of detection (kg)'] = valkg
            if 'Mean' in name:
                self.out['Mean (counts)'] = val
                self.out['Mean (kg)'] = valkg

    def getMassKg(self):
        start = self.df.index[self.df[1] == 'Mass (kg)'][0]
        self.massKg = self.df[1][start+1:-1]

    # DEPRECATED
    def makeCSV(self):
        csvDF = pd.DataFrame(data=self.values)
        csvDF.to_csv('values.csv')

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()

    print('File path is: {}'.format(file_path))

    files = []
    for f in glob.glob('{}/*.csv'.format(file_path)):
        if ('values.csv' in f) or ('masskg.csv' in f): continue
        print('Opening File: {}'.format(f))
        a = analyzer(f)
        a.getValues()
        #a.makeCSV()
        a.getMassKg()
        files.append(a)

    print('Writing output files....')
    outDF = pd.DataFrame([a.out for a in files])
    outDF.to_csv('values.csv')

    massDF = pd.concat([a.massKg for a in files], keys=[a.filename for a in files], axis=1)
    massDF.to_csv('masskg.csv')

    print('Finished writing output files')
