#!/usr/bin/python2.7

import csv
from datetime import datetime, date, timedelta
import os
import glob

def get_two_last_csvs():
    path = os.getcwd()
    os.chdir(path)
    result = [i for i in glob.glob('{}/condor/data/*-*-*_*-*-*.csv'.format(path))]
    return [result[-2],result[-1]]

def export_csv(my_prices_table):
    filename = datetime.now().__format__('%Y-%m-%d_%H-%M-%S')
    my_price_table_s = sorted(my_price_table,key=lambda x: x[1])
    cwd = os.getcwd()
    filepath = '{}/../data/{}.csv'.format(cwd,filename)
    filepath_s = '{}/../data/{}_s.csv'.format(cwd,filename)
    with open(filepath, 'w') as myfile:
        wr = csv.writer(myfile, lineterminator = '\n' )
        for val in my_prices_table:
            wr.writerow(val)
    myfile.close()
    with open(filepath_s, 'w') as myfilesorted:
        wr = csv.writer(myfilesorted, lineterminator = '\n' )
        for val in my_prices_table:
            wr.writerow(val)
    myfilesorted.close()

def are_csvs_equal(first_csv,second_csv):
    with open(first_csv, 'rb') as master:
        master_indices = dict((r[1], i) for i, r in enumerate(csv.reader(master)))
    with open(second_csv, 'rb') as hosts:
        with open('results.csv', 'wb') as results:    
            reader = csv.reader(hosts)
            writer = csv.writer(results)
            writer.writerow(next(reader, []) + ['RESULTS'])
            for row in reader:
                index = master_indices.get(row[1])
                if index is not None:
                    message = 'FOUND in master list (row {})'.format(index)
                    equality = True
                else:
                    message = 'NOT FOUND in master list'
                    equality = False
                writer.writerow(row + [message])
    if equality:
        print('Files are equal. Last created csv is going to be deleted!')
    else:
        print('Files are different.')
    return equality

