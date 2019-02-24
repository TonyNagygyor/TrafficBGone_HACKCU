from bottle import route, run, error, post, static_file, request
import requests
import os

#fake_data = [('0:00',	4744),('0:15',	4744),('0:30',	4744),('0:45',	4744),('1:00',	4744),('1:15',	4744),('1:30',	4744),('1:45',	4744),('2:00',	4744),('2:15',	4744),('2:30',	4744),('2:45',	4744),('3:00',	4744),('3:15',	4744),('3:30',	4744),('3:45',	4744),('4:00',	4744),('4:15',	4744),('4:30',	4744),('4:45',	4744),('5:00',	4744),('5:15',	4744),('5:30',	4744),('5:45',	4744),('6:00',	4744),('6:15',	4744),('6:30',	4744),('6:45',	5692.8),('7:00',	7116),('7:15',	9488),('7:30',	11860),('7:45',	14232),('8:00',	14706.4),('8:15',	13757.6),('8:30',	14184.56),('8:45',	15180.8),('9:00',	13283.2),('9:15',	14232),('9:30',	13757.6),('9:45',	13283.2,('10:00',	11860),('10:15',	10436.8),('10:30',	10436.8),('10:45',	7116),('11:00',	6641.6),('11:15',	5692.8),('11:30',	5692.8),('11:45',	5692.8),('12:00',	5218.4),('12:15',	5692.8),('12:30',	6167.2),('12:45',	5692.8),('13:00',	5692.8),('13:15',	4744),('13:30',	5692.8),('13:45',	5692.8),('14:00',	5692.8),('14:15',	5218.4),('14:30',	5692.8),('14:45',	6641.6),('15:00',	5692.8),('15:15',	5313.28),('15:30',	5692.8),('15:45',	6167.2),('16:00',	7116),('16:15',	9488),('16:30',	18976),('16:45',	19924.8),('17:00',	18976),('17:15',	23720),('17:30',	18976),('17:45',	18501.6),('18:00',	18976),('18:15',	12808.8),('18:30',	7116),('18:45',	5692.8),('19:00',	7116),('19:15',	5692.8),('19:30',	5218.4),('19:45',	5218.4),('20:00',	5218.4),('20:15',	5218.4),('20:30',	5218.4),('20:45',	5218.4),('21:00',	4744),('21:15',	4744),('21:30',	4744),('21:45',	4744),('22:00',	4744),('22:15',	4744),('22:30',	4744),('22:45',	4744),('23:00',	4744),('23:15',	4744),('23:30',	4744),('23:45',	4744)]
# These function exptect the request to be valid
def time_with_trafic(r):
    return (r.json()['rows'][0]['elements'][0]['duration_in_traffic']['value'])
def time_normal(r):
    return (r.json()['rows'][0]['elements'][0]['duration']['value'])
def load_data():
    file = open('data.csv')
    data = []
    for line in file:
        temp = line.split(',')
        data.append((temp[0], int(float(temp[1]))))
    return data

# returns an integer that seconds since midnight, January 1, 1970 UTC to your depart time
def generate_time(early_arival, late_arival, current_time):
    return 12344
    

@route('/')
def index():
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
    r = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + origin + '&destinations=' + destination + '&arrival_time=1551020400&key=' + api_key)
    print(r.text)
    if(r.json()['status'] != 'OK'):
        print('warning invalid query')
        return(error505('invalid query'))
    try:
        time = time_with_trafic(r)
    except KeyError:
        time = time_normal(r)
    leave_time = generate_time(early_arival, late_arival, time)
    r = requests.get(f'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={origin}&destinations={destination}&departure_time={leave_time}&key=' + api_key)
    return f'You are scheduled to leave artIt will take {time // 60} minutes to go from {origin} to {destination}'

api_key = os.environ['APIKEY']
if api_key == '':
    print('ERROR NO API KEY')
    quit()
data = load_data()
print(data)

run(host='localhost', port=8080, debug=True)
