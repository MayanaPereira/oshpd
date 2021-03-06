import ocsv
import sys

# argv[1] - input file
# argv[2] - name of the column to be flipped
# argv[3] - output file

fin = open(sys.argv[1], 'r')

col = ocsv.getColumns(fin.readline())
flipCol = col[sys.argv[2]]

currentpid = ''
# list of list of list
seqs = []
def func(line):
  global currentpid, seqs
  row = line.strip().split(',')
  pid = row[col['PID']]
  if pid == currentpid:
    seqs[-1][0].append(row[flipCol])
    seqs[-1][1].append(row[col['thirtyday']])
  else:
    seqs.append([[row[flipCol]], [row[col['thirtyday']]]])
  currentpid = pid

ocsv.runFunc(fin, func)
fin.close()

freq = dict()
fout = open(sys.argv[3], 'w')
for seq in seqs:
  # skip sequence longer than 100
  if len(seq[0]) >= 50: continue
  # take the last 7 items only
  #if len(seq[0]) > 7: seq[0] = seq[0][-7:]
  for i in range(len(seq[0])):
    for j in range(len(seq[0]) - i):
      key = ','.join(seq[0][j:j + i + 1]) + ',' + seq[1][j + i] 
      dum = fout.write(key + '\n') 
      if key in freq:
        freq[key] = freq[key] + 1
      else:
        freq[key] = 1

fout.close()

posseqs = []
for item in freq.items():
  if item[0][-1] == '1':
    key = item[0][0:-1] + '0'
    if key not in freq: continue
    count0 = freq[key]
    prob = item[1] / (item[1] + count0)
    if prob > 0.5: posseqs.append(item[0])
