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
import config
global files, filesRed, green, red
green = int(config.readCfg(os.getcwd())[3])
red = int(config.readCfg(os.getcwd())[4])

files = []
filesRed = []

def scanFolders(path):
    global files, filesRed, green, red
    green = int(config.readCfg(os.getcwd())[3])
    red = int(config.readCfg(os.getcwd())[4])
    for entry in os.scandir(path):
        if entry.is_dir():
            if (not entry.path.endswith("Results")):
                files.clear()
                scanFolders(entry)
            else:
                if len(os.listdir(entry.path)) != 0:
                    for i in os.listdir(entry.path):
                
                        if i.endswith("G.csv"):
                            files.append(i)
                        elif i.endswith("R.csv"):
                            filesRed.append(i)
                    excel_wr = pd.ExcelWriter(entry.path +"\output.xlsx", engine = "xlsxwriter")
                    if green:
                        if len(files) != 0:
                            #global peak_list
                            peak_list = pd.DataFrame(columns=["Image/File", "Foci"]) #DF for peak list
                        for i in range(len(files)):
                            print(entry.path + "\\" + files[i])
                            
                            df = pd.read_csv(entry.path + "\\" + files[i], skiprows = 0) 
                            file_name_temp = files[i]
                            cell_count = len(df.loc[:, 'Area'])
                            peak_count = df.loc[:, 'FociGreen'].sum() #Number of peaks/foci in the current file or image
                            df_temp = pd.DataFrame([[file_name_temp, cell_count, peak_count]], columns=["Image/File", "Cells", "Foci"]) #Temporary data to append
                            peak_list = peak_list.append(df_temp, ignore_index = True) #Append new data to list
                        
                        
                    if red:
                        if len(filesRed) != 0:
                            #global peak_list_red
                            peak_list_red = pd.DataFrame(columns=["Image/File", "Foci"]) #DF for peak list
                            for i in range(len(filesRed)):
                                print(entry.path + "\\" + filesRed[i])
                                
                                df = pd.read_csv(entry.path + "\\" + filesRed[i], skiprows = 0) 
                                file_name_temp = filesRed[i]
                                cell_count = len(df.loc[:, 'Area'])
                                peak_count = df.loc[:, 'FociRed'].sum() #Number of peaks/foci in the current file or image
                                df_temp = pd.DataFrame([[file_name_temp, cell_count, peak_count]], columns=["Image/File", "Cells", "Foci"]) #Temporary data to append
                                peak_list_red = peak_list_red.append(df_temp, ignore_index = True) #Append new data to list
                    
                    if green:
                        #GREEN                                   
                        peak_list.to_excel(excel_wr, sheet_name = "Output Green")
                        #global foci_value_counts
                        foci_value_counts = peak_list["Foci"].value_counts().sort_index()

                        #global df2
                        df2 = pd.DataFrame(columns = ["Count", "Foci"])
                        df2 = df2.append(foci_value_counts, ignore_index = True)
                        foci_value_counts.to_excel(excel_wr, sheet_name = "Output Green", startcol = 8)
                   
                    if red:
                        #RED                                   
                        peak_list_red.to_excel(excel_wr, sheet_name = "Output Red")
                        #global foci_value_counts_red
                        foci_value_counts_red = peak_list_red["Foci"].value_counts().sort_index()

                        #global df3
                        df3 = pd.DataFrame(columns = ["Count", "Foci"])
                        df3 = df3.append(foci_value_counts_red, ignore_index = True)
                        foci_value_counts_red.to_excel(excel_wr, sheet_name = "Output Red", startcol = 8)


                    workbook = excel_wr.book
                    bold = workbook.add_format({'bold': True})
                    if green:
                        #Green
                        worksheet = excel_wr.sheets["Output Green"]
                        
                        
                        worksheet.write("I1", "Foci/Cell", bold)
                        
                        worksheet.write("K1", "%", bold)
                        i = 0 
                        for index, value in foci_value_counts.items():
                            worksheet.write(i+1, 10, (value/peak_list.loc[:,"Cells"].sum())*100)
                            i+=1
                        worksheet.write("J1", "Count", bold)
                        worksheet.write("M2", "Ʃ Foci", bold)
                        worksheet.write("N2", peak_list.loc[:,"Foci"].sum()) 
                        
                        worksheet.write("M3", "Ʃ Cells", bold)
                        worksheet.write("N3", peak_list.loc[:, "Cells"].sum())
                        
                        worksheet.write("M4", "Mean", bold)
                        worksheet.write("N4", peak_list.loc[:,"Foci"].sum()/peak_list.loc[:, "Cells"].sum()) 
                        
                        worksheet.write("M5", "Median", bold)
                        worksheet.write("N5", peak_list["Foci"].median())
                        worksheet.write("M6", "STD", bold)
                        worksheet.write("N6", str(peak_list["Foci"].std(skipna = True)))
                        worksheet.write("M7", "Max", bold)
                        worksheet.write("N7", str(peak_list["Foci"].max()))
                        chart = workbook.add_chart({'type': 'column'})
                        
                        chart.add_series({
                                "values": ["Output Green", 1, 10, foci_value_counts.shape[0], 10],
                                "categories": ["Output Green", 1, 8, foci_value_counts.shape[0], 8],
                                "fill": {"color": "green"}
                                #"y_error_bars": {"type": "standard_deviation"},
                                
                        })
                        chart.set_y_axis({
                                "name": "Fraction",
                                "min": 0,
                                
                        })
                        chart.set_x_axis({
                                "name": "Foci/Cell"
                        })
                        worksheet.insert_chart("M8", chart)
                       
                    if red:
                        #RED
                        worksheetRed = excel_wr.sheets["Output Red"]
                        
                        
                        worksheetRed.write("I1", "Foci/Cell", bold)
                        
                        worksheetRed.write("K1", "%", bold)
                        i = 0 
                        for index, value in foci_value_counts_red.items():
                            worksheetRed.write(i+1, 10, (value/peak_list_red.loc[:,"Cells"].sum())*100)
                            i+=1
                        worksheetRed.write("J1", "Count", bold)
                        worksheetRed.write("M2", "Ʃ Foci", bold)
                        worksheetRed.write("N2", peak_list_red.loc[:,"Foci"].sum()) 
                        
                        worksheetRed.write("M3", "Ʃ Cells", bold)
                        worksheetRed.write("N3", peak_list_red.loc[:, "Cells"].sum())
                        
                        worksheetRed.write("M4", "Mean", bold)
                        worksheetRed.write("N4", peak_list_red.loc[:,"Foci"].sum()/peak_list_red.loc[:, "Cells"].sum()) 
                        
                        worksheetRed.write("M5", "Median", bold)
                        worksheetRed.write("N5", peak_list_red["Foci"].median())
                        worksheetRed.write("M6", "STD", bold)
                        worksheetRed.write("N6", str(peak_list_red["Foci"].std(skipna = True)))
                        worksheetRed.write("M7", "Max", bold)
                        worksheetRed.write("N7", str(peak_list_red["Foci"].max()))
                        chart = workbook.add_chart({'type': 'column'})
                        
                        chart.add_series({
                                "values": ["Output Red", 1, 10, foci_value_counts_red.shape[0], 10],
                                "categories": ["Output Red", 1, 8, foci_value_counts_red.shape[0], 8],
                                "fill": {"color": "red"}
                                #"y_error_bars": {"type": "standard_deviation"},
                                
                        })
                        chart.set_y_axis({
                                "name": "Fraction",
                                "min": 0,
                                
                        })
                        chart.set_x_axis({
                                "name": "Foci/Cell"
                        })
                        worksheetRed.insert_chart("M8", chart)
                        
                        #Close workbook
                    workbook.close()
                    files = []
                    filesRed = []    
                 

#scanFolders("E:/Foci/")                       