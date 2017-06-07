#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import re
import turtle

def sigmoid(x):
	return 1.0 / (1.0 + np.exp(-1.0*x))


# phenotype is a string that has been generated from an l-system
class Phenotype(object):

	def __init__(self, code, env):
		self.code = code
		self.env = env

		self.draw()
		self.features = np.array([
			self.efficiency(),
			self.phototropism(),
			self.symmetry(),
			self.light(),
			self.branching()
		])


	def __eq__(self, other):
		return self.code == other.code


	@property
	def image(self):
		if not hasattr(self, '_image'):
			self.draw()
		return self._image


	@property
	def height(self):
		if len(self._states) == 0:
			return 0.0
		h = max(self._states, key=lambda (heading, position): position[1])[1][1]
		return self.env.max_height * sigmoid(h)


	@property
	def width(self):
		if len(self._states) == 0:
			return 0.0
		left = min(self._states, key=lambda (heading, position): position[0])[1][0]
		right = max(self._states, key=lambda (heading, position): position[0])[1][0]
		w = abs(right - left)
		return self.env.max_width * sigmoid(w)


	def efficiency(self):
		return 0.0 if len(self.code) == 0 else 1.0 / len(self.code)


	def phototropism(self):
		return self.height


	# ratio of weight on left to weight on right
	def symmetry(self):
		# indices into state array corresponding to nodes
		pattern = r'F'
		nodes = [self._states[match.start()] for match in re.finditer(pattern, self.code)]
		if len(nodes) == 0:
			return 0

		xs = [p[0] for (h, p) in nodes]
		left = sum([abs(x) for x in xs if x < 0])
		right = sum([x for x in xs if x > 0])
		if left == 0 or right == 0:
			return 0.0
		return left / right if left < right else right / left


	# number of leaves (end segments) not shaded by other leaves
	def light(self):
		# indices into state array corresponding to leaves
		pattern = r'F[+-F]*\]'
		leaves = [match.end()-1 for match in re.finditer(pattern, self.code)]
		if len(leaves) == 0:
			return 0

		# TODO implement this better
		# also count shading by stem/branch?
		buckets = []
		for leaf_ind in leaves:
			leaf_x, leaf_y = self._states[leaf_ind][1]
			contains = False
			for other_x in buckets:
				if abs(other_x - leaf_x) < self.env.leaf_size:
					contains = True
					break
			if not contains:
				buckets.append(leaf_x)
		return len(buckets)


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
		t.setpos(0, -250)
		t.pencolor('#367132')

		# stores position and heading of turtle at each step
		self._states = []

		# draw
		for c in self.code:
			self._states.append((t.heading(), t.pos()))
			if c == 'F':
				t.forward(self.env.step)
			elif c == 'f': #not currently used
				t.penup()
				t.forward(self.env.step)
				t.pendown()
			elif c == '+':
				t.left(self.env.angle)
			elif c == '-':
				t.right(self.env.angle)
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
