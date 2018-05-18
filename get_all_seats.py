#!/usr/bin/python2.7

from selenium import webdriver
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
from flyingMethods_support import * 
from selenium.webdriver.firefox.options import Options
from export_to_csv import *
from list_last_two_csvs import get_two_last_csvs
from compare_csvs import are_csvs_equal
import os

def select_airport(driver, airport_id, airport_abrev, wait_for_element = 100, wait_to_enter = 1):   
    inputOriginAirport = WebDriverWait(driver, wait_for_element).until(EC.element_to_be_clickable((By.ID, airport_id)))
    inputOriginAirport.send_keys(airport_abrev)
    time.sleep(wait_to_enter)
    inputOriginAirport.send_keys(Keys.ENTER)

def get_seats(year,month,day):
    # Creates privately navegation option
    o = Options()
    o.add_argument('-private')

    # Creates browser instance
    driver = webdriver.Firefox(firefox_options=o)
    #driver.set_preference("browser.privatebrowsing.autostart", True)
    driver.get("https://www.condor.com/de/index.jsp")

    origin_airport_elem = driver.find_element_by_id('searchAirportOrigin').click()

    # Inserts choosen origin airport
    select_airport(driver,"airportinput_id_origin", 'GRU')

    # Inserts choosen destination airport
    select_airport(driver,"airportinput_id_destination", 'FRA')

    # Chooses stop method
    stopmethod_button = driver.find_element_by_xpath('/html/body/tca-modal-content-wrapper/div[3]/div/div[2]/modal-pages/tca-modal-content-page[3]/div/div/div/div/date-select/div/div/fieldset/div/label[2]/span')
    wait_twenty = WebDriverWait(driver, 20) 
    wait_twenty.until(EC.visibility_of(stopmethod_button))
    stopmethod_button.click()

    # Waits for table with prices to load and returns element
    #time.sleep(1)
    #cal = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'uib-daypicker')))
    ##calender = driver.find_element_by_class_name('uib-daypicker')
    #wait_twenty.until(EC.visibility_of(cal))
    ##table_id = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'uib-daypicker')))
    number_of_seats, occupation_rate = get_flight_seats(driver, wait_twenty, date(year,month,day))
    ## Clicks and returns first flight
    driver.close()
    return number_of_seats, occupation_rate
    #PriceTable_sort = PriceTable
    #PriceTable_sort = sorted(PriceTable_sort,key=lambda x: x[1])
    #export_to_csv(PriceTable_sort)
    #driver.close()
    #
    #my_last_two_csvs = get_two_last_csvs()
    #
    #are_my_csvs_equal = are_csvs_equal(my_last_two_csvs[0],my_last_two_csvs[1])
    #
    #if are_my_csvs_equal:
    #    os.remove(my_last_two_csvs[1])

