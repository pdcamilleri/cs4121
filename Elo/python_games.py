#!/usr/bin/env python
# converts a file that contains one item of data per line, for 14 lines
# and produces a pipe delimited file
# eg
# cat example_file
# col1
# col2
# ...
# col14
# becomes
# col1|col2|...|col14

f = open('all2013games', 'r')

i = 0
game = []
for line in iter(f):
  line = line.rstrip()
  game.append(line)
  i += 1
  if i == 14:
    print '|'.join(map(str,game))
    game = []
    i = 0
    



