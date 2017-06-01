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


def evolve():
	pass
	# generate a random population
	# evaluate fitness (generate individuals and score, or just expected values...)
	# recombine and mutate production rules


def save_image(phenotype):
	cv = phenotype.image
	cv.postscript(file='tmp.ps', colormode='color')
	subprocess.call(['convert',
		'tmp.ps',
		'-gravity', 'Center',
		'-crop', '512x512+0+0',
		'tmp.png'
	])


if __name__ == '__main__':
	#step_size = np.random.rand() * (MAX_STEP - MIN_STEP) + MIN_STEP
	#angle = np.random.rand() * (MAX_ANGLE - MIN_ANGLE) + MIN_ANGLE

	#'F[+F]F[-F]F'
	axiom, rules = lsys()
	g = Genotype(rules['F'][0])
	p = g.generate()
	print p.code
	print p.score()
	save_image(p)
