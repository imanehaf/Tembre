# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 15:00:37 2015

@author: imanies
"""
import xml.etree.ElementTree as ET
import numpy as np
import re
from os.path import join, isfile
from os import listdir, curdir
import subprocess as sp
#import h5py

def main(src, param): #src is path to executables
    exe_files = [ f for f in listdir(src) if isfile(join(curdir, src,f)) ]
    t=cfg2xml('ref.cfg' )
    t= modifyXml(t, param)    
    xml2cfg(t, 'arch.cfg')
    collectData(src, exe_files, 'arch.cfg')
    
    return 

        
def cfg2xml(cfg, xml=None):
    root = ET.Element('dataa')
    root.text = '\n'
    parent=root
    li=[]
    with open(cfg, 'r+') as f:
        for line in f:
            
            txt = re.split('\W+', line.strip())
            if re.search('{', line):
                child = txt[0]
                li.append((parent, child))
                cell=ET.SubElement(li[-1][0],li[-1][1])
                parent = cell
            elif re.search('=', line):
                cell.attrib[txt[0]] = txt[1]
            elif re.search('}', line):
                cell = li[-1][0]
                parent = cell
                li.remove(li[-1])
                if not li:
                    parent = root
                    
    for cell in root.iter('l2'):
            cell.attrib['children'] = 'l1i|l1d'    
    tree = ET.ElementTree(root)
    if xml:    
        tree.write(xml, encoding='utf-8', xml_declaration=True)
    
    return tree
    
    
def collectData(src, exe_files, cfg_file):
        for exe in exe_files:
            print "Executing ZSim for the exe: %s"%(exe)
            with open(cfg_file, 'r') as f:
                fil = f.read()
            t=fil.split('command = ',1)[0] + 'command = "./'+join(src,exe)+\
                '";\n};' +fil.split('command = ',1)[1].split('";\n};',1)[1]
            with open('modif.cfg', 'w') as mf:            
                mf.write(t)
            cmd = 'bash manage.sh %s'%(exe) 
            sp.call(cmd, shell=True)
            
            
                       
        #df=pd.DataFrame([zdata[0]]).append(pd.DataFrame([zdata[1]])).transpose()
        return 

def generateArch(nbEx):
    Lc =[2,3]
    Hz = [1400, 2300, 3400]
    Sz = [1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 524288,
          1048576, 2097152]
    As = ['Direct', 'SetAssoc']
    Ws = [1, 2, 4, 8, 16, 32, 64, 128]
    Lat = [10, 20, 30, 40, 50]
    Rep = ['LRU', 'Random']
    header = [Lc, Hz, Sz, As, Ws, Rep, Lat]
    t = [[2]*nbEx]
    t.append(np.random.choice(Hz, size=(nbEx)))
    for feat in header[2:]:
        for i in range(0,3):
            t.append(np.random.choice(feat, size=(nbEx)))
    
    return np.swapaxes(np.matrix(t),0,1).tolist()
    
def generateParam(archs):
    cells = ['sys', 'l1d', 'l1i', 'l2',  'array', 'repl']
    atts = ['frequency', 'size', 'latency', 'ways', 'type']
    for arch in archs:
        param = [[cells[0], atts[0], arch[1]]]
        for cache, sz, lat in zip(cells[1:4], arch[2:5], arch[-3:]):
            param.append([cache, atts[2], sz])
            param.append([cache, atts[3], lat])
        param.append([cells[-2], atts[-2], (arch[8:11])])
        param.append([cells[-2], atts[-1], (arch[5:8])])
        param.append([cells[-1], atts[-2], (arch[11:14])])
    return param
            
            
    '''
    param = [[sys, frequency, xxx], [l1d, size, xxx][ld1, latency, xxx]
    [array, type, (xxx)][array, ways. (xxx)][repl, type, (xxx)]]
    '''
    return 
    
def modifyXml(tree, parameters, addParam=None):
    #parameters = [[cell, att, (values)]]
    #addParam = [parent*n, child, att]
#np.random.choice(l, size=(10))
    
    root = tree.getroot()
    if addParam:
        for i in range(0, len(addParam)-3):
            for cell in root.iter(addParam[i]):
                ET.SubElement(cell, addParam[i+1])
        for cell in root.iter(addParam[-3]):
            ET.SubElement(cell, addParam[-2], addParam[-1])
    for param in parameters:
        i=0
        for elem in root.iter(param[0]):
            elem.attrib[param[1]]=param[2][i]
            i+=1
    
    
    return tree
    
    
def xml2cfg(tree, cfg):
    root = tree.getroot()
    with open(cfg, 'w') as f:
        for child in root:
            f.write(child.tag + ' = { \n')
            for key, value in child.attrib.items():
                try: 
                    f.write(key + ' = '+str(int(value)) +';\n') 
                except:
                    f.write(key + ' = "'+str(value)+'";\n')
            for cores in child:
                f.write(cores.tag + ' = { \n')
                for core in cores:
                    f.write(core.tag + ' = { \n')
                    for key, value in core.attrib.items():
                        try: 
                            f.write(key + ' = '+str(int(value)) +';\n') 
                        except:
                            f.write(key + ' = "'+str(value)+'";\n')
                    for things in core:
                        f.write(things.tag + ' = { \n')
                        for key, value in things.attrib.items():
                            try: 
                                f.write(key + ' = '+str(int(value)) +';\n') 
                            except:
                                f.write(key + ' = "'+str(value)+'";\n')
                        f.write('};\n')
                    f.write('};\n')
                f.write('};\n')
            f.write('};\n') 
        
            