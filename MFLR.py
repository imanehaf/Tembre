# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 15:00:37 2015

@author: imanies
"""
import xml.etree.ElementTree as ET
import re
import collect
from os.path import join, isfile
from os import listdir

def main(src, cfg, param): #src is path to executables
    exe_files = [ f for f in listdir(src) if isfile(join(src,f)) ]
    host = collect.Collect()
    cfg2xml(cfg, 'ref.xml')
    modifyXml('ref.xml', param)    
    xml2cfg('ref.xml', 'arch.cfg')
    
    hData = host.zsimCall(src, exe_files, 'host.cfg')

    return hData
    
def modifyXml(xml, parameters, addParam=None):
    #parameters = [[cell, att, value]]
    #addParam = [parent*n, child, att]
#np.random.choice(l, size=(10))
    
    
    tree = ET.parse(xml)
        
    
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
    
    if xml:    
        tree.write(xml, encoding='utf-8', xml_declaration=True)
    return tree
    
    
def xml2cfg(xml, cfg):
    if type(xml) == 'xml.etree.ElementTree.ElementTree'    :
        tree = xml
    else:
        tree = ET.parse(xml)
        
    root = tree.getroot()
    with open(cfg, 'w') as f:
        for child in root:
            f.write(child.tag + ' = { \n')
            for key, value in child.attrib.items():
                f.write(key + ' = '+value +';\n')
            for cores in child:
                f.write(cores.tag + ' = { \n')
                for core in cores:
                    f.write(core.tag + ' = { \n')
                    for key, value in core.attrib.items():
                        print str(value)+ 'type: '+str(type(value))
                        f.write(key + ' = '+(value) +';\n') 
                        '''   
                        except:
                            print value+ ': exception'
                            f.write(key + ' = "'+value +'";\n')'''
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
                li.remove(li[-1])
                if li:
                    parent = li[-1][0]
                else:
                    parent = root
                
    tree = ET.ElementTree(root)
    if xml:    
        tree.write(xml, encoding='utf-8', xml_declaration=True)
    
    return tree
    
    
    
    