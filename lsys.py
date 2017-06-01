#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import random


# grammar for generating an l-system
# slightly more general than what we use in the evolution

variables = ['F']
rotations = ['+', '-']

def lsys():
	return axiom(),	{
		v : productions()
		for v in variables
	}

def axiom():
	return random.choice(variables)

def productions():
	n = random.rand()
	if n < 0.5:
		return [chunk()]
	return [chunk()] + productions()

def chunk():
	n = random.rand()
	if n < 1.0 / 3.0:
		return symbol()
	if n < 2.0 / 3.0:
		return branch()
	return symbol() + chunk()

def branch():
	n = random.rand()
	if n < 0.5:
		return '[{}]'.format(chunk())
	return '[{}]{}'.format(chunk(), chunk())

def symbol():
	n = random.rand()
	if n < 0.5:
		return random.choice(variables)
	return random.choice(rotations)
