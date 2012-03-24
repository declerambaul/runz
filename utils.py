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

	availableStats = ['totalnumber','totaltime','totaldistance','totalAverageSpeed','totalAveragePace']

	def __init__(self,runz):

		self.runz = runz

		self.totalnumber = len(self.runz)
		self.totaltime = Stat.duration(self.runz)
		self.totaldistance = Stat.distance(self.runz)
		self.totalAverageSpeed = Stat.averageSpeed(self.runz)
		self.totalAveragePace = Stat.averagePace(self.runz)


	@staticmethod
	def duration(runz):
		'''Total duration of runz passed in parameters
		'''
		return sum([r.duration for r in runz])

	@staticmethod
	def distance(runz):
		'''Total duration of runz passed in parameters
		'''
		return sum([r.distance for r in runz])

	@staticmethod
	def averageSpeed(runz):
		'''Average speed of runz passed in parameters
		'''
		return 1.*sum([r.totalspeed for r in runz])/len(runz) if not len(runz)==0 else 0

	@staticmethod
	def averagePace(runz):
		'''Average page of runz passed in parameters
		'''
		return 1.*sum([r.totalpace for r in runz])/len(runz) if not len(runz)==0 else 0


	def __repr__(self):
		s = ''
		for stat in self.availableStats:
			s+= '%s : %s\n'%(stat,self.__dict__[stat])
		return s

