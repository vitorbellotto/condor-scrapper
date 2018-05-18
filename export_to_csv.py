#!/usr/bin/python2.7

#from datetime import *
from datetime import datetime, date, timedelta
import csv
from csv import *
import pdb
import os

#print(my_prices_table)
# pdb.set_trace()
#filename = '{}_{}-{}-{}.csv'.format(datetime.now().date(),datetime.now().time().hour, datetime.now().time().minute, datetime.now().second)
#filename = 'test.csv'.format(datetime.now().date(),datetime.now().time().hour, datetime.now().time().minute, datetime.now().second)
def export_to_csv(my_prices_table):
    #filename = '{}_{}-{}-{}.csv'.format(datetime.now().date(),datetime.now().time().hour, datetime.now().time().minute, datetime.now().second)
    cwd = os.getcwd()
    filename = '{}/condor/data/{}.csv'.format(cwd,datetime.now().__format__('%Y-%m-%d_%H-%M-%S'))
    with open(filename, 'w') as myfile:
        wr = csv.writer(myfile, lineterminator = '\n' )
        for val in my_prices_table:
            wr.writerow(val)
    myfile.close()
#    wr.writerow(my_prices_table)

