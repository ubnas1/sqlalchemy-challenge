# sqlalchemy-challenge

This project contains 2 Parts

## Part 1 | SQLAlchemy

In part one of this project, I have used Python library SQLAlchemy to query and extract Data from a database. The Extracted Date was then converted to Pandas Dataframe. 

Then I found the bussiest weather station and grabbed the precipitaion and temperatures for last 1 year of the previously mentioned weather station.

The collected Data is then used to plot histogram using Matplotlib and Bar plot using Seaborn.

## Part 2 | API creation | Flask

In part 2 of this project, I have created an API using Flask.

I used SQLAlchemy again to extract data from database and find the bussiest weather station. 

Flask is used to create a local server and create ROUTES. 

The user is given the list of available routes at homepage. 

In two of the several route inputs, user can provide the start and end date. These Dates are used to caluclate minimum, maximum and average temperatures of the bussiest weather station.
