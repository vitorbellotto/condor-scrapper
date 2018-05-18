#!/usr/bin/python2.7

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pdb
import time
from regular_expression import *
from datetime import datetime, date, timedelta
import csv
import re


def select_airport(driver, airport_id, airport_abrev, wait_for_element = 20, wait_to_enter = 1):   
    inputOriginAirport = WebDriverWait(driver, wait_for_element).until(EC.element_to_be_clickable((By.ID, airport_id)))
    inputOriginAirport.send_keys(airport_abrev)
    time.sleep(wait_to_enter)
    inputOriginAirport.send_keys(Keys.ENTER)

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

def savePriceTableToCSV(my_price_table):
    filename = '{}_{}-{}-{}.csv'.format(datetime.now().date(),datetime.now().time().hour, datetime.now().time().minute, datetime.now().second)
    with open(filename, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(my_price_table)
