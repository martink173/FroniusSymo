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

def plot_months():
    conn = sqlite3.connect(froniusconfig.dbname)
    c = conn.cursor()
    c.execute('''select year, month, sum(daymax) from (select month, year,
    daymax from (select
    strftime('%m',datetime(timestamp,'unixepoch','localtime')) as month,
    strftime('%d',datetime(timestamp,'unixepoch','localtime')) as day,
    strftime('%Y',datetime(timestamp,'unixepoch','localtime')) as year,
    max(energy_day_kwh) as daymax FROM powerflowrealtimedata WHERE
    DATETIME(timestamp,'unixepoch') > DATETIME('now','-1 years') GROUP BY day))
    GROUP BY year, month;''')

    data = c.fetchall()
    
    month = []
    year = []
    monthsum = []

    local_tz = datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo

    for row in data:
        month.append(row[1])
        year.append(row[0])
        monthsum.append(row[2])

    x = np.arange(len(month))

    matplotlib.rcParams.update({'font.size': 8})
    fig, ax1 = plt.subplots()
    fig.set_figheight(4)
    fig.set_figwidth(8)
    fig.set_dpi(100)

    width = 0.50
   
    rects1 = ax1.bar(x, monthsum, width, label='Wh')

    color = 'tab:blue'
    ax1.set_ylabel('Energy [Wh]', color=color)
    ax1.set_title('Solar Energy by Month')
    ax1.set_xticks(x)
    ax1.set_xticklabels(month)
    ax1.set_axisbelow(True)

    plt.grid(True)
    plt.tight_layout()
    plt.savefig(froniusconfig.figurepath + '/fronius_power_months.png')
    plt.close()

def main(argv):
    plot_months()

if __name__ == "__main__":
	main(sys.argv)

