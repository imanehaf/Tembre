# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from os.path import join, isfile
from os import listdir
import subprocess as sp
import h5py # presents HDF5 files as numpy arrays

def main(src, cfg_f):
    exe_files = [ f for f in listdir(src) if isfile(join(src,f)) ]
    
    #Execution times of executables from running ZSim
    zData = zsimCall(src, exe_files, cfg_f)

    #Execution times of executables from running perf
    pData = perfCall(src, exe_files)
    return zData, pData
    
def perfCycles(src, exe_files):
    print '\n++++++ PERF EXECUTABLE PROFILING+++++\n'
    sp.call('rm res.*', shell=True)
    for exe in exe_files:
        
        cmd = '3>>res.txt perf stat --repeat 20 -e cycles:u --log-fd 3 ./%s/%s >> res.txt' % (src,exe)
        print 'Executing the perf cmd for exe : ' + exe
        sp.call(cmd, shell=True)

def perfCall(src, exe_files):
    perfCycles(src, exe_files)
    with open('res.txt','r') as f:
        fil = f.read()
    t = [ff.split('cycles')[0].strip(' ').replace(',','') for ff in fil.split(':\n\n')][1::]
    ETs = [float(tt) for tt in t]
    return dict(zip(exe_files, ETs))
    
def zsimCycles(src):
    # Open stats file
    f = h5py.File(src+'/zsim-ev.h5', 'r')
    # Get the single dataset in the file
    dset = f["stats"]["root"]
    procCycles = dset[-1]['procCycles'][0]
    return procCycles
    
def zsimCall(src, exe_files, cfg_file):
    zdata={}
    print '\n++++++ ZSIM EXECUTABLE PROFILING+++++\n'
    for exe in exe_files:
        
        with open(cfg_file, 'r') as f:
            fil = f.read()
        t=fil.split('command = ',1)[0] +'command = "./'+join(src,exe)+'";\n};'
        sp.call('rm modif.cfg', shell=True)
        with open('modif.cfg', 'w') as mf:            
            mf.write(t)
        cmd = './../zsim/build/opt/zsim modif.cfg' 
        print 'Executing ZSim for the exe : %s' % (exe)
        sp.call(cmd, shell=True)
        
        while (not isfile('zsim-ev.h5')):
            print '..waiting for %s...'%(exe)
                   
        zdata [exe] = zsimCycles('.') 
        cmd = 'mv zsim-ev.h5 cfg_files/%s.h5'%(exe)
        sp.call(cmd, shell=True)
    #df=pd.DataFrame([zdata[0]]).append(pd.DataFrame([zdata[1]])).transpose()
    return zdata