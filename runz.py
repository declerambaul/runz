from os import path
from datetime import datetime,timedelta
from collections import OrderedDict


from run_xml import RunParser,DirParser
from utils import BaseRun,Stat,timeformat


class Runz(BaseRun):
	'''A run!'''

	def __init__(self,distances,date):

		self.timeinterval = 10
		'''Measurements per second'''

		self.distances = distances
		'''Time series of distance measurements'''

		self.date = date
		'''Datetime object of run'''

		self.computeStatistics()

	def computeStatistics(self):
		'''Compute stats about run
		'''
		self.distance = self.distances[-1]
		'''Total distance'''
		self.duration = len(self.distances)*self.timeinterval
		'''Length of run in seconds'''
		self.totalpace = self.pace(self.distances)
		'''Pace during run'''
		self.totalspeed = self.speed(self.distances)
		'''Speed during run'''		
	
	def speed(self,distances):
		''' km/h '''
		time = len(distances)*self.timeinterval/3600.
		return distances[-1]/time

	def pace(self,distances):
		''' min/km ''' 		
		time = len(distances)*self.timeinterval/60.
		if distances[-1]==0:
			return 0
		else:
			return time/distances[-1]

	def save(self):		
		return '%s\t%s\n'%(datetime.strftime(self.date,timeformat),','.join(['%s'%d for d in self.distances]))

	def __repr__(self):
		return 'Date: %s | Duration : %7s  |  Distance : %2.3f  |  Speed : %2.3f km/h  |  Pace : %2.3f min/km'%(self.date,self.prettytime(self.duration),self.distance,self.totalspeed,self.totalpace)



class RunCollection(BaseRun):
	'''Stores a collection of runs'''

	def __init__(self,podz,dest,xmldir=None):

		self.podz = podz

		if xmldir:
			self.xmldirectory = xmldir
		else:
			self.xmldirectory = '/Volumes/%s/iPod_Control/Device/Trainer/Workouts/Empeds/nikeinternal/synched/'%self.podz

		self.destfile = path.join(dest,'%s.runz'%self.podz)
		open(self.destfile,'a')

		self.runz = OrderedDict()

		# Load existing runz
		self.loadRunz()

		# Load ipod runz
		self.ipodImport()

		# Save runz
		self.saveRunz()

	def ipodImport(self):

		b = len(self.runz)

		for data in DirParser(self.xmldirectory).parse():
			r = Runz(**data)

			if r.date not in self.runz:
				print 'Added new run to %s.runz : %s'%(self.podz,r)
				self.runz[r.date] = r

		print 'Loaded %s runz from ipod %s.runz'%(len(self.runz)-b,self.podz)


		self.computeStatistics()

	def computeStatistics(self):

		self.overAllStat = Stat(self.runz.values())

		self.dayStats = {}
		for day in self.days:
			self.dayStats[day] = Stat([r for r in self.runz.values() if r.day==day])
		
	
	def saveRunz(self):
		'''Stores run collection to disk in a tsv file
		'''
		with open(self.destfile,'w') as f:
			for d in sorted(self.runz.keys()):
				r = self.runz[d]
				f.write(r.save())


	def loadRunz(self):
		'''Stores run collection to disk in a tsv file
		'''

		b = len(self.runz)

		
		with open(self.destfile,'r') as f:
			for line in f:
				(d,dists) = line.split('\t')

				date = datetime.strptime(d,timeformat)
				distances = [float(i) for i in dists.split(',')]

				r = Runz(date=date,distances=distances)

				if r.date not in self.runz:
					self.runz[r.date] = r

		print 'Loaded %s runz from %s.runz'%(len(self.runz)-b,self.podz)
		
