#!/usr/env/python
# compares FIDEs Elo ranking with those produced by PageRank
# by predicting the outcome of all win/loss matches played in 2013

import sys
import pprint as pprint
import numpy
import re

# some players names have been changed from Last, First Middle to Last FirstMiddle
# this just changes it back to the correct format
def correct_names(firstname, lastname):
   pattern = re.compile(r'([a-z])([A-Z])')
   lastname = pattern.sub(r'\1 \2', lastname)
   firstname = pattern.sub(r'\1 \2', firstname)
   return (firstname, lastname)
         

def get_FIDE_rankings():
   rankings = {}
   ordering = {} 
   f = open('FIDE_rankings.txt', 'r')

   for line in f:
      (rank, lastname, firstname, rating) = line.rstrip().rstrip(',').split(' ')
      (firstname, lastname) = correct_names(firstname, lastname)
      rankings[lastname + ' ' + firstname] = [rank, rating]
      ordering[rank] = lastname + ' ' + firstname
   return (rankings, ordering)

def get_pagerank_rankings():
   rankings = {}
   f = open('chessranks.2012.txt', 'r')

   for line in f:
      (rank, rating, lastname, firstname) = line.rstrip().rstrip(',').split(' ')
      (firstname, lastname) = correct_names(firstname, lastname)
      rating = rating.replace(':', '')
      rankings[lastname + ' ' + firstname] = [rank, rating]
   return rankings

def get_predicted_winner(rankings, player_a, player_b):
   try:
      a_rank = rankings[player_a][0]
      b_rank = rankings[player_b][0]
      if int(a_rank) < int(b_rank):
         return player_a
      else:
         return player_b
   except KeyError:
      return None

def get_file():
  try:
    sys.argv[1]
  except IndexError:
    filename = 'games_2013.txt'
  else:
    filename = sys.argv[1]

  f = open(filename, 'r')
  return f


(FIDE_rankings, ordering) = get_FIDE_rankings()

pagerank_rankings = get_pagerank_rankings()

#for k,v in pagerank_rankings.iteritems():
#   print k, "-->>", v

#print get_predicted_winner(pagerank_rankings, 'Carlsen, Magnus', 'Aronian, Levon')
# wrong
#print get_predicted_winner(pagerank_rankings, 'Carlsen, Magnus', 'Leko, Peter')

f = get_file()
pagerank_correct_predictions = 0
fide_correct_predictions = 0
total_predictions = 0

for line in f:
   (_,_,white,black,_,_,_,_,_,_,_,_,result,_) = line.rstrip().split('|')
   total_predictions += 1
   result = result[0]
   pagerank_prediction = get_predicted_winner(pagerank_rankings, white, black)
   fide_prediction = get_predicted_winner(FIDE_rankings, white, black)
   if result == '1':
      if pagerank_prediction == white:
         pagerank_correct_predictions += 1
      if fide_prediction == white:
         fide_correct_predictions += 1
   elif result == '0':
      if pagerank_prediction == black:
         pagerank_correct_predictions += 1
      if fide_prediction == black:
         fide_correct_predictions += 1
   else: # ignore draws 
      total_predictions -= 1


print "FIDE", fide_correct_predictions, " / ", total_predictions, " = ", fide_correct_predictions / (1.0 * total_predictions)
print "PageRank", pagerank_correct_predictions, " / ", total_predictions, " = ", pagerank_correct_predictions / (1.0 * total_predictions)




















