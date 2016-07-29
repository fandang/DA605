import sqlite3
from bottle import route, install, template, run, view, Bottle, static_file
from bottle_sqlite import SQLitePlugin

import numpy as np
import StringIO
import matplotlib.cm as cm

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from pandas import DataFrame

install(SQLitePlugin(dbfile='./da602.sqlite'))

app = Bottle()

def get_ncaa_data():
	conn = sqlite3.connect('./da602.sqlite')
	c = conn.cursor()
	# select sum(percent_picked) from picks_2016
	c.execute("SELECT id, tourney_year, winner_seed, winner_team, loser_seed, loser_team, other_seed_1, other_team_1, other_seed_2, other_team_2, (winner_seed + loser_seed + other_seed_1 + other_seed_2) as final_four_sum FROM final_four order by tourney_year desc")
	result = c.fetchall()
	return result

def get_probabilities():
	conn = sqlite3.connect('./da602.sqlite')
	c = conn.cursor()
	c.execute("select seed, (sum(percent_picked)/4) as odds_of_seed from picks_2016 group by seed")
	result = c.fetchall()
	return result

@route('/main')
@view('tmpl_main')
def main():
	result = get_ncaa_data()
	dict = {'name': 'DAN', 'rows': result}
	df = DataFrame(result)
	df.columns = ['id', 'tourney_year', 'winner_seed', 'winner_team', 'loser_seed', 'loser_team', 'other_seed_1', 'other_team_1', 'other_seed_2', 'other_team_2', 'final_four_sum']
	dict['mean_ff_sum'] = round(np.mean(df['final_four_sum']),2)
	dict['sd_ff_sum'] = round(np.std(df['final_four_sum']),2)
	dict['var_ff_sum'] = round(np.var(df['final_four_sum']),2)
	dict['min_ff_sum'] = round(np.min(df['final_four_sum']),2)
	dict['max_ff_sum'] = round(np.max(df['final_four_sum']),2)
	probs = get_probabilities()
	dict['probs'] = probs
	
	return dict

@route('/<filename:re:.*\.png>')
def ff_img(filename): 
	result = get_ncaa_data()
	df = DataFrame(result)
	df.columns = ['id', 'tourney_year', 'winner_seed', 'winner_team', 'loser_seed', 'loser_team', 'other_seed_1', 'other_team_1', 'other_seed_2', 'other_team_2', 'final_four_sum']
	
	x = df['tourney_year']
	#x = np.arange(1979,2016,1)
	y = df['final_four_sum']
	#y = x**2 + 2*x - 5
	fig = Figure()  # Plotting
	canvas = FigureCanvas(fig)
	ax1 = fig.add_subplot(311)
	ax2 = fig.add_subplot(312)
	ax3 = fig.add_subplot(313)

	colors = cm.rainbow(np.linspace(0, 1, len(df)))
	ax1.scatter(x,y,c=colors)
	ax1.set_xlabel('')
	ax1.set_ylabel('SUM OF SEEDS')

	ax2.hist(y, bins=22)
	ax2.set_xlabel('SUM OF SEEDS')
	ax2.set_ylabel('COUNT')

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

	ax3.hist(seed_sums, normed=1, bins=15)
	#ax3.set_title("Peoples Real Picks Sums Histogram")
	ax3.set_xlabel("Sum")
	ax3.set_ylabel("Frequency")

	conn.commit()
	conn.close()




	canvas.print_figure(filename)
	return static_file(filename, root='./', mimetype='image/png')
    
run(host='localhost', port=8080, debug=True, reloader=True)