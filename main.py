#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

import numpy as np
from flask import Flask, jsonify, request

from crossdomain import crossdomain
from genotype import Genotype
from lsys import lsys

app = Flask(__name__)


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / np.sum(e_x)


class Environment(object):  # TODO compute params from input here
    def __init__(self, input):
        self.step = 5.0
        self.angle = 0.396
        self.weights = np.array([0.1, 0.1, 0.2, 0.3, 0.3])
        self.elitism_rate = 0.25
        self.mutation_rate = 0.2  # TODO mutation rate should be per codon
        self.pop_size = 400
        self.max_height = 300.0
        self.max_width = 500.0
        self.leaf_size = 10.0


# ENV = Environment(5.0, 0.396,  # step and angle
#                   np.array([  # scoring weights
#                     0.1,
#                     0.1,
#                     0.2,
#                     0.3,
#                     0.3,
#                   ]),
#                   0.25, 0.2, 400,  # pop rates and size
#                   300.0, 500.0, 10.0)  # size and leaf


def get_scores(population, env):
    features = np.array([g.generate(env).features for g in population])
    features = np.apply_along_axis(softmax, 0, features)
    return np.dot(features, env.weights).tolist()


# TODO yield population on each generation -> can we stream to the FE?
def evolve(env, generations=10):
    # random starting population
    population = [Genotype(lsys()) for j in range(env.pop_size)]
    n = int(env.elitism_rate * env.pop_size)

    # rank descending by fitness score
    scores = get_scores(population, env)
    population = sorted(population, key=lambda g: scores[population.index(g)], reverse=True)
    scores = sorted(scores, reverse=True)

    for i in range(generations):
        print 'generation', i
        print 'best score:', scores[0]
        print 'best rule:', population[0].rules
        print '============='
        # save_image(population[0].generate(env), filename='gen_{:02d}'.format(i))

        # bottom n get tossed, top n go through unchanged
        population = population[:-n]
        scores = scores[:-n]
        probs = softmax(scores)
        new_pop = population[:n]

        # rest are product of crossover + mutation
        for j in range(n, env.pop_size):
            parents = np.random.choice(population, 2, p=probs)
            new_g = parents[0].crossover(parents[1])
            new_pop.append(new_g.mutate() if np.random.rand() < env.mutation_rate else new_g)

        scores = get_scores(new_pop, env)
        population = sorted(new_pop, key=lambda g: scores[new_pop.index(g)], reverse=True)
        scores = sorted(scores, reverse=True)

    return population


@app.route("/plants", methods=["POST", "OPTIONS"])
@crossdomain(origin="*", headers="Content-Type")
def plants():
    input = request.get_json()
    gens = input['generations']
    env = Environment(input)
    population = evolve(env, gens)
    return jsonify({'results': [g.generate(env).code for g in population]})


def save_image(phenotype, filename='tmp'):
    cv = phenotype.image
    ps_file = 'output/{}.ps'.format(filename)
    png_file = 'output/{}.png'.format(filename)
    cv.postscript(file=ps_file, colormode='color')
    subprocess.call(['convert',
                     ps_file,
                     '-gravity', 'Center',
                     '-crop', '600x600+0+0',
                     png_file
                     ])
    subprocess.call(['rm', '-r', ps_file])

app.run()

# if __name__ == '__main__':
#     population = evolve(env)
#     print 'final best rule:', population[0].rules
#     for g in population[:10]:
#         save_image(g.generate(env),
#                    filename='{},{}'.format(g.rules['F'], g.rules['X']))
