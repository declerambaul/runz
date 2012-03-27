from datetime import datetime,timedelta

import operator
import smtplib

timeformat = '%Y-%m-%dT%H:%M:%S'

class Base:
	'''Base class for common methods'''

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

	def prettyDuration(self, time):
		'''Pretty display of time'''
		(h,m,s) = self.hms(int(time))
		return '%s%02d:%02d'%( 	'%s:'%h if h!=0 else '', m, s)

	def prettyDistance(self,distance):
		'''Pretty display of distance'''
		return '%2.2f km'%distance

	def prettySpeed(self,speed):
		'''Pretty display of speed'''
		return '%2.2f km/h'%speed

	def prettyPace(self,pace):
		'''Pretty display of pace'''
		return '%2.2f min/km'%pace



class Stat(Base):
	"""A statstic about a set of runs"""

	availableStats = {'totalnumber':'Number of runs','totalduration':'Duration','averageduration':'Average duration','totaldistance':'Distance','averagedistance':'Average distance','averagespeed':'Average speed','averagepace':'Average pace'}

	def __init__(self,runz,name=None,owner=None):

		self.runz = runz
		self.name = name
		self.owner = owner

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
		return "Duration: %s (%2.1f%%) |  Distance: %s (%2.1f%%) | Speed: %s (%2.1f%%) |  Pace: %s (%2.1f%%)"%(self.prettyDuration(run.duration),durP,run.prettyDistance(run.distance),distP,run.prettySpeed(run.speed),speedP,run.prettyPace(run.pace),paceP)

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
		sep = '\t'
		format = '%s%s : %s\n'

		ret = '%s\n'%self.name if self.name else ''

		ret += format%(sep,self.availableStats['totalnumber'],self.totalnumber)

		ret += format%(sep,self.availableStats['totalduration'],self.prettyDuration(self.totalduration))

		ret += format%(sep,self.availableStats['averageduration'],self.prettyDuration(self.averageduration))
		
		ret += format%(sep,self.availableStats['totaldistance'],self.
			prettyDistance(self.totaldistance))

		ret += format%(sep,self.availableStats['averagedistance'],self.
			prettyDistance(self.averagedistance))

		ret += format%(sep,self.availableStats['averagespeed'],self.
			prettySpeed(self.averagespeed))

		ret += format%(sep,self.availableStats['averagepace'],self.
			prettyPace(self.averagepace))


		# s = '%s\n'%self.name if self.name else ''
		# for stat,desc in self.availableStats.items():
		# 	s+= '\t%s : %s\n'%(desc,self.__dict__[stat])

		return ret



class CompareStat(Base):
	'''Compares and ranks a collection of Stat objects
	'''	
	def __init__(self,statList):
		'''Compare a list of stats'''

		self.comp = {}

		if len(set([s.name for s in statList]))==1:
			self.name = statList[0].name
		else:
			self.name = ','.join(['%s:%s'%(s.owner,s.name) for s in statList])


		for astat in Stat.availableStats:
			
			self.comp[astat] = sorted([(stat.owner, stat.__dict__[astat]) for stat in statList], key=operator.itemgetter(1),reverse=True)

	def __repr__(self):

		sep = '\t'
		format = '%s:\n%s'

		def ranking(d):
			pass


		ret = '%s\n%s\n'%(self.name,'-'*len(self.name))


		ret += format%(Stat.availableStats['totalnumber'],''.join(['\t%s: %s\n'%(o,v) for o,v in self.comp['totalnumber']]))


		ret += format%(Stat.availableStats['totalduration'],''.join(['\t%s: %s\n'%(o,self.prettyDuration(v)) for o,v in self.comp['totalduration']]))

		ret += format%(Stat.availableStats['averageduration'],''.join(['\t%s: %s\n'%(o,self.prettyDuration(v)) for o,v in self.comp['averageduration']]))

		ret += format%(Stat.availableStats['totaldistance'],''.join(['\t%s: %s\n'%(o,self.prettyDistance(v)) for o,v in self.comp['totaldistance']]))

		ret += format%(Stat.availableStats['averagedistance'],''.join(['\t%s: %s\n'%(o,self.prettyDistance(v)) for o,v in self.comp['averagedistance']]))

		ret += format%(Stat.availableStats['averagespeed'],''.join(['\t%s: %s\n'%(o,self.prettySpeed(v)) for o,v in self.comp['averagespeed']]))
		
		return ret

		

class Notify:
		
	SMTP_SERVER = 'smtp.gmail.com'
	SMTP_PORT = 587
	 
	def __init__(self,email,pw):
		self.email = email
		self.pw = pw

	def send(self,rec,msg):

		subject = 'Running stats'

		headers = '\n'.join(["From: " + self.email, "Subject: %s"%subject, "To: %s"%rec, "MIME-Version: 1.0", "Content-Type: text/html"])

	
	 
		session = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
	 
		session.ehlo()
		session.starttls()
		session.ehlo
		session.login(self.email, self.pw)

		text = '%s\n\n%s'%(headers,msg)
	 
		session.sendmail(self.email, rec, text)
		session.quit()
		