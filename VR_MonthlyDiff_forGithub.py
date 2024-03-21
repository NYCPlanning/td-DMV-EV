# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:31:37 2024

@author: R_Lin
"""

import pandas as pd
import os
import datetime
from dateutil import rrule
token = os.environ.get('NYS_APP_TOKEN')


# specify standard series registration classes
regClassList = ['ARG', 	'AYG', 	'BOB', 	'CBS', 	'CCK', 	'CLG', 	'CME', 	'CMH', 	'EDU', 	'FPW', 	'GAC', 	'GSC', 	'GSM', 	'HAM', 	'HIS', 	'JCA', 	'JCL', 	'JSC', 	'JWV', 	'LOC', 	'LUA', 	'MCL', 	'MED', 	'NLM', 	'NYA', 	'NYC', 	'NYS', 	'ORG', 	'PAS', 	'PHS', 	'PPH', 	'RGL', 	'SCL', 	'SOS', 	'SPO', 	'SRF', 	'SRN', 	'STG', 	'SUP', 	'USC', 	'USS', 	'VPL', 	'WUG']

boroughList = ["KINGS", "NEW YORK", "QUEENS" ,"BRONX", "RICHMOND"]

start=datetime.datetime.now()
start_date = datetime.datetime(2019, 12, 1)
end_date = start
monthList = []
monthLabelList = []
for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
    monthList.append(calendar.month_name[dt.month] + " " + str(dt.year))
monthLabelList = ['November 2019'] + monthList[:-1]

rawdf = pd.read_csv("DMV_borough_full_excl_susp_rvct_output.csv")
print("read output")
