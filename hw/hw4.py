from alchemyapi import AlchemyAPI
import urllib2
import json
# http://stackoverflow.com/questions/3115448/best-way-to-convert-the-this-html-file-into-an-xml-file-using-python
from bs4 import BeautifulSoup
import re
from lxml import html
import requests
import numpy as np

'''
Design and implement a system that takes a webpage URL as input.  
The program will read the page and extract the important text (news story, blog post, etc.) from the page's source. 
Writing a program that can do this for any webpage is a major undertaking, so we will just focus on a single page.
You can hard-code the link into the program. 

Take the important text that you extracted from the page and submit it to the Alchemy API for analysis.  
Specifically, obtain the Ranked Keywords.  Once you have the keywords, print to the console the top ten results.  
Below are the detailed steps:

Get an API key from Alchemy.  If you really don't want to sign-up, let me know (I'll lend you a key).
Download the Python SDK from the site.
Look at the example provided in the SDK.
Import the Alchemy module into your code.
Call the function to get Ranked Keywords.
The result will be in XML.  Process that XML and get the top ten keywords, and their relevance.
Print those results to the console.
'''
	
def run_app():	

	##### part 1

	page = requests.get('https://en.wikipedia.org/wiki/Michael_Jordan')
	tree = html.fromstring(page.content)
	h3s = tree.xpath('//h3/span/text()')
	h3s_combined = ''

	for next_h3 in h3s:
		h3s_combined += ' '
		h3s_combined += next_h3
	
	print('***********************************************')
	print('*** The h3s on this page were: ', h3s_combined)
	print('***********************************************')

	##### part 2

	#alchemy_api_key="xxxx"
	alchemyapi = AlchemyAPI()

	response = alchemyapi.keywords('text', h3s_combined, {'sentiment': 1, 'maxRetrieve': 10})

	if response['status'] == 'OK':
		print('## Response Object ##')
		# print(json.dumps(response, indent=4))

		print('')
		print('## Keywords ##')
		for keyword in response['keywords']:
			print('text: ', keyword['text'].encode('utf-8'))
			print('relevance: ', keyword['relevance'])
			print('sentiment: ', keyword['sentiment']['type'])
			print('')
	else:
		print('Error in keyword extaction call: ', response['statusInfo'])

if __name__ == "__main__":
	run_app()
	
	