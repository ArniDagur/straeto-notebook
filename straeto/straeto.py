import requests
#from datetime import datetime

_STOKKUR_URL = "https://app.straeto.is/pele/api/v1/"
#BASE_URL = "https://otp.straeto.is/otp/"
#ADMIN_URL = "https://admin.straeto.is/api/"

def getAllBusPositions():
    r = requests.get(_STOKKUR_URL + "positions/all")
    return r.json()['positions']

def getBusPositionsFor(buses):
    r = requests.get(_STOKKUR_URL + "positions/filter/{}".format(",".join(buses)))
    return r.json()['positions']


#def getBusStops():
#    r = requests.get(BASE_URL + "routers/default/index/stops")
#    return r.json()
#
#def getAllBusForStop(bus_stop, date): #Does this work?
#    if date == "now":
#        date = datetime.now().strftime("%d%m%Y")
#    r = requests.get(BASE_URL + "routers/default/index/stops/{}/stoptimes/{}".format(bus_stop, date))
#    return r.json()
#
#def getTrip(trip_id):
#    r = requests.get(BASE_URL + "routers/default/index/trips/{}".format(trip_id))
#    return r.json()
#
#def getAreas(language="is"):
#    r = requests.get(STOKKUR_URL + "areas/{}".format(language))
#    return r.json()
#    
#def getPlan(fromLatLng, toLatLng, time, date, arriveBy, maxPlans, language="is"):
#    if date == "now":
#        date = datetime.now().strftime("%d%m%Y")
#    if time == "now":
#        time = datetime.now().strftime("%H%M")
#    r = requests.get(STOKKUR_URL + \
#                     "routers/default/plan?fromPlace={}&toPlace={}&time={}&date={}&mode={}&arriveBy={}&wheelchair=false&showIntermediateStops=false&numItineraries={}&locale={}"\
#                     .format(fromLatLng, toLatLng, time, date, arriveBy, maxPlans, language))
#    return r.json()
#
#def getSearch(query, language="is"):
#    r = requests.get(STOKKUR_URL + "location/{}?search={}".format(language, query))
#    return r.json()
#
#def getReverseSearch(latitude, longitude):
#    r = requests.get("https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}".format(latitude, longitude))
#    return r.json()
#
#def getTimeTables(slug):
#    r = requests.get(ADMIN_URL + "timetables/{}".format(slug), headers={'web-language':'is'})
#    return r.json()
#
#def getTimeTableForRoute(schedule_id, route_id, category_id):
#    r = requests.get(ADMIN_URL + "timetables/{}/{}/{}".format(schedule_id, route_id, category_id), headers={'web-language':'is'})
#    return r.json()