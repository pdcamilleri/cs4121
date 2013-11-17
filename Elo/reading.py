#!/usr/bin/env python

import sys

# create a link in the graph from src to dest
def create_link(graph, src, dest):
  if src in graph:
    graph[src].append(dest)
  else:
    # entry doesnt exist, so create it and add dest
    graph[src] = [dest]


graph = {}

try:
  sys.argv[1]
except IndexError:
  filename = 'training_data.csv'
else:
  filename = sys.argv[1]

f = open(filename, 'r')
f.readline() # skip first line with meta data

for line in f:
#  print line,
  (month, white, black, result) = line.split(',')
  if result == 1: # white has won, so create link black -->> white
    create_link(graph, black, white)
  elif result == 0: # black won, create link white --> black
    create_link(graph, white, black)
  else: # draw, create links back and forth white <<-->> black
    create_link(graph, black, white)
    create_link(graph, white, black)

print 'showing graph\n\n'
for key in sorted(graph.keys(), key=int):
  print key, graph[key]
#print key, len(graph[key])




