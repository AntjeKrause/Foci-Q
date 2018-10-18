# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 14:20:11 2018

@author: Phil Honl
-------------------------------------------------------------------------------------
Scans all folders and sub folders in given directory, collects all information from CSVs
and summarizes them as output.xlsx 
-------------------------------------------------------------------------------------
"""

import os
import pandas as pd

files = []

def scanFolders(path):
    for entry in os.scandir(path):
        if entry.is_dir():
            if (not entry.path.endswith("Results")):
                files.clear()
                scanFolders(entry)
            else:
                if len(os.listdir(entry.path)) != 0:
                    print("T" + entry.path)
                    for i in os.listdir(entry.path):
                        if i.endswith("csv"):
                            files.append(i)
                    if len(files) != 0:
                        excel_wr = pd.ExcelWriter(entry.path +"\output.xlsx", engine = "xlsxwriter")
                        peak_list = pd.DataFrame(columns=["Bild", "Foci"]) #DF for peak list
                        for i in range(len(files)):
                            print(entry.path + "\\" + files[i])
                 
                            df = pd.read_csv(entry.path + "\\" + files[i], skiprows = 0) 
                            file_name_temp = files[i]
                            cell_count = len(df.loc[:, 'Area'])
                            peak_count = df.loc[:, 'Foci'].sum() #Number of peaks/foci in the current file or image
                            df_temp = pd.DataFrame([[file_name_temp, cell_count, peak_count]], columns=["Bild", "Zellen", "Foci"]) #Temporary data to append
                            peak_list = peak_list.append(df_temp) #Append new data to list
                             
                        peak_list.to_excel(excel_wr, sheet_name = "Output")
                        #Add avg, max
                        workbook = excel_wr.book
                        worksheet = excel_wr.sheets["Output"]
                        bold = workbook.add_format({'bold': True})
                        worksheet.write("E1", "Avg Foci/Cell", bold)
                        worksheet.write("E2", peak_list.loc[:,"Foci"].sum()/peak_list.loc[:, "Zellen"].sum())          
                        #Close workbook
                        workbook.close()

print("Finished!")
