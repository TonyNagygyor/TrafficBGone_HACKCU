from bottle import route, run, error
import requests
import os


#These function exptect the request to be valid
def time_with_trafic(r):
    print(r.json()['rows'][0]['elements'][0]['duration_in_traffic']['value'])
def time_normal(r):
    print(r.json()['rows'][0]['elements'][0]['duration_in_traffic']['value'])

@route('/hello')
def hello():
    return "Hello World!"

@error(505)
def error505(error):
    return 'The gerbals are confused'

@post('/get_time')
def get_time():
    origin = request.forms.get('origin')
    destination = request.forms.get('destination')
    r = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + origin + '&destinations=' + destination + '&departure_time=1551020400&key=' + api_key)
    if(r.json()['status'] != 'OK'):
        print('warning invalid query')
        return(error505('invalid query'))
    time = time_with_trafic(r)
    return 'It will take ' + time + ' second to go from ' + origin + ' to ' + destination 
    
api_key = os.environ['APIKEY']
if api_key == '':
    print('ERROR NO API KEY')

run(host='localhost', port=8080, debug=True)