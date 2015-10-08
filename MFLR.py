# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 15:00:37 2015

@author: imanies
"""
import xml.etree.ElementTree as ET
import re
import collect
from os.path import join, isfile
from os import listdir, curdir

def main(src, cfg, param): #src is path to executables
    exe_files = [ f for f in listdir(src) if isfile(join(curdir, src,f)) ]
    host = collect.Collect()
    t=cfg2xml(cfg )
    
    t= modifyXml(t, param)    
    xml2cfg(t, 'arch.cfg')
    
    hData = host.zsimCall(src, exe_files, 'arch.cfg')

    return hData
    
def modifyXml(tree, parameters, addParam=None):
    #parameters = [[cell, att, value]]
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
        for elem in root.iter(param[0]):
            elem.attrib[param[1]]=param[2]
    
    
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
                    f.write('};\n')
                f.write('};\n')
            f.write('};\n') 
        
        
        
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
    
    
    
    