import urllib2
import json
import math
import time

url_root = "https://64.129.254.38:8000/api/?session=6bcf489f-756d-4e36-962f-12f3b76c8eb6"

def get_ship():
    ship_response = urllib2.urlopen(url_root + '&command=ship&arg=show')
    html = ship_response.read()
    return json.loads(html)

def dist(a, b):
    return math.sqrt( pow(a[0]-b[0], 2) + pow(a[1]-b[1],2) )

def go_to_destination_within_star(dest):
    ship_obj = get_ship()
    ship = [ float(ship_obj["systemx"]),float(ship_obj["systemy"]) ]
    
    while dist(ship, dest) >= 0.05:
        move_vec = [ dest[0] - ship[0], dest[1] - ship[1] ]
        urllib2.urlopen(url_root + '&command=ship&arg=setsystemvecx&arg2=' + str(move_vec[0]))
        urllib2.urlopen(url_root + '&command=ship&arg=setsystemvecy&arg2=' + str(move_vec[1]))
    
        time.sleep(0.3)
        print 'Planetary movement: ('+str(ship[0])+', '+str(ship[1])+') moving to ('+str(dest[0])+', '+str(dest[1])+') with move vector of ('+str(move_vec[0])+', '+str(move_vec[1])+')'

        ship_obj = get_ship()
        ship = [ float(ship_obj["systemx"]),float(ship_obj["systemy"]) ]

    # stop!
    urllib2.urlopen(url_root + '&command=ship&arg=setsystemvecx&arg2=0')
    urllib2.urlopen(url_root + '&command=ship&arg=setsystemvecy&arg2=0')

    ship_obj = get_ship()
    print 'Ship has stopped at', ship_obj["currentplanet"]

def go_to_planet(planet_name):
    response = urllib2.urlopen(url_root + '&command=shortrange')
    html = response.read()
    objects = json.loads(html)

    for planet in objects["system"]["planetarray"]:
        if planet["planet_no"] == planet_name:
            dest = [float(planet["x"]), float(planet["y"])]

    print 'Going to', dest
    go_to_destination_within_star(dest)

def get_closest_corner_within_star():
    ship_obj = get_ship()
    ship = [ float(ship_obj["systemx"]),float(ship_obj["systemy"]) ]
    ship[0] = 0 if ship[0] < 100 else 199
    ship[1] = 0 if ship[1] < 100 else 199
    return ship

def go_to_star(star_name):
    response = urllib2.urlopen(url_root + '&command=longrange')
    html = response.read()
    objects = json.loads(html)

    for star in objects['stars']:
        if star['name'] == star_name:
            dest = [float(star["x"]), float(star["y"])]

    print 'Going to', dest

    ship_obj = get_ship()
    ship = [ float(ship_obj["unix"]),float(ship_obj["uniy"]) ]
    
    while dist(ship, dest) >= 0.05:
        move_vec = [ dest[0] - ship[0], dest[1] - ship[1] ]
        move_response = urllib2.urlopen(url_root + '&command=ship&arg=setunivecx&arg2=' + str(move_vec[0]))
        urllib2.urlopen(url_root + '&command=ship&arg=setunivecy&arg2=' + str(move_vec[1]))
    
        # Check if we're too close to a planet. If so, move to a corner.
        move_response_parsed = json.loads(move_response.read())
        if ('error' in move_response_parsed and move_response_parsed['error'] == 'Cannot activate FTL drive so close to star'):
            corner = get_closest_corner_within_star()
            go_to_destination_within_star(corner)
    
        time.sleep(0.3)
        print 'Universe movement: ('+str(ship[0])+', '+str(ship[1])+') moving to ('+str(dest[0])+', '+str(dest[1])+') with move vector of ('+str(move_vec[0])+', '+str(move_vec[1])+')'

        ship_obj = get_ship()
        ship = [ float(ship_obj["unix"]),float(ship_obj["uniy"]) ]

    # stop!
    urllib2.urlopen(url_root + '&command=ship&arg=setunivecx&arg2=0')
    urllib2.urlopen(url_root + '&command=ship&arg=setunivecy&arg2=0')

    ship_obj = get_ship()
    print 'Ship has stopped at', ship_obj["currentsystem"]



resource = 'Xenium'
    
destination = raw_input("Enter a planet: ")
go_to_planet(destination)
# destination = raw_input("Enter a star: ")
# go_to_star(destination)
# mine(resource)