import requests
import sys
import os
import json
import re
import html
import sqlite3
from datetime import datetime
import froniusconfig

def parse_getInverterInfo(endpoint):
    print("Fetching " + endpoint)
    url = "http://" + froniusconfig.hostname + endpoint
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    jsondata = r.json()

    inverterType = html.unescape(jsondata['Body']['Data']['1']['CustomName'])
    timestamp = jsondata['Head']['Timestamp']

def parse_getInverterRealtimeData(endpoint):
    print("Fetching " + endpoint)
    url = "http://" + froniusconfig.hostname + endpoint
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    jsondata = r.json() # already delivers dict

    day_energy_wh = jsondata['Body']['Data']['DAY_ENERGY']['Values']['1']
    power_ac_w = jsondata['Body']['Data']['PAC']['Values']['1']
    total_energy_wh = jsondata['Body']['Data']['TOTAL_ENERGY']['Values']['1']
    year_energy_wh = jsondata['Body']['Data']['YEAR_ENERGY']['Values']['1']
    
    timestamp = jsondata['Head']['Timestamp']

def parse_getLoggerLedInfo(endpoint):
    print("Fetching " + endpoint)
    url = "http://" + froniusconfig.hostname + endpoint
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    jsondata = r.json() # already delivers dict

    powerled_state = jsondata['Body']['Data']['PowerLED']['State']
    powerled_color = jsondata['Body']['Data']['PowerLED']['Color']
    solarnetled_state = jsondata['Body']['Data']['SolarNetLED']['State']
    solarnetled_color = jsondata['Body']['Data']['SolarNetLED']['Color']
    solarwebled_state = jsondata['Body']['Data']['SolarWebLED']['State']
    solarwebled_color = jsondata['Body']['Data']['SolarWebLED']['Color']
    wlanled_state = jsondata['Body']['Data']['WLANLED']['State']
    wlanled_color = jsondata['Body']['Data']['WLANLED']['Color']
    timestamp = datetime.fromisoformat(jsondata['Head']['Timestamp']).timestamp()

    conn = sqlite3.connect(froniusconfig.dbname)
    c = conn.cursor()
    c.execute(''' INSERT INTO loggerledinfo VALUES(CAST(? AS INTEGER),?,?,?,?,?,?,?,?) ''',(timestamp, powerled_state, powerled_color, solarnetled_state, solarnetled_color, solarwebled_state, solarwebled_color, wlanled_state, wlanled_color))
    conn.commit()
    conn.close()


def parse_getPowerFlowRealtimeData(endpoint):
    print("Fetching " + endpoint)
    url = "http://" + froniusconfig.hostname + endpoint
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    jsondata = r.json() # already delivers dict

    energy_day_kwh = jsondata['Body']['Data']['Inverters']['1']['E_Day']
    energy_total_kwh = jsondata['Body']['Data']['Inverters']['1']['E_Total']
    energy_year_kwh = jsondata['Body']['Data']['Inverters']['1']['E_Year']
    power_w = jsondata['Body']['Data']['Inverters']['1']['P']

    power_load_w = jsondata['Body']['Data']['Site']['P_Load']
    power_grid_w = jsondata['Body']['Data']['Site']['P_Grid']
    power_pv_w = jsondata['Body']['Data']['Site']['P_PV']
    rel_autonomy = jsondata['Body']['Data']['Site']['rel_Autonomy']
    rel_self_consumption = jsondata['Body']['Data']['Site']['rel_SelfConsumption']

    timestamp = datetime.fromisoformat(jsondata['Head']['Timestamp']).timestamp()

    conn = sqlite3.connect(froniusconfig.dbname)
    c = conn.cursor()
    c.execute(''' INSERT INTO powerflowrealtimedata VALUES(CAST(? AS INTEGER),CAST(? AS INTEGER),CAST(? AS INTEGER),CAST(? AS INTEGER),CAST(? AS INTEGER),CAST(? AS INTEGER),CAST(? AS INTEGER),CAST(? AS INTEGER),CAST(? AS INTEGER),CAST(? AS INTEGER)) ''',(timestamp, energy_day_kwh, energy_total_kwh, energy_year_kwh, power_w, power_load_w, power_grid_w, power_pv_w, rel_autonomy, rel_self_consumption))
    conn.commit()
    conn.close()


def main(argv):
    conn = sqlite3.connect(froniusconfig.dbname)
    c = conn.cursor()
    
    c.execute(''' CREATE TABLE IF NOT EXISTS powerflowrealtimedata (
    timestamp INTEGER PRIMARY KEY,
    energy_day_kwh INTEGER,
    energy_total_kwh INTEGER,
    energy_year_kwh INTEGER,
    power_w INTEGER,
    power_load_w INTEGER,
    power_grid_w INTEGER,
    power_pv_w INTEGER,
    rel_autonomy INTEGER,
    rel_self_consumption INTEGER) ''')
    conn.commit()

    c.execute(''' CREATE TABLE IF NOT EXISTS loggerledinfo (
    timestamp INTEGER PRIMARY KEY,
    powerled_state TEXT,
    powerled_color TEXT,
    solarnetled_state TEXT,
    solarnetled_color TEXT,
    solarwebled_state TEXT,
    solarwebled_color TEXT,
    wlanled_state TEXT,
    wlanled_color TEXT) ''')
    conn.commit()
    conn.close()

	#get_example("/solar_api/v1/GetActiveDeviceInfo.cgi?DeviceClass=System")
    #parse_getInverterInfo("/solar_api/v1/GetInverterInfo.cgi")
    #parse_getInverterRealtimeData("/solar_api/v1/GetInverterRealtimeData.cgi?Scope=System")
    # delivers same information as getPowerFlowRealtimeData
	#get_example("/solar_api/v1/GetLoggerInfo.cgi")
    parse_getLoggerLedInfo("/solar_api/v1/GetLoggerLEDInfo.cgi")
	#get_example("/solar_api/v1/GetMeterRealtimeData.cgi?Scope=System")
    parse_getPowerFlowRealtimeData("/solar_api/v1/GetPowerFlowRealtimeData.fcgi")
	#get_example("/solar_api/v1/GetStorageRealtimeData.cgi?Scope=System")

if __name__ == "__main__":
	main(sys.argv)

