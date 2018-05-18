#!/usr/bin/python2.7

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pdb
from regular_expression import *
from datetime import datetime, date, timedelta
import csv
import re
import time
from get_all_seats import *
from flyingMethods_support_twice import *


#def get_flight_data(calendar_id):
#    lim_flights = 3
#    stop = 0
#    FlightDataPrice = []
#    time.sleep(1.5)
###    WebDriverWait(driver, 10).until(EC.visibility_of((By.CLASS_NAME, 'btn btn-default btn-sm dayOfWeek')))
#    rows = calendar_id.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
#    for row in rows:
#        # Get the columns (all the column 2)
#        cols = row.find_elements(By.TAG_NAME, "td") #note: index start from 0, 1 is col 2
#        if (cols != []):            
#            for col in cols:
###                print(col)                
#                buttons = col.find_elements_by_tag_name("button")
###                print(buttons)
###                print(buttons[0])
###                pdb.set_trace()
#                if 'Nicht' not in buttons[0].get_attribute("aria-label"):
#                    time.sleep(1)
#                    stop = stop + 1
#                    break
#    if lim_flights == stop:
#        FlightDataPrice = get_date_price(buttons[0])
#        buttons[0].click()
#        break
#return FlightDataPrice

def get_all_flights_and_seats(driver,wait):
    CalMonth = list()
    PriceTable = list()
    months_german = ['Januar','Februar', u'M\xe4rz','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
    # Waits for table with prices to load and returns element
    monthHasPrice = True
    while monthHasPrice:
        monthHasPrice = False
        time.sleep(1)
        cal_month = driver.find_element_by_class_name('ng-binding')
        str_title_cal = re.split('\s',cal_month.text,re.UNICODE)
        month = str_title_cal[0]
        CalMonth.append(cal_month)
        cal_month_index = months_german.index(month)+1
        time.sleep(1.5)
        cal = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'uib-daypicker')))
        wait.until(EC.visibility_of(cal))
        time.sleep(1.5)
        # Gets all rows in the table
        rows = cal.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
        for row in rows:
            # Gets all columns
            cols = row.find_elements(By.TAG_NAME, "td") #note: index start from 0, 1 is col 2
            # Selects only non-empty
            if (cols != []):            
                for col in cols:
                    buttons = col.find_elements_by_tag_name("button")
                    if 'Nicht' not in buttons[0].get_attribute("aria-label"):
                        time.sleep(1)
                        temp_date = get_date_price_second(buttons)
                        print(temp_date[0].month)
                        print(cal_month_index)
                        if temp_date[0].month == cal_month_index:
                            PriceTable.append([temp_date[0].isoformat(),temp_date[1]])
                            monthHasPrice = True
                            number_of_seats, occupation_rate = get_seats(temp_date[0].year,temp_date[0].month,temp_date[0].day)
                            print('Number of seats: {}'.format(number_of_seats))
                            print('Occupation rate: {}'.format(occupation_rate))
        next_month = driver.find_element_by_class_name('icon-next')
        next_month.click()
        time.sleep(1.5)
    return PriceTable

def get_all_flights(driver,wait):
    CalMonth = list()
    PriceTable = list()
    months_german = ['Januar','Februar', u'M\xe4rz','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
    # Waits for table with prices to load and returns element
    monthHasPrice = True
    while monthHasPrice:
        monthHasPrice = False
        time.sleep(1)
        cal_month = driver.find_element_by_class_name('ng-binding')
        str_title_cal = re.split('\s',cal_month.text,re.UNICODE)
        month = str_title_cal[0]
        CalMonth.append(cal_month)
        cal_month_index = months_german.index(month)+1
        time.sleep(1.5)
        cal = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'uib-daypicker')))
        wait.until(EC.visibility_of(cal))
        time.sleep(1.5)
        # Gets all rows in the table
        rows = cal.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
        for row in rows:
            # Gets all columns
            cols = row.find_elements(By.TAG_NAME, "td") #note: index start from 0, 1 is col 2
            # Selects only non-empty
            if (cols != []):            
                for col in cols:
                    buttons = col.find_elements_by_tag_name("button")
                    if 'Nicht' not in buttons[0].get_attribute("aria-label"):
                        time.sleep(1)
                        temp_date = get_date_price_second(buttons)
                        print(temp_date[0].month)
                        print(cal_month_index)
                        if temp_date[0].month == cal_month_index:
                            PriceTable.append([temp_date[0].isoformat(),temp_date[1]])
                            monthHasPrice = True
        next_month = driver.find_element_by_class_name('icon-next')
        next_month.click()
        time.sleep(1.5)
    return PriceTable

def get_number_of_seats(driver,buttons):
    buttons[0].click()
    button_continue = WebDriverWait(driver,100).until(EC.element_to_be_clickable((By.XPATH,'/html/body/tca-modal-content-wrapper/div[3]/div/div[2]/modal-pages/tca-modal-content-page[4]/div/div/div/div/passenger-select/div/div/div/div/a')))
    button_continue.click()
    button_search = driver.find_element_by_id('search')
    button_search.click()
    button_flight = WebDriverWait(driver,100).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/div/div/div/div/div[2]/div[1]/div/div[2]/div[1]/div/div[1]/vacancy-segment-wrapper/div/div[4]/div/vacancy-flight/div/ul/li[1]/a[2]/div/div[2]/div')))
    button_flight.click()
    continue_again_button = WebDriverWait(driver,100).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/div/div/div/div/div[2]/div[1]/div/div[2]/div[1]/div/div[3]/div/div/div[2]/a')))
    continue_again_button.click()
    button_continue_ignore_storn = WebDriverWait(driver,100).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/div/div/div/div/div[3]/div[1]/div/div/div[4]/div/a')))
    button_continue_ignore_storn.click()
    field_seat_reservation = WebDriverWait(driver,100).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/div/div/div/div/div[4]/div[1]/div/div/div/div/div[2]/div/tca-teaser/div/div[2]/div/a')))
    field_seat_reservation.click()
    open_view_seats = WebDriverWait(driver,100).until(EC.element_to_be_clickable((By.CLASS_NAME,'list-item__subtitle')))
    open_view_seats.click()
    table_seats = WebDriverWait(driver,100).until(EC.element_to_be_clickable((By.XPATH,'/html/body/tca-modal-content-wrapper/div[3]/div/div[2]/modal-pages/tca-modal-content-page[2]/div/div/div/div/tca-seat-map/div[2]/div[3]/table')))
    #rows_seats = table_seats.find_elements(By.TAG_NAME, "tr")
    seats = table_seats.find_elements(By.CLASS_NAME,'seat-v2')
    seats_occupied = table_seats.find_elements(By.CLASS_NAME,'seat-v2--taken')
    number_of_seats = len(seats)
    number_of_seats_occupied = len(seats_occupied)
    occupation_ratio = ( float(number_of_seats_occupied) * 100 )/number_of_seats
    return number_of_seats, occupation_ratio

def get_flight_seats(driver, wait, my_flight_date):
    number_of_seats = 0
    occupation_ratio = 0
    CalMonth = list()
    PriceTable = list()
    months_german = ['Januar','Februar', u'M\xe4rz','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
    # Waits for table with prices to load and returns element
    monthHasPrice = True
    while monthHasPrice:
        monthHasPrice = False
        found_flight_date = False
        time.sleep(1)
        cal_month = driver.find_element_by_class_name('ng-binding')
        str_title_cal = re.split('\s',cal_month.text,re.UNICODE)
        month = str_title_cal[0]
        CalMonth.append(cal_month)
        cal_month_index = months_german.index(month)+1
        time.sleep(1.5)
        cal = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'uib-daypicker')))
        wait.until(EC.visibility_of(cal))
        time.sleep(1.5)
        # Gets all rows in the table
        rows = cal.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
        for row in rows:
            if found_flight_date:
                break
            # Gets all columns
            cols = row.find_elements(By.TAG_NAME, "td") #note: index start from 0, 1 is col 2
            # Selects only non-empty
            if (cols != []):            
                for col in cols:
                    buttons = col.find_elements_by_tag_name("button")
                    if 'Nicht' not in buttons[0].get_attribute("aria-label"):
                        time.sleep(1)
                        temp_date = get_date_price_second(buttons)
                        print(temp_date[0].month)
                        print(cal_month_index)
                        if temp_date[0].month == cal_month_index:
                            PriceTable.append([temp_date[0].isoformat(),temp_date[1]])
                            monthHasPrice = True
                            if PriceTable[-1][0] == my_flight_date.isoformat():
                                found_flight_date = True 
                                number_of_seats, occupation_ratio = get_number_of_seats(driver,buttons)
                                break
        if not found_flight_date:
            next_month = driver.find_element_by_class_name('icon-next')
            next_month.click()
            time.sleep(1.5)
        else:
            break
    return number_of_seats, occupation_ratio

def savePriceTableToCSV(my_price_table):
    filename = '{}_{}-{}-{}.csv'.format(datetime.now().date(),datetime.now().time().hour, datetime.now().time().minute, datetime.now().second)
    with open(filename, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(my_price_table)







