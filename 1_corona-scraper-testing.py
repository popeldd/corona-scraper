import re, requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import time
import os
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

def daterange(daterange_min, daterange_max):
    for n in range(int((daterange_max - daterange_min).days+1)):
        yield daterange_min + timedelta(n)


list_main = [i.lower() for i in soup.text.split('\n')]
list_title = str(list_main[0]).split(',')
list_title_mod = ['First Occurance','% Cases Gain Total','% Cases Gain 30-Day','% Cases Gain Prev-Day']

time_min = min(list_main)[0:10]
time_now = datetime.today().strftime('%Y-%m-%d')
time_max = max(dt for dt in list_main if dt <= time_now)[0:10]


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
        csv_row_count = 0
        for row in file:
            csv_row_count += 1
            csv_list.append(row.strip())

        """
        csv_location1 = csv_list[1].split(',')
        
        location1_a = csv_location1[1]
        location1_b = csv_location1[2]

        location1 = ',' + location1_a.lower() + ',' + location1_b.lower()
        """
        # improved for expandability
        csv_title = csv_list[0].split(',')
        for row in range(csv_row_count):
            locals()['csv_location' + str(row)] = csv_list[row].split(',')
            globals()['location' + str(row)] = ',' + locals()['csv_location' + str(row)][1].lower() + ',' + locals()['csv_location' + str(row)][2].lower()


# ________________________________________________________________________________ UI DEF
# load UI
def load_ui_master():
    global list_time, daterange_min, daterange_max

    list_time = []
    daterange_min = date(int(time_min[:4]),int(time_min[5:7]),int(time_min[8:10]))
    daterange_max = date(int(time_max[:4]),int(time_max[5:7]),int(time_max[8:10]))
    for i in daterange(daterange_min,daterange_max):
        list_time.append(i.strftime('%Y-%m-%d'))
    
def load_ui(loc_num):
    globals()['location' + str(loc_num) + '_max'] = time_max + globals()[str('location') + str(loc_num)]

    globals()['location' + str(loc_num) + '_all'] = []
    for i in daterange(daterange_min,daterange_max):
        globals()['location' + str(loc_num) + '_all'].append(i.strftime('%Y-%m-%d')+globals()[str('location') + str(loc_num)])
        
    locals()['list_max_location' + str(loc_num)] = str([i for i in list_main if i.startswith(globals()['location' + str(loc_num) + '_max'])])[2:-2].split(',')

    locals()['list_all_location' + str(loc_num)] = str([i for i in list_main if i.startswith(tuple(globals()['location' + str(loc_num) + '_all']))])[2:-2].split(',')

    # ________________________________________________________________________________
    # main UI
    if locals()['list_max_location' + str(loc_num)] == ['']:
        print(globals()[str('location') + str(loc_num)][1:].title())
        print('n/a'.upper())
    else:
        for item1,item2 in zip(list_title,locals()['list_max_location' + str(loc_num)]):
            print(str(item1).upper() + ':', item2.title())
        print()
        print(list_title_mod[0].upper() + ':', locals()['list_all_location' + str(loc_num)][0])
    print()
    print('____________________')
    print()
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
    global return_process, time_max
    command_loop = 0
    while command_loop <= 3:
        command_loop += 1
        print('Change day "yyyy-mm-dd":',end=' ')
        command_time = input()
        if command_time == 'help':
            print('"yyyy-mm-dd" - Exact display day')
            print('"min" - First occurence')
            print('"max" - Display most recent')
            print()
        elif command_time in list_time:
            return_process = True
            time_max = command_time
            return
        elif command_time == 'min':
            return_process = True
            time_max = min(list_time)
            return
        elif command_time == 'max':
            return_process = True
            time_max = max(list_time)
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
    global return_process, csv_list
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
    load_ui_master()
    ui_loop = 1
    while ui_loop == 1:
        clear_console()
        print()
        load_ui(1)
        load_ui(2)
        print('Today: '.upper(), time_now, end=' | ')
        print('Latest: '.upper(), time_max)
        print()
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
