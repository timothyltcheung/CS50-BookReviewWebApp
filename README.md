# Project 1

Web Programming with Python and JavaScript
=======
This is a Flask web app that utilizes a PostgreSQL database that was created for Harvard's CS50: Web Programming with Python and JavaScript course.  HTML and Jinja2 are used to create a simple front end for this web app.

The main objectives for this project were to become more comfortable with Python, gain experience with Flask,
and to learn to use SQL to interact with databases.

This application allows users to register for the website with a username and password, search for books to read reviews,
and to leave their own reviews.  In addition, the Goodreads API is utilized to pull in reviews from a broader audience.
Lastly, this application has its own API that allows users to query for reviews.

A preloaded database of books is provided with books.csv and imported using import.py

Requirements: https://docs.cs50.net/web/2018/x/projects/1/project1.html

API Key:
========

To use this web app, a key from Goodreads is necessary (can be found here: https://www.goodreads.com/api/keys)

Once obtained, set up an environment variable shown below in order to run the app 

GOODREADS_KEY = 'Your Key Here'

