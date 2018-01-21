import sys
import math
import operator

DEBUG = True


def debug(*args):
    if (DEBUG):
        print(args, file=sys.stderr)


class Network:
    iNbNodes = 0
    iSkynetNode = None
    aMap = {}
    aGateways = {}
    aCritNodes = {}
    aDistances = {}
    aPathes = {}
    oDijk = None

    def __init__(self):
        self.iNbNodes, l, e = [int(i) for i in input().split()]
        self._defineMap(l)
        self._defineGateways(e)
        # debug('map', self.aMap)
        # debug('aCritNodes', self.aCritNodes);

    def _defineMap(self, nbLinks):
        for i in range(nbLinks):
            # n1: N1 and N2 defines a link between these nodes
            n1, n2 = [int(j) for j in input().split()]
            self.aMap.setdefault(n2, {})[n1] = 1
            self.aMap.setdefault(n1, {})[n2] = 1
            self.aMap.setdefault(n2, {})[n2] = 0
            self.aMap.setdefault(n1, {})[n1] = 0

    def _defineGateways(self, nbExit):
        for i in range(nbExit):
            ei = int(input())  # the index of a gateway node
            self.aGateways[ei] = self.aMap[ei]
            del (self.aGateways[ei][ei])
            del (self.aMap[ei])
            self.aMap[ei] = {ei: 0}
            for iGWChildren in self.aGateways[ei].keys():
                if self.aCritNodes.get(iGWChildren, False):
                    self.aCritNodes[iGWChildren] += 1
                else:
                    self.aCritNodes[iGWChildren] = 1

    def runRound(self):
        self.iSkynetNode = int(input())  # The index of the node on which the Skynet agent is positioned this turn
        if (self.isUnderPressure()):
            debug('isUnderPressure')
            return None

        debug('findDistancesAndPaths')
        self.findDistancesAndPaths()

        if (self.findCriticalPressureForGateways()):
            debug('findCriticalPressureForGateways')
            return None

        if (self.findPressureForAllGateways()):
            debug('findPressureForAllGateways')
            return None

        debug('cutClosestLink')
        self.cutClosestLink()

    def isUnderPressure(self):
        for iGWNode, aChildrenPath in self.aGateways.items():
            aChildren = aChildrenPath.keys()
            if self.iSkynetNode in aChildren:
                self.cutLink(iGWNode, self.iSkynetNode)
                return True
        return False

    def findDistancesAndPaths(self, si=None):
        if (si is None):
            si = self.iSkynetNode

        self.oDijk = Dijkstra(self.aMap, self.iNbNodes)
        for iGw in self.aGateways.keys():
            self.oDijk.findShortestPath(si, iGw)
            self.aDistances[iGw] = self.oDijk.getDistance(iGw)
            self.aPathes[iGw] = self.oDijk.getShortestPath(iGw)

    def findCriticalPressureForGateways(self):
        #debug(self.aCritNodes.items())
        for iCriticalNode, criticalLevel in self.aCritNodes.items():
            if (criticalLevel <= 1):
                continue

            self.oDijk.findShortestPath(self.iSkynetNode, iCriticalNode)
            aPath = self.oDijk.getShortestPath(iCriticalNode)[1::-1]
            aPath = aPath[1:]
            while (len(aPath) > 0):
                iAnalyzingNode = aPath[0]
                aPath = aPath[1:]
                #debug(self.aCritNodes)
                #debug(iAnalyzingNode)
                if (iAnalyzingNode not in self.aCritNodes):
                    continue
                criticalLevel -= 1

            if (criticalLevel <= 0):
                continue

            for iGW, aChildren in self.aGateways.items():
                if (iCriticalNode in aChildren):
                    return self.cutLink(iCriticalNode, iGW)

        return False

    def findPressureForAllGateways(self):
        sorted(self.aDistances.items(), key=lambda x: x[1])
        for iGW in self.aDistances.keys():
            aPathToFarest = self.aPathes[iGW][1:-1]
            for iNodeInWay in aPathToFarest:
                if (not(self.aCritNodes[iNodeInWay])):
                    iWeakNode = self.hasWeakNode(iGW)
                    if (False != iWeakNode):
                        self.cutLink(iGW, iWeakNode)
                        return True

                    break

                if (iNodeInWay in self.aCritNodes and self.aCritNodes[iNodeInWay] > 1):
                    self.cutLink(iGW, iNodeInWay)
                    return True

        return False

    def cutClosestLink(self):
        sorted(self.aDistances.items(), key=lambda x: x[1])
        # reset(this->aDistances);
        iNearestNode = list(self.aDistances.keys())[0]
        debug('iNearestNode',iNearestNode)
        aShortestPath = self.aPathes[iNearestNode]
        debug('aPathes',self.aPathes)
        aLinkRemoved = aShortestPath[:-2]
        debug('aShortestPath',aShortestPath)
        iNode1, iNode2 = aLinkRemoved
        self.cutLink(iNode1, iNode2)

    def cutLink(self, n1, n2):
        if n1 in self.aCritNodes:
            self.aCritNodes[n1] -= 1
        if n2 in self.aCritNodes:
            self.aCritNodes[n2] -= 1

        if (n1 in self.aMap and n1 in self.aMap[n1]):
            del (self.aMap[n1][n1])
        if (n1 in self.aMap and n2 in self.aMap[n1]):
            del (self.aMap[n1][n2])
        if (n2 in self.aMap and n1 in self.aMap[n2]):
            del (self.aMap[n2][n1])
        if (n2 in self.aMap and n2 in self.aMap[n2]):
            del (self.aMap[n2][n2])
        if (n1 in self.aGateways and n2 in self.aGateways[n1]):
            del (self.aGateways[n1][n2])
        if (n2 in self.aGateways and n1 in self.aGateways[n2]):
            del (self.aGateways[n2][n1])

        print('{} {}'.format(n1, n2))
        return True


class Dijkstra():
    visited = {}
    distance = {}
    previousNode = {}
    startnode = None
    map = []
    infiniteDistance = 0
    numberOfNodes = 0
    bestPath = 0
    matrixWidth = 0

    def __init__(self, ourMap, infiniteDistance):
        self.infiniteDistance = infiniteDistance
        self.map = ourMap
        self.numberOfNodes = len(ourMap)
        self.bestPath = 0

    def findShortestPath(self, start, to=None):
        self.startnode = start
        for node, aLinks in self.map.items():
            if node == self.startnode:
                self.visited[node] = True
                self.distance[node] = 0
            else:
                self.visited[node] = False
                if self.startnode in self.map and node in self.map[self.startnode]:
                    self.distance[node] = self.map[self.startnode][node]
                else:
                    self.distance[node] = self.infiniteDistance
                self.previousNode[node] = self.startnode

        tries = 0
        while (False in self.visited.values() and tries <= self.numberOfNodes):
            self.bestPath = self.findBestPath(self.distance, self.visited.keys())
            if (to != None and self.bestPath == to):
                break

            self.updateDistanceAndPrevious(self.bestPath)
            self.visited[self.bestPath] = True
            tries += 1

    def findBestPath(self, ourDistance, ourNodesLeft):
        bestPath = self.infiniteDistance
        bestNode = None
        for nodeLeft in ourNodesLeft:
            if ourDistance[nodeLeft] < bestPath:
                bestPath = ourDistance[nodeLeft]
                bestNode = nodeLeft

        return bestNode

    def updateDistanceAndPrevious(self, obp):
        for node, aLinks in self.map.items():
            if (obp in self.map and node in self.map[obp] and (
                    not (self.map[obp][node] == self.infiniteDistance) or (self.map[obp][node] == 0)) and (
                    (self.distance[obp] + self.map[obp][node]) < self.distance[node])):
                self.distance[node] = self.distance[obp] + self.map[obp][node]
                self.previousNode[node] = obp

    def getDistance(self, to):
        return self.distance[to]

    def getShortestPath(self, to=None):
        ourShortestPath = {}
        for node, aLinks in self.map.items():
            if (to != None and to != node):
                continue

            ourShortestPath[node] = []
            endNode = None
            currNode = node
            ourShortestPath[node].append(node)

            while (endNode == None or endNode != self.startnode):
                ourShortestPath[node].append(self.previousNode[currNode])
                endNode = self.previousNode[currNode]
                currNode = self.previousNode[currNode]

            ourShortestPath[node] = ourShortestPath[node][::-1]
            if (to == None or to == node):
                if (self.distance[node] >= self.infiniteDistance):
                    ourShortestPath[node] = []
                    continue

                if (to == node):
                    break

        if (to == None):
            return ourShortestPath

        if (to in ourShortestPath):
            return ourShortestPath[to]

        return []


oNetwork = Network()
while True:
    oNetwork.runRound()