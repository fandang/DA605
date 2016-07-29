'''
Plot everything!  

In this homework we will explore the matplotlib library and its features by plotting the results of previous assignments.

Please do all of the following:
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mahotas as mh
import pylab
from pylab import imshow, gray, show
'''
I)
Express the cars.data.csv data as a series of bar graphs.  
The x-axis represents a feature and the y-axis is the frequency in the sample.  
Do this with the 'buying', 'maint', 'safety', and 'doors' fields with one plot for each for a total of four.  
Make each graph a subplot of a single output.  
Something like this:       
'''
def go_1():
	df = pd.read_csv('cars.data.csv')
	df.columns = ['buying','maint','doors','persons','lug_boot','safety','acceptability']
	df = df[['buying','maint','safety','doors']]
	#print df
	##############################################
	plt.subplot(221)
	plt.title('buying')
	df['buying'].value_counts().plot(kind='bar')
	##############################################
	plt.subplot(222)
	plt.title('maint')
	df['maint'].value_counts().plot(kind='bar')
	##############################################
	plt.subplot(223)
	plt.title('safety')
	df['safety'].value_counts().plot(kind='bar')
	##############################################
	plt.subplot(224)
	plt.title('doors')
	df['doors'].value_counts().plot(kind='bar')
	##############################################
	plt.show()

'''
II)
Plot your results from the linear regression in homework 5 and 7 (for any of the provided data sets).  
The plot should include.  
1) a scatter of the points in the .csv file 
2) a line showing the regression line (either from the calculation in homework 5 or line-fitting from homework 7).  
3) something on the plot that specifies the equation for the regression line.  
Something like this:
'''
def least_squares(df, x_label, y_label, do_plot):	
	# Use the logic from: https://en.wikipedia.org/wiki/Simple_linear_regression
	# col sums: axis=0
	x_data = df[x_label]
	y_data = df[y_label]
	
	x_sum = np.sum(x_data, axis=0)
	y_sum = np.sum(y_data, axis=0)
	x_sq_sum = np.sum(x_data * x_data, axis=0)
	y_sq_sum = np.sum(y_data * y_data, axis=0)
	x_y_sum = np.sum(x_data * y_data, axis=0)
	
	n = len(x_data) # or use len(y_data)

	# From: https://en.wikipedia.org/wiki/Simple_linear_regression
	# "These quantities would be used to calculate the estimates of the regression coefficients, and their standard errors."

	beta_hat = (n * x_y_sum - x_sum * y_sum) / (n * x_sq_sum - x_sum * x_sum)
	alpha_hat = (1.0 / n) * y_sum - (1.0 / n) * beta_hat * x_sum

	df[y_label + '_projected'] = df[x_label] * beta_hat + alpha_hat

	if(do_plot):
		# Just to double check my result:
		plt.scatter(df[x_label], df[y_label])

		# draw diagonal line with supplied x values and their corresponding least squares y values...
		plt.plot(x_data, (x_data * beta_hat + alpha_hat), 'k-')
		plt.xlabel('Height')
		plt.ylabel('Mass')

		plt.title("HW 10 Part 2")
		plt.show() # Depending on whether you use IPython or interactive mode, etc.


def run_with_least_squares():
	do_plot = True
	df = pd.DataFrame({ 'X_Height' : get_wiki_height_array(), 'Y_Mass' : get_wiki_mass_array() })
	least_squares(df, 'X_Height', 'Y_Mass', do_plot)

def get_wiki_height_array():
	x_height_array = [1.47, 1.50, 1.52, 1.55, 1.57, 1.60, 1.63, 1.65, 1.68, 1.70, 1.73, 1.75, 1.78, 1.80, 1.83]
	return x_height_array
	
def get_wiki_mass_array():
	y_mass_array = [52.21, 53.12, 54.48, 55.84, 57.20, 58.57, 59.93, 61.29, 63.11, 64.47, 66.28, 68.10, 69.92, 72.19, 74.46]
	return y_mass_array

def go_2():
	df = pd.DataFrame({ 'X_Height' : get_wiki_height_array(), 'Y_Mass' : get_wiki_mass_array() })
	least_squares(df, 'X_Height', 'Y_Mass', True)


'''
III)
Create an overlay of the center points found in objects.png from homework 8.  
The image should be in the background and the object centers can be small circles or points at or around the center points.  
Something like this:
'''
def process_with_mahotas(obj_name, filter_val, show_popups):
	print "-----------------------------------------------------"
	print obj_name + ":"
	print "-----------------------------------------------------"
	# http://mahotas.readthedocs.org/en/latest/thresholding.html
	the_img = mh.imread(obj_name + '.png')
	the_img = the_img.astype(np.uint8)
	gray()

	# Thresholding
	the_img_filtered = mh.gaussian_filter(the_img, filter_val)
	T = mh.thresholding.otsu(the_img)
	pylab.imshow(the_img_filtered > T)

	# Count
	labeled, nr_objects = mh.label(the_img_filtered > T)
	print "num objects: " + str(nr_objects)

	# Center Points
	center_pts = mh.center_of_mass(the_img_filtered, labeled)[1:]
	print "center_pts: " + str(center_pts)

	x_vals = center_pts[:,0]
	y_vals = center_pts[:,1]

	print "X VALS:"
	print x_vals
	print "Y VALS:"
	print y_vals

	# ******
	pylab.plot(y_vals, x_vals,marker="o", linestyle='None', color='red')
	pylab.title('Counting Objects for HW #3')

	if(show_popups):
		pylab.show()


def go_3():
	process_with_mahotas("objects", 4.5, True)

'''
Plot a line graph that shows the hour by hour change in number of server requests from the HTTP in homework 9.  
The x-axis is the discrete hour intervals (eg 13:00-14:00) and the y-axis is the number of requests.  
Something like this:
'''
def go_4():
	# the quote within quotes is always separated by an = sign, so just make that equal sign your default escape character:
	df = pd.read_csv("epa-http.txt", sep="\s+", header=None, error_bad_lines=False, escapechar='=')
	df.columns = ['request_host', 'the_date', 'request_text', 'response_code', 'response_bytes']
	df = df.convert_objects(convert_numeric=True)

	# During what hour was the server the busiest in terms of requests? (note: [DD:HH:MM:SS])
	df["the_hour"] = df.the_date.str[4:6]
	#summed_hours = df.groupby('the_hour').response_bytes.count().sort_values(ascending=False)
	summed_hours = df.groupby('the_hour').response_bytes.count()
	
	print "-----------------------------------------------------------------------"
	print "Busiest Hour was: "
	print "-----------------------------------------------------------------------"
	print summed_hours.head(1)
	print ""
	print "[top 5:]"
	print summed_hours.head(5)
	print "\n"
	print summed_hours
	print "\n"

	plt.plot(summed_hours.index, summed_hours, marker='o', linestyle='--', color='r', label='Hourly Traffic')
	
	plt.xlabel('HOUR')
	plt.ylabel('# REQUESTS')
	plt.title('Requests per Hour')
	plt.legend()
	plt.show()

if __name__ == "__main__":
	go_1()
	go_2()
	go_3()
	go_4()
