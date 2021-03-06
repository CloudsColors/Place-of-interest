from flask import Flask, render_template, request, jsonify, make_response
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os, sys, sanitize, datetime,controller

dir_loadconfig = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,dir_loadconfig)
import loadconfig

app = Flask(__name__, template_folder=".")
#path from where this file is executed.
path = os.path.dirname(os.path.realpath(__file__))

config = loadconfig.load_json_file()

#sanitizer
sanitizer = sanitize.Sanitizer(config["server"]) # Verkar inte användas

#controller
Controller = controller.Controller(config)

config = None
del config

#What icon to show on map (flagged location & current location of user).
flaggedLocationsIcon = "http://maps.google.com/mapfiles/ms/icons/green-dot.png" #http://maps.google.com/mapfiles/ms/icons/blue-dot.png
currentLocationIcon = "http://maps.google.com/mapfiles/dir_0.png"

#marks which combine the icon and flaggedLocations.
marks = []

#read in the google maps API key
try:
    f = open(os.path.realpath(path+"/api_key/key.txt"), "r") #text file with your API key
except IOError:
    print("Couldn't fetch key for google maps API from "+path)
else:
    key = f.read()
    app.config['GOOGLEMAPS_KEY'] = key
    f.close()

GoogleMaps(app)

@app.route("/", methods=['GET', 'POST'])
def mapview():
    #lng & lat for positions to show.
        #flaggedLocations = [(65.621650, 22.117025, "Vänortsvägen"), (65.618776, 22.139475, "E-huset"), (65.618929, 22.051285, "Storheden")
    if request.method == "POST":
        return Controller.createQuery(request)

    if request.method == "GET":
        response = make_response(render_template('./templates/index.html', sndmap=renderMap()))
        return response

def addMark(lat, lng): # Verkar inte användas
    '''Retrieves all markers within a given circle from database
    Parameters
    ----------
    lat - latitude
    lng - longitude
    Returns
    -------
    A list containing all markers within the given circle 
    '''
    marks.append({
        "icon": flaggedLocationsIcon,
        "lat": lat,
        "lng": lng,
        "infobox": "Current location",
    })

def setup(): # Verkar inte användas
	min_range = 1000
	max_range = 10000
	step = 100
	return max_range, min_range

def renderMap():
    '''Renders the map to send to client.
    Returns
    -------
    The map with markers added.
    '''
    sndmap = Map(
        identifier="sndmap",
        lat=65.618776,
        lng=22.139475,
        markers=marks,
        style=(
            "height:100%;"
            "width:100%;"
			"border-radius: 4px;"
            "top:0;"
            "left:0;"
            "position: absolute;"
            "z-index:200;"
        ),
        zoom=14,
        center_on_user_location=True, 
        zoom_control = False,
        streetview_control = False,
        maptype_control = False,
    )
    return sndmap


if __name__ == "__main__":
    app.run( debug=True)
