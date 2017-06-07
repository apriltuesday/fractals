#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess
import numpy as np

from lsys import lsys
from genotype import Genotype


def softmax(x):
	e_x = np.exp(x - np.max(x))
	return e_x / np.sum(e_x)


ENVIRONMENT = {
	'step': 5.0,
	'angle': 22.7,
	'weights': np.array([
		0.05,
		0.05,
		0.3,
		0.3,
		0.3
	]),
	'elitism_rate': 0.2,
	'mutation_rate': 0.2,
}


def get_scores(population, env):
	features = np.array([g.generate(env['step'], env['angle']).features for g in population])
	features = np.apply_along_axis(softmax, 0, features)
	return np.dot(features, env['weights']).tolist()


def evolve(env, generations=10, pop_size=500):
	elitism_rate = env['elitism_rate']
	mutation_rate = env['mutation_rate']

	# random starting population
	population = [Genotype(lsys()[1]['F'][0]) for j in range(pop_size)]
	n = int(elitism_rate * pop_size)

	# rank descending by fitness score
	scores = get_scores(population, env)
	population = sorted(population, key=lambda g: scores[population.index(g)], reverse=True)
	scores = sorted(scores, reverse=True)

	for i in range(generations):
		print 'generation', i
		print 'best score:', scores[0]
		print 'best rule:', population[0].rule
		print '============='
		save_image(population[0].generate(env['step'], env['angle']), filename='gen_{:02d}'.format(i))

		# bottom n get tossed, top n go through unchanged
		population = population[:-n]
		scores = scores[:-n]
		probs = softmax(scores)
		new_pop = population[:n]

		# rest are product of crossover + mutation
		for j in range(n, pop_size):
			parents = np.random.choice(population, 2, p=probs)
			new_g = parents[0].crossover(parents[1])
			new_pop.append(new_g.mutate() if np.random.rand() < mutation_rate else new_g)

		scores = get_scores(new_pop, env)
		population = sorted(new_pop, key=lambda g: scores[new_pop.index(g)], reverse=True)
		scores = sorted(scores, reverse=True)

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
	population = evolve(ENVIRONMENT)
	print 'final best rule:', population[0].rule
	for g in population[:10]:
		save_image(g.generate(ENVIRONMENT['step'], ENVIRONMENT['angle']), filename=g.rule)
