import matplotlib
matplotlib.use('Agg')
import sqlite3
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
from matplotlib import style
import sys
import os
import numpy as np
import froniusconfig

def plot_days():
    conn = sqlite3.connect(froniusconfig.dbname)
    c = conn.cursor()
    c.execute('''select timestamp, day, daymax from (select
    timestamp,
    strftime('%d',datetime(timestamp,'unixepoch','localtime')) as day,
    max(energy_day_kwh) as daymax FROM powerflowrealtimedata WHERE
    DATETIME(timestamp,'unixepoch') > DATETIME('now','-31 days') GROUP BY
    day) order by timestamp ASC; ''')
 
    data = c.fetchall()
    
    timestamp = []
    day = []
    daymax = []

    local_tz = datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo

    for row in data:
        day.append(row[1])
        daymax.append(row[2])

    print(day)
    print(daymax)

    x = np.arange(len(day))

    matplotlib.rcParams.update({'font.size': 8})
    fig, ax1 = plt.subplots()
    fig.set_figheight(4)
    fig.set_figwidth(10)
    fig.set_dpi(100)

    width = 0.50
   
    rects1 = ax1.bar(x, daymax, width, label='Wh')

    color = 'tab:blue'
    ax1.set_ylabel('Energy [Wh]', color=color)
    ax1.set_title('Solar Energy by Day')
    ax1.set_xticks(x)
    ax1.set_xticklabels(day)
    ax1.set_axisbelow(True)

    plt.grid(True)
    plt.tight_layout()
    plt.savefig(froniusconfig.figurepath + 'fronius_power_days.png')
    plt.close()

def main(argv):
    plot_days()

if __name__ == "__main__":
	main(sys.argv)

