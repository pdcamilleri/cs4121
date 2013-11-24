#!/usr/bin/env python

# runs a modified version of PageRank on the chess games played 
# by the current top 50 chess grandmasters in 2012
# The modifications made in this file are:
#    1) weighting multiple wins
#    2) down weighting links produced by draws to 1/2 of that of a win
#
# format is of the data file is
# View|Date|White|Black|W ELO|B ELO|Av ELO|Event|Site|ECO|Opening|Round|Res|# Mvs


import sys
import pprint as pprint
import numpy
from collections import Mapping

def get_file():
  try:
    sys.argv[1]
  except IndexError:
    filename = 'training_data.csv'
  else:
    filename = sys.argv[1]

  f = open(filename, 'r')
  return f

# create a link in the graph from src to dest
def create_link(graph, src, dest):
  if src in graph:
    graph[src].append(dest)
  else:
    # entry doesnt exist, so create it and add dest
    graph[src] = [dest]

# do a mapping to the first n natural numbers
# if the player numbers are not continuous, 
# eg 1, 3, 4, 5, 7 -->> 0, 1, 2, 3, 4
def fix_up_ids(graph, players):
  player_ids = sorted(players)

  for key in sorted(graph.keys()):
    outgoing_links = graph[key]
    updated_links = [player_ids.index(link) for link in outgoing_links]
    graph[player_ids.index(key)] = updated_links
    del graph[key]
  return player_ids

# displays a graph of the form { node: [adjacency list], ... }
def show_graph(graph):
  for key in graph.keys():
    print key, graph[key]
    print

# prints the sum of each row to check that it sums to 1.0, hence being row stochastic
def check_row_stochastic(matrix):
  for row in matrix:
    sum = 0
    for item in row:
      sum += item
    print sum




# taken from StackOverflow
# http://stackoverflow.com/questions/10306672/
# how-do-you-iterate-over-two-dictionaries-and-grab-the-values-at-the-same-path
def treeZip(t1,t2):
  if isinstance(t1,Mapping) and isinstance(t2,Mapping):
    assert set(t1)==set(t2)
    for k,v1 in t1.items():
      v2 = t2[k]
      for tuple in treeZip(v1,v2):
        yield tuple
  else:
    yield (t1,t2)

# graph, represented as an adjacency list
graph = {}
draw_graph = {}
players = set()
alpha = 0.99
draw_weighting = 1.0 / 2.0
win_weighting = 1.0

f = get_file()
f.readline() # skip first line with meta data

# turn the file in an adjacency list
for line in f:
  (_,_,white,black,_,_,_,_,_,_,_,_,result,_) = line.rstrip().split('|')

  # keep track of all players in our graph
#white = int(white)
#  black = int(black)
  result = result[0]
  players.add(white)
  players.add(black)

  if result == '1': # white has won, so create link black -->> white
    create_link(graph, black, white)
  elif result == '0': # black won, create link white --> black
    create_link(graph, white, black)
  else: # draw, create links back and forth white <<-->> black
    create_link(draw_graph, black, white)
    create_link(draw_graph, white, black)

# make sure that dangling nodes are included in our graph with empty adjacency lists
for player in players:
  if player not in graph.keys():
    graph[player] = [] 
  if player not in draw_graph.keys():
    draw_graph[player] = [] 

#reverse_graph = {}
#for k, v in graph.iteritems():
#   for player in v:
#     create_link(reverse_graph, player, k)


# do a mapping to the first n natural numbers
# if the player numbers are not continuous, 
# eg 1, 3, 4, 5, 7 -->> 0, 1, 2, 3, 4
player_ids = fix_up_ids(graph, players)
player_ids = fix_up_ids(draw_graph, players)

show_graph(graph)
print "--"
show_graph(draw_graph)
print player_ids



# remove duplicate losses/links from the list
#for k, v in graph.iteritems():
#   print len(v) - len(list(set(v)))
#   graph[k] = list(set(v))

num_players = len(players)

# create a matrix G1 where the i-th row contains 1 / #(Pi) in the j-th col
# if there is a link from i to j
g_1 = [[0 for i in range(num_players)] for j in range(num_players)]



# we use the win_weighting and the draw_weighting to keep
# the matrix row stochastic
for key, value in graph.iteritems():
  wins = value
  draws = draw_graph[key]
  total_games = (len(wins) * win_weighting) + (len(draws) * draw_weighting)
  for player in wins:
    g_1[key][player] += win_weighting / total_games
  for player in draws:
    g_1[key][player] += draw_weighting / total_games

# g_1 matrix complete

# G_2 is the same matrix but with the dangling webpages handled

# create a copy of g_1
# list comprehension says
# if the row is empty then each entry is 1 / total_number of players
# else just make a copy of the row
g_2 = [[1.0 / num_players] * num_players if all([i == 0 for i in row]) else row[:] for row in g_1]

#pprint.pprint(g_2)

check_row_stochastic(g_2)
# all rows sum to 1, as expected

# create actual matrix G where chance to jump to random link is 1-alpha/M

g = [[( (alpha * entry) + ((1-alpha)/num_players) ) for entry in row] for row in g_2] 

pprint.pprint(g)


#for row in g:
#  sum = 0
#  for item in row:
#    sum += item
#  print sum


x = [0] * num_players
x[0] = 1
iterations = 0

while True:
  iterations += 1
  x_tmp = numpy.dot(x, g)
  dist = numpy.linalg.norm(x-x_tmp)
  if dist < 0.00000001:
    break
  x = x_tmp

print iterations, "iterations"
for player, ranking in zip(player_ids, x):
#print "%30s: %10.8lf" % (player, ranking)
  print " %10.8lf: %s" % (ranking, player)










































