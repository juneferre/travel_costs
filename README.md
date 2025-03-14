# travel_costs
## What's in this repository?

### scraping.ipynb
This repository includes a jupyter notebook called "scraping.ipynb", which walks through web scraping code to webscrape tables from [Wikipedia's 2018/2016 top 100 ranked Most Visited Cities](https://en.wikipedia.org/wiki/List_of_cities_by_international_visitors) and [Budget Your trip's](https://www.budgetyourtrip.com/) pricing information for the corresponding cities. 


### city_links.txt
This .txt file includes a list of the BudgetYourTrip.com URL's for each city that was listed in the Wikipedia 2018/2016 top 100 ranked Most Visited Cities table. 


### top_cities.csv
This is the .csv file made after scraping Wikipedia's 2018/2016 top 100 ranked Most Visited Cities. It contains the following variables:
**Unnamed**: it indexes the rows starting at 0, but it will be removed at somepoint in the scraping.

**Rank (Euromonitor)**: The Most Visited ranking according to Euromonitor

**City**: The city

**Country / Territory**: The country the city is located in


### cities.csv
The cities.csv file is a dataset that was created by mergeing the city_links.txt file and the top_cities.csv file. It contains the following variables: 
**Unnamed: 0**: it indexes the rows starting at 0, but it will be removed at somepoint in the scraping.

**Rank (Euromonitor)**: The Most Visited ranking according to Euromonitor

**City**: The city

**Country / Territory**: The country the city is located in

**Links**: The BudgetYourTrip.com link to that city's pricing information. 

