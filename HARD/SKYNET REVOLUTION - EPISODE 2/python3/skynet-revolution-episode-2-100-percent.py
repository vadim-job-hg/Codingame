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
        if (si is None) {
            si = self.iSkynetNode;
        }
        $this->oDijk = new Dijkstra($this->aMap, $this->iNbNodes);
        foreach (array_keys($this->aGateways) as $iGw) {
            $this->oDijk->findShortestPath($si, $iGw);
            $this->aDistances[$iGw] = $this->oDijk->getDistance($iGw);
            $this->aPathes[$iGw] = $this->oDijk->getShortestPath($iGw);
        }




oNetwork = Network()
while True:
    oNetwork.runRound()