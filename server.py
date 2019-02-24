from bottle import route, run
import requests
import os
print(os.environ['APIKEY'])

api_key = os.environ['APIKEY']
origin = 'Golden,CO'
destination = 'Keystone_Resort'

if api_key == '':
    print('ERROR NO API KEY')

r = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + origin + '&destinations=' + destination + '&departure_time=1551020400&key=' + api_key)
print(r.text)
print('hello')

@route('/hello')
def hello():
    return "Hello World!"

run(host='localhost', port=8080, debug=True)

@post('/get_time')
def get_time():
    origin = request.forms.get('origin')
    destination = request.forms.get('destination')
    r = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + origin + '&destinations=' + destination + '&departure_time=1551020400&key=' + api_key)
    print(r.text)