Covid-19 Coronavirus Web Scraping Tool
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
Required packages:
	BeautifulSoup
	https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
		pip install beautifulsoup4
	Requests
	https://requests.readthedocs.io/en/master/	
		pip install requests

	Note: 	There are many other ways to parse content from the web
		I chose BeautifulSoup+Requests, since I am using a pre-formatted dataset.
		Otherwise, I would have chosen Scrapy, since it is more recommended for incomplete or more complex data.

Objective:
	Read from online repository
		Note:	https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv
	Write to local database of saved locations
		Note:	corona-scraper.csv (see future task list on bottom: #2)
	Output information on desired locations
	+ more (graph, future estimate, overall numbers)

Note:	This is a very rugged version of my program; there is still a more to come.


---------------------------------------------------------------------------------------------------------------------------------------------------------------------
Future Task List:
	(In Progress)
		#1: Display (x) amount of locations depending on what has been written to database

	(Not Started)
		#2: Create a seperate version to test saving a dataset by line, not rewriting the whole thing
			Note:	Test with SQLlite
				Prove me if I am wrong, but I assume it will take less actions.