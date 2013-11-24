
#f = open('pageranks.orig.2012.txt', 'r')
f = open('chessranks.2012.txt', 'r')

for line in f:
   (rank, _, pagerank, player, last) = line.rstrip().split(' ')
   pagerank = pagerank[:-1]
   print rank, '&', player, last, '&', pagerank, '\\\\'
