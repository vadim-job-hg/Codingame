import math
import sys

class Network:
    graph = {}
    gateways = {}
    nodeDanger = {}
    gatewayCounter = 0
    g = 0
    SI = 0

    def __init__(self, n, g):
        #graph = new int[N][N];
        #gateways = new boolean[N];
        #nodeDanger = new int[N];
        self.g=g


    def addLink(self, n1, n2):
        self.graph.setdefault(n2, {})[n1]=1
        self.graph.setdefault(n1, {})[n2]=1

    def addGateWay(self, EI):
        self.gateways[EI] = True        
        for i in range(len(self.graph)):
            if(self.graph.get(i, {}).get(EI, 0) != 0):
                self.graph[i][EI] = 2
            if(self.graph.get(EI, {}).get(i, 0) != 0):
                self.graph[EI][i] = 2

        self.gatewayCounter+=1
        print(self.graph, file=sys.stderr)
        if(self.gatewayCounter == self.g):
            self.calculateDnagerForNodes()


    def calculateDnagerForNodes(self):
        for i in range(len(self.nodeDanger)):
            if(not(self.gateways[i])):
                for i in range(len(self.graph[i])):
                    if(self.graph[i][j] == 2):
                        self.nodeDanger[i]+=1



    def setSI(self, SI):
        this.SI = SI


    #Calculates distances from agent, if the path always contains nodes that link to gateways then that distance is 0, otherwise it incurs a penalty if the path contains illogical hops
    def distanceFromSI(self):
        '''
        int[] distances = new int[graph.length];
        Arrays.fill(distances, Integer.MAX_VALUE);
        emptyCells = graph.length;
        int checkAgainst = -1;
        List<Integer> queue = new LinkedList<Integer>();
        Arrays.fill(distances, Integer.MAX_VALUE);
        distances[SI] = 0;
        emptyCells--;
        queue.add(SI);
        while (emptyCells>0 && !queue.isEmpty()){
            checkAgainst = queue.remove(0);
            if(distances[checkAgainst] != Integer.MAX_VALUE) {
                for (int i = 0; i < graph.length; i++)
                    if (graph[i][checkAgainst] != 0 && distances[i] > distances[checkAgainst] + 1 + (nodeDanger[checkAgainst] == 0 ? (nodeDanger[i] == 0 ? 2 : 1) : 0)) {
                        queue.add(i);
                        distances[i] = distances[checkAgainst] + (nodeDanger[checkAgainst] == 0 ? (nodeDanger[i] == 0 ? 2 : 1) : 0);
                        emptyCells--;
                    }
            }
        }
        return distances
        '''
        pass


    def severBestLink(self):
        '''
        #First we see if SI can jump to an exit node this turn, if so then we sever that link.
        for(int i = 0; i<graph.length; i++)
            if(graph[i][SI] == 2){
                graph[i][SI] = 0;
                graph[SI][i] = 0;
                nodeDanger[SI]--;
                return i+" "+SI;
            }
        # We find the "closest" dangerous node, meaning node which links to two or more gateways
        int[] distances = distanceFromSI();
        int smallestDoubleDist = Integer.MAX_VALUE;
        int closestDoubleNode = -1;
        int smallestSingleDist = Integer.MAX_VALUE;
        int closestSingleNode = -1;
        for(int i = 0; i<distances.length; i++){
            if(nodeDanger[i] > 1 && distances[i]<smallestDoubleDist) {
                closestDoubleNode = i;
                smallestDoubleDist = distances[i];
            }
            if(nodeDanger[i] > 0 && distances[i]<smallestSingleDist) {
                closestSingleNode = i;
                smallestSingleDist = distances[i];
            }
        }
        int closestNode = closestDoubleNode == -1 ? closestSingleNode : closestDoubleNode;
        for(int i = 0; i<graph[closestNode].length; i++){
            if(graph[i][closestNode] == 2){
                graph[i][closestNode] = 0;
                graph[closestNode][i] = 0;
                nodeDanger[closestNode]--;
                return i+" "+closestNode;
            }
        }
        return "Zolda"
        '''
        pass

n, l, e = [int(i) for i in input().split()]

network = Network(n, e)

for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]
    network.addLink(n1, n2)

for i in range(e):
    network.addGateWay(int(input()))

# game loop
#while True:
#   si = int(input())  # The index of the node on which the Skynet agent is positioned this turn
#    network.setSI(si)
#    print(network.severBestLink())