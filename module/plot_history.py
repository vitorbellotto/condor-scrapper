#!/usr/bin/python2.7

import os
import glob
import re
import csv
import pdb
import matplotlib.pyplot as plt
from datetime import *
from pprint import pprint

def get_list_csvs():
    path = os.getcwd()
    os.chdir(path)
    result = [i for i in glob.glob('{}/../data/*-*-*_*-*-*.csv'.format(path))]
    return result

def find_flight_date(l, elem):
    for row, i in enumerate(l):
        try:
            column = i.index(elem)
        except ValueError:
            continue
        return row
    return -1

def column_of_matrix(matrix, i):
        return [row[i] for row in matrix]

def extract_data_days_passed(number_of_days):
    timespan = timedelta(days=1)
    initial_time_point = datetime.now()-timespan
    return initial_time_point

def get_elapsed_time2fly(flight_date_searched):
    pass

def plot_flight_history_price(flight_date_searched):
    date_regular_expression = '2\d\d\d-\d\d-\d\d_\d\d?-\d\d?-\d\d?'
    results = get_list_csvs()
    dates_import = [[[] for i in range(2)] for i in range(len(results))]
    i_csv_path = 0
    for csv_path in results:
        m = re.search(date_regular_expression, csv_path)
        dates_import[i_csv_path][0] = m.group(0)
        with open(csv_path,'rb') as csv_file:
            reader = csv.reader(csv_file)
            csv_file_list = list(reader)
        column = find_flight_date(csv_file_list,flight_date_searched)
        dates_import[i_csv_path][1] = float(csv_file_list[column][1])
        i_csv_path = i_csv_path + 1
    
    #print(dates_import)
    dates_import_unsorted = dates_import
    dates_array = column_of_matrix(dates_import,0)
    dates_import_sorted = sorted(dates_import_unsorted,key=lambda x: x[0])
    dates = column_of_matrix(dates_import_sorted,0)
    dates_format_datetime = [datetime.strptime(flight_date_searched,"%Y-%m-%d") - datetime.strptime(single_date,"%Y-%m-%d_%H-%M-%S") for single_date in dates] 
    dates_format_timedelta_days = [single_timedelta.days for single_timedelta in dates_format_datetime]
    #pdb.set_trace()
    #print(dates_import_sorted)
    #pdb.set_trace()
    prices = column_of_matrix(dates_import_sorted,1)
    #extract_data_days_passed(1)
    #print(dates)
    #plt.plot(dates,prices)
    #plt.plot(range(len(prices)),prices)
    plt.plot(dates_format_timedelta_days,prices, marker='x')
    plt.ylabel('Price [Euros]')
    plt.title('Price history for Condor Flight {} GRU->FRA'.format(flight_date_searched))
    plt.gca().invert_xaxis()
    plt.show()


flight_date_searched = '2018-10-05' 
plot_flight_history_price(flight_date_searched)


