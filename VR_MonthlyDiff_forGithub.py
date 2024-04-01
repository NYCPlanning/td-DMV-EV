# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:31:37 2024

@author: R_Lin
"""

import pandas as pd
import os
import datetime
from dateutil import rrule
import calendar
from sodapy import Socrata

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
print(rawdf)

query = f"""SELECT * WHERE record_type="VEH" and suspension_indicator ="N" and revocation_indicator = "N" and county IN ("KINGS", "NEW YORK", "QUEENS" ,"BRONX", "RICHMOND") LIMIT 20000000"""
client = Socrata("data.ny.gov", "88Jdq3O5tU0yCZopaE7GJtLul")
results = client.get("w4pv-hbkt", query=query)
results_df = pd.DataFrame.from_records(results)
print("Reading Data done!")


N = len(monthList) - 1
        
vehdf = results_df.loc[results_df["registration_class"].isin(regClassList)]
    
bkdf = vehdf.loc[vehdf["county"] == "KINGS"]
mndf = vehdf.loc[vehdf["county"] == "NEW YORK"]
qndf = vehdf.loc[vehdf["county"] == "QUEENS"]
bxdf = vehdf.loc[vehdf["county"] == "BRONX"]
sidf = vehdf.loc[vehdf["county"] == "RICHMOND"] 

evdf = vehdf.loc[vehdf["fuel_type"] == "ELECTRIC"]

evbkdf = evdf.loc[evdf["county"] == "KINGS"]
evmndf = evdf.loc[evdf["county"] == "NEW YORK"]
evqndf = evdf.loc[evdf["county"] == "QUEENS"]
evbxdf = evdf.loc[evdf["county"] == "BRONX"]
evsidf = evdf.loc[evdf["county"] == "RICHMOND"] 

rawdf.insert((len(monthList)-13), monthLabelList[N] + "-Total", [bkdf.shape[0], mndf.shape[0], qndf.shape[0], bxdf.shape[0], sidf.shape[0], vehdf.shape[0]], True)
rawdf.insert((len(monthList)-13)*2, monthLabelList[N]+"-EV", [evbkdf.shape[0], evmndf.shape[0], evqndf.shape[0], evbxdf.shape[0], evsidf.shape[0], evdf.shape[0]], True)
rawdf.insert((len(monthList)-13)*3, monthLabelList[N]+"-EV Perc", [evbkdf.shape[0]/bkdf.shape[0], evmndf.shape[0]/mndf.shape[0], evqndf.shape[0]/qndf.shape[0], evbxdf.shape[0]/bxdf.shape[0], evsidf.shape[0]/sidf.shape[0], evdf.shape[0]/vehdf.shape[0]], True)


rawdf.to_csv("DMV_borough_full_excl_susp_rvct_output.csv")
print(rawdf)
