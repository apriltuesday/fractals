#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess
import numpy as np

from lsys import lsys
from phenotype import Phenotype
from genotype import Genotype

MIN_STEP = 1
MAX_STEP = 20
MIN_ANGLE = 10
MAX_ANGLE = 40
MAX_STRING_LENGTH = 500


def evolve(generations=10, pop_size=400, elitism_rate=0.1, mutation_rate=0.5):
	# random starting population
	population = [Genotype(lsys()[1]['F'][0]) for j in range(pop_size)]
	n = int(elitism_rate * pop_size)

	for i in range(generations):
		print 'generation', i
		# rank descending by fitness score
		scores = [g.generate().score() for g in population]
		population = sorted(population, key=lambda g: scores[population.index(g)], reverse=True)
		scores = sorted(scores, reverse=True)
		print 'best score:', scores[0]
		print 'best rule:', population[0].rule
		print '============='

		# bottom n get tossed, top n go through unchanged
		population = population[:-n]
		scores = scores[:-n]
		probs = np.array(scores) / np.sum(scores)
		new_pop = population[:n]

		# rest are product of crossover + mutation
		for j in range(n, pop_size):
			parents = np.random.choice(population, 2, p=probs)
			new_g = parents[0].crossover(parents[1])
			new_pop.append(new_g.mutate() if np.random.rand() < mutation_rate else new_g)

		population = new_pop

	return population


def save_image(phenotype, filename='tmp'):
	cv = phenotype.image
	ps_file = 'output/{}.ps'.format(filename)
	png_file = 'output/{}.png'.format(filename)
	cv.postscript(file=ps_file, colormode='color')
	subprocess.call(['convert',
		ps_file,
		'-gravity', 'Center',
		'-crop', '512x512+0+0',
		png_file
	])
	subprocess.call(['rm', '-r', ps_file])


if __name__ == '__main__':
	#'F[+F]F[-F]F'

	population = evolve()
	for g in population[:10]:
		save_image(g.generate(), filename=g.rule)
