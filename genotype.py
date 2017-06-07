#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import re
from phenotype import Phenotype
from lsys import chunk


# genotype is an l-system with axiom and production rules
class Genotype(object):

	def __init__(self, lsys):
		self.axiom = lsys[0]
		self.rules = lsys[1]


	def generate(self, env, max_iter=5, max_len=500):
		i = 0
		current = self.axiom
		while i < max_iter and len(current) < max_len:
			i += 1
			for lhs, rhs in self.rules.items():
				current = re.sub(lhs, rhs, current)
		current = re.sub('X', 'F', current)
		return Phenotype(current, env)


	def mutate(self):
		lhs = np.random.choice(self.rules.keys())
		rule = self.rules[lhs]
		if np.random.rand() < 0.5:
			i = self.random_symbol(rule)
			new_rule = rule[:i] + chunk() + rule[i+1:]
		else:
			i, j = self.random_subtree(rule)
			if i == -1:
				i = j = self.random_symbol(rule)
			new_rule = rule[:i] + chunk() + rule[j:]

		new_rules = {
			k : v if k != lhs else new_rule
			for k, v in self.rules.items()
		}
		return Genotype((self.axiom, new_rules))


	def crossover(self, other):
		new_rules = {}
		for lhs in self.rules.keys():
			self_rule = self.rules[lhs]
			other_rule = other.rules[lhs]
			self_i, self_j = self.random_subtree(self_rule)
			other_i, other_j = other.random_subtree(other_rule)
			if np.random.rand() < 0.5:
				new_axiom = self.axiom
				new_rule = self_rule[:self_i] + other_rule[other_i:other_j] + self_rule[self_j:]
			else:
				new_axiom = other.axiom
				new_rule = other_rule[:other_i] + self_rule[self_i:self_j] + other_rule[other_j:]
			new_rules[lhs] = new_rule
		return Genotype((new_axiom, new_rules))


	def random_symbol(self, rule):
		pattern = r'[+-F]'
		symbols = list(re.finditer(pattern, rule))
		if len(symbols) == 0:
			return -1
		t = np.random.choice(symbols)
		return t.start()


	def random_subtree(self, rule):
		pattern = r'\[[+-F]*\]'
		left_brackets = list(re.finditer(r'\[', rule))
		if len(left_brackets) == 0:
			return -1, -1

		start = np.random.choice(left_brackets).start()
		count = 0
		for i, c in enumerate(rule[start:]):
			if c == '[':
				count += 1
			elif c == ']':
				if count == 1:
					break
				count -= 1

		return start, start + i + 1

