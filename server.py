from bottle import route, run, error, post, static_file, request, template
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
    early_arrivalHour = request.forms.get('earlyHour')
    late_arrivalHour = request.forms.get('lateHour')
    early_arrivalAMPM = request.forms.get('earlyAMPM')
    late_arrivalAMPM = request.forms.get('lateAMPM')
    early_arrivalMin = request.forms.get('earlyMin')
    late_arrivalMin = request.forms.get('lateMin')
    day = request.forms.get('Day')
    departure_time = -1

    if(early_arrivalAMPM == "AM"):
        early_arrival_24hours = 12 + int(early_arrivalHour)
        early_arrival_time = int(str(early_arrival_24hours) + early_arrivalMin)
        early_arrival_seconds = 3600 * early_arrival_24hours + int(early_arrivalMin) * 60 + 86400*int(day) + 1614236400
    else:
        early_arrival_time = int(earlyHour + early_arrivalMin)
        early_arrival_seconds = 3600 * early_arrival_24hours + int(early_arrivalMin) * 60 + 86400*int(day) + 1614236400
    if(late_arrivalAMPM == "AM"):
        late_arrival_24hours = 12 + int(late_arrivalHour)
        late_arrival_time = int(str(late_arrival_24hours) + late_arrivalMin)
        late_arrival_seconds = 3600 * late_arrival_24hours + int(late_arrivalMin) * 60 + 86400*int(day) + 1614236400 #Time to midnight on a random Thursday in the future
    else:
        late_arrival_time = int(lateHour + late_arrivalMin)
        late_arrival_seconds = 3600 * late_arrival_24hours + int(late_arrivalMin) * 60 + 86400*int(day) + 1614236400
    departure_time = late_arrival_seconds
    r = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + origin + '&destinations=' + destination + '&departure_time='+ str(departure_time) + '&key=' + api_key)
    if(r.json()['status'] != 'OK'):
        print('warning invalid query')
        return(error505('invalid query'))
    time = time_normal(r)
    departure_time = departure_time - time
    arrival_time_sec = 1614236000
    while(arrival_time_sec < early_arrival_seconds and arrival_time_sec > late_arrival_seconds):
        r = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + origin + '&destinations=' + destination + '&departure_time='+ str(departure_time) + '&key=' + api_key)
        if(r.json()['status'] != 'OK'):
            print('warning invalid query')
            return(error505('invalid query'))
        time = time_with_trafic(r)
        #departure_time = departure_time - 300
        arrival_time_sec = departure_time + time
        departure_time = departure_time + 300


    strTime = str(int(time/3600)) + " Hours " + str(int((time/60))%60) + " Minutes " + str(time%60) + " Seconds "
    points = (int(late_arrival_time)-int(early_arrival_time))
    return template('Solution.tpl', timeToDest=strTime, points = str(points), arrivalTime = str(1), departureTime = str(1))

api_key = os.environ['APIKEY']
if api_key == '':
    print('ERROR NO API KEY')
    quit()
data = load_data()
print(data)

run(host='localhost', port=8080, debug=True)
