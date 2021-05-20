#!/usr/bin/python3

class Waypoint:

    def __init__(self, id, name, x, y, lat, lon, alt, ground_alt):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.ground_alt = ground_alt