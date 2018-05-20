#!/usr/bin/python2.7

from flight import Flight
from condor import Condor
import subprocess
import manipulate_csvs

class Airline:
    '''
    Cool thing
    '''

    def __init__(self,name):
        self.name = name

    def set_route(self,departure_airport,arrival_airport):
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
    
    def set_travel_mode(self,travel_mode):
        self.travel_mode = travel_mode
        
    def set_name(self,airline):
        self.name = airline

    def kill_drivers(self):
        # Kills all browser instances
        kill_browser_instances_bash_command = "killall firefox"
        process = subprocess.Popen(kill_browser_instances_bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        
    def get_flights(self, is_headless):
        self.kill_drivers()
        try:
            if self.name == 'Condor':
                driver = Condor(self.departure_airport,self.arrival_airport) 
                price_table, price_table_sort = driver.get_flights(is_headless) 
            self.price_table = price_table
            self.price_table_sort = price_table_sort
            print(price_table)
            print('I think it worked!')
        except AttributeError:
            print('You are pretty dumb!')

    def export_flights(self):
        try:
            manipulate_csvs.export_csv(self.price_table)
        except AttributeError:
            print('Error exporting flights!')

if __name__ == '__main__':
    my_airline = Airline('Condor')
    my_airline.set_route('GRU','FRA')
    my_airline.get_flights(False)
    my_airline.export_flights()

            
