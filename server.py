from bottle import route, run, error, post, static_file, request, template
import requests
import os
import matplotlib
matplotlib.use("Agg")
import pylab as pl

def time_with_trafic(r):
    return (r.json()['rows'][0]['elements'][0]['duration_in_traffic']['value'])
def time_normal(r):
    return (r.json()['rows'][0]['elements'][0]['duration']['value'])
def load_data():
    file = open('data.csv')
    data = [[],[]]
    for line in file:
        temp = line.split(',')
        data[0].append(temp[0])
        data[1].append(int(float(temp[1])))
    file.close()
    return data

# returns an integer that seconds since midnight, January 1, 1970 UTC to your depart time
def generate_time(early_arival, late_arival, current_time):
    return 12344
    

@route('/')
def index():
    return static_file('/Home.html', root = './')

@route('/static/<filename>')
def server_static(filename):
    print(filename)
    return static_file(filename, root='./static')

@error(505)
def error505(error):
    return 'The gerbals are confused'

@post('/get_time')
def get_time():
    data = load_data()
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

    pl.plot(data[0], data[1])
    pl.xlabel("Time")
    pl.ylabel("Ride Duration")
    pl.title("Traffic")
    pl.axvline(x="6:30", 'r')
    pl.savefig("static/ride.png")

    if(early_arrivalAMPM == "AM"):
        early_arrival_24hours = 12 + int(early_arrivalHour)
        early_arrival = int(str(early_arrival_24hours) + early_arrivalMin)
    else:
        early_arrival = int(earlyHour + early_arrivalMin)
    if(late_arrivalAMPM == "AM"):
        late_arrival_24hours = 12 + int(late_arrivalHour)
        late_arrival = int(str(late_arrival_24hours) + late_arrivalMin)
        departure_time = 3600 * late_arrival_24hours + int(late_arrivalMin) * 60 + 86400*int(day) + 1614236400 #Time to midnight on a random Thursday in the future
    else:
        late_arrival = int(lateHour + late_arrivalMin)


    r = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + origin + '&destinations=' + destination + '&departure_time='+ str(departure_time) + '&key=' + api_key)
    if(r.json()['status'] != 'OK'):
        print('warning invalid query')
        return(error505('invalid query'))
    time = time_with_trafic(r)

    strTime = str(int(time/3600)) + " Hours " + str(int((time/60))%60) + " Minutes " + str(time%60) + " Seconds "
    points = (int(late_arrival)-int(early_arrival))
    return template('Solution.tpl', timeToDest=strTime, points = str(points))

api_key = os.environ['APIKEY']
if api_key == '':
    print('ERROR NO API KEY')
    quit()
data = load_data()
print(data)

run(host='localhost', port=8080, debug=True)
