#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import re


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-1.0 * x))


# phenotype is a string that has been generated from an l-system
class Phenotype(object):
    def __init__(self, code, env):
        self.code = code
        self.env = env
        # stores position and heading of turtle at each step
        self._states = []

        self.draw()
        self.features = np.array([
            self.efficiency(),
            self.phototropism(),
            self.symmetry(),
            self.light(),
            self.branching()
        ])

    def __eq__(self, other):
        return self.code == other.code

    @property
    def height(self):
        if len(self._states) == 0:
            return 0.0
        h = max(self._states, key=lambda state: state[1][1])[1][1]
        return self.env.max_height * sigmoid(h)

    @property
    def width(self):
        if len(self._states) == 0:
            return 0.0
        left = min(self._states, key=lambda state: state[1][0])[1][0]
        right = max(self._states, key=lambda state: state[1][0])[1][0]
        w = abs(right - left)
        return self.env.max_width * sigmoid(w)

    def efficiency(self):
        return 0.0 if len(self.code) == 0 else 1.0 / len(self.code)

    def phototropism(self):
        return self.height

    # ratio of weight on left to weight on right
    def symmetry(self):
        # indices into state array corresponding to nodes
        pattern = r'F'
        nodes = [self._states[match.start()] for match in re.finditer(pattern, self.code)]
        if len(nodes) == 0:
            return 0

        xs = [p[0] for (h, p) in nodes]
        left = sum([abs(x) for x in xs if x < 0])
        right = sum([x for x in xs if x > 0])
        if left == 0 or right == 0:
            return 0.0
        return left / right if left < right else right / left

    # number of leaves (end segments) not shaded by other leaves
    def light(self):
        # indices into state array corresponding to leaves
        pattern = r'F[+-F]*\]'
        leaves = [match.end() - 1 for match in re.finditer(pattern, self.code)]
        if len(leaves) == 0:
            return 0

        # TODO implement this better
        # also count shading by stem/branch?
        buckets = []
        for leaf_ind in leaves:
            leaf_x, leaf_y = self._states[leaf_ind][1]
            contains = False
            for other_x in buckets:
                if abs(other_x - leaf_x) < self.env.leaf_size:
                    contains = True
                    break
            if not contains:
                buckets.append(leaf_x)
        return len(buckets)

    # total number of branching points with more than one branch leaving
    def branching(self):
        pattern = r'(?=(F[+-F]*?\[[+-F]*[+-]+[+-F]*F[+-F]*\][+-F]*?F))'
        matches = [match.group(1) for match in re.finditer(pattern, self.code)]
        return len(matches)

    def draw(self):
        state = (90, (0, 0))
        self._states.append(state)
        stack = []

        for c in self.code:
            self._states.append(state)
            if c == 'F':
                x, y = state[1]
                x -= self.env.step * np.cos(self.env.angle)
                y -= self.env.step * np.sin(self.env.angle)
                state = (state[0], (x, y))
            elif c == 'X':
                continue
            elif c == '+':
                h = state[0] + self.env.angle
                state = (h, state[1])
            elif c == '-':
                h = state[0] - self.env.angle
                state = (h, state[1])
            elif c == '[':
                stack.append(state)
            elif c == ']':
                state = stack.pop()
            else:
                print('not supported:', c)

