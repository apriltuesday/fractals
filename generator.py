#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess
import turtle
import numpy as np

MIN_STEP = 1
MAX_STEP = 20
MIN_ANGLE = 10
MAX_ANGLE = 40


class Generator:

	def __init__(self):
		self.sample_params()

	def sample_params(self):
		self.step_size = np.random.rand() * (MAX_STEP - MIN_STEP) + MIN_STEP
		self.angle = np.random.rand() * (MAX_ANGLE - MIN_ANGLE) + MIN_ANGLE
		self.rules = {
			'F': 'F[+F]F[-F]F',
		}
		self.current = 'F'


	def iterate(self, n):
		for i in range(n):
			for pat, rep in self.rules.items():
				self.current = re.sub(pat, rep, self.current)


	def draw(self):
		t = turtle.Turtle()
		s = turtle.Screen()
		stack = []

		t.hideturtle()
		t.speed(0)
		t.penup()
		t.left(90)
		t.setpos(0, -200)
		t.pencolor('#367132')

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

		cv = s.getcanvas()
		cv.postscript(file='tmp.ps', colormode='color')
		subprocess.call(['convert',
			'tmp.ps',
			'-gravity', 'Center',
			'-crop', '512x512+0+0',
			'tmp.png'
		])


if __name__ == '__main__':
	gen = Generator()
	gen.iterate(3)
	print gen.current
	print gen.step_size, gen.angle
	gen.draw()