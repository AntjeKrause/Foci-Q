# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 12:48:39 2018

@author: Phil Honl
"""
wd = ""
import os
import sys
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
            #Updates log window with given text
            self.user_log.configure(state="normal")
            text = text + "\n"
            self.user_log.insert(END, text)
            self.user_log.see("end")
            self.user_log.configure(state="disabled")
            pass
        
        def choosePath(event=None):
            #Opens file dialog to search 
            global dirname
            print("Select a directory.")
            dirname = filedialog.askdirectory(initialdir=os.getcwd(),title='Please select a directory')
            if len(dirname) > 0:
                print ("Chose" + str(dirname))
            else: 
                print ("No directory selected.. Using config.")
            self.path_field_image.delete("1.0", END) 
            self.path_field_image.insert(CURRENT, dirname)   
            updateLog("Updated Path to: " + dirname)
                       
        def startThread():
            #starts a thread which starts ImageJ
             config.writeCfg(os.getcwd(), dirname, self.noise_field.get("1.0", END+"-1c"),  self.background_field.get("1.0", END+"-1c"))
             updateLog("Saving parameters...")
             updateLog("Starting IJ macro...")
             global t
             t = threading.Thread(target=startIj())
             t.start()

        def startIj():
            #start ImageJ in new subprocess with given params
            global child
            child = subprocess.Popen(["java", "-jar", "ij.jar", "-m", "foci.ijm"])            #,  "-m", "foci.ijm"
            t1 = threading.Thread(target=startEvaluation)
            t1.start()
                        
        def startEvaluation():
            #start evaluation of files after IJ is done locating foci
            while child.poll() is None:
                time.sleep(1)
            updateLog("IJ done...")
            updateLog("Starting evaluation...")
            evaluation.scanFolders(dirname)
            updateLog("Finished. Check Results folder!")
            
        def checkInput(path):
            #check if path exists and start thread
            if os.path.exists(path):
                startThread()
            else:
                updateLog("Error: path does not exist.")
            
        global dirname
        dirname = config.readCfg(os.getcwd())[2]
        #master settings
        self.master = master
        master.title("FociQ")
        master.geometry('470x300')
        #master.configure(background='grey')
        self.font = tkFont.Font(family="courier", size=8)
        #Path text label and input label
        self.choose_label = Label(master, text = "Image path: ")
        self.choose_label.grid(column = 0, row = 0, sticky = W, padx = 10)
        self.path_field_image =Text(root, height = 1, width = 50)
        self.path_field_image.grid(column = 0, row = 1, padx = 10, columnspan = 2)
        self.path_field_image.insert(CURRENT, config.readCfg(os.getcwd())[2])
        #Choose path btn
        self.choose_btn = Button(root, text="...", command = choosePath)
        self.choose_btn.grid(column = 3, row = 1, sticky = W)
        #Noise text label and input label
        self.noise_label = Label(master, text = "Noise (Find Maxima): ")
        self.noise_label.grid(column = 0, row = 3, sticky = W, padx = 10)
        self.noise_field = Text(root, height = 1, width = 5)
        self.noise_field.insert(CURRENT, config.readCfg(os.getcwd())[0])
        self.noise_field.grid(column = 0, row = 4, sticky = W, padx = 10)
        #Background subtraction radius text label and input label
        self.background_label = Label(master, text = "Background Subtraction Radius: ")
        self.background_label.grid(column = 0, row = 5, sticky = W, padx = 10)
        self.background_field = Text(root, height = 1, width = 5)
        self.background_field.insert(CURRENT, config.readCfg(os.getcwd())[1])
        self.background_field.grid(column = 0, row = 6, sticky = W, padx = 10)
        #User log text and input label
        self.user_log_label = Label(master, text = "Log:")
        self.user_log_label.grid(column = 0, row = 7, sticky = W, padx = 10)
        self.user_log = ScrolledText.ScrolledText(root, height = 5, width = 50, font = self.font)
        self.user_log.grid(column = 0, row = 8, sticky = W, padx = 10)
        self.user_log.configure(state="disabled")
        updateLog("Ready...")
        #Execute button for foci counting
        self.start_btn = Button(root, text="Go!", command = lambda : checkInput(dirname))
        self.start_btn.grid(column = 0, row = 9, sticky = W, padx = 10, pady = 10)
        
        self.version = Label(master, text = "0.1.0")
        self.version.grid(column = 1, row = 10, sticky = E)

root = Tk()
gui = App(root)
root.mainloop()
