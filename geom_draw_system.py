import pygame
from pygame.draw import *
import math
import geom_intersection
from geom_intersection import *

# framework for geometry drawing system (right now will just be lines with waypoints)
# i think main engine.py loop will catch the mouse clicks & positions but these will interface with the geom_draw_system to set up the line/geometry drawing & waypoints

class geom_draw_system():
	def __init__(self):
		# mode variables are related to setting mode and helper stuff for making the button not toggle the mode too quickly if button is held down briefly
		self.mode_button_counter = 0
		self.mode_button_speed = 30 
		self.mode_button_pressed = False
		self.mode_enabled = False
		self.mouse_x = None
		self.mouse_y = None
		self.mouse_click_counter = 0
		self.mouse_click_speed = 30
		self.mouse_click_holding = False
		self.initial_pos_x = None
		self.initial_pos_y = None
		self.selected_points = 0
		self.curr_distance = 0.0
		self.ready_to_stop = False
		self.point_list = [(None, None)]
		self.hits_calculated = None
		self.available_distance = None

	def update(self):
		if (self.mode_button_pressed == True) & (self.mode_button_counter < self.mode_button_speed):
			self.mode_button_counter = self.mode_button_counter + 1
		else:
			self.mode_button_counter = 0
			self.mode_button_pressed = False

		if (self.mouse_click_holding == True) & (self.mouse_click_counter < self.mouse_click_speed):
			self.mouse_click_counter = self.mouse_click_counter + 1
		else:
			self.mouse_click_counter = 0
			self.mouse_click_holding = False

	def update_mode_mouse_position(self, pos):
		self.mouse_x = pos[0]
		self.mouse_y = pos[1]
		if (len(self.point_list) == (self.selected_points + 2)):
			self.point_list[self.selected_points + 1] = (pos[0], pos[1])
			res = self.update_distance_used()
			if res[0] != None:
				self.point_list[self.selected_points + 1] = (res[0], res[1])
		else:
			self.point_list.append((pos[0], pos[1]))
			res = self.update_distance_used()
			if res[0] != None:
				self.point_list[self.selected_points + 1] = (res[0], res[1])

	def is_mode_button_pressed(self):
		return self.mode_button_pressed

	def calculate_distanced_used(self):
		runningDist = 0.0
		for i in range(1, len(self.point_list)):
			runningDist = runningDist + math.sqrt((float(self.point_list[i - 1][0]) - float(self.point_list[i][0]))**2 + (float(self.point_list[i - 1][1]) - float(self.point_list[i][1]))**2)
		return runningDist

	def update_distance_used(self):
		runningDist = 0.0
		currSlope = 0
		for i in range(1, len(self.point_list)):
			runningDist = runningDist + math.sqrt((float(self.point_list[i - 1][0]) - float(self.point_list[i][0]))**2 + (float(self.point_list[i - 1][1]) - float(self.point_list[i][1]))**2)
			if (runningDist > self.available_distance) & (len(self.point_list) > 2):
				remainingDist = self.available_distance - self.curr_distance
				if (self.point_list[i][0] - self.point_list[i - 1][0]) != 0:
					currSlope = (float(self.point_list[i][1]) - float(self.point_list[i - 1][1])) / (float(self.point_list[i][0]) - float(self.point_list[i - 1][0]))
				else:
					currSlope = 0.0

				# adjust direction to maximum distance remaining out of the available
				if(self.point_list[i - 1][0] < self.point_list[i][0]):
					adjustedX = self.point_list[i - 1][0] + (remainingDist / math.sqrt(1 + currSlope**2))
					adjustedY = currSlope * (adjustedX - self.point_list[i - 1][0]) + self.point_list[i - 1][1]
				elif(self.point_list[i - 1][0] > self.point_list[i][0]):
					adjustedX = self.point_list[i - 1][0] - (remainingDist / math.sqrt(1 + currSlope**2))
					adjustedY = currSlope * (adjustedX - self.point_list[i - 1][0]) + self.point_list[i - 1][1]
				elif (self.point_list[i - 1][1] < self.point_list[i][1]):
					adjustedX = self.point_list[i - 1][0] 
					adjustedY = remainingDist + self.point_list[i - 1][1]
				else:
					adjustedX = self.point_list[i - 1][0] 
					adjustedY = -remainingDist + self.point_list[i - 1][1]

				self.ready_to_stop = True
				break
			if (runningDist > self.available_distance) & (len(self.point_list) == 2):
				remainingDist = self.available_distance
				if (self.point_list[i][0] - self.point_list[i - 1][0]) != 0:
					currSlope = (float(self.point_list[i][1]) - float(self.point_list[i - 1][1])) / (float(self.point_list[i][0]) - float(self.point_list[i - 1][0]))
				else:
					currSlope = 0.0

				# adjust direction to maximum distance remaining out of the available
				if(self.point_list[i - 1][0] < self.point_list[i][0]):
					adjustedX = self.point_list[i - 1][0] + (remainingDist / math.sqrt(1 + currSlope**2))
					adjustedY = currSlope * (adjustedX - self.point_list[i - 1][0]) + self.point_list[i - 1][1]
				elif(self.point_list[i - 1][0] > self.point_list[i][0]):
					adjustedX = self.point_list[i - 1][0] - (remainingDist / math.sqrt(1 + currSlope**2))
					adjustedY = currSlope * (adjustedX - self.point_list[i - 1][0]) + self.point_list[i - 1][1]
				elif (self.point_list[i - 1][1] < self.point_list[i][1]):
					adjustedX = self.point_list[i - 1][0] 
					adjustedY = remainingDist + self.point_list[i - 1][1]
				else:
					adjustedX = self.point_list[i - 1][0] 
					adjustedY = -remainingDist + self.point_list[i - 1][1]

				self.ready_to_stop = True
				break			
			else:
				self.curr_distance = runningDist
				adjustedX = None
				adjustedY = None
				self.ready_to_stop = False

		return (adjustedX, adjustedY)


	def press_mode_button(self, loc_x, loc_y, available_distance):
		if self.hits_calculated == True:
			self.__init__()
			self.hits_calculed = None
		self.mode_button_pressed = True
		if(self.mode_enabled == False):
			self.point_list = [(None, None)]
			self.mode_enabled = True
			self.initial_pos_x = loc_x 
			self.initial_pos_y = loc_y
			self.point_list = [(loc_x, loc_y)]
			self.available_distance = available_distance
			self.hits_calculated = False
		else:
			self.mode_enabled = False

	def press_mouse_click(self):
		if self.mouse_click_holding == False:
			self.mouse_click_holding = True
			self.selected_points = self.selected_points + 1
			#if (self.ready_to_stop == True):
				# last point selected -- do nothing, allow engine to use stored data to check whether enemies collide (for now)
				# self.__init__() -- was used to clear data
				
	def is_mode_enabled(self):
		return self.mode_enabled

	def draw_system(self, surface, color):
		if(len(self.point_list) > 1):
			pygame.draw.lines(surface, color, False, self.point_list, 2)

	def does_collide(self, rect):
		collision = False
		i = 1
		while (i < len(self.point_list)):
			res = calculateLineIntersectsRectangle(self.point_list[i - 1], self.point_list[i], rect)
			if len(res) > 0:
				collision = True
				break
			i = i + 1
		return collision

