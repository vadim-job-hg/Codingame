/*~~~~~~~~~~~~~~~~~~*
 *                  *
 * $Dollar Akshay$  *
 *                  *
 *~~~~~~~~~~~~~~~~~~*/

//

#include <math.h>
#include <time.h>
#include <ctype.h>
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <map>
#include <set>
#include <deque>
#include <queue>
#include <stack>
#include <string>
#include <vector>
#include <iostream>
#include <algorithm>


using namespace std;

#define sp system("pause")
#define FOR(i,a,b) for(int i=a;i<=b;++i)
#define FORD(i,a,b) for(int i=a;i>=b;--i)
#define REP(i,n) FOR(i,0,(int)n-1)
#define pb(x) push_back(x)
#define mp(x) make_pair(x)
#define DB(s,x) fprintf(stderr,s,x);
#define MS(x,n) memset(x,n,sizeof(x))
#define SORT(a,n) sort(begin(a),begin(a)+n)
#define REV(a,n) reverse(begin(a),begin(a)+n)
#define ll long long
#define MOD 1000000007

struct zoneNode{
	int ID;
	int ownerID;
	int platinum;
	bool visible;
	int enemyPods, myPods;
	vector<int> neighbours;
};

int roundNo;
int enemyID, myID;
int zoneCount, linkCount;
int enemyBase, myBase;
int platinum[251];
int podCount[251];
vector<int> enemyPods;
vector<int> myPods;

zoneNode zone[500];

void init(){

	roundNo = 1;
	srand(time(NULL));
}

void randomMove(int pod){

	int podZoneID = myPods[pod];
	int neighbours = zone[podZoneID].neighbours.size();
	int randomNeighbour = zone[podZoneID].neighbours[rand() % neighbours];
	printf("1 %d %d", podZoneID, randomNeighbour);

}

int main(){

	init();

	int players;
	scanf("%d%d%d%d", &players, &myID, &zoneCount, &linkCount);
	enemyID = !myID;

	//Reading ZoneID and Platinum
	REP(i, zoneCount){
		int id, p;
		scanf("%d%d", &id, &p);
		zone[id].platinum = p;
	}

	//Reading Links
	REP(i, linkCount){
		int z1, z2;
		scanf("%d%d", &z1, &z2);
		zone[z1].neighbours.pb(z2);
		zone[z2].neighbours.pb(z1);
	}
	while (1)printf("WAIT\nWAIT\n");
	//Game Loop
	while(1){
		//Reading Current Platinum
		scanf("%d", &platinum[roundNo]);
		myPods.clear();
		enemyPods.clear();

		//Reading Zones
		REP(i, zoneCount){
			int id, own,p0,p1,v,p;
			scanf("%d%d%d%d%d%d", &id, &own, &p0, &p1, &v, &p);
			zone[id].ownerID = own;
			zone[i].visible = v;
			zone[i].enemyPods = myID ? p0 : p1;
			REP(j, zone[i].enemyPods)
				enemyPods.pb(i);
			zone[i].myPods = myID ? p1 : p0;
			REP(j, zone[i].myPods)
				myPods.pb(i);
			zone[id].platinum = p;
		}

		podCount[roundNo] = myPods.size();
		DB("POD Count : %d\n", podCount[roundNo]);
		DB("Platinum Earned Last Round : %d\n",
			platinum[roundNo] - platinum[roundNo - 1] + 20 * (podCount[roundNo] - podCount[roundNo - 1]));

		if (roundNo == 1){
			enemyBase = enemyPods[0];
			myBase = myPods[0];
			DB("My Base ID : %d\n", myBase);
			DB("Enemy Base ID : %d\n", enemyBase);
		}

		//Make a move for all the pods
		REP(i, myPods.size()){
			if (i)
				printf(" ");
			randomMove(i);
		}
		printf("\nWAIT\n");

		DB("End of Round #%d\n", roundNo);
		roundNo++;
	}

	return 0;
}

//RANDOM AI : Each pod moves to a random zone next to it.