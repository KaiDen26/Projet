# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 19:30:39 2022

@author: 33642
"""

#!/usr/bin/python3
#-*-coding:utf-8-*-

data_file_name = '2_Piscine-Patinoire_Campus.txt'

try:
    with open(data_file_name, 'r') as f:
        content = f.read()
except OSError:
    # 'File not found' error message.
    print("File not found")

def dates2dic(dates):
    dic = {}
    splitted_dates = dates.split("\n")
    #print(splitted_dates)
    for stop_dates in splitted_dates:
        tmp = stop_dates.split(" ")
        dic[tmp[0]] = tmp[1:]
    return dic

def getListOfStop(liste):
    return list(liste.keys())

def getListOfHours(liste, arret):
    
    return list(liste.get(arret))     

splited_content = content.split("\n\n")
#regular_path = slited_content[0]
regular_date_go2 = dates2dic(splited_content[1])
regular_date_back2 = dates2dic(splited_content[2])
#we_holidays_path = slited_content[3]
#we_holidays_date_go = dates2dic(slited_content[4])
#we_holidays_date_back = dates2dic(slited_content[5])



