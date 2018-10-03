# Note this code is heavily based on the Thingspeak plugin by Atle Ravndal
# and I acknowledge his efforts have made the creation of this plugin possible
#
# TODO
#	* Check result of request() call and react
#	* Log results to multiple places (brewstat.us, brewfather?, MQTT?

from modules import cbpi
from thread import start_new_thread
import logging
import requests
import datetime

DEBUG = True
drop_first = None

# Parameters
brewfather_comment = None
brewfather_url = None

# brewfather uses brew name to direct data to a particular batch 
#   associate a Tilt color with a Brew Name here. I don't like
#   doing it this way must be an array or some way better to do this
brewfather_RED_beer = None
brewfather_PINK_beer = None

def log(s):
    if DEBUG:
        s = "brewfather: " + s
        cbpi.app.logger.info(s)

@cbpi.initalizer(order=9000)
def init(cbpi):
    cbpi.app.logger.info("brewfather plugin Initialize")
    log("Brewfather params")
    global brewfather_comment
    global brewfather_url
    global brewfather_RED_beer
    global brewfather_PINK_beer

    brewfather_comment = cbpi.get_config_parameter("brewfather_comment", None)
    log("Brewfather brewfather_comment %s" % brewfather_comment)
    brewfather_url = cbpi.get_config_parameter("brewfather_url", None)
    log("Brewfather brewfather_url %s" % brewfather_url)
    brewfather_RED_beer = cbpi.get_config_parameter("brewfather_RED_beer", None)
    log("Brewfather brewfather_RED_beer %s" % brewfather_RED_beer)
    brewfather_PINK_beer = cbpi.get_config_parameter("brewfather_PINK_beer", None)
    log("Brewfather brewfather_PINK_beer %s" % brewfather_PINK_beer)

    if brewfather_comment is None:
	log("Init brewfather config Comment")
	try:
# TODO: is param2 a default value?
	    cbpi.add_config_parameter("brewfather_comment", "", "text", "Brewfather comment")
	except:
	    cbpi.notify("Brewfather Error", "Unable to update Brewfather comment parameter", type="danger")
    if brewfather_url is None:
	log("Init brewfather config URL")
	try:
# TODO: is param2 a default value?
	    cbpi.add_config_parameter("brewfather_url", "", "text", "Brewfather url")
	except:
	    cbpi.notify("Brewfather Error", "Unable to update Brewfather url parameter", type="danger")
    if brewfather_RED_beer is None:
	log("Init brewfather config RED_beer")
	try:
# TODO: is param2 a default value?
	    cbpi.add_config_parameter("brewfather_RED_beer", "", "text", "Brewfather RED_beer")
	except:
	    cbpi.notify("Brewfather Error", "Unable to update Brewfather RED_beer parameter", type="danger")
    if brewfather_PINK_beer is None:
	log("Init brewfather config PINK_beer")
	try:
# TODO: is param2 a default value?
	    cbpi.add_config_parameter("brewfather_PINK_beer", "", "text", "Brewfather PINK_beer")
	except:
	    cbpi.notify("Brewfather Error", "Unable to update Brewfather PINK_beer parameter", type="danger")
    log("Brewfather params ends")

# interval=900 is 900 seconds, 15 minutes, same as the Tilt Android App logs.
@cbpi.backgroundtask(key="brewfather_task", interval=900)
def brewfather_background_task(api):
    log("brewfather background task")
    global drop_first
    if drop_first is None:
        drop_first = False
        return False

    if brewfather_url is None:
        return False
# TODO might want to check we have at least one COLOR_beer param here too

    now = datetime.datetime.now()
    for key, value in cbpi.cache.get("sensors").iteritems():
	log("key %s value.name %s value.instance.last_value %s" % (key, value.name, value.instance.last_value))
#
# TODO: IMPORTANT - Temp sensor must be defined preceeding Gravity sensor and 
#		    each Tilt must be defined as a pair without another Tilt
#		    defined between them, e.g.
#			RED Temperature
#			RED Gravity
#			PINK Temperature
#			PINK Gravity
#
	if (value.type == "TiltHydrometer"):
	    if (value.instance.sensorType == "Temperature"):
# A Tilt Temperature device is the first of the Tilt pair of sensors so
#    reset the data block to empty
		data = {}
# generate timestamp in "Excel" format
		data['Timepoint'] = now.toordinal() - 693594 + (60*60*now.hour + 60*now.minute + now.second)/float(24*60*60)
		data['Color'] = value.instance.color
		if (value.instance.color == 'Red'):
		    data['beer'] = cbpi.get_config_parameter("brewfather_RED_beer", None)
		elif (value.instance.color == 'Pink'):
		    data['beer'] = cbpi.get_config_parameter("brewfather_PINK_beer", None)
# TODO: would this work here? data['beer'] = cbpi.get_config_parameter("brewfather_%s" % value.instance.color, None)
		data['Temp'] = value.instance.last_value
# brewfather expects *F so convert back if we use C
		if (cbpi.get_config_parameter("unit",None) == "C"):
		    data['Temp'] = value.instance.last_value * 1.8 + 32
	    if (value.instance.sensorType == "Gravity"):
		data['SG'] = value.instance.last_value
		data['Comment'] = cbpi.get_config_parameter("brewfather_comment", None)
		log("Data %s" % data)
		headers = {'content-type': '"application/x-www-form-urlencoded; charset=utf-8"'}
		url = cbpi.get_config_parameter("brewfather_url", None)
		r = requests.post(url, headers=headers, data=data)
		log("Result %s" % r.text)
    log("brewfather done")
