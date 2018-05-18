#!/usr/bin/python2.7

import csv

def are_csvs_equal(first_csv,second_csv):
    equality = True
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
                else:
                    message = 'NOT FOUND in master list'
                    equality = False
                writer.writerow(row + [message])

    if equality:
        print('Files are equal. Last created csv is going to be deleted!')
    else:
        print('Files are different.')

    return equality

#are_csvs_equal('test.csv','test_equal.csv')
