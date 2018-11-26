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
def writeCfg(path, imgpath, noise, background, green, red):
    fw = open(path + pathVar + "foci.cfg", "w")
    fw.write("noise="+str(noise)+"\n")
    fw.write("background="+str(background)+"\n")
    if str(imgpath).endswith("/"):
        fw.write("path="+str(imgpath)+"\n")
    else:
        fw.write("path="+str(imgpath)+"/\n")
    fw.write("green="+str(green)+"\n")
    fw.write("red="+str(red)+"\n")
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
    path = settings[2]
    green = settings[3]
    red = settings[4]
    return noise[6:], background[11:], path[5:], green[6:], red[4:]


print(readCfg(os.getcwd()))