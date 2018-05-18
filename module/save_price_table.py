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

# User-created funtions
from flyingMethods import *
from export_to_csv import *
from list_last_two_csvs import get_two_last_csvs
from compare_csvs import are_csvs_equal




# Creates privately navegation option
o = Options()
o.add_argument('-private')

# Creates browser instance
#firefox_capabilities = DesiredCapabilities.FIREFOX
#firefox_capabilities['marionette'] = True
#firefox_capabilities['binary'] = '/usr/bin/firefox'
binary = FirefoxBinary('/usr/bin/firefox')
driver = webdriver.Firefox(firefox_binary=binary,firefox_options=o)
#driver = webdriver.Firefox(executable_path='/usr/bin/firefox')

#driver = webdriver.Firefox(firefox_options=o)
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
PriceTable = get_all_flights(driver, wait_twenty)

# Clicks and returns first flight
PriceTable_sort = PriceTable
PriceTable_sort = sorted(PriceTable_sort,key=lambda x: x[1])
export_to_csv(PriceTable_sort)
driver.close()

my_last_two_csvs = get_two_last_csvs()

are_my_csvs_equal = are_csvs_equal(my_last_two_csvs[0],my_last_two_csvs[1])

if are_my_csvs_equal:
    os.remove(my_last_two_csvs[1])

