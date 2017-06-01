#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import re
from phenotype import Phenotype


# genotype is an l-system with axiom and production rules
class Genotype:

	def __init__(self, rule):
		self.axiom = 'F'
		self.rule = rule

	def generate(self, max_iter=5, max_len=500):
		i = 0
		current = self.axiom
		while i < max_iter and len(current) < max_len:
			i += 1
			current = re.sub('F', self.rule, current)
		return Phenotype(current)

	def random_subtree(self): #for mutation & recombination
		pass