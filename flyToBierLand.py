#!/usr/bin/python2.7

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pdb
import time
from regular_expression import *
from datetime import date, timedelta
import re


def select_airport(airport_id, airport_abrev, wait_for_element = 20, wait_to_enter = 1):   
    inputOriginAirport = WebDriverWait(driver, wait_for_element).until(EC.element_to_be_clickable((By.ID, airport_id)))
    inputOriginAirport.send_keys(airport_abrev)
    time.sleep(wait_to_enter)
    inputOriginAirport.send_keys(Keys.ENTER)

def get_all_flights(calender_id):
    pass


def get_flight_data(calendar_id):
    lim_flights = 3
    stop = 0
    FlightDataPrice = []
    time.sleep(1.5)
##    WebDriverWait(driver, 10).until(EC.visibility_of((By.CLASS_NAME, 'btn btn-default btn-sm dayOfWeek')))
    rows = calendar_id.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
    for row in rows:
        # Get the columns (all the column 2)
        cols = row.find_elements(By.TAG_NAME, "td") #note: index start from 0, 1 is col 2
        if (cols != []):            
            for col in cols:
##                print(col)                
                buttons = col.find_elements_by_tag_name("button")
##                print(buttons)
##                print(buttons[0])
##                pdb.set_trace()
                if 'Nicht' not in buttons[0].get_attribute("aria-label"):
                    time.sleep(1)
                    stop = stop + 1
                    break
        if lim_flights == stop:
            FlightDataPrice = get_date_price(buttons[0])
            buttons[0].click()
            break
    return FlightDataPrice



# Creates browser instance
driver = webdriver.Firefox()
driver.set_preference("browser.privatebrowsing.autostart", True)
driver.get("https://www.condor.com/de/index.jsp")

origin_airport_elem = driver.find_element_by_id('searchAirportOrigin').click()

# Inserts choosen origin airport
select_airport("airportinput_id_origin", 'GRU')

# Inserts choosen destination airport
select_airport("airportinput_id_destination", 'FRA')

# Waits for table with prices to load and returns element
table_id = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'uib-daypicker')))

# Clicks and returns first flight
FlightDataDeparture= get_flight_data(table_id)

pdb.set_trace()
directflight_button = driver.find_element_by_id('btngroup_oneway').click()
time.sleep(1)
continue_button = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/tca-modal-content-wrapper/div[3]/div/div[2]/modal-pages/tca-modal-content-page[4]/div/div/div/div/passenger-select/div/div/div/div/a')))
continue_button.click()

search_button = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'search')))
search_button.click()


driver.close()


