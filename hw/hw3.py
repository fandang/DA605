'''
http://archive.ics.uci.edu/ml/datasets/Car+Evaluation
Class Values: 
unacc, acc, good, vgood 
Attributes: 
buying: vhigh, high, med, low. 
maint: vhigh, high, med, low. 
doors: 2, 3, 4, 5more. 
persons: 2, 4, more. 
lug_boot: small, med, big. 
safety: low, med, high. 
'''

import numpy as np
import pandas as pd
from Tkinter import *
import re
	
def go_clicked():	
	sortBySelection=sortBy.get(sortBy.curselection())
	showtopSelection=showtop.get(showtop.curselection())
	topOrBottomSelection=topOrBottom.get(topOrBottom.curselection())
	sortorderSelection=sortorder.get(sortorder.curselection())
	outfileVal=outfile.get()
	
	isTop = ("top"==topOrBottomSelection)
	isAsc = ("asc"==sortorderSelection)
	
	go('cars.data.csv', sortBySelection, int(showtopSelection), isTop, isAsc, outfileVal, False, False)

def go(infile, sortby, howmany, top, asc, filename, filter2C, filter2D):
	print "-------------------------------------------------------"
	print "sortby = %s" % sortby
	print "howmany = %s" % howmany
	print "top = %s" % top
	print "asc = %s" % asc
	print "filename = %s" % filename
	print "isTop = %s" % top
	print "isAsc = %s" % asc
	print "filter2C = %s" % filter2C
	print "-------------------------------------------------------"
	
	df = pd.read_csv(infile)
	df.columns = ['buying','maint','doors','persons','lug_boot','safety','acceptability']
	
	try:
		df['buying'] = df['buying'].astype('category', categories=['low', 'med', 'high', 'vhigh'], ordered=True)
		df['maint'] = df['maint'].astype('category', categories=['low', 'med', 'high', 'vhigh'], ordered=True)
		df['doors'] = df['doors'].astype('category', categories=['2', '3', '4', '5more'], ordered=True)
		df['persons'] = df['persons'].astype('category', categories=['2', '4', 'more'], ordered=True)
		df['lug_boot'] = df['lug_boot'].astype('category', categories=['small', 'med', 'big'], ordered=True)
		df['safety'] = df['safety'].astype('category', categories=['low', 'med', 'high'], ordered=True)
	except ValueError:
		print "AN ERROR OCCURRED!!!!!!!!!"

	# this gets rid of the empty row that the above categories code left behind upon a bad value:
	df = df[df['buying'].notnull() & df['maint'].notnull() & df['doors'].notnull() & df['persons'].notnull() & df['lug_boot'].notnull() & df['safety'].notnull()]
	
	df = df.sort_values([sortby], ascending=asc)
	
	if(top):
		df = df.head(howmany)
	else:
		df = df.tail(howmany)


	# 2C: all rows (that are high or vhigh in buying, maint, AND safety
	if(filter2C):
		df = df
		# 'high' is contained in 'vhigh', so not bothering with an OR in the regex
		df = df[df['buying'].str.contains('v?high')]
		df = df[df['maint'].str.contains('v?high')]
		df = df[df['safety'].str.contains('v?high')]

	# 2D: all rows (in any order) that are: buying=vhigh, maint=med, doors=4, and persons=4 or more"
	if(filter2D):
		df = df[df['buying'] == 'vhigh']
		df = df[df['maint'] == 'med']
		df = df[df['doors'] == '4']
		df = df[df['persons'].isin(['4', 'more'])]

	if(filename):
		df.to_csv(filename, sep=',')
	else:	
		print df

def hw_2a():
	#a - Print to the console the top 10 rows of the data sorted by 'safety' in descending order
	print "----------------------------------------------"
	print "2A: top 10 rows by safety descending"
	print "----------------------------------------------"
	go('cars.data.csv', 'safety', 10, True, False, None, False, False)

def hw_2b():
	#b - Print to the console the bottom 15 rows of the data sorted by 'maint' in ascending order
	print "----------------------------------------------"
	print "2B: bottom 15 rows by maint ascending"
	print "----------------------------------------------"
	go('cars.data.csv', 'maint', 15, False, True, None, False, False)

def hw_2c():
	#c - Print to the console all rows that are high or vhigh in fields 'buying', 'maint', and 'safety', sorted by 'doors' in ascending order.  Find these matches using regular expressions.
	print "----------------------------------------------"
	print "2C: all rows (that are high or vhigh in buying, maint, AND safety) by doorts ascending"
	print "----------------------------------------------"
	go('cars.data.csv', 'doors', None, True, True, None, True, False)

def hw_2d():
	#d - Save to a file all rows (in any order) that are: 'buying': vhigh, 'maint': med, 'doors': 4, and 'persons': 4 or more.  The file path can be a hard-coded location (name it output.txt) or use a dialog box.
	print "----------------------------------------------"
	print "2D: all rows (in any order) that are: buying=vhigh, maint=med, doors=4, and persons=4 or more"
	print "----------------------------------------------"
	go('cars.data.csv', 'doors', None, True, True, "output.txt", False, True)
	
def show_gui():
	root = Tk()

	title = Label(root, text="DA602 - Homework 3")
	title.pack()
	
	outfileTitle = Label(root, text="Output File Path: (leave blank to output to console.)")
	outfileTitle.pack()
	global outfile
	outfile = Entry(root)
	outfile.insert(0, "APP_OUTPUT.txt")
	outfile.pack()

	topOrBottomTitle = Label(root, text="Top/Bottom:")
	topOrBottomTitle.pack()
	global topOrBottom
	topOrBottom = Listbox(root, height=2, exportselection=0)
	topOrBottom.insert(0,'top')
	topOrBottom.insert(1,'bottom')
	topOrBottom.select_set(0)
	topOrBottom.pack() 

	showtopTitle = Label(root, text="Show Top:")
	showtopTitle.pack()
	global showtop
	showtop = Listbox(root, height=5, exportselection=0)
	showtop.insert(0,'5')
	showtop.insert(1,'10')
	showtop.insert(2,'15')
	showtop.insert(3,'20')
	showtop.insert(4,'25')
	showtop.select_set(0)
	showtop.pack() 

	sortByTitle = Label(root, text="Sort By:")
	sortByTitle.pack()
	global sortBy
	sortBy = Listbox(root, height=6, exportselection=0)
	sortBy.insert(0,'buying')
	sortBy.insert(1,'maint')
	sortBy.insert(2,'doors')
	sortBy.insert(3,'persons')
	sortBy.insert(4,'lug_boot')
	sortBy.insert(5,'safety')
	sortBy.select_set(0)
	sortBy.pack() 

	sortorderTitle = Label(root, text="Sort Order:")
	sortorderTitle.pack()
	global sortorder
	sortorder = Listbox(root, height=2, exportselection=0)
	sortorder.insert(0,'asc')
	sortorder.insert(1,'desc')
	sortorder.select_set(0)
	sortorder.pack() 

	goButton = Button(root, text = 'GO!', command = go_clicked, width = '25')
	goButton.pack()

	hw2AButton = Button(root, text = 'HW #2A', command = hw_2a, width = '25')
	hw2AButton.pack()

	hw2BButton = Button(root, text = 'HW #2B', command = hw_2b, width = '25')
	hw2BButton.pack()

	hw2CButton = Button(root, text = 'HW #2C', command = hw_2c, width = '25')
	hw2CButton.pack()

	hw2DButton = Button(root, text = 'HW #2D', command = hw_2d, width = '25')
	hw2DButton.pack()

	root.mainloop()

if __name__ == "__main__":
	hw_2a()
	hw_2b()
	hw_2c()
	hw_2d()
	
	show_gui()
	
	