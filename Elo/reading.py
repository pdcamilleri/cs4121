#!/usr/bin/env python

import sys
import pprint as pprint

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


def fix_up_ids(graph, players):
  player_ids = sorted(players)

  for key in sorted(graph.keys()):
    outgoing_links = graph[key]
    updated_links = [player_ids.index(link) for link in outgoing_links]
    graph[player_ids.index(key)] = updated_links
    del graph[key]

# graph, represented as an adjacency list
graph = {}
players = set()

f = get_file()
f.readline() # skip first line with meta data

# turn the file in an adjacency list
for line in f:
  (month, white, black, result) = line.rstrip().split(',')
  # keep track of all players in our graph
  white = int(white)
  black = int(black)
  players.add(white)
  players.add(black)

  if result == '1': # white has won, so create link black -->> white
    create_link(graph, black, white)
  elif result == '0': # black won, create link white --> black
    create_link(graph, white, black)
  else: # draw, create links back and forth white <<-->> black
    create_link(graph, black, white)
    create_link(graph, white, black)

# make sure that dangling nodes are included in our graph with empty adjacency lists
for player in players:
  if player not in graph.keys():
    graph[player] = [] 

# do a mapping to the first n natural numbers
# if the player numbers are not continuous, 
# eg 1, 3, 4, 5, 7 -->> 0, 1, 2, 3, 4
fix_up_ids(graph, players)

print 'showing graph\n\n'
for key in sorted(graph.keys(), key=int):
  print key, graph[key]

num_players = len(players)
print num_players

# create a matrix G1 where the i-th row contains 1 / #(Pi) in the j-th col
# if there is a link from i to j
g_1 = [[0 for i in range(num_players)] for j in range(num_players)]

for key, value in graph.iteritems():
  for player in value:
    g_1[key][player] = 1.0 / len(value)
  print key, "-->>", value

pprint.pprint(g_1)

# g_1 matrix complete

# G_2 is the same matrix but with the dangling webpages handled

# create a copy of g_1
# list comprehension says
# if the row is empty then each entry is 1 / total_number of players
# else just make a copy of the row
g_2 = [[1.0 / num_players] * num_players if all([i == 0 for i in row]) else row[:] for row in g_1]

pprint.pprint(g_2)

for row in g_2:
  sum = 0
  for item in row:
    sum += item
  print sum

# all rows sum to 1, as expected






































