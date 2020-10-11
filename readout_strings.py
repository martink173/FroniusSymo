import sys
import requests
import os
import json
import re
import sqlite3
from datetime import datetime, date, timezone
import froniusconfig

def parse_getArchiveData(endpoint):
    print("Fetching " + endpoint)
    url = "http://" + froniusconfig.hostname + endpoint
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    jsondata = r.json()

    current_dc_string_1_a = jsondata['Body']['Data']['inverter/1']['Data']['Current_DC_String_1']['Values']
    current_dc_string_2_a = jsondata['Body']['Data']['inverter/1']['Data']['Current_DC_String_2']['Values']
    voltage_dc_string_1_v = jsondata['Body']['Data']['inverter/1']['Data']['Voltage_DC_String_1']['Values']
    voltage_dc_string_2_v = jsondata['Body']['Data']['inverter/1']['Data']['Voltage_DC_String_2']['Values']
    log_date = jsondata['Body']['Data']['inverter/1']['Start']
    timestamp = datetime.fromisoformat(log_date).timestamp() # saved in UTC time format

    conn = sqlite3.connect(froniusconfig.dbname)
    c = conn.cursor()
    
    count = 0
    while count < 86400:
        if str(count) in jsondata['Body']['Data']['inverter/1']['Data']['Current_DC_String_1']['Values']:
            current_dc_string_1_a = jsondata['Body']['Data']['inverter/1']['Data']['Current_DC_String_1']['Values'][str(count)]
            current_dc_string_2_a = jsondata['Body']['Data']['inverter/1']['Data']['Current_DC_String_2']['Values'][str(count)]
            voltage_dc_string_1_v = jsondata['Body']['Data']['inverter/1']['Data']['Voltage_DC_String_1']['Values'][str(count)]
            voltage_dc_string_2_v = jsondata['Body']['Data']['inverter/1']['Data']['Voltage_DC_String_2']['Values'][str(count)]
            power_w = jsondata['Body']['Data']['inverter/1']['Data']['PowerReal_PAC_Sum']['Values'][str(count)]

            c.execute(''' INSERT OR IGNORE INTO stringdata VALUES(CAST(? AS INTEGER),CAST(? AS REAL ),CAST(? AS REAL),CAST(? AS REAL),CAST(? AS REAL),CAST(? AS REAL))''',(timestamp + count,current_dc_string_1_a,current_dc_string_2_a,voltage_dc_string_1_v,voltage_dc_string_2_v,power_w))
            conn.commit()
        count = count + 300

    conn.close()

def main(argv):
    conn = sqlite3.connect(froniusconfig.dbname)
    c = conn.cursor()

    c.execute(''' CREATE TABLE IF NOT EXISTS stringdata (
    timestamp INTEGER PRIMARY KEY,
    current_dc_string_1_a REAL,
    current_dc_string_2_a REAL,
    voltage_dc_string_1_v REAL,
    voltage_dc_string_2_v REAL,
    power_w REAL) ''')
    conn.commit()
    conn.close()
    
    today = date.today()
    date_string = today.strftime("%d.%m.%Y")
    parse_getArchiveData("/solar_api/v1/GetArchiveData.cgi?Scope=System&StartDate="+ date_string +"&EndDate=" + date_string + "&Channel=Current_DC_String_1&Channel=Current_DC_String_2&Channel=Voltage_DC_String_1&Channel=Voltage_DC_String_2&Channel=PowerReal_PAC_Sum")

if __name__ == "__main__":
	main(sys.argv)

