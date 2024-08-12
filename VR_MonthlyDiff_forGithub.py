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
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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
print(rawdf)

query = f"""SELECT * WHERE record_type="VEH" and suspension_indicator ="N" and revocation_indicator = "N" and county IN ("KINGS", "NEW YORK", "QUEENS" ,"BRONX", "RICHMOND") LIMIT 20000000"""
client = Socrata("data.ny.gov", "88Jdq3O5tU0yCZopaE7GJtLul")
results = client.get("w4pv-hbkt", query=query)
results_df = pd.DataFrame.from_records(results)


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

#rawdf.insert((len(monthList)-13), monthLabelList[N] + "-Total", [bkdf.shape[0], mndf.shape[0], qndf.shape[0], bxdf.shape[0], sidf.shape[0], vehdf.shape[0]], True)
#rawdf.insert((len(monthList)-13)*2, monthLabelList[N]+"-EV", [evbkdf.shape[0], evmndf.shape[0], evqndf.shape[0], evbxdf.shape[0], evsidf.shape[0], evdf.shape[0]], True)
#rawdf.insert((len(monthList)-13)*3, monthLabelList[N]+"-EV Perc", [evbkdf.shape[0]/bkdf.shape[0], evmndf.shape[0]/mndf.shape[0], evqndf.shape[0]/qndf.shape[0], evbxdf.shape[0]/bxdf.shape[0], evsidf.shape[0]/sidf.shape[0], evdf.shape[0]/vehdf.shape[0]], True)

rawdf[monthLabelList[N] + "-Total"] = pd.Series([bkdf.shape[0], mndf.shape[0], qndf.shape[0], bxdf.shape[0], sidf.shape[0], vehdf.shape[0]])
rawdf[monthLabelList[N] + "-EV"] = pd.Series([evbkdf.shape[0], evmndf.shape[0], evqndf.shape[0], evbxdf.shape[0], evsidf.shape[0], evdf.shape[0]])
rawdf[monthLabelList[N] + "-EV Perc"] = pd.Series([evbkdf.shape[0]/bkdf.shape[0], evmndf.shape[0]/mndf.shape[0], evqndf.shape[0]/qndf.shape[0], evbxdf.shape[0]/bxdf.shape[0], evsidf.shape[0]/sidf.shape[0], evdf.shape[0]/vehdf.shape[0]])
rawdf[monthLabelList[N] + "-EV Perc"] = rawdf[monthLabelList[N] + "-EV Perc"] * 100
rawdf[monthLabelList[N] + "-EV Perc"] = rawdf[monthLabelList[N] + "-EV Perc"].apply(lambda x: round(x, 2))
rawdf.to_csv("DMV_borough_full_excl_susp_rvct_output.csv", index=False)
print(rawdf)

mergedf = rawdf[["County"]+ rawdf.columns[rawdf.columns.str.contains(pat = '-Total')].tolist()].melt(id_vars='County')
mergedf['variable'] = mergedf['variable'].str.rstrip('-Total')
mergedf = mergedf[mergedf["County"]!="Total"]
#mergedf["HOVER"] ='<b>Month: </b>'+mergedf['variable']+'<br><b>County: </b>'+ mergedf['County']+'<br><b>Vehicle Registrations: </b>'+mergedf['value'].map('{:,.0f}'.format)

linedf = rawdf[["County"]+ rawdf.columns[rawdf.columns.str.contains(pat = '-EV Perc')].tolist()].melt(id_vars='County')
linedf['variable'] = linedf['variable'].str.rstrip('-EV Perc')
linedf = linedf[linedf["County"]=="Total"]
#linedf["HOVER"] ='<b>Month: </b>'+linedf['variable']+'<br><b>County: </b>'+ linedf['County']+'<br><b>Percent of EV Registrations: </b>'+linedf['value'].map('{:,.0f}'.format)

mergedf.columns = ["County", "Month", "Vehicle Registrations"]
linedf.columns = ["County", "Month", "Percent of EV Registrations"]

fig1 = make_subplots(specs=[[{"secondary_y": True}]])

mn = mergedf[mergedf["County"]=="NEW YORK"]
fig1.add_trace(go.Bar(name='New York', x=mn['Month'], y=mn['Vehicle Registrations']))
bk = mergedf[mergedf["County"]=="KINGS"]
fig1.add_trace(go.Bar(name='Kings', x=bk['Month'], y=bk['Vehicle Registrations']))
bx = mergedf[mergedf["County"]=="BRONX"]
fig1.add_trace(go.Bar(name='Bronx', x=bx['Month'], y=bx['Vehicle Registrations']))
qn = mergedf[mergedf["County"]=="QUEENS"]
fig1.add_trace(go.Bar(name='Queens', x=qn['Month'], y=qn['Vehicle Registrations']))
mn = mergedf[mergedf["County"]=="RICHMOND"]
fig1.add_trace(go.Bar(name='Staten Island', x=mn['Month'], y=mn['Vehicle Registrations']))
fig1.add_trace(go.Scatter(x=linedf["Month"], y=linedf["Percent of EV Registrations"], mode='lines', name = "Percent of EV Registrations"),secondary_y=True)
#fig1.add_trace(go.Bar(name='DMV Standard Series Vehicle Registrations in NYC (Nov 2019 - Jan 2024) Excluding Revocation and Suspension', x=mergedf['variable'], y=mergedf['value'],  barmode = 'stack'),secondary_y=False)
#fig1.add_trace(go.Bar(name='DMV Standard Series Vehicle Registrations in NYC (Nov 2019 - Jan 2024) Excluding Revocation and Suspension', x=mergedf['variable'], y=mergedf['value'], marker_color='#000080', hoverinfo='text', hovertext=mergedf['HOVER']),secondary_y=False)
fig1.update_layout(barmode='stack',
                  title = '<b>DMV Standard Series Vehicle and Electric Vehicle Registrations in NYC</b><br>Excluding Revocation and Suspension (November 2019 - '+ monthLabelList[N] +')').show()
fig1.update_yaxes(title_text="Total Vehicle Registrations", secondary_y=False)
fig1.update_yaxes(title_text="Percent of EV Registrations", secondary_y=True)
fig1.update_xaxes(tickangle=45)


with open('index.html', 'w') as f:
    f.write(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
