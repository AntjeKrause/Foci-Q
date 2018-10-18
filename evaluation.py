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
                        global peak_list
                        peak_list = pd.DataFrame(columns=["Image/File", "Foci"]) #DF for peak list
                        for i in range(len(files)):
                            print(entry.path + "\\" + files[i])
                            
                            df = pd.read_csv(entry.path + "\\" + files[i], skiprows = 0) 
                            file_name_temp = files[i]
                            cell_count = len(df.loc[:, 'Area'])
                            peak_count = df.loc[:, 'Foci'].sum() #Number of peaks/foci in the current file or image
                            df_temp = pd.DataFrame([[file_name_temp, cell_count, peak_count]], columns=["Image/File", "Cells", "Foci"]) #Temporary data to append
                            
                            peak_list = peak_list.append(df_temp, ignore_index = True) #Append new data to list
                            

                        peak_list.to_excel(excel_wr, sheet_name = "Output")
                        global foci_value_counts
                        foci_value_counts = peak_list["Foci"].value_counts().sort_index()

                        global df2
                        df2 = pd.DataFrame(columns = ["Count", "Foci"])
                        df2 = df2.append(foci_value_counts, ignore_index = True)
                        foci_value_counts.to_excel(excel_wr, sheet_name = "Output", startcol = 8)

                        workbook = excel_wr.book
                        worksheet = excel_wr.sheets["Output"]
                        bold = workbook.add_format({'bold': True})
                        
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
                        worksheet.write("N6", peak_list["Foci"].std())
                        chart = workbook.add_chart({'type': 'column'})
                        
                        chart.add_series({
                                "values": ["Output", 1, 10, foci_value_counts.shape[0], 10],
                                "categories": ["Output", 1, 8, foci_value_counts.shape[0], 8],
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
                        #Close workbook
                        workbook.close()