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
    aGateways = []
    aCritNodes = []
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
            gat.append(ei)
            self.aGateways[ei] = self.aMap[ei]
            del(self.aGateways[ei][ei])
            del(self.aMap[ei])
            self.aMap[ei][ei] = 0
            for iGWChildren in self.aGateways[ei].keys():
                self.aCritNodes.setdefault(iGWChildren, 0) +=1

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


        debug('cutClosestLink');
        self.cutClosestLink()



    oNetwork = Network()
    while True:
        oNetwork.runRound()