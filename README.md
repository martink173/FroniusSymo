# FroniusSymo
This Python code is intended to read recorded data from a Fronius Symo inverter device, typically used in connection with photovoltaic panels. It reads information about power, voltage, current, and energy from the networked inverter (readout_\*.py files) . Information is then stored in an SQLite3 database.
The same database is used for evaluation of data using Matplotlib (plot_\*.py files).

The code can be deployed to a Linux platform, with periodic execution for data collection and evaluation. This can be realized with e.g. cronjobs. The resulting graphics can be published on e.g. a webserver.

If you can make any use of this, please drop me a line :)
