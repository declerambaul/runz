from os import path
from datetime import datetime,timedelta
from collections import OrderedDict


from run_xml import RunParser,DirParser
from utils import Base,Stat,timeformat


class Runz(Base):
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
		self.pace = self.paceFromDistances(self.distances)
		'''Pace during run'''
		self.speed = self.speedFromDistances(self.distances)
		'''Speed during run'''		
	
	def speedFromDistances(self,distances):
		''' km/h '''
		time = len(distances)*self.timeinterval/3600.
		return distances[-1]/time

	def paceFromDistances(self,distances):
		''' min/km ''' 		
		time = len(distances)*self.timeinterval/60.
		if distances[-1]==0:
			return 0
		else:
			return time/distances[-1]

	def save(self):		
		return '%s\t%s\n'%(datetime.strftime(self.date,timeformat),','.join(['%s'%d for d in self.distances]))

	def __repr__(self):
		return 'Date: %s | Duration : %7s  |  Distance : %s  |  Speed : %s  |  Pace : %s'%(self.date,self.prettyDuration(self.duration),self.prettyDistance(self.distance),self.prettySpeed(self.speed),self.prettyPace(self.pace))



class RunCollection(Base):
	'''Stores a collection of runs'''

	def __init__(self,podz,dest,xmldir=None):

		self.podz = podz

		if xmldir:
			self.xmldirectory = path.expanduser(xmldir)
		else:
			self.xmldirectory = '/Volumes/%s/iPod_Control/Device/Trainer/Workouts/Empeds/nikeinternal/synched/'%self.podz

		self.destfile = path.expanduser(path.join(dest,'%s.runz'%self.podz))
		if not path.exists(self.destfile):
			open(self.destfile,'w').close()

		self.runz = OrderedDict()

		# Load existing runz
		self.loadRunz()

		# Load ipod runz
		self.ipodImport()


	def ipodImport(self):

		self.newrunz = []

		for data in DirParser(self.xmldirectory).parse():
			r = Runz(**data)

			if r.date not in self.runz:
				# print 'Added new run to %s.runz : %s'%(self.podz,r)
				self.runz[r.date] = r

				self.newrunz.append(r)

		if len(self.newrunz)>0:

			print 'Loaded %s new runz from ipod %s'%(len(self.newrunz),self.podz)

			for nr in self.newrunz:
				print '\t%s'%nr

			# Save runz
			self.saveRunz()

		else:
			print 'No new runz from ipod %s'%(self.podz)

		self.computeStatistics()

	
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

		with open(self.destfile,'r+') as f:
			for line in f:
				(d,dists) = line.split('\t')

				date = datetime.strptime(d,timeformat)
				distances = [float(i) for i in dists.split(',')]

				r = Runz(date=date,distances=distances)

				if r.date not in self.runz:
					self.runz[r.date] = r

		print 'Loaded %s runz from %s.runz'%(len(self.runz)-b,self.podz)

		
	def computeStatistics(self):

		self.overAllStat = Stat(self.runz.values(),name='Over all statistics',owner=self.podz)

		self.dayStats = {}
		for day in self.days:
			self.dayStats[day] = Stat([r for r in self.runz.values() if r.day==day],name='%s statistics'%day,owner='%s (%s)'%(day,self.podz))
		

		self.lastWeek = Stat([r for r in self.runz.values() if (datetime.now()-r.date) < timedelta(days=7)],name='Last week statistics',owner=self.podz)

		self.lastMonth = Stat([r for r in self.runz.values() if (datetime.now()-r.date) < timedelta(days=30)],name='Last month statistics',owner=self.podz)




