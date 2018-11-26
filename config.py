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
def writeCfg(path, imgpath, noise_g, noise_r, background_g, background_r, green, red):
    fw = open(path + pathVar + "foci.cfg", "w")
    fw.write("noise_g="+str(noise_g)+"\n")
    fw.write("background_g="+str(background_g)+"\n")
    fw.write("noise_r="+str(noise_r)+"\n")
    fw.write("background_r="+str(background_r)+"\n")
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
    noise_g = settings[0]
    background_g = settings[1]
    noise_r = settings[2]
    background_r = settings[3]
    path = settings[4]
    green = settings[5]
    red = settings[6]
    return noise_g[8:], background_g[13:], noise_r[8:], background_r[13:], path[5:], green[6:], red[4:]


print(readCfg(os.getcwd()))
