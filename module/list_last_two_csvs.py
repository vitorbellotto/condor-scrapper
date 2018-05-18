#!/usr/bin/python2.7

import os
import glob

def get_two_last_csvs():
    path = os.getcwd()
    os.chdir(path)
    result = [i for i in glob.glob('{}/condor/data/*-*-*_*-*-*.csv'.format(path))]
    return [result[-2],result[-1]]

