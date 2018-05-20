#!/usr/bin/python2.7

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import pdb
from datetime import date, timedelta
import time
from regular_expression import *
import re
import os
import subprocess

# User-created funtions
'Documatition '
from export_to_csv import *
from list_last_two_csvs import get_two_last_csvs
from compare_csvs import are_csvs_equal

class Condor:
    '''
    Cool thing
    '''
    def __init__(self,departure_airport,arrival_airport):
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        

    def select_airport(self,driver, airport_id, airport_abrev, wait_for_element = 100, wait_to_enter = 1):   
        inputOriginAirport = WebDriverWait(driver, wait_for_element).until(EC.element_to_be_clickable((By.ID, airport_id)))
        inputOriginAirport.send_keys(airport_abrev)
        time.sleep(wait_to_enter)
        inputOriginAirport.send_keys(Keys.ENTER)

    def get_dates_and_prices(self,driver,wait):
        CalMonth = list()
        PriceTable = list()
        months_german = ['Januar','Februar', u'M\xe4rz','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
        # Waits for table with prices to load and returns element
        monthHasPrice = True
        one_price_in_the_analysed_month_found = True
        while ( monthHasPrice or one_price_in_the_analysed_month_found):
            monthHasPrice = False
            one_price_in_the_analysed_month_found = False
            time.sleep(1)
            cal_month = driver.find_element_by_class_name('ng-binding')
            str_title_cal = re.split('\s',cal_month.text,re.UNICODE)
            month = str_title_cal[0]
            the_year = str_title_cal[1]
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
                            one_price_in_the_analysed_month_found = True
                            time.sleep(1)
                            temp_date = get_date_price_second(the_year,buttons)
                            print(temp_date[0].month)
                            print(cal_month_index)
                            if temp_date[0].month == cal_month_index:
                                PriceTable.append([temp_date[0].isoformat(),temp_date[1]])
                                monthHasPrice = True
            next_month = driver.find_element_by_class_name('icon-next')
            next_month.click()
            time.sleep(1.5)
        return PriceTable
    
    def get_flights(self, boolean_headless = True):
        o = Options()
        o.add_argument('-private')              # Assures navigation is private
        if boolean_headless:
            o.add_argument("--headless")            # Hides browser
        # Creates browser instance
        binary = FirefoxBinary('/usr/bin/firefox')                               # Gets firefox binary
        driver = webdriver.Firefox(firefox_binary=binary,firefox_options=o)      # Creates driver out of binary. Uses options previously set

        driver.get("https://www.condor.com/de/index.jsp")                        # Opens webpage

        origin_airport_elem = driver.find_element_by_id('searchAirportOrigin').click()

        # Inserts choosen origin airport
        self.select_airport(driver,"airportinput_id_origin", self.departure_airport)

        # Inserts choosen destination airport
        self.select_airport(driver,"airportinput_id_destination", self.arrival_airport)

        stopmethod_button = driver.find_element_by_xpath('/html/body/tca-modal-content-wrapper/div[3]/div/div[2]/modal-pages/tca-modal-content-page[3]' 
                                                        '/div/div/div/div/date-select/div/div/fieldset/div/label[2]/span')
        wait_twenty = WebDriverWait(driver, 20)
        wait_twenty.until(EC.visibility_of(stopmethod_button))
        stopmethod_button.click()

        # Waits for table with prices to load and returns element
        price_table = self.get_dates_and_prices(driver, wait_twenty)
        price_table_sorted = sorted(price_table,key=lambda x: x[1])
        driver.close()
        return price_table, price_table_sorted 


#from compare_csvs import are_csvs_equal
#
#class Condor:
#    '''
#    Cool thing
#    '''
#    def __init__(self,departure_airport,arrival_airport):
#        self.departure_airport = departure_airport
#        self.arrival_airport = arrival_airport
#        
#
#    def select_airport(self,driver, airport_id, airport_abrev, wait_for_element = 100, wait_to_enter = 1):   
#        inputOriginAirport = WebDriverWait(driver, wait_for_element).until(EC.element_to_be_clickable((By.ID, airport_id)))
#        inputOriginAirport.send_keys(airport_abrev)
#        time.sleep(wait_to_enter)
#        inputOriginAirport.send_keys(Keys.ENTER)
#
#    def get_dates_and_prices(self,driver,wait):
#        CalMonth = list()
#        PriceTable = list()
#        months_german = ['Januar','Februar', u'M\xe4rz','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
#        # Waits for table with prices to load and returns element
#        monthHasPrice = True
#        one_price_in_the_analysed_month_found = True
#        while ( monthHasPrice or one_price_in_the_analysed_month_found):
#            monthHasPrice = False
#            one_price_in_the_analysed_month_found = False
#            time.sleep(1)
#            cal_month = driver.find_element_by_class_name('ng-binding')
#            str_title_cal = re.split('\s',cal_month.text,re.UNICODE)
#            month = str_title_cal[0]
#            the_year = str_title_cal[1]
#            CalMonth.append(cal_month)
#            cal_month_index = months_german.index(month)+1
#            time.sleep(1.5)
#            cal = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'uib-daypicker')))
#            wait.until(EC.visibility_of(cal))
#            time.sleep(1.5)
#            # Gets all rows in the table
#            rows = cal.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
#            for row in rows:
#                # Gets all columns
#                cols = row.find_elements(By.TAG_NAME, "td") #note: index start from 0, 1 is col 2
#                # Selects only non-empty
#                if (cols != []):            
#                    for col in cols:
#                        buttons = col.find_elements_by_tag_name("button")
#                        if 'Nicht' not in buttons[0].get_attribute("aria-label"):
#                            one_price_in_the_analysed_month_found = True
#                            time.sleep(1)
#                            temp_date = get_date_price_second(the_year,buttons)
#                            print(temp_date[0].month)
#                            print(cal_month_index)
#                            if temp_date[0].month == cal_month_index:
#                                PriceTable.append([temp_date[0].isoformat(),temp_date[1]])
#                                monthHasPrice = True
#            next_month = driver.find_element_by_class_name('icon-next')
#            next_month.click()
#            time.sleep(1.5)
#        return PriceTable
#    
#    def get_flights(self, boolean_headless = True):
#        o = Options()
#        o.add_argument('-private')              # Assures navigation is private
#        if boolean_headless:
#            o.add_argument("--headless")            # Hides browser
#        # Creates browser instance
#        binary = FirefoxBinary('/usr/bin/firefox')                               # Gets firefox binary
#        driver = webdriver.Firefox(firefox_binary=binary,firefox_options=o)      # Creates driver out of binary. Uses options previously set
#
#        driver.get("https://www.condor.com/de/index.jsp")                        # Opens webpage
#
#        origin_airport_elem = driver.find_element_by_id('searchAirportOrigin').click()
#
#        # Inserts choosen origin airport
#        self.select_airport(driver,"airportinput_id_origin", self.departure_airport)
#
#        # Inserts choosen destination airport
#        self.select_airport(driver,"airportinput_id_destination", self.arrival_airport)
#
#        stopmethod_button = driver.find_element_by_xpath('/html/body/tca-modal-content-wrapper/div[3]/div/div[2]/modal-pages/tca-modal-content-page[3]' 
#                                                        '/div/div/div/div/date-select/div/div/fieldset/div/label[2]/span')
#        wait_twenty = WebDriverWait(driver, 20)
#        wait_twenty.until(EC.visibility_of(stopmethod_button))
#        stopmethod_button.click()
#
#        # Waits for table with prices to load and returns element
#        price_table = self.get_dates_and_prices(driver, wait_twenty)
#        price_table_sorted = sorted(price_table,key=lambda x: x[1])
#        driver.close()
#        return price_table, price_table_sorted 
#
