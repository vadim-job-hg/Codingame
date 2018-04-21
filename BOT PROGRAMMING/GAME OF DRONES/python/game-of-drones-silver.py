###############################################################################
# Imports
###############################################################################

from __future__ import with_statement
import time
import sys
import math


###############################################################################
# Class declarations
###############################################################################

class Timer(object):
    def __init__(self):
        pass

    def __enter__(self):
        self.__start = time.time()

    def __exit__(self, type, value, traceback):
        self.__finish = time.time()

    def duration_in_seconds(self):
        return self.__finish - self.__start


class Point(object):
    """Defines the point object
    Has data attributes the x and y coordinate"""

    def __init__(self):
        self.x = 0
        self.y = 0

    def __str__(self):
        return (str(self.x) + ' ' + str(self.y))

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Drone(object):
    """Drone object referencing to the drone
    and contains an object referencing the position of drones"""

    def __init__(self):
        # Position of drone
        self.pos = Point()


class Zone(object):
    """Zone object referencing the zone
    Attributes are coordinates of the center
    and the owner id"""

    def __init__(self):
        # center of zone (radius = 100 units)
        self.center = Point()
        # Id is -1 for neutral zone
        self.OwnerId = -1
        # No. of mydrones in the zone
        self.numberMyDrones = 0
        # No. of max enemy drones in the zone
        self.maxEnemyDrones = 0


class Team(object):
    """One single team containing multiple drones"""

    def __init__(self):
        # list to store the Drone objects
        self.drones = []


class Game(object):
    """Game class running the show"""

    ###############################################################################
    # Functions to initialize the game
    ###############################################################################

    def __init__(self):
        # list of zone objects
        self.zones = []
        # list of team objects
        self.teams = []
        # My team id
        self.myTeamId = -1
        # Number of rounds
        self.numberOfRounds = 0
        # list of targets for each drone
        self.targetList = []
        # Boolean variable to indicate whether all zones belong to us
        self.allZonesBelongToUs = False
        # Boolean variable list to indicate whether to move or not to move
        self.moveDroneFromZone = []
        # create a list for zones that need help
        self.help = []
        # variable to store proximity
        self.proximity = 200
        # counters
        self.counter1 = []
        self.counter2 = []
        self.counter3 = []

    def debug(self, s):
        print >> sys.stderr, s

    def init(self):
        """Function to read initialization data
        from standard input"""

        # Enter first data
        s = raw_input()
        # p = number of players in the game 2 to 4
        # i = id of player(0,1,2 or 3)
        # d = number of drones in each team( 3 to 11)
        # z = number of zones in map(4 to 8)

        self.p, self.i, self.d, self.z = [int(var) for var in s.split()]

        # set my team id tag
        self.myTeamId = self.i

        # Enter details for each zone
        for areadId in xrange(self.z):

            # for each zone create a zone object
            z1 = Zone()

            # Enter the center of zone
            s = raw_input()
            z1.center.x, z1.center.y = [int(var) for var in s.split()]

            if z1 not in self.zones:
                self.zones.append(z1)

        # assign teams
        # for each team create an object and store in list
        t1 = [Team() for teamId in xrange(self.p)]

        for teamId in xrange(self.p):

            t1[teamId].drones = []

            # For each drone create a drone object and store in list
            d1 = [Drone() for droneId in xrange(self.d)]

            for droneId in xrange(self.d):
                # add the drone to the team
                t1[teamId].drones.append(d1[droneId])

            # add each team to the team list
            self.teams.append(t1[teamId])

        self.counter1 = [0] * self.d
        self.counter2 = [0] * self.d
        self.counter3 = [0] * self.d

    def run(self):
        """Function running during each round, takes as input
        zone ownerId and coordinates of all drones of all players"""

        while 1:

            for zone in self.zones:
                zone.ownerId = int(raw_input())

            for team in self.teams:
                for drone in team.drones:
                    s = raw_input()
                    drone.pos.x, drone.pos.y = [int(var) for var in s.split()]

            if self.numberOfRounds == 0:

                # create initial target List
                myDrones = self.teams[self.myTeamId].drones
                count = 0
                oldValue = []

                for drone in myDrones:
                    res = (self.createTarget(drone.pos, self.zones))

                    self.targetList.append(res)
                    self.debug('Drone %s goes to %s' % (count, res))
                    count += 1
                self.debug("run only once")

            timer = Timer()
            with timer:

                self.play()

            self.debug(str(timer.duration_in_seconds()))

    def findDistance(self, x1, y1, x2, y2):
        """Given coordinates of two points, finds the distance
        between them"""

        dx = x2 - x1
        dy = y2 - y1
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return distance

    def upDateMyDrones(self, zone):
        """Takes zone and finds number
        of my drones in the zone """

        count = 0
        myDrones = self.teams[self.myTeamId].drones
        for drone in myDrones:
            distance = int(self.findDistance(drone.pos.x, drone.pos.y,
                                             zone.center.x, zone.center.y))
            if distance <= 95:
                count += 1
        return count

    def maxEnemy(self, zone):
        """Takes zone and finds max number of enemy drones
        in the zone"""

        count = 0
        for playerNum in xrange(self.p):
            if playerNum != self.myTeamId:
                drones = self.teams[playerNum].drones
                for drone in drones:
                    distance = int(self.findDistance(drone.pos.x, drone.pos.y,
                                                     zone.center.x, zone.center.y))
                    if distance <= 100:
                        count += 1
        return count

    def closestPoint(self, x2, y2, x1, y1):
        """Find the closest point to the center of zone from the drone"""

        radius = 94
        dx = x2 - x1
        dy = y2 - y1

        distance = math.sqrt(dx ** 2 + dy ** 2)

        x3 = x1 + ((dx / distance) * radius)
        y3 = y1 + ((dy / distance) * radius)

        res = Point()
        res.x = int(x3)
        res.y = int(y3)

        return res

    def createTarget(self, pos, zones):
        """Creates an initial list of targets for each drone"""

        distList = []

        for zone in zones:
            if zone.ownerId != self.myTeamId:
                mDrones = zone.numberMyDrones
                eDrones = zone.maxEnemyDrones

                for playerNum in xrange(self.p):

                    if zone.ownerId == self.myTeamId:
                        coeff = 2
                    else:
                        coeff = 1

                if zone.ownerId == -1:
                    coeff = 0

                diff = mDrones - eDrones
                distance = self.findDistance(pos.x, pos.y, zone.center.x,
                                             zone.center.y)
                distList.append({(distance, diff, coeff): zone.center})

        if len(distList) == 0:
            return zones[0].center

        distList = sorted(distList, key=lambda k: k.keys()[0][1])
        distList = sorted(distList, key=lambda k: k.keys()[0][0])
        distList = sorted(distList, key=lambda k: k.keys()[0][2])

        res = distList[0].values()[0]
        # for i in xrange(len(distList)):
        #     self.debug('Debug target list created')
        #     self.debug('Distance %s ' % distList[i].keys()[0][0])
        #     self.debug('Drone difference %s ' % distList[i].keys()[0][1])
        #     self.debug('Zone ownage %s ' % distList[i].keys()[0][2])
        #     self.debug('Center of zone coordinates %s ' % distList[i].values()[0])

        # now find the closest point to the center of zone
        res1 = self.closestPoint(pos.x, pos.y, res.x, res.y)
        # self.debug('%s' %res1)

        return res1

    def findZone(self, pos):
        """Given the coordinates of a drone, find the zone in which it is"""

        distance = 0
        count = 0
        for zone in self.zones:
            distance = (self.findDistance(pos.x, pos.y, zone.center.x,
                                          zone.center.y))
            # self.debug('distance is %s' % distance)
            distance = int(distance)
            if distance <= 101:
                break
            count += 1

        return count

    def scanZone(self, center):
        """ Given the coordinates , find out enemy drones in area """

        count = 0

        for playerNum in xrange(self.p):

            if playerNum != self.myTeamId:
                drones = self.teams[playerNum].drones

                for drone in drones:
                    distance = int(self.findDistance(drone.pos.x, drone.pos.y, center.x, center.y))
                    if distance <= self.proximity:
                        count += 1

        return count

    def play(self):

        """The main algorithm to run the drones live here"""

        ###############################################################################
        # Updates to be done at start of a round
        ###############################################################################

        # Update no. of myDrones and maxEnemyDrones in the zone
        for zone in self.zones:
            zone.numberMyDrones = self.upDateMyDrones(zone)
            zone.maxEnemyDrones = self.maxEnemy(zone)

            ## Print debug info at the start of each round
            # self.debug('The input details for round number %s' %
            # self.numberOfRounds)

            # count = 0
            # for zone in self.zones:
            # self.debug('OwnerId for zone no %s %s' % (count, zone.ownerId))
            # self.debug('Zone no. %s zone center %s' % (count, zone.center))
            # self.debug('Number of myDrones in zone %s are %s' %
            # (count, zone.numberMyDrones))
            # self.debug('Number of max enemy drones in zone %s are %s' %
            # (count, zone.maxEnemyDrones))
            # count += 1

            # self.debug('Do all zones belong to us %s' % self.allZonesBelongToUs)

            # for i in xrange(self.p):
            # drones = self.teams[i].drones
            # self.debug('For player %s' % i)
            # for drone in drones:
            # self.debug('Coordinates are %s' % drone.pos)
            # self.debug(' ')

            # count = 0
            # for target in self.targetList:
            # self.debug('drone %s goes to %s' % (count, target))
            # count += 1
            # self.debug('#######################################################')
        ###############################################################################

        ###############################################################################
        # Code for the movement of drones
        ###############################################################################


        myDrones = self.teams[self.myTeamId].drones

        count1 = 0
        for drone in myDrones:
            self.debug('Drone no. %s location %s goes to %s' % (count1, drone.pos, self.targetList[count1]))
            count1 += 1

        count2 = 0
        for zone in self.zones:
            self.debug("My drones in zone %s are %s" % (count2, zone.numberMyDrones))
            self.debug("Enemy drones in zone %s are %s" % (count2, zone.maxEnemyDrones))


            # boolean variable to see whether my drones hold all the zones
        isZoneOwned = False

        # variable to count the no. of zones I own
        countZones = 0

        for zone in self.zones:
            if zone.ownerId == self.myTeamId:
                countZones += 1

        # check if its equal to my condition for owning all zones
        # condition: countZones >= self.z - 1

        if countZones >= self.z - 1:

            # CONDITION : WE OWN ALL THE ZONES
            # for drones who are at their destination, keep them there
            # for drones who have not yet reached their destination
            # either make them move to the destination if we don't own them or move them to the
            # zone where eDrones == mDrones

            # variabe to count the drones
            count = 0

            # run a loop for the drones
            for drone in myDrones:
                # check has the drone reached its destination

                # if drone.pos == self.targetList[count]:

                # CONDITION: WE OWN ALL THE ZONES AND DRONE HAS REACHED ITS TARGET

                # the drone has reached its target
                # keep it here
                print self.targetList[count]

                # Find the zone number in which the drone is
                zoneNumber = self.findZone(self.targetList[count])

                # debug info
                self.debug('Drone no. %s Zone number %s stays at %s' % (count, zoneNumber, self.targetList[count]))
                self.debug('Reason: the drone has reached its target, we own all the zones')

        else:

            self.debug("All zones not owned")

            myDrones = self.teams[self.myTeamId].drones

            count = 0

            for drones in myDrones:

                self.debug("drone %s" % drones.pos)
                self.debug("target %s" % self.targetList[count])

                if drones.pos.x == self.targetList[count].x and drones.pos.y == self.targetList[count].y:

                    self.debug('Drone has reached its target')

                    zoneNumber = self.findZone(self.targetList[count])

                    if self.zones[zoneNumber].ownerId == self.myTeamId:

                        self.debug('My team owns the drone')

                        mDrones = self.zones[zoneNumber].numberMyDrones
                        eDrones = self.zones[zoneNumber].maxEnemyDrones

                        if eDrones == 0 and mDrones >= 1:

                            # stay here

                            # if self.counter1[count] != 5:
                            print self.targetList[count]

                            self.debug('Drone no. %s stays at %s' % (count, self.targetList[count]))
                            self.debug('Reason: no enemy drones')

                            #   self.counter1[count] += 1
                            # else:

                            #     zones = self.zones

                            #     zones = zones[:zoneNumber] + zones[zoneNumber+1:]

                            #     self.targetList[count] = self.createTarget(drones.pos, zones)

                            #     print self.targetList[count]

                            #     self.counter1[count] = 0

                            #     self.debug('Drone no. %s goes to %s' % (count, self.targetList[count]))
                            #     self.debug('Reason: counter over')




                        elif eDrones == mDrones:

                            # stay here
                            print self.targetList[count]

                            self.debug('Drone no. %s stays at %s' % (count, self.targetList[count]))
                            self.debug('Reason: equal enemy and my drones')



                        elif mDrones > eDrones:

                            # move


                            zones = self.zones

                            zones = zones[:zoneNumber] + zones[zoneNumber + 1:]

                            self.targetList[count] = self.createTarget(drones.pos, zones)
                            print self.targetList[count]

                            self.zones[zoneNumber].numberMyDrones -= 1

                            self.debug('Drone no. %s goes to %s' % (count, self.targetList[count]))
                            self.debug('Reason: more drones than enemy')

                        else:

                            print self.targetList[count]



                    else:

                        self.debug('My team does not own the zone')

                        mDrones = self.zones[zoneNumber].numberMyDrones
                        eDrones = self.zones[zoneNumber].maxEnemyDrones

                        if mDrones == eDrones:

                            if self.counter2[count] != 10:

                                print self.targetList[count]

                                self.counter2[count] += 1

                                # call for help


                                self.debug('Drone no. %sstays at %s' % (count, self.targetList[count]))
                                self.debug('Reason: equal enemy and my drones')

                            else:

                                self.counter2[count] = 0

                                zones = self.zones

                                zones = zones[:zoneNumber] + zones[zoneNumber + 1:]

                                self.targetList[count] = self.createTarget(drones.pos, zones)

                                print self.targetList[count]

                                self.zones[zoneNumber].numberMyDrones -= 1

                                self.debug('Drone no. %s goes to %s' % (count, self.targetList[count]))
                                self.debug('Reason: timer over, same enemy drones')

                        else:

                            zones = self.zones

                            zones = zones[:zoneNumber] + zones[zoneNumber + 1:]

                            self.targetList[count] = self.createTarget(drones.pos, zones)

                            print self.targetList[count]

                            self.zones[zoneNumber].numberMyDrones -= 1

                            self.debug('Drone no. %s goes to %s' % (count, self.targetList[count]))
                            self.debug('Reason: more enemy drones')



                else:

                    # CONDITION DRONE HAS NOT REACHED THE TARGET
                    # see how the conditions are in the zone that you are going to reach


                    zoneNumber = self.findZone(self.targetList[count])

                    if self.zones[zoneNumber].ownerId == self.myTeamId:

                        # CONDITION IF WE OWN THE ZONE, THEN DON'T GO THERE

                        zones = self.zones

                        zones = zones[:zoneNumber] + zones[zoneNumber + 1:]

                        self.targetList[count] = self.createTarget(drone.pos, zones)

                        # move there
                        print self.targetList[count]

                        # new zone number
                        zoneNumber = self.findZone(self.targetList[count])

                        # debug info
                        self.debug('Drone no. %s goes to zone %s at coordinates %s' % (
                        count, zoneNumber, self.targetList[count]))
                        self.debug('Reason: Drone has not reached destination and the destination is already owned')

                    else:

                        # CONDITION WE DO NOT OWN THE TARGET ZONE, GO THERE

                        print self.targetList[count]

                        # debug info
                        self.debug('Drone no. %s goes to zone %s at coordinates %s' % (
                        count, zoneNumber, self.targetList[count]))
                        self.debug(
                            'Reason: Drone has not reached destination and the destination is either neutral or enemies')

                count += 1




                ###############################################################################

                ###############################################################################
                # Updates to be done at the end
                ###############################################################################

        # Update round number
        self.numberOfRounds += 1


###############################################################################


g = Game()
g.init()
g.run()
