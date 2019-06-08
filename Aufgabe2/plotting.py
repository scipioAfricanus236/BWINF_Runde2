import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('Aufgabe2/findBestSeq.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[1]))
        y.append(int(row[0]))

plt.plot(x,y, label='Loaded from file!')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()