import re, requests
from bs4 import BeautifulSoup
#import urllib3
from datetime import datetime, timedelta, date
import time
import os
#from os import system, name
#import pandas as pd
import csv


# ________________________________________________________________________________ ON STARTUP
# yummy SOUPS
source = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
soup = BeautifulSoup(requests.get(source).text, 'lxml')
    
        
# ________________________________________________________________________________ ON STARTUP
# On Launch
def clear_console(): 
    if os.name == 'nt': 
        _ = os.system('cls') 
    else: 
        _ = os.system('clear')

def expected_error():
    print('Expected Input Error, please try again!')

def daterange(time_min2, time_max2):
    for n in range(int((time_max2 - time_min2).days)):
        yield time_min2 + timedelta(n+1)


list_main = [i.lower() for i in soup.text.split('\n')]
list_title = str(list_main[0]).split(',')

time_min = min(list_main)[0:10]
time_now = datetime.today().strftime('%Y-%m-%d')
time_max = max(dt for dt in list_main if dt < time_now)[0:10]


# ________________________________________________________________________________ ON STARTUP
# CSV stuffs
def load_csv():
    #global csv_title, csv_location1, csv_location2
    global location1, location2, csv_filename, csv_list
    
    cwd = os.getcwd()
    csv_filename = 'corona-scraper.csv'
    csv_path = cwd + '\\' + csv_filename
    while os.path.exists(csv_path) == False:
        print('Creating file in directory: "' + csv_path + '"')
        time.sleep(1)
        csv_list = [['#','county','state'],['1','Henrico','Virginia'],['2','Richmond city','Virginia']]
        with open((csv_filename), 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(csv_list)
            continue

    csv_list = []
    print('Retrieving file from directory: "' + csv_path + '"')
    time.sleep(1)
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        for row in file:
            csv_list.append(row.strip())
        csv_title = csv_list[0].split(',')
        csv_location1 = csv_list[1].split(',')
        csv_location2 = csv_list[2].split(',')
        
        location1_a = csv_location1[1]
        location2_a = csv_location2[1]
        location1_b = csv_location1[2]
        location2_b = csv_location2[2]

        location1 = ',' + location1_a.lower() + ',' + location1_b.lower()
        location2 = ',' + location2_a.lower() + ',' + location2_b.lower()
            

# ________________________________________________________________________________ UI DEF
# load UI
def load_ui():
    global list_time

    location1_max = time_max + location1
    location2_max = time_max + location2

    location1_all = []
    location2_all = []
    list_time = []
    time_min2 = date(int(time_min[0:4]),int(time_min[5:7]),int(time_min[8:10]))
    time_max2 = date(int(time_max[0:4]),int(time_max[5:7]),int(time_max[8:10]))
    for i in daterange(time_min2,time_max2):
        location1_all.append(i.strftime('%Y-%m-%d')+location1)
        location2_all.append(i.strftime('%Y-%m-%d')+location2)
        list_time.append(i.strftime('%Y-%m-%d'))
        
    list_max_location1 = str([i for i in list_main if i.startswith(location1_max)])[2:-2].split(',')
    list_max_location2 = str([i for i in list_main if i.startswith(location2_max)])[2:-2].split(',')

    list_all_location1 = str([i for i in list_main if i.startswith(tuple(location1_all))])[2:-2].split(',')
    list_all_location2 = str([i for i in list_main if i.startswith(tuple(location2_all))])[2:-2].split(',')


    list_title_mod = ['First Occurance','% Cases Gain Total','% Cases Gain 30-Day','% Cases Gain Prev-Day']

    # ________________________________________________________________________________
    # main UI
    print()
    if list_max_location1 == ['']:
        print(location1_a.title() + ', ' + location1_b.title())
        print('n/a'.upper())
    else:
        for item1,item2 in zip(list_title,list_max_location1):
            print(str(item1).upper() + ':', item2.title())
        print()
        print(list_title_mod[0].upper() + ':', list_all_location1[0])
    print()
    print('____________________')
    print()
    print()

    if list_max_location2 == ['']:
        print(location2_a.title() + ', ' + location2_b.title())
        print('n/a'.upper())
    else:
        for item1,item2 in zip(list_title,list_max_location2):
            print(str(item1).upper() + ':', item2.title())
        print()
        print(list_title_mod[0].upper() + ':', list_all_location2[0])
    print()
    print('____________________')
    print()
    print()
    print('Today: '.upper(), time_now, end=' | ')
    print('Latest: '.upper(), time_max)
    print()

    
# ________________________________________________________________________________ UI-2 DEF
# DEF

def command_help():
    print('"time" - Change displayed day.')
    print('"location" - Change active location1 or location2')
    print('"quit" - You can either type quit or have an error 3 times to back out.')
    print()
    return

def command_time():
    global return_process
    command_loop = 0
    while command_loop <= 3:
        command_loop += 1
        print('Change day "yyyy-mm-dd":',end=' ')
        command_time = input()
        if command_time in list_time:
            global time_max
            return_process = True
            time_max = command_time
            return
        elif command_time == 'quit':
            return_process = False
            break
        else:
            expected_error()

def rewrite_csv(x):
    with open((csv_filename), 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(x)

def command_location():
    global return_process, rewrite_location2_a, rewrite_location2_b, csv_list
    command_loop = 0
    while command_loop <= 3:
        command_loop += 1
        print('Input location number [1-10]:', end=' ')
        command_location = input()
        if command_location == '1':
            print('Please input the County or City name:', end=' ')
            location1_a = input()
            print('Please input the State or Region name:', end=' ')
            location1_b = input()
            location1 = ',' + location1_a.lower() + ',' + location1_b.lower()
            command_location_temp = str([i for i in list_main if i.startswith(time_max + location1)])[2:-2]
            command_location_find = command_location_temp in list_main
            if command_location_find == True:
                csv_list = [csv_list[0].split(','),str(csv_list[1][0] + location1).split(','),csv_list[2].split(',')]
                rewrite_csv(csv_list)
                load_csv()
                return_process = True
                return
            else:
                expected_error()
                continue
        elif command_location == '2':
            print('Please input the County or City name:', end=' ')
            location2_a = input()
            print('Please input the State or Region name:', end=' ')
            location2_b = input()
            location2 = ',' + location2_a.lower() + ',' + location2_b.lower()
            command_location_temp = str([i for i in list_main if i.startswith(time_max + location2)])[2:-2]
            command_location_find = command_location_temp in list_main
            if command_location_find == True:
                csv_list = [csv_list[0].split(','),csv_list[1].split(','),str(csv_list[2][0] + location2).split(',')]
                rewrite_csv(csv_list)
                load_csv()
                return_process = True
                return
            else:
                expected_error()
                continue
        elif command_location == 'quit':
            return_process = False
            break
        else:
            expected_error()

def command_print():
    print('Please input debug print statement:',end=' ')
    command_print = eval(input())
    print(command_print)
            
def command_prompt():
    global quit_process
    command_loop = 1
    while command_loop == 1:
        print('>',end=' ')
        command_prompt = input()
        if command_prompt == 'help':
            command_help()
        elif command_prompt == 'time':
            command_time()
            if return_process == True:
                command_loop = 0
            else:
                continue
        elif command_prompt == 'location':
            command_location()
            if return_process == True:
                command_loop = 0
            else:
                continue
        elif command_prompt == 'print':
            command_print()
            continue
        elif command_prompt == 'quit':
            quit_process = True
            return
        else:
            continue

def ui_master():
    load_csv()
    ui_loop = 1
    while ui_loop == 1:
        clear_console()
        load_ui()
        command_prompt()
        if quit_process == True:
            ui_loop = 0
            break
        else:
            continue

# ________________________________________________________________________________ UI LOOP
# load UI loop
return_process = False
quit_process = False
ui_master()
