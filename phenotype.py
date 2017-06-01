#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import re
import turtle

EPSILON = 10.0

# phenotype is a string that has been generated from an l-system
class Phenotype:

	def __init__(self, code):
		self.code = code
		# not currently used...
		# idea: these parameters are controlled by environment
		# evolution modifies the rules
		self.weights = np.array([
			1.0,
			0.05,
			20.0,
			1.0,
			0.0,
			2.0
		])
		self.step = 5.0
		self.angle = 22.7


	# scores should be non-negative to make sampling easier
	def score(self):
		if not hasattr(self, '_score'):
			self.draw()
			if len(self._states) == 0:
				return 0

			self._score = np.dot(self.weights, [
				self.efficiency(),
				self.phototropism(),
				self.symmetry(),
				self.light(),
				self.stability(),
				self.branching()
			])
		return self._score


	@property
	def image(self):
		if not hasattr(self, '_image'):
			self.draw()
		return self._image


	@property
	def height(self):
		return max(0, max(self._states, key=lambda (heading, position): position[1])[1][1])


	@property
	def width(self):
		left = min(self._states, key=lambda (heading, position): position[0])[1][0]
		right = max(self._states, key=lambda (heading, position): position[0])[1][0]
		return abs(right - left)


	def efficiency(self):
		return 1.0 / len(self.code)


	def phototropism(self):
		return self.height


	# ratio of weight on left to weight on right
	def symmetry(self):
		xs = [p[0] for (h, p) in self._states]
		left = sum([abs(x) for x in xs if x < 0])
		right = sum([x for x in xs if x > 0])
		if left == 0 or right == 0:
			return 0.0
		return left / right if left < right else right / left


	# number of leaves (end segments) not shaded by other leaves
	def light(self):
		if len(self._leaves) == 0:
			return 0
		# TODO implement this better
		buckets = []
		for leaf_ind in self._leaves:
			leaf_x, leaf_y = self._states[leaf_ind][1]
			contains = False
			for other_x in buckets:
				if abs(other_x - leaf_x) < EPSILON:
					contains = True
					break
			if not contains:
				buckets.append(leaf_x)
		return len(buckets)


	def stability(self):
		# i don't know how to do this
		return 0


	# total number of branching points with more than one branch leaving
	def branching(self):
		pattern = r'(?=(F[+-F]*?\[[+-F]*[+-]+[+-F]*F[+-F]*\][+-F]*?F))'
		matches = [match.group(1) for match in re.finditer(pattern, self.code)]
		return len(matches)


	def draw(self):
		# init turtle
		t = turtle.Turtle()
		s = turtle.Screen()
		stack = []
		t.getscreen().clear()
		s.tracer(500, 0)
		t.hideturtle()
		t.speed(0)
		t.penup()
		t.left(90)
		t.setpos(0, -200)
		t.pencolor('#367132')

		# stores position and heading of turtle at each step
		self._states = []
		# indices into state array corresponding to leaves
		self._leaves = []

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
				# we assume these are leaves
				self._leaves.append(len(self._states)-1)
				t.penup()
				heading, position = stack.pop()
				t.setheading(heading)
				t.setpos(position)
				t.pendown()
			else:
				print 'not supported:', c

		self._image = s.getcanvas()
