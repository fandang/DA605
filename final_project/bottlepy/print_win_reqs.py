import sqlite3
import numpy as np
import matplotlib.pyplot as plt

db_url = 'da602.sqlite'
conn = sqlite3.connect(db_url)
c = conn.cursor()

c.execute('select seed, team, percent_picked from PICKS_2016')
picks_results = c.fetchall()

seeds = []
teams = []
probs = []

team_sample = []

for picks_row in picks_results:
	seeds.append(int(picks_row[0]))
	teams.append(picks_row[1])
	probs.append(float(picks_row[2]))

print(probs)

# make probs add to 1
multiplier = (1.0/sum(probs))

numpy_probs = np.asarray(probs)

numpy_probs = numpy_probs * multiplier
print(sum(numpy_probs))

seed_sums = []

for i in range(0, 99000):
	four_seeds = np.random.choice(seeds, 4, p=numpy_probs)
	four_seeds_sum = sum(four_seeds)
	seed_sums.append(four_seeds_sum)
	#print four_seeds_sum 

plt.hist(seed_sums, normed=1, bins=15)
plt.title("Peoples Real Picks Sums Histogram")
plt.xlabel("Sum")
plt.ylabel("Frequency")
plt.show()

conn.commit()
conn.close()
