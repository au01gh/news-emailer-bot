import requests

from bs4 import BeautifulSoup

def w_news():
    print('-------------------------------------------------- Weather News --------------------------------------------------')

    req = requests.get('https://forecast.weather.gov/MapClick.php?lat=37.92326500000007&lon=-122.06927099999996').text
    soup = BeautifulSoup(req, 'html.parser')
    week = soup.find('div', id = 'seven-day-forecast-body')
    days = week.findAll('li', {'class': 'forecast-tombstone'})

    if soup.find(class_ = 'forecast-tombstone current-hazard current-hazard-warning'): #if there is an extra element in the list
        d = 1
        n = 2
    else:
        d = 0
        n = 1

    dayTemp = (days[d].find(class_= 'temp').getText().lower())
    dayDesc = (days[d].find(class_= 'short-desc').getText().lower())

    nightTemp = (days[n].find(class_= 'temp').getText().lower())
    nightDesc = (days[n].find(class_= 'short-desc').getText().lower())

    day = ['The day temperature for ', dayTemp, ' // ', 'The day will be: ', dayDesc]
    night = ['The night temperature for ', nightTemp, ' // ', 'The night will be: ', nightDesc]

    #iterates through the lists and prints the elements
    for i in day:
        print(i, end = '' '')
    print()
    for i in night:
        print(i, end = '' '')
    print()