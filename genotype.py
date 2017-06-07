#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import re
from phenotype import Phenotype
from lsys import chunk


# genotype is an l-system with axiom and production rules
class Genotype(object):

	def __init__(self, rule):
		self.axiom = 'F'
		self.rule = rule


	def __eq__(self, other):
		return self.rule == other.rule


	def generate(self, step, angle, max_iter=5, max_len=500):
		i = 0
		current = self.axiom
		while i < max_iter and len(current) < max_len:
			i += 1
			current = re.sub('F', self.rule, current)
		return Phenotype(current, step, angle)


	def mutate(self):
		if np.random.rand() < 0.5:
			i = self.random_symbol()
			new_rule = self.rule[:i] + chunk() + self.rule[i+1:]
		else:
			i, j = self.random_subtree()
			if i == -1:
				i = j = self.random_symbol()
			new_rule = self.rule[:i] + chunk() + self.rule[j:]
		return Genotype(new_rule)


	def crossover(self, other):
		self_i, self_j = self.random_subtree()
		other_i, other_j = other.random_subtree()
		if np.random.rand() < 0.5:
			new_rule = self.rule[:self_i] + other.rule[other_i:other_j] + self.rule[self_j:]
		else:
			new_rule = other.rule[:other_i] + self.rule[self_i:self_j] + other.rule[other_j:]
		return Genotype(new_rule)


	def random_symbol(self):
		pattern = r'[+-F]'
		symbols = list(re.finditer(pattern, self.rule))
		if len(symbols) == 0:
			return -1
		t = np.random.choice(symbols)
		return t.start()


	def random_subtree(self):
		pattern = r'\[[+-F]*\]'
		left_brackets = list(re.finditer(r'\[', self.rule))
		if len(left_brackets) == 0:
			return -1, -1

		start = np.random.choice(left_brackets).start()
		count = 0
		for i, c in enumerate(self.rule[start:]):
			if c == '[':
				count += 1
			elif c == ']':
				if count == 1:
					break
				count -= 1

		return start, start + i + 1

