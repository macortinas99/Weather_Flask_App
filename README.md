# Weather_Flask_App
Web-Scraping application using Python Flask, geocoder, requests, JSON, and simple HTML and CSS.
Flask is the backend for creating the web application. Reqeusts is used for pulling the JSON data from the API website: https://openweathermap.org/api
Geocoder was added as an improvement, instead of the user having to select the city to pull weather data for, Geocder uses the IP address to get your city location automatically. 

The only reason the % chance rain could not be completed is because I am using a free account within the https://openweathermap.org/api website and the % chance rain was not included in the free version. Otherwise it would be filled dynamically according to the weather data for your current location

# How to run weather app
Once repository has been cloned, open the app.py file and run the file. It will open a local hosted application using flask on the local host port 3000.

# This widget will show up once the app.py file has been ran
![image](https://user-images.githubusercontent.com/58274004/172258298-72fb17f9-fccc-4e10-93e3-bcf7d4b6cdab.png)

