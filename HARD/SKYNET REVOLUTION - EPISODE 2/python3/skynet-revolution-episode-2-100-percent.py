import sys
import math
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
    aDistances = []
    aPaths = []
    oDijk = None

    def __init__(self):
        self.iNbNodes, l, e = [int(i) for i in input().split()]
        self._defineMap(l)
        self._defineGateways(e)

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
                if self.aCritNodes.get(iGWChildren):
                    self.aCritNodes[iGWChildren] += 1
                else:
                    self.aCritNodes[iGWChildren] = 0

    def runRound(self):
        self.iSkynetNode = int(input())  # The index of the node on which the Skynet agent is positioned this turn
        if (self.isUnderPressure()):
            debug('isUnderPressure')
            return None

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

    def findDistancesAndPaths(self, si = None):
        if (si is None):
            si = self.iSkynetNode

        self.oDijk = Dijkstra(self.aMap, self.iNbNodes)
        for iGw in self.aGateways.keys():
            self.oDijk.findShortestPath(si, iGw)
            self.aDistances[iGw] = self.oDijk.getDistance(iGw)
            self.aPathes[iGw] = self.oDijk.getShortestPath(iGw)



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

    def findShortestPath(self, start, to = None):
        self.startnode = start
        for node, aLinks in self.map.items():
            if node == self.startnode:
                self.visited[node] = True
                self.distance[node] = 0
            else:
                self.visited[node] = False
                if self.map[self.startnode][node]:
                    self.distance[node] =  self.map[self.startnode][node]
                else:
                    self.distance[node] = self.infiniteDistance
                self.previousNode[node] = self.startnode


        tries = 0
        while (False in self.visited and tries <= self.numberOfNodes):
            self.bestPath = self.findBestPath(self.distance, self.visited.keys())
            if (to != None and self.bestPath == to):
                break

            self.updateDistanceAndPrevious(self.bestPath)
            self.visited[self.bestPath] = True
            tries +=1



    def findBestPath(self, ourDistance, ourNodesLeft):
        bestPath = self.infiniteDistance
        bestNode = None
        for nodeLeft in ourNodesLeft:
            if ourDistance[nodeLeft] < bestPath:
                bestPath = ourDistance[nodeLeft]
                bestNode = nodeLeft

        return bestNode

    '''
def updateDistanceAndPrevious(self, obp) {
foreach(self.map as node = > aLinks) {
if (
       (isset(self.map[obp][node])) & &
   (!(self.map[obp][node] == self.infiniteDistance) | | (self.map[obp][node] == 0)) & &
((self.distance[obp] + self.map[obp][node]) < self.distance[node])
) {
self.distance[node] = self.distance[obp] + self.map[obp][node];
self.previousNode[node] = obp;
}
}
}
def getDistance(self, to) {
return self.distance[to];
}

def getShortestPath(self, to = null) {
ourShortestPath = array();
foreach(self.map as node = > aLinks) {
if (to != = null & & to != = node)
{
continue;
}
ourShortestPath[node] = array();
endNode = null;
currNode = node;
ourShortestPath[node][] = node;
while (endNode == = null | | endNode != self.startnode) {
ourShortestPath[node][] = self.previousNode[currNode];
endNode = self.previousNode[currNode];
currNode = self.previousNode[currNode];
}
ourShortestPath[node] = array_reverse(ourShortestPath[node]);
if (to == = null | | to == = node) {
if (self.distance[node] >= self.infiniteDistance) {
ourShortestPath[node] =[];
continue;
}
if (to == = node) {
break;
}
}
}

if (to == = null) {
return ourShortestPath;
}
if (isset(ourShortestPath[to])) {
return ourShortestPath[to];
}
return [];
}
'''

oNetwork = Network()
while True:
    oNetwork.runRound()