#!/usr/bin/env python

# Certain compound can be found at certain planets, for example 
# can Tiberium be mined on planets with a hydrosphere, 
# Vespene gas need a volatile gas inventory and 
# Xenium can often be found on minor moons of planet. 
# dont know about unobtanium

import json, urllib2, time, math
# from pylab import *
# import numpy as np
# import matplotlib.pyplot as plt

url_root = "https://64.129.254.38:8000/api/?session=6bcf489f-756d-4e36-962f-12f3b76c8eb6"

# Phil's move code
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




def getMapData():
        # get star data
    
    response = urllib2.urlopen(url_root + '&command=longrange')
    html = response.read()
    
    #print html
    
    objects = json.loads(html)
    print objects
    
    x = []
    y = []
    labels = []
    x.append(88)
    y.append(144)
    labels.append("ship")
    
    for stars in objects["stars"]:
        x.append(float(stars["x"]))
        y.append(float(stars["y"]))
        labels.append(stars["name"])
    
    print len(x)

def moveToSystemCoord(x,y):
    response = urllib2.urlopen(url_root + '&command=shortrange')
    html = response.read()
    objects = json.loads(html)
    
    fin_x = x
    fin_y = y
    
    response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
    
    html = response2.read()
    ship = json.loads(html)
    beg_x = float(ship["systemx"])
    beg_y = float(ship["systemy"])
    print beg_x, fin_x, beg_y, fin_y
    
    while abs(beg_x - fin_x) > 0.01:
        print 'x:', beg_x, '->', fin_x
        response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
        html = response2.read()
        ship = json.loads(html)
        beg_x = float(ship["systemx"])
        dist = max(-0.4, fin_x - beg_x)
        dist = min(0.4, dist)
        print dist
        resp = urllib2.urlopen(url_root + '&command=ship&arg=setsystemvecx&arg2=' + str(dist))
        time.sleep(0.3)
    
    resp = urllib2.urlopen(url_root + '&command=ship&arg=setsystemvecx&arg2=' + str(0))
    
    while abs(beg_y - fin_y) > 0.01:
        print 'y:', beg_y, '->', fin_y
        response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
        html = response2.read()
        ship = json.loads(html)
        beg_y = float(ship["systemy"])
        dist = max(-0.4, fin_y - beg_y)
        dist = min(0.4, dist)
        print dist
        urllib2.urlopen(url_root + '&command=ship&arg=setsystemvecy&arg2=' + str(dist))
        time.sleep(0.3)
    
    resp = urllib2.urlopen(url_root + '&command=ship&arg=setsystemvecy&arg2=' + str(0))
    
    response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
    html = response2.read()
    ship = json.loads(html)
    print ship["currentplanet"]  #TODO change
    
    
def moveToUniCoord(x,y):
    response = urllib2.urlopen(url_root + '&command=longrange')
    html = response.read()
    objects = json.loads(html)
    
    fin_x = x
    fin_y = y
    
    response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
    
    html = response2.read()
    ship = json.loads(html)
    beg_x = float(ship["unix"])
    beg_y = float(ship["uniy"])
    print beg_x, fin_x, beg_y, fin_y
    
    while abs(beg_x - fin_x) > 0.01:
        print 'x:', beg_x, '->', fin_x
        response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
        html = response2.read()
        ship = json.loads(html)
        beg_x = float(ship["unix"])
        dist = max(-0.4, fin_x - beg_x)
        dist = min(0.4, dist)
        print dist
        resp = urllib2.urlopen(url_root + '&command=ship&arg=setunivecx&arg2=' + str(dist))
        time.sleep(0.3)
    
    resp = urllib2.urlopen(url_root + '&command=ship&arg=setunivecx&arg2=' + str(0))
    
    while abs(beg_y - fin_y) > 0.01:
        print 'y:', beg_y, '->', fin_y
        response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
        html = response2.read()
        ship = json.loads(html)
        beg_y = float(ship["uniy"])
        dist = max(-0.4, fin_y - beg_y)
        dist = min(0.4, dist)
        print dist
        urllib2.urlopen(url_root + '&command=ship&arg=setunivecy&arg2=' + str(dist))
        time.sleep(0.3)
    
    resp = urllib2.urlopen(url_root + '&command=ship&arg=setunivecy&arg2=' + str(0))
    
    response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
    html = response2.read()
    ship = json.loads(html)
    print ship["currentsystem"]
    
def moveShipLongRange():

    response = urllib2.urlopen(url_root + '&command=longrange')
    html = response.read()
    objects = json.loads(html)
    destination = raw_input("Enter a star:")
    
    print 'You entered', destination
    
    fin_x = 0
    fin_y = 0
    
    for stars in objects["stars"]:
    
        if stars["name"] == destination:
            fin_x = float(stars["x"])
            fin_y = float(stars["y"])
    
    response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
    
    html = response2.read()
    ship = json.loads(html)
    beg_x = float(ship["unix"])
    beg_y = float(ship["uniy"])
    print beg_x, fin_x, beg_y, fin_y
    
    while abs(beg_x - fin_x) > 0.01:
        print 'x:', beg_x, '->', fin_x
        response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
        html = response2.read()
        ship = json.loads(html)
        beg_x = float(ship["unix"])
        dist = max(-0.4, fin_x - beg_x)
        dist = min(0.4, dist)
        print dist
        resp = urllib2.urlopen(url_root + '&command=ship&arg=setunivecx&arg2=' + str(dist))
        time.sleep(0.3)
    
    resp = urllib2.urlopen(url_root + '&command=ship&arg=setunivecx&arg2=' + str(0))
    
    while abs(beg_y - fin_y) > 0.01:
        print 'y:', beg_y, '->', fin_y
        response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
        html = response2.read()
        ship = json.loads(html)
        beg_y = float(ship["uniy"])
        dist = max(-0.4, fin_y - beg_y)
        dist = min(0.4, dist)
        print dist
        urllib2.urlopen(url_root + '&command=ship&arg=setunivecy&arg2=' + str(dist))
        time.sleep(0.3)
    
    resp = urllib2.urlopen(url_root + '&command=ship&arg=setunivecy&arg2=' + str(0))
    
    response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
    html = response2.read()
    ship = json.loads(html)
    print ship["currentsystem"]

def moveShipShortRange():

    response = urllib2.urlopen(url_root + '&command=shortrange')
    html = response.read()
    objects = json.loads(html)
    destination = raw_input("Enter a planet:")
    
    print 'You entered', destination
    
    fin_x = 0
    fin_y = 0
    
    for planets in objects['system']["planetarray"]:
    
        if planets["planet_no"] == destination:
            fin_x = float(planets["x"])
            fin_y = float(planets["y"])
    
    response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
    
    html = response2.read()
    ship = json.loads(html)
    beg_x = float(ship["systemx"])
    beg_y = float(ship["systemy"])
    print beg_x, fin_x, beg_y, fin_y
    
    while abs(beg_x - fin_x) > 0.01:
        print 'x:', beg_x, '->', fin_x
        response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
        html = response2.read()
        ship = json.loads(html)
        beg_x = float(ship["systemx"])
        dist = max(-0.4, fin_x - beg_x)
        dist = min(0.4, dist)
        print dist
        resp = urllib2.urlopen(url_root + '&command=ship&arg=setsystemvecx&arg2=' + str(dist))
        time.sleep(0.3)
    
    resp = urllib2.urlopen(url_root + '&command=ship&arg=setsystemvecx&arg2=' + str(0))
    
    while abs(beg_y - fin_y) > 0.01:
        print 'y:', beg_y, '->', fin_y
        response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
        html = response2.read()
        ship = json.loads(html)
        beg_y = float(ship["systemy"])
        dist = max(-0.4, fin_y - beg_y)
        dist = min(0.4, dist)
        print dist
        urllib2.urlopen(url_root + '&command=ship&arg=setsystemvecy&arg2=' + str(dist))
        time.sleep(0.3)
    
    resp = urllib2.urlopen(url_root + '&command=ship&arg=setsystemvecy&arg2=' + str(0))
    
    response2 = urllib2.urlopen(url_root + '&command=ship&arg=show')
    html = response2.read()
    ship = json.loads(html)
    print ship["currentplanet"]  #TODO change

def repairOptions():
    repairs = open("/Users/pj/Documents/Aptana Studio 3 Workspace/devnull/space/repairs.json", "r")
    repairoptions = json.load(repairs)
    return repairoptions

def showSystems():
    shipsystems = urllib2.urlopen(url_root + "&command=ship&arg=showsystems")
    systems = json.load(shipsystems)
    return systems['systems']

    
def printResources():
    shipresources = urllib2.urlopen(url_root + "&command=ship&arg=showresources")
    resources = json.load(shipresources)
    print 'Resources:'
    for resource in resources['resources']:
        print resource['name'],'----','Amount:',resource['amount']
        
def scanUniverse():    
    longrange = urllib2.urlopen(url_root + "&command=longrange")
    spacedata = json.load(longrange) 
    return spacedata

def scanSystem():
    shortrange = urllib2.urlopen(url_root + "&command=shortrange")
    planetdata = json.load(shortrange) 
    return planetdata

def listStars():
    longrange = urllib2.urlopen(url_root + "&command=longrange")
    spacedata = json.load(longrange) 
    stars = spacedata['stars']
    for star in stars:
        print star['name'],'x',star['x'],'y',star['y']

def shipLocation():
    shippositionurl = urllib2.urlopen(url_root +"&command=ship&arg=show")
    shipposition = json.load(shippositionurl)
    #print shipposition
    print 'ship system:', shipposition['currentsystem']
    print 'ship planet:', shipposition['currentplanet']
    print 'ship X uni coord:', shipposition['unix']
    print 'ship Y uni coord:', shipposition['uniy']
    print 'ship X uni velocity:', shipposition['univecx']
    print 'ship Y uni velocity:', shipposition['univecy']
    print 'ship X system coord:', shipposition['systemx']
    print 'ship Y system coord:', shipposition['systemy']
    print 'ship X system velocity:', shipposition['systemvecx']
    print 'ship Y system velocity:', shipposition['systemvecy']

def mine(resource):
    mineurl = urllib2.urlopen(url_root +"&command=ship&arg=drones&arg2="+resource)
    minedata = json.load(mineurl)
    return minedata

def mineUntilFull(resource):
    result='mining'
    while result[0]=='m':
        result = mine(resource).values()[0]
        print result
        time.sleep(0.1)  #throttling
    
def objectScan():
    scanurl = urllib2.urlopen(url_root + "&command=object")
    html = scanurl.read()
    objectdata = json.loads(html)
    for key, value in objectdata['object_data'].iteritems():
        print str(key)+':'+str(value)

def autopilot(resource):
    pass
    
while 1:
    print '\n======MENU======'
    print 'Universe scan - 1'
    print 'System scan - 2'
    print 'Resources - 3'
    print 'List Stars - 4'
    print 'Ship Location - 5'
    print 'Mine - 6'
    print 'Repair Options - 7'
    print 'Ship Systems - 8'
    print 'Short Range Dest Move - 10'
    print 'Long Range Dest Move - 11'
    print 'Short Range Coord Move - 12'
    print 'Long Range Coord Move - 13'
    print 'Object Scan - 14'
    print 'Exit - 9'
    command = raw_input("Enter a command:")
    if command=='1':
        print scanUniverse()
    if command=='2':
        scanresults = scanSystem()
        ships = scanresults['otherships']
        for ship in ships:
            print ship
        system = scanresults['system']
        print system['name']
        for planet in system['planetarray']:
            for key in planet.keys():
                print key,'=',planet[key]
            print '********'
    if command=='3':
        printResources()
    if command=='4':
        listStars()
    if command=='5':
        shipLocation()
    if command=='6':
        miner = raw_input("Would you like to mine (T)iberium, (V)espene Gas, (U)nobtainium, or (X)enium?")
        if miner=='T':
            mineUntilFull('Tiberium')
        if miner=='V':
            mineUntilFull('Vespene%20gas')
        if miner=='U':
            mineUntilFull('Unobtainium')
        if miner=='X':
            mineUntilFull('Xenium')
            
    if command=='7':
        for system in repairOptions():
            print system
    if command=='8':
        for system in showSystems():
            print system['name'],'--- Functionality:',system['functionality']
    if command=='9':
        break
    if command=='10': 
        print 'Planets in range:'
        scanresults = scanSystem()
        system = scanresults['system']
        print system['name']
        for planet in system['planetarray']:
            print planet['planet_no']
        #moveShipShortRange()
        go_to_planet(raw_input("Enter a planet:"))
        
    if command=='11':
        print 'Stars:'
        universe = scanUniverse()
        for star in universe['stars']:
            print star['name']
        #moveShipLongRange()
        go_to_star(raw_input("Enter a star:"))
        
    if command=='12':
        x = float(raw_input("Enter the x value:"))
        y = float(raw_input("Enter the y value:"))
        moveToSystemCoord(x,y)
    if command=='13':
        x = float(raw_input("Enter the x value:"))
        y = float(raw_input("Enter the y value:"))
        moveToUniCoord(x,y)
    if command=='14':
        objectScan()

