#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from numpy import random

# TODO: want to encourage height, less turning, less backtracking

variables = ['F', 'X']
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
		return [clean(chunk())]
	return [chunk()] + productions()

def chunk():
	n = random.rand()
	if n < 0.25:
		return symbol()
	if n < 0.5:
		return branch()
	return symbol() + chunk()

def branch():
	n = random.rand()
	if n < 0.5:
		return '[{}]'.format(chunk())
	return '[{}]{}'.format(chunk(), chunk())

def symbol():
	n = random.rand()
	if n < 0.6:
		return random.choice(variables)
	return random.choice(rotations)


def clean(s):
	s = re.sub(r'[+]+', '+', s)
	s = re.sub(r'[-]+', '-', s)
	s = re.sub(r'\+\-|\-\+', '', s)
	s = re.sub(r'\[(\+|\-)\]', '', s)
	s = re.sub(r'\[\]', '', s)
	print s
	return s

