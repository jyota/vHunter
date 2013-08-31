import pygame
from pygame import Rect
from pygame import Surface
import piece
from piece import *

class entities():
	def __init__(self, _list = []):
		self._list = _list

	def addEntity(self, toAdd):
		self._list.append(toAdd)

	def getLength(self):
		return len(self._list)

	def getEntityByID(self, ID):
		for i in self._list:
			if i[0] == id:
				return i
		
	def removeEntity(self, ID):
		if ID != None:	
			allitems = []
			gotit = 0
			for i in self._list:
				if i[0] == ID and gotit == 0:
					gotit = 1
				else:
					allitems.append(i)
	
		self._list = allitems
