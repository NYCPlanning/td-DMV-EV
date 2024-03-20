# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:31:37 2024

@author: R_Lin
"""

import pandas as pd
import datetime
import calendar
import os
from sodapy import Socrata
from dateutil import rrule
from plotly.subplots import make_subplots
import plotly.graph_objects as go

start=datetime.datetime.now()
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

token = os.environ.get('NYS_APP_TOKEN')


# specify standard series registration classes
regClassList = ['ARG', 	'AYG', 	'BOB', 	'CBS', 	'CCK', 	'CLG', 	'CME', 	'CMH', 	'EDU', 	'FPW', 	'GAC', 	'GSC', 	'GSM', 	'HAM', 	'HIS', 	'JCA', 	'JCL', 	'JSC', 	'JWV', 	'LOC', 	'LUA', 	'MCL', 	'MED', 	'NLM', 	'NYA', 	'NYC', 	'NYS', 	'ORG', 	'PAS', 	'PHS', 	'PPH', 	'RGL', 	'SCL', 	'SOS', 	'SPO', 	'SRF', 	'SRN', 	'STG', 	'SUP', 	'USC', 	'USS', 	'VPL', 	'WUG']

boroughList = ["KINGS", "NEW YORK", "QUEENS" ,"BRONX", "RICHMOND"]

start_date = datetime.datetime(2019, 12, 1)
end_date = start
monthList = []
monthLabelList = []
for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
    monthList.append(calendar.month_name[dt.month] + " " + str(dt.year))
monthLabelList = ['November 2019'] + monthList[:-1]


rawdf = pd.read_csv("DMV_borough_full_excl_susp_rvct_output.csv")

client = Socrata("data.ny.gov", token)
results = client.get("w4pv-hbkt", limit=20000000)
results_df = pd.DataFrame.from_records(results)


N = len(monthList) - 1
        
results_df['record_type'] = results_df['record_type'].str.rstrip()
vehdf = results_df.loc[results_df["record_type"] == "VEH"]
vehdf = vehdf.loc[vehdf["suspension_indicator"] == "N"]
vehdf = vehdf.loc[vehdf["revocation_indicator"] == "N"]
#vehdf = vehdf.loc[vehdf["Body Type"] != "PICK"]
vehdf = vehdf.loc[vehdf["registration_class"].isin(regClassList)]
vehdf['CountyMod'] = vehdf['county'].str.rstrip()
vehdf = vehdf.loc[vehdf["CountyMod"].isin(boroughList)]
    
bkdf = vehdf.loc[vehdf["CountyMod"] == "KINGS"]
mndf = vehdf.loc[vehdf["CountyMod"] == "NEW YORK"]
qndf = vehdf.loc[vehdf["CountyMod"] == "QUEENS"]
bxdf = vehdf.loc[vehdf["CountyMod"] == "BRONX"]
sidf = vehdf.loc[vehdf["CountyMod"] == "RICHMOND"] 

evdf = vehdf.loc[vehdf["fuel_type"] == "ELECTRIC"]

evbkdf = evdf.loc[evdf["CountyMod"] == "KINGS"]
evmndf = evdf.loc[evdf["CountyMod"] == "NEW YORK"]
evqndf = evdf.loc[evdf["CountyMod"] == "QUEENS"]
evbxdf = evdf.loc[evdf["CountyMod"] == "BRONX"]
evsidf = evdf.loc[evdf["CountyMod"] == "RICHMOND"] 

rawdf.insert((len(monthList)-13), monthLabelList[N] + "-Total", [bkdf.shape[0], mndf.shape[0], qndf.shape[0], bxdf.shape[0], sidf.shape[0], vehdf.shape[0]], True)
rawdf.insert((len(monthList)-13)*2, monthLabelList[N]+"-EV", [evbkdf.shape[0], evmndf.shape[0], evqndf.shape[0], evbxdf.shape[0], evsidf.shape[0], evdf.shape[0]], True)
rawdf.insert((len(monthList)-13)*3, monthLabelList[N]+"-EV Perc", [evbkdf.shape[0]/bkdf.shape[0], evmndf.shape[0]/mndf.shape[0], evqndf.shape[0]/qndf.shape[0], evbxdf.shape[0]/bxdf.shape[0], evsidf.shape[0]/sidf.shape[0], evdf.shape[0]/vehdf.shape[0]], True)


rawdf.to_csv("DMV_borough_full_excl_susp_rvct_output.csv")

