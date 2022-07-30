#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""darksky.py"""
# pylint: disable=line-too-long

from subprocess import getoutput as unix
from time import time
import sys
import getopt
import json
import os

HOME = os.environ["HOME"]


def write_weather(name, value):
    """write weather"""
    with open(f"{HOME}/bin/geektool/weather.{name}.1", "w", encoding="utf-8") as fptr:
        fptr.write(value)


def read_cached_weather():
    """read cached weather"""
    with open(f"{HOME}/bin/geektool/weather.darksky.1", "r", encoding="utf-8") as fptr:
        darkskydata = fptr.read()
        try:
            weather = json.loads(darkskydata)
        except json.decoder.JSONDecodeError:
            weather = {'currently':{'temperature':'0.0', 'icon':'0', 'summary':'', 'uvIndex':'0', 'pressure':'999'}}
    return weather


def location_lat_long():
    """get the lat long of current location"""
    city = unix("curl -Ss https://wttr.in/?format=%l").split(",")[0]
    #print(city)
    location = unix(f"curl -Ss https://wttr.in/~{city} | grep ^Location:  ")
    #print(location)
    lat, long = location.split("]")[0].split("[")[1].split(",")
    #print(lat,long)
    loc = {'latitude': float(lat), 'longitude': float(long), 'city': city, 'location': {} }
    return loc


def get_weather(location):
    """# https://api.darksky.net/forecast/1719de3dfd7218343551e387a2f4694e/37.8267,-122.4233"""
    darksky_key = '1719de3dfd7218343551e387a2f4694e'
    darkskyurl = f"https://api.darksky.net/forecast/{darksky_key}/{location['latitude']},{location['longitude']}?units=uk2&exclude=hourly,minutely,flags"

    weather = read_cached_weather()
    if cache_valid(weather):
        return weather

    #print("get new weather")
    darkskydata = unix(f'curl -s "{darkskyurl}"')
    #print("DARKSKYDATA=",darkskydata)
    write_weather("darksky", darkskydata)
    try:
        weather = json.loads(darkskydata)
    except json.decoder.JSONDecodeError:
        weather = {'currently':{'temperature':'0.0', 'icon':'0', 'summary':'', 'uvIndex':'0', 'pressure':'999'}}
    return weather


def near(origin, newval):
    """within a small margin of a float value"""
    margin = 0.1
    return origin+margin > newval > origin-margin


def cache_valid(weather):
    """check time and location in cache against current values"""
    #print(f"weather[time] = {weather['currently']['time']}")
    current_time = int(time())
    #print(f"current time = {current_time}")
    if current_time - 3600 > int(weather['currently']['time']):
        #print("Need new weather - time")
        return False
    location = location_lat_long()
    #print(weather['latitude'], weather['longitude'])
    #print(location)
    if not near(weather['latitude'], location['latitude']) or not near(weather['longitude'], location['longitude']):
        #print("Need new weather - loc")
        return False
    return True


def details():
    """details"""
    weather = get_weather(location_lat_long())
    print("current weather", weather['currently'])
    print(f"temperature: {int(weather['currently']['temperature'])}°C")
    print(f"summary: {weather['currently']['summary']}")


def summary():
    """summary"""
    weather = get_weather(location_lat_long())
    print(f"{weather['currently']['summary']} {int(weather['currently']['temperature'])}°C")


def main():
    """main"""
    usage = "darksky.py -h   help\n           -d   details\n           -s   summary"
    try:
        longopt = ["help", "details", "summary"]
        shortopt = "hds"
        opts, _args = getopt.getopt(sys.argv[1:], shortopt, longopt)
    except getopt.GetoptError:
        print('GetoptError')
        print(usage)
        sys.exit(2)
    for opt, _arg in opts:
        #print(opt, arg)
        if opt in ('-h','--help'):
            print(usage)
            sys.exit()
        elif opt in ('-d','--details'):
            details()
            sys.exit()

    summary()
    sys.exit()


if __name__ == '__main__':
    main()
