#!/usr/bin/python2.7

def savePriceBitch(my_price_table):
     filename = '{}_{}-{}-{}.csv'.format(datetime.now().date(),datetime.now().time().hour, datetime.now().time().minute, datetime.now().second)
     with open(filename, 'wb') as myfile:
         wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
         wr.writerow(my_price_table)

