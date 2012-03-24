from datetime import datetime,timedelta


timeformat = '%Y-%m-%dT%H:%M:%S'

class BaseRun:
	'''A run!'''

	days = ['Mo','Tu','We','Th','Fr','Sa','Su',]
	months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

	days_dict = {0:'Mo',1:'Tu',2:'We',3:'Th',4:'Fr',5:'Sa',6:'Su'}
	months_dict = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}

	@property		
	def day(self):		
		return self.days_dict[self.date.weekday()]
	@property		
	def month(self):				
		return self.months_dict[self.date.month]
	
	def hms(self,time):
		''' (hours,minutes,seconds) 
		'''
		return (time/3600,(time%3600)/60,time%60)

	def prettytime(self, time):
		'''Pretty display of time'''
		(h,m,s) = self.hms(time)
		return '%s%02d:%02d'%( 	'%s:'%h if h!=0 else '', m, s)



class Stat():
	"""A statstic about a set of runs"""

	availableStats = {'totalnumber':'Number of runs','totalduration':'Duration','averageduration':'Average duration','totaldistance':'Distance','averagedistance':'Average distance','averagespeed':'Average speed','averagepace':'Average pace','lastruninfo':'Last run in comparison'}

	def __init__(self,runz,name=None):

		self.runz = runz
		self.name = name

		self.totalnumber = len(self.runz)
		self.totalduration = self.duration()
		self.averageduration = 1.*self.totalduration/self.totalnumber
		self.totaldistance = self.distance()
		self.averagedistance = 1.*self.totaldistance/self.totalnumber
		self.averagespeed = self.averageSpeed()
		self.averagepace = self.averagePace()

		self.lastruninfo = self.runInfo(self.runz[-1])
	
	def runInfo(self,run):
		'''Returns str info about the last run
		'''
		durP = 100.*run.duration/self.averageduration
		distP = 100.*run.distance/self.averagedistance
		speedP = 100.*run.speed/self.averagespeed
		paceP = 100.*run.pace/self.averagepace
		return "Duration: %s (%2.1f%%) |  Distance: %skm (%2.1f%%) | Speed: %2.3f km/h (%2.1f%%) |  Pace: %2.3f min/km (%2.1f%%)"%(run.prettytime(run.duration),durP,run.distance,distP,run.speed,speedP,run.pace,paceP)
	def duration(self):
		'''Total duration of runz passed in parameters
		'''
		return sum([r.duration for r in self.runz])

	
	def distance(self):
		'''Total duration of runz passed in parameters
		'''
		return sum([r.distance for r in self.runz])

	def averageSpeed(self):
		'''Average speed of runz passed in parameters
		'''
		return 1.*sum([r.speed for r in self.runz])/len(self.runz) if not len(self.runz)==0 else 0

	def averagePace(self):
		'''Average page of runz passed in parameters
		'''
		return 1.*sum([r.pace for r in self.runz])/len(self.runz) if not len(self.runz)==0 else 0


	def __repr__(self):
		s = '%s\n'%self.name if self.name else ''
		for stat,desc in self.availableStats.items():
			s+= '\t%s : %s\n'%(desc,self.__dict__[stat])
		return s

