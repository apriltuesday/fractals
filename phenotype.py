#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import re
import turtle


# phenotype is a string that has been generated from an l-system
class Phenotype:

	def __init__(self, code):
		self.code = code
		# these are same for all trees, for now
		# idea: these parameters are controlled by environment
		# evolution modifies the rules
		self.weights = np.array([
			#0.2,
			100,
			90,
			40,
			20,
			30
		])
		self.step = 5.0
		self.angle = 22.7


	@property
	def image(self):
		if not hasattr(self, '_image'):
			self.draw()
		return self._image


	@property
	def height(self):
		if not hasattr(self, '_states'):
			self.draw()
		return max(self._states, key=lambda (heading, position): position[1])[1][1]


	def score(self):
		if not hasattr(self, '_score'):
			self._score = np.dot(self.weights, [
				#self.efficiency(),
				self.phototropism(),
				self.symmetry(),
				self.light(),
				self.stability(),
				self.branching()
			])
		return self._score


	def efficiency(self):
		return -1 * len(self.code)


	def phototropism(self):
		return self.height


	# difference between weight on left to weight on right
	def symmetry(self):
		if not hasattr(self, '_states'):
			self.draw()
		xs = [p[0] for (h, p) in self._states]
		left = sum([abs(x) for x in xs if x < 0])
		right = sum([x for x in xs if x > 0])
		return -1 * abs(left - right)


	def light(self):
		return 0


	def stability(self):
		return 0
		

	# total number of branching points with more than one branch leaving
	def branching(self):
		pattern = r'(?=(F[+-F]*?\[.*F.*\][+-F]*?F))'
		matches = [match.group(1) for match in re.finditer(pattern, self.code)]
		return len(matches)


	def draw(self):
		# init turtle
		t = turtle.Turtle()
		s = turtle.Screen()
		stack = []
		s.tracer(500, 0)
		t.hideturtle()
		t.speed(0)
		t.penup()
		t.left(90)
		t.setpos(0, -200)
		t.pencolor('#367132')

		# stores position and heading of turtle at each step
		self._states = []

		# draw
		for c in self.code:
			self._states.append((t.heading(), t.pos()))
			if c == 'F':
				t.forward(self.step)
			elif c == 'f': #not currently used
				t.penup()
				t.forward(self.step)
				t.pendown()
			elif c == '+':
				t.left(self.angle)
			elif c == '-':
				t.right(self.angle)
			elif c == '[':
				stack.append((t.heading(), t.pos()))
			elif c == ']':
				t.penup()
				heading, position = stack.pop()
				t.setheading(heading)
				t.setpos(position)
				t.pendown()
			else:
				print 'not supported:', c

		self._image = s.getcanvas()
