#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess
import turtle
import numpy as np

from generator import lsys

MIN_STEP = 1
MAX_STEP = 20
MIN_ANGLE = 10
MAX_ANGLE = 40


class Drawer:

	def __init__(self):
		self.sample_params()


	def sample_params(self):
		self.step_size = np.random.rand() * (MAX_STEP - MIN_STEP) + MIN_STEP
		self.angle = np.random.rand() * (MAX_ANGLE - MIN_ANGLE) + MIN_ANGLE
		self.current, self.rules = lsys()


	def iterate(self, n):
		for i in range(n):
			for pat, reps in self.rules.items():
				rep = np.random.choice(reps)
				self.current = re.sub(pat, rep, self.current)
		self.current = re.sub('X', 'F', self.current)

		# redo if nothing gets drawn
		if 'F' not in self.current:
			self.sample_params()
			self.iterate(n)


	def draw(self):
		t = turtle.Turtle()
		s = turtle.Screen()
		stack = []

		# init turtle
		t.hideturtle()
		t.speed(0)
		t.penup()
		t.left(90)
		t.setpos(0, -200)
		t.pencolor('#367132')

		# draw
		for c in self.current:
			if c == 'F':
				t.forward(self.step_size)
			elif c == 'f':
				t.penup()
				t.forward(self.step_size)
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

		# save image
		cv = s.getcanvas()
		cv.postscript(file='tmp.ps', colormode='color')
		subprocess.call(['convert',
			'tmp.ps',
			'-gravity', 'Center',
			'-crop', '512x512+0+0',
			'tmp.png'
		])


if __name__ == '__main__':
	d = Drawer()
	d.iterate(5)
	print d.current
	d.draw()