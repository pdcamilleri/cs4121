#!/usr/env/python
# compares current FIDE rankings with those produced by the pagerank algo

def get_FIDE_rankings():
   rankings = {}
   ordering = {} 
   f = open('FIDE_rankings.txt', 'r')

   for line in f:
      (rank, lastname, firstname, rating) = line.rstrip().rstrip(',').split(' ')
      rankings[lastname + ' ' + firstname] = [rank, rating]
      ordering[rank] = lastname + ' ' + firstname
   return (rankings, ordering)

def get_pagerank_rankings():
   rankings = {}
   f = open('chessranks.2012.txt', 'r')

   for line in f:
      (rank, rating, lastname, firstname) = line.rstrip().rstrip(',').split(' ')
      rating = rating.replace(':', '')
      rankings[lastname + ' ' + firstname] = [rank, rating]
   return rankings



(FIDE_rankings, ordering) = get_FIDE_rankings()

pagerank_rankings = get_pagerank_rankings()

#for k,v in pagerank_rankings.iteritems():
#   print k, "-->>", v

total_error = 0
players_ranked = 0
for ranking in (sorted(ordering, key=int))[:10]:
   player = ordering[ranking]
   print ordering[ranking], '&', FIDE_rankings[player][0], '&',
   try:
      diff = abs(int(FIDE_rankings[player][0]) - int(pagerank_rankings[player][0]))
      print pagerank_rankings[player][0], '&', diff,
      total_error += diff
      players_ranked += 1
   except:
      print 'not ranked', '&', '-',
   print ' \\\\ '


print "total difference =", total_error
print "total difference / players = ", total_error, " / ", players_ranked, " = ", total_error / (players_ranked * 1.0)



