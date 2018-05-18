# -*- coding: U8 -*-
import re
from datetime import date,datetime
import pdb

class AvailableFlightData:
    def __init__(self,date,price):
        self.d = date
        self.p = price
        
def get_date_price(buttons):
    message = buttons[0].get_attribute("aria-label")    
    obj_re = re.split('\s',message,re.UNICODE)
    day = int(obj_re[0])
    month = obj_re[1]
    price = obj_re[4].replace(",",".")
    print('The day is {}\nThe month is {}.\nPrice flight: {}'.format(day,month,price))

    months_german = ['Januar','Februar', 'März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']

    index_month = months_german.index(month)+1

    flightdepartdate = date(2018,index_month,day)
    MyFlight = AvailableFlightData(flightdepartdate,price)
    return MyFlight

def get_date_price_second(the_year,buttons):
    try:
        message = buttons[0].get_attribute("aria-label")    
        obj_re = re.split('\s',message,re.UNICODE)
        day = int(obj_re[0])
        month = obj_re[1]
        price = obj_re[4].replace(".","")
        price = price.replace(",",".")
        print(u'The day is {}\nThe month is {}.\nPrice flight: {}'.format(day,month,price))
        months_german = ['Januar','Februar', u'M\xe4rz','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
        index_month = months_german.index(month)+1
        flightdepartdate = date(int(the_year),index_month,day)
    except Exception:
        flightdepartdate = date(2018,1,1)
        price = 0

    return [ flightdepartdate, float(price) ] 


##class AvailableFlightData:
##    months_german = ['Januar','Februar', 'März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
##    
##    def __init__(self,tag_string):
##        self.date= self.get_date(tag_string)
##        self.p = self.get_price(tag_string)
##
##    def get_date(message):
##        obj_re = re.split('\s',message,re.UNICODE)
##        day = int(obj_re[0])
##        month = months_german.index(obj_re[1])+1
##        return date(2018,month,day)
##
##    def get_price(message):
##        obj_re = re.split('\s',message,re.UNICODE)
##        return obj_re[4].replace(",",".")
        
#def get_date_price(tg_string):
#    message = "25 Februar verfügbar ab 509,99 € p.P."
#    obj_re = re.split('\s',message,re.UNICODE)
#    day = int(obj_re[0])
#    month = obj_re[1]
#    price = obj_re[4].replace(",",".")
#    print('The day is {}\nThe month is {}.\nPrice flight: {}'.format(day,month,price))
#
#    months_german = ['Januar','Februar', 'März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
#
#    index_month = months_german.index(month)+1
#
#    flightdepartdate = date(2018,index_month,day)
#    MyFlight = AvailableFlightData(flightdepartdate,price)
#    return MyFlight

