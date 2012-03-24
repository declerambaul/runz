import os
import xml.parsers.expat 
from datetime import datetime

from utils import timeformat

class RunParser():

	def __init__(self):

		self.data = {}

		self.createPaser()

	def createPaser(self):

		self.p = xml.parsers.expat.ParserCreate()        
		self.p.StartElementHandler = self.start_element
		self.p.EndElementHandler = self.end_element
		self.p.DefaultHandler = None


	def parse(self,fn):

		# print 'Parsing %s'%fn

		self.data = {}
		self.createPaser()

		# extract
		self.p.ParseFile(open(fn)) 

		# transform
		self.data['distances'] = [float(d) for d in self.data['distances'].split(',') if d !=''] if 'distances' in self.data else [0.0]

		# load
		return self.data

	def start_element(self, element, attrs):
		'''Sets the appropriate defaulthandler
		'''
		# print element,
		# print attrs

		if element=='extendedData' and attrs['dataType']=="distance":
			self.setHandler(self.collectDistances)
		elif element=='time':
			self.setHandler(self.collectTime)


	def end_element(self, element):

		self.setHandler(handler = None)

	def setHandler(self, handler = None):
		self.p.DefaultHandler = handler

	def collectTime(self,value):		
		self.data['date'] = datetime.strptime(value[:-6],timeformat)

	def collectDistances(self,value):
			if 'distances' in self.data:
				self.data['distances'] += value
			else:
				self.data['distances'] = value


class DirParser():

	def __init__(self,directory):

		self.parser = RunParser()
		self.directory = directory

	def parse(self):
		for root, dirs, files in os.walk(self.directory):			
			for f in files:				
				if f[-3:]=='xml':
					yield self.parser.parse(os.path.join(root,f))
					

