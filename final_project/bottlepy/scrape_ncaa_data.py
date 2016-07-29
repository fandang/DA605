import urllib2
from bs4 import BeautifulSoup
import re


#db_url = './app/da602/databases/da602.sqlite'
db_url = 'da602.sqlite'
#db_url = './app/da602/databases/storage.sqlite'
#db_url = 'storage.sqlite'

response = urllib2.urlopen('https://en.wikipedia.org/wiki/List_of_NCAA_men%27s_Division_I_basketball_tournament_Final_Four_participants')
html = response.read()

parsed_html = BeautifulSoup(html)

all_tables = parsed_html.findAll('table')
current_year = 0

import sqlite3
conn = sqlite3.connect(db_url)
c = conn.cursor()
c.execute('DROP TABLE if exists FINAL_FOUR')
c.execute('CREATE TABLE FINAL_FOUR(id bigint primary key, tourney_year int, winner_seed int, winner_team text, loser_seed int, loser_team text, other_seed_1 int, other_team_1 text, other_seed_2 int, other_team_2 text)')
c.execute('DROP TABLE if exists PICKS_2016')
c.execute('CREATE TABLE PICKS_2016(id bigint primary key, seed int, team text, percent_picked NUMERIC)')

# http://www.businessinsider.com/most-popular-final-four-picks-2016-3
c.execute('INSERT INTO PICKS_2016 values (1, 1, "Kansas", 0.729)')
c.execute('INSERT INTO PICKS_2016 values (2, 2, "Michigan State", 0.693)')
c.execute('INSERT INTO PICKS_2016 values (3, 1, "North Carolina", 0.537)')
c.execute('INSERT INTO PICKS_2016 values (4, 1, "Oklahoma", 0.449)')
c.execute('INSERT INTO PICKS_2016 values (5, 1, "Oregon", 0.241)')
c.execute('INSERT INTO PICKS_2016 values (6, 1, "Virginia", 0.194)')
c.execute('INSERT INTO PICKS_2016 values (7, 4, "Kentucky", 0.18)')
c.execute('INSERT INTO PICKS_2016 values (8, 4, "Duke", 0.121)')
c.execute('INSERT INTO PICKS_2016 values (9, 3, "Texas A&M", 0.121)')
c.execute('INSERT INTO PICKS_2016 values (10, 2, "Villanova", 0.11)')
c.execute('INSERT INTO PICKS_2016 values (11, 2, "Xavier", 0.097)')
c.execute('INSERT INTO PICKS_2016 values (12, 3, "West Virginia", 0.094)')
c.execute('INSERT INTO PICKS_2016 values (13, 5, "Maryland", 0.041)')
c.execute('INSERT INTO PICKS_2016 values (14, 3, "Miami (FL)", 0.041)')
c.execute('INSERT INTO PICKS_2016 values (15, 5, "Indiana", 0.039)')
c.execute('INSERT INTO PICKS_2016 values (16, 3, "Utah", 0.026)')
c.execute('INSERT INTO PICKS_2016 values (17, 5, "Baylor", 0.024)')
c.execute('INSERT INTO PICKS_2016 values (18, 4, "California", 0.022)')
c.execute('INSERT INTO PICKS_2016 values (19, 5, "Purdue", 0.021)')
c.execute('INSERT INTO PICKS_2016 values (20, 6, "Arizona", 0.02)')


id = 0
             
winner_seed = 0
loser_seed = 0
other_seed_1 = 0
other_seed_2 = 0

winner_team = 'team: n/a'
loser_team = 'team: n/a'
other_team_1 = 'team: n/a'
other_team_2 = 'team: n/a'

row_of_year = 0

for row in all_tables[0].findAll('tr'):
	all_cells_for_row = row.findAll('td')
	num_cells_for_row = len(all_cells_for_row)
	final_four_team = 'not set'
	final_four_region_and_seed = 'not set'
	if(num_cells_for_row == 5):
		row_of_year = 1
		current_year = all_cells_for_row[0].text
		print '-------------------'
		print current_year
		print '-------------------'
		final_four_team = all_cells_for_row[1].text
		final_four_region_and_seed = all_cells_for_row[3].text
	elif(num_cells_for_row == 4):
		row_of_year = row_of_year + 1
		final_four_team = all_cells_for_row[0].text
		final_four_region_and_seed = all_cells_for_row[2].text
	else:
		print('dont know what to do with %d cells in row.' | num_cells_for_row)

	# next row of code just checks that its the year in parens
	if(current_year != 'Year' and '(' in final_four_region_and_seed and ')' in final_four_region_and_seed):	
		seed = final_four_region_and_seed[final_four_region_and_seed.index("(") + 1:final_four_region_and_seed.rindex(")")]
		print seed, ': ', final_four_team
		#print final_four_region_and_seed
		if(row_of_year == 1):
			winner_seed = seed
			winner_team = final_four_team
		elif(row_of_year == 2):	
			loser_seed = seed
			loser_team = final_four_team
		elif(row_of_year == 3):	
			other_seed_1 = seed
			other_team_1 = final_four_team
		elif(row_of_year == 4):	
			other_seed_2 = seed
			other_team_2 = final_four_team

	if(winner_seed > 0 and loser_seed > 0 and other_seed_1 > 0 and other_seed_2 > 0):
		data = [id, current_year, winner_seed, winner_team, loser_seed, loser_team, other_seed_1, other_team_1, other_seed_2, other_team_2]
		c.execute('INSERT INTO FINAL_FOUR (id, tourney_year, winner_seed, winner_team, loser_seed, loser_team, other_seed_1, other_team_1, other_seed_2, other_team_2) values(?,?,?,?,?,?,?,?,?,?)', data)
		id = id + 1

		winner_seed = 0
		loser_seed = 0
		other_seed_1 = 0
		other_seed_2 = 0

		winner_team = 'team: n/a'
		loser_team = 'team: n/a'
		other_team_1 = 'team: n/a'
		other_team_2 = 'team: n/a'

#print parsed_html.body.find('table', attrs={'class':'wikitable'}).text
#print parsed_html.body.find('table/tr').text
#print parsed_html.body.find('table/tr[number(td) >= 1979]').text

#print html

conn.commit()
conn.close()
