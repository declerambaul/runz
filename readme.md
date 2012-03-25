# Running statistics from Ipod

Utility that collects running data from an iPod and computes simple statistics about it. 

# Basic Usage

The name of an iPod can't contain white spaces and disk use of the iPod has to be enabled. That option can be set in the iPod's main screen in iTunes.

	from runz import RunCollection

	ipodname = 'iPodName'
	dest = '~/myruns'

	collz = RunCollection(podz=ipodname,dest=dest)
	# collz = RunCollection(podz=ipodname,dest=dest,xmldir=xxxxx)


	print collz.lastWeek

If you are not an a mac, you can pass the directory where the running data is stored (on the mac it is _/Volumes/iPodName/iPod_Control/Device/Trainer/Workouts/Empeds/nikeinternal/synched/_) using the _xmldir_ argument - .

The run data will be parsed and stored in a plain data file (_iPodname.runz_) in the _dest_ directory. When executed a second time only new runs will be added to the data file. The last call will display stats about the runs of the 7 previous days.

	Last week statistics
		Number of runs : 5
		Distance : 31.65 km
		Average distance : 6.33 km
		Duration : 3:10:20
		Average duration : 38:04
		Average pace : 6.01 min/km	
		Average speed : 9.99 km/h
		
		
# Compare runners

It is possible to compare statistics for different runners. For example, assuming that a data files are available for multiple iPods (_iPodname1.runz_ and _iPodname2.runz_). 

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





