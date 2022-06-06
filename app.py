from calendar import weekday
from flask import Flask, render_template
import requests
from datetime import date, timedelta
import geocoder
from geopy.geocoders import Nominatim
import json


app = Flask(__name__)


@app.route('/')
def get_weather():
    API_KEY = '70472fb8a874fa069f63979916a1bb42'
    g = geocoder.ip('me')
    coordinates = g.latlng
    lat = coordinates[0]
    long = coordinates[1]
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(str(lat)+","+str(long))
    address = location.raw['address']
    state = address.get('state')
    country = address.get('country')

    url = "http://api.openweathermap.org/data/2.5/weather?lat=" + \
        str(lat) + "&lon=" + str(long) + "&appid=" + API_KEY + "&units=metric"
    url2 = "http://api.openweathermap.org/data/2.5/onecall?lat=" + \
        str(lat) + "&lon=" + str(long) + "&exclude=minutely,hourly" + \
        "&units=imperial" + "&appid=" + API_KEY

    weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat']
    full_date = date.today()
    weekday = full_date.strftime("%A")
    data = requests.get(url.format()).json()
    data2 = requests.get(url2.format()).json()
    year = date.today().year
    month = date.today().strftime('%B')
    day = date.today().day
    day_ofWeek = full_date.isoweekday()

    # IF statements looks at what day of week, and outputs next following 4 days
    # in standard, Mon, Tues, Wed, etc.
    # If sunday
    if day_ofWeek == 7:
        tomorrow = 1
        twoDaysFromNow = 2
        threeDaysFromNow = 3
        fourDaysFromNow = 4
    # If Monday, tuesday, etc....
    if day_ofWeek == 1:
        tomorrow = 2
        twoDaysFromNow = 3
        threeDaysFromNow = 4
        fourDaysFromNow = 5
    if day_ofWeek == 2:
        tomorrow = 3
        twoDaysFromNow = 4
        threeDaysFromNow = 5
        fourDaysFromNow = 6
    if day_ofWeek == 3:
        tomorrow = 4
        twoDaysFromNow = 5
        threeDaysFromNow = 6
        fourDaysFromNow = 0
    if day_ofWeek == 4:
        tomorrow = 5
        twoDaysFromNow = 6
        threeDaysFromNow = 0
        fourDaysFromNow = 1
    if day_ofWeek == 5:
        tomorrow = 6
        twoDaysFromNow = 0
        threeDaysFromNow = 1
        fourDaysFromNow = 2
    if day_ofWeek == 6:
        tomorrow = 0
        twoDaysFromNow = 1
        threeDaysFromNow = 2
        fourDaysFromNow = 2

    # Variables set once day of week determined, thesee values are then used to access
    # list of weekday strings
    tom_Weekday = weekdays[tomorrow]
    two_daysNowWeekday = weekdays[twoDaysFromNow]
    three_daysNowWeekday = weekdays[threeDaysFromNow]
    four_daysNowWeekday = weekdays[fourDaysFromNow]
    print(tom_Weekday, two_daysNowWeekday,
          three_daysNowWeekday, four_daysNowWeekday)

    # Sets empty list
    dayTemp = []
    nightTemp = []
    descr = []

    # Searches each day in 8day forecast in JSON data from API Openweathermap
    # Grabs Day/Night Temp and descriptions
    for i in data2['daily']:
        dayTemp.append(round(i['temp']['day']))
        nightTemp.append(round(i['temp']['night']))
        descr.append(i['weather'][0]['main'] + ': ' +
                     i['weather'][0]['description'])

    # Used to keep all data in one spot, this dictionary is returned in this function
    # and called within the hmtl to input live data into CSS template
    weather = {
        'city': data['name'],
        'state': state,
        'country': country,
        'weekday': weekday,
        'day': day,
        'month': month,
        'year': year,
        'temperature': round((data['main']['temp']*1.8 + 32)),
        'description': data['weather'][0]['description'],
        # NEED TO WORK ON CHANCE OF RAIN
        # 'chanceOfRain': ,
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
        'icon': data['weather'][0]['icon'],
        'tomorrow': tom_Weekday,
        'tomorrowDayTemp': dayTemp[0],
        'tomorrowNightTemp': nightTemp[0],
        'twodaysFromNow': two_daysNowWeekday,
        'twodaysDayTemp': dayTemp[1],
        'twodaysNightTemp': nightTemp[1],
        'threedaysFromNow': three_daysNowWeekday,
        'threedaysDayTemp': dayTemp[2],
        'threedaysNightTemp': nightTemp[2],
        'fourdaysFromNow': four_daysNowWeekday,
        'fourdaysDayTemp': dayTemp[3],
        'fourdaysNightTemp': nightTemp[3],
    }
    # print(data)

    # the weather variable MUST be returned otherwise it is only used within the
    # the function and can't be used by the rest of the code!!
    return render_template('base.html', weather=weather)


if __name__ == '__main__':
    app.run(debug=True)
