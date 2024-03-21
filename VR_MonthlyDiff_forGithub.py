# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:31:37 2024

@author: R_Lin
"""

import pandas as pd
import os
token = os.environ.get('NYS_APP_TOKEN')


# specify standard series registration classes
regClassList = ['ARG', 	'AYG', 	'BOB', 	'CBS', 	'CCK', 	'CLG', 	'CME', 	'CMH', 	'EDU', 	'FPW', 	'GAC', 	'GSC', 	'GSM', 	'HAM', 	'HIS', 	'JCA', 	'JCL', 	'JSC', 	'JWV', 	'LOC', 	'LUA', 	'MCL', 	'MED', 	'NLM', 	'NYA', 	'NYC', 	'NYS', 	'ORG', 	'PAS', 	'PHS', 	'PPH', 	'RGL', 	'SCL', 	'SOS', 	'SPO', 	'SRF', 	'SRN', 	'STG', 	'SUP', 	'USC', 	'USS', 	'VPL', 	'WUG']

boroughList = ["KINGS", "NEW YORK", "QUEENS" ,"BRONX", "RICHMOND"]

rawdf = pd.read_csv("DMV_borough_full_excl_susp_rvct_output.csv")
print("read output")
