# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 12:48:39 2018

@author: Phil Honl
"""
wd = ""
import os
import threading
import time
import subprocess
from tkinter import *
import tkinter.scrolledtext as ScrolledText
import tkinter.font as tkFont
from tkinter import filedialog
import config
import evaluation

folders = []
files = []
print("Working in directory: " + wd)


class App:
    
    def __init__(self, master):
        
        def updateLog(text):
            text = text + "\n"
            self.user_log.insert(END, text)
            pass
        
        def choosePath(event=None):
            global dirname
            print("Initializing Dialogue...\nPlease select a directory.")
            dirname = filedialog.askdirectory(initialdir=os.getcwd(),title='Please select a directory')
            if len(dirname) > 0:
                print ("You chose %s" % dirname)
            else: 
                dirname = os.getcwd()
                print ("\nNo directory selected")
            self.path_field_image.delete("1.0", END) 
            self.path_field_image.insert(CURRENT, dirname)   
            updateLog("Updated Path to: " + dirname)
            #root.update()
            
        def startThread():
             config.writeCfg(os.getcwd(), dirname, self.noise_field.get("1.0", END+"-1c"),  self.background_field.get("1.0", END+"-1c"))
             updateLog("Saving parameters...")
             updateLog("Starting IJ macro...")
             global t
             t = threading.Thread(target=startIj())
             t.start()

             #print(child.poll())

             #os.system("start /wait cmd /c {java -jar ij.jar -m dialog3.ijm}")  
             #global child
             #child = subprocess.Popen(["java", "-jar", "ij.jar",  "-m", "dialog3.ijm"])
             
        def startIj():
            global child
            child = subprocess.Popen(["java", "-jar", "ij.jar",  "-m", "foci.ijm"])            
           
        def checkInput(path):
            if os.path.exists(path):
                startThread()
            else:
                updateLog("Error: path does not exist.")
            
    

        self.master = master
        master.title("Foci Macro")
        master.geometry('470x300')
        
        self.font = tkFont.Font(family="courier", size=8)
        self.choose_label = Label(master, text = "Image path: ")
        self.choose_label.grid(column = 0, row = 0, sticky = W, padx = 10)
        self.path_field_image =Text(root, height = 1, width = 50)
        self.path_field_image.grid(column = 0, row = 1, padx = 10, columnspan = 2)
        
        self.choose_btn = Button(root, text="...", command = choosePath)
        self.choose_btn.grid(column = 3, row = 1, sticky = W)
        
        self.noise_label = Label(master, text = "Noise (Find Maxima): ")
        self.noise_label.grid(column = 0, row = 3, sticky = W, padx = 10)
        self.noise_field = Text(root, height = 1, width = 5)
        self.noise_field.insert(CURRENT, config.readCfg(os.getcwd())[0])
        self.noise_field.grid(column = 0, row = 4, sticky = W, padx = 10)

        self.background_label = Label(master, text = "Background subtraction radius: ")
        self.background_label.grid(column = 0, row = 5, sticky = W, padx = 10)
        self.background_field = Text(root, height = 1, width = 5)
        self.background_field.insert(CURRENT, config.readCfg(os.getcwd())[1])
        self.background_field.grid(column = 0, row = 6, sticky = W, padx = 10)
        
        self.user_log_label = Label(master, text = "Log:")
        self.user_log_label.grid(column = 0, row = 7, sticky = W, padx = 10)
        self.user_log = ScrolledText.ScrolledText(root, height = 5, width = 50, font = self.font)
        self.user_log.grid(column = 0, row = 8, sticky = W, padx = 10)
        
        self.start_btn = Button(root, text="Go!", command = lambda : checkInput(dirname))
        self.start_btn.grid(column = 0, row = 9, sticky = W, padx = 10, pady = 10)
        global x
        x = self.noise_field.get("1.0", "end-1c")
root = Tk()
gui = App(root)
root.mainloop()
