#!/usr/bin/env python

import numpy

a = [1, 1, 1, 1, 1];
b = [[1], [1], [1], [1], [1]];

print numpy.dot(a, b);

j = [ [0, 1, 0],
      [0, 0, 1],
      [0, 0, 0]
    ]

print a
print b
print j

print numpy.dot(j, j)
  
print numpy.transpose(numpy.transpose(a))

print numpy.outer(a, a)


