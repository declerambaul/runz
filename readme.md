# Running statistics from Ipod

Utility that collects running data from an iPod and computes simple statistics about it. 

# Basic Usage

First you have to enable disk use of the iPod. That option can be set in the iPod's main screen in iTunes.

	from runz import RunCollection

	ipodname = 'iPodName'
	dest = '~/myruns'

	collz = RunCollection(podz=ipodname,dest=dest)

	print collz.lastWeek

The run data will be parsed and stored in a plain text file in the _dest_ directory. When executed a second time only new runs will be added to the text file (_'iPodname.runz'_). The last call will display stats about the runs of the 7 previous days.

	Last week statistics
		Number of runs : 5
		Distance : 31.65 km
		Average distance : 6.33 km
		Duration : 3:10:20
		Average duration : 38:04
		Average pace : 6.01 min/km	
		Average speed : 9.99 km/h
		
		
# Compare runners

It is possible to compare statistics for different runners. For example, assuming that a data files are available for multiple iPods (_'iPodname1.runz'_ and _'iPodname2.runz'_). 

	from runz import RunCollection
	from utils import CompareStat

	collz1 = RunCollection(podz='iPodname1',dest='~/Dropbox/ourruns')
	collz2 = RunCollection(podz='iPodname2',dest='~/Dropbox/ourruns')

	compLastMonth = CompareStat([collz1.lastMonth,collz2.lastMonth])

	print compLastMonth

The code above will output a ranking of all runners.
	
	Last month statistics
	---------------------
	Number of runs:
		iPodname1: 20
		iPodname2: 13
	Duration:
		iPodname1: 12:16:40
		iPodname2: 8:30:30
	Average duration:
		iPodname2: 39:16
		iPodname1: 36:50
	Distance:
		iPodname1: 127.07 km
		iPodname2: 96.32 km
	Average distance:
		iPodname2: 7.41 km
		iPodname1: 6.35 km
	Average speed:
		iPodname2: 11.05 km/h
		iPodname1: 9.84 km/h





