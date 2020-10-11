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
    c.execute(''' SELECT * FROM powerflowrealtimedata WHERE DATETIME(timestamp,'unixepoch') > DATETIME('now','-7 days');''')
    data = c.fetchall()
    timestamp = []
    energy_day_wh = []
    power_pv_w = []
    power_load_w = []
    power_grid_w = []

    local_tz = datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo

    for row in data:
        timestamp.append(row[0])
        energy_day_wh.append(row[1])
        power_load_w.append(row[5])
        power_grid_w.append(row[6])
        power_pv_w.append(row[7])

    timestamp_converted = [mdate.epoch2num(row) for row in timestamp]

    matplotlib.rcParams.update({'font.size': 8})
    fig, ax1 = plt.subplots()
    fig.set_figheight(4)
    fig.set_figwidth(16)
    fig.set_dpi(100)
    fig.autofmt_xdate(rotation=90)

    color = 'tab:blue'
    ax1.set_xlabel('time')
    ax1.set_ylabel('Power [W]', color=color)
    ax1.xaxis.set_major_locator(mdate.HourLocator(interval=4))
    ax1.xaxis.set_major_formatter(mdate.DateFormatter('%d.%m.%Y %H:%M',tz=local_tz))
    ax1.xaxis.set_minor_locator(mdate.HourLocator(interval=1))
    ax1.xaxis.grid(which='minor', linewidth=0.5)
    ax1.plot_date(timestamp_converted, power_pv_w, xdate=True,color=color, linestyle='solid', marker='None')
    
    ax2 = ax1.twinx()

    color = 'tab:red'
    ax2.set_ylabel('Energy [Wh]', color=color)
    ax2.xaxis.set_major_locator(mdate.HourLocator(interval=4))
    ax2.xaxis.set_major_formatter(mdate.DateFormatter('%d.%m.%Y %H:%M', tz=local_tz))
    ax2.xaxis.set_minor_locator(mdate.HourLocator(interval=1))
    ax2.xaxis.grid(which='minor', linewidth=0.5)
    ax2.plot_date(timestamp_converted, energy_day_wh, xdate=True,linestyle='solid', marker='None', color=color)

    plt.grid(True)
    plt.tight_layout()
    plt.savefig(froniusconfig.figurepath + 'fronius_power_week.png')
    plt.close()

def main(argv):
    plot_week()

if __name__ == "__main__":
	main(sys.argv)

