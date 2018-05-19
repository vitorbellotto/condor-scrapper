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
from flyingMethods import *
from export_to_csv import *
from list_last_two_csvs import get_two_last_csvs
from compare_csvs import are_csvs_equal

# Kills all browser instances
# kill_browser_instances_bash_command = "killall firefox-esr"
# process = subprocess.Popen(kill_browser_instances_bash_command.split(), stdout=subprocess.PIPE)
# output, error = process.communicate()
#
## Creates privately navegation option
o = Options()
o.add_argument('-private')              # Assures navigation is private
#o.add_argument("--headless")            # Hides browser

# Creates browser instance
binary = FirefoxBinary('/usr/bin/firefox')                               # Gets firefox binary
driver = webdriver.Firefox(firefox_binary=binary,firefox_options=o)      # Creates driver out of binary. Uses options previously set


driver.get("https://www.condor.com/de/index.jsp")                        # Open webpage

# 
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
#PriceTable_sort = sorted(PriceTable_sort,key=lambda x: x[1])
export_to_csv(PriceTable_sort)
driver.close()

my_last_two_csvs = get_two_last_csvs()

are_my_csvs_equal = are_csvs_equal(my_last_two_csvs[0],my_last_two_csvs[1])

if are_my_csvs_equal:
    os.remove(my_last_two_csvs[1])

