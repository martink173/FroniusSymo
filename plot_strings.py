import matplotlib
matplotlib.use('Agg')
import sqlite3
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
from matplotlib import style
import sys
import os
import froniusconfig

def plot_week():
    conn = sqlite3.connect(froniusconfig.dbname)
    c = conn.cursor()
    c.execute(''' SELECT * FROM stringdata WHERE DATETIME(timestamp,'unixepoch') > DATETIME('now','-7 days');''')
    data = c.fetchall()
    timestamp = []
    current_dc_string_1_a = []
    current_dc_string_2_a = []
    voltage_dc_string_1_v = []
    voltage_dc_string_2_v = []
    power_w = []

    local_tz = datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo

    for row in data:
        timestamp.append(row[0])
        current_dc_string_1_a.append(row[1])
        current_dc_string_2_a.append(row[2])
        voltage_dc_string_1_v.append(row[3])
        voltage_dc_string_2_v.append(row[4])
        power_w.append(row[5])

    timestamp_converted = [mdate.epoch2num(row) for row in timestamp]

    matplotlib.rcParams.update({'font.size': 8})
    fig, ax1 = plt.subplots()
    fig.set_figheight(4)
    fig.set_figwidth(16)
    fig.set_dpi(100)
    fig.autofmt_xdate(rotation=90)

    color1 = 'tab:blue'
    color2 = 'tab:cyan'
    ax1.set_xlabel('time')
    ax1.set_ylabel('Current [A]', color=color1)
    ax1.xaxis.set_major_locator(mdate.HourLocator(interval=4))
    ax1.xaxis.set_major_formatter(mdate.DateFormatter('%d.%m.%Y %H:%M',tz=local_tz))
    ax1.xaxis.set_minor_locator(mdate.HourLocator(interval=1))
    ax1.xaxis.grid(which='minor', linewidth=0.5)
    ax1.plot_date(timestamp_converted,current_dc_string_1_a, xdate=True, color=color1, linestyle='solid', marker='None')
    ax1.plot_date(timestamp_converted,current_dc_string_2_a, xdate=True, color=color2, linestyle='solid', marker='None')
   
    ax2 = ax1.twinx()

    color3 = 'tab:red'
    color4 = 'tab:orange'
    ax2.set_ylabel('Voltage [V]', color=color3)
    ax2.xaxis.set_major_locator(mdate.HourLocator(interval=4))
    ax2.xaxis.set_major_formatter(mdate.DateFormatter('%d.%m.%Y %H:%M', tz=local_tz))
    ax2.xaxis.set_minor_locator(mdate.HourLocator(interval=1))
    ax2.xaxis.grid(which='minor', linewidth=0.5)
    ax2.plot_date(timestamp_converted, voltage_dc_string_1_v, xdate=True,linestyle='solid', marker='None', color=color3)
    ax2.plot_date(timestamp_converted, voltage_dc_string_2_v, xdate=True,linestyle='solid', marker='None', color=color4)

    plt.grid(True)
    plt.tight_layout()
    plt.savefig(froniusconfig.figurepath + 'fronius_strings_week.png')
    plt.close()

def main(argv):
    plot_week()

if __name__ == "__main__":
	main(sys.argv)

