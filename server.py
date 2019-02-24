from bottle import route, run, error, post, static_file, request, template
import requests
import os


#These function exptect the request to be valid
def time_with_trafic(r):
    return (r.json()['rows'][0]['elements'][0]['duration_in_traffic']['value'])
def time_normal(r):
    return (r.json()['rows'][0]['elements'][0]['duration_in_traffic']['value'])

@route('/')
def hello():
    return static_file('/Home.html', root = './')

@error(505)
def error505(error):
    return 'The gerbals are confused'

@post('/get_time')
def get_time():
    origin = request.forms.get('origin')
    destination = request.forms.get('destination')
    early_arival = request.forms.get('early')
    late_arival = request.forms.get('late')
    r = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + origin + '&destinations=' + destination + '&departure_time=1551020400&key=' + api_key)
    if(r.json()['status'] != 'OK'):
        print('warning invalid query')
        return(error505('invalid query'))
    time = time_with_trafic(r)
    strTime = str(int(time/3600)) + " Hours " + str(int((time/60))%60) + " Minutes " + str(time%60) + " Seconds "
    return template('Solution.tpl', timeToDest=strTime)

api_key = os.environ['APIKEY']
if api_key == '':
    print('ERROR NO API KEY')

run(host='localhost', port=8080, debug=True)
