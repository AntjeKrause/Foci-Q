# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 13:23:29 2018

@author: Phil Honl
"""
import os 
import sys

if sys.platform.startswith("win"):
    pathVar = "\\"
else:
    pathVar = "/"

"""
Write configuration (tolerated noise level, rolling background subtraction radius)
to foci.cfg in given path
"""
def writeCfg(path, imgpath, noise, background):
    fw = open(path + pathVar + "foci.cfg", "w")
    fw.write("noise="+str(noise)+"\n")
    fw.write("background="+str(background)+"\n")
    fw.write("path="+str(imgpath)+"/\n")
    fw.close()
    pass


"""
Read and return configuration from foci.cfg in given path
"""
def readCfg(path):
    global settings
    fr = open(path + pathVar + "foci.cfg", "r")
    settings = fr.readlines()
    settings = [line.rstrip('\n') for line in settings]
    fr.close()
    noise = settings[0]
    background = settings[1]
    return noise[6:], background[11:]
"""
writeCfg(os.getcwd(), 200, 1038)
test = readCfg(os.getcwd())
"""