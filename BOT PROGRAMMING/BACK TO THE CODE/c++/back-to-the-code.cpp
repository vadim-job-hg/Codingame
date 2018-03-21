/*~~~~~~~~~~~~~~~~~~*
 *                  *
 * $Dollar Akshay$  *
 *                  *
 *~~~~~~~~~~~~~~~~~~*/

//https://www.codingame.com/ide/1526078ee19ffd189c4ed396e14b55c2e42a526

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
#include <unordered_map>

using namespace std;

#define sp system("pause")
#define FOR(i,a,b) for(int i=a;i<=b;++i)
#define FORD(i,a,b) for(int i=a;i>=b;--i)
#define REP(i,n) FOR(i,0,(int)n-1)
#define pb(x) push_back(x)
#define mp(a,b) make_pair(a,b)
#define DB(format,...) fprintf(stderr,format, ##__VA_ARGS__)
#define MS(a,x) memset(a,x,sizeof(a))
#define SORT(a,n) sort(begin(a),begin(a)+n)
#define REV(a,n) reverse(begin(a),begin(a)+n)
#define ll long long
#define pii pair<int,int>
#define MOD 1000000007

int MAX_DEPTH = 6;
int playerCount, ordering = 0;
const int MIN = -10000;
const int MAX = 10000;

struct point {
	int x, y;
public:
	inline point() {
		x = 1;
		y = 1;
	}
	inline point(int px, int py) {
		x = px;
		y = py;
	}
	inline void print() {
		printf("%d %d\n", x, y);
	}
	inline int manhatanDistance(point p) {
		return abs(x-p.x) + abs(y-p.y);
	}
	inline bool operator != (const point rhs) const{
		return x!=rhs.x || y!=rhs.y;
	}
	inline bool operator == (const point rhs) const {
		return x==rhs.x && y==rhs.y;
	}
	inline bool operator < (const point rhs) const {
		return (x<rhs.x) || (x==rhs.x && y<rhs.y);
	}
	inline point operator + (point rhs) {
		return point( x+rhs.x, y+rhs.y);
	}
	inline point operator - (point rhs) {
		return point(x-rhs.x, y-rhs.y);
	}


};

const point offset = point(1, 1);
point UP = point(0, -1), RIGHT = point(1, 0), DOWN = point(0, 1), LEFT = point(-1, 0);
point dir[4][4] = {
	{ UP, RIGHT, DOWN, LEFT },
	{ RIGHT, DOWN, LEFT, UP },
	{ DOWN, LEFT, UP, RIGHT },
	{ LEFT, UP, RIGHT, DOWN }
};
point neighbour[8] = { { -1, -1 },{ 0, -1 },{ 1, -1 },{ -1, 0 },{ 1, 0 },{ -1, 1 },{ 0, 1 },{ 1, 1 } };

struct score {
	int playerScore[4];
public :
	score() {
		REP(i, 4)
			playerScore[i] = MAX;
	}
	score(int score[4]) {
		REP(i, 4)
			playerScore[i] = score[i];
	}
	int getPlayerScore(int playerId) {
		int res = 2*playerScore[playerId];
		REP(i, 4)
			res -= playerScore[i];
		return res;
	}
};

struct GameMove {

	int goBackRounds;
	point destination;
public:
	GameMove() {
		goBackRounds = -1;
		destination = point(1, 1);
	}
	GameMove(int rounds, point pos) {
		goBackRounds = rounds;
		destination = pos;
	}
	inline void print() {
		if (goBackRounds>0)
			printf("BACK %d\n", goBackRounds);
		else
			(destination-offset).print();
	}
};

struct GameState {

	char canGoBack, playerVaild;
	char board[22][37];
	int playerScore[4];
	int cellsLeft;
	vector<point> playerPos[4];

public:

	bool doGoodMove(point move, int playerId) {

		char player = playerId + '0';
		point newPos = move + playerPos[playerId].back();

		if (board[newPos.y][newPos.x]!='.') {
			return false;
		}
		else {
			playerPos[playerId].push_back(newPos);
			board[newPos.y][newPos.x] = player;
			playerScore[playerId]++;
			cellsLeft--;
			int count = 0;
			REP(i, 4) {
				point p = playerPos[playerId].back() + dir[ordering][i];
				if (board[p.y][p.x]==player)
					count++;
			}
			if (count>=2) {
				REP(i, 8) {
					point p = playerPos[playerId].back() + neighbour[i];
					if (board[p.y][p.x]=='.')
						checkFillBFS(p, player);
				}
			}
			return true;
		}
	}

	bool doMove(point move, int playerId) {

		char player = playerId + '0';
		point newPos = move + playerPos[playerId].back();

		if (board[newPos.y][newPos.x]=='#') {
			return false;
		}
		else {
			playerPos[playerId].push_back(newPos);
			if (board[newPos.y][newPos.x]=='.') {
				board[newPos.y][newPos.x] = player;
				playerScore[playerId]++;
				cellsLeft--;
			}
			int count = 0;
			REP(i, 4) {
				point p = playerPos[playerId].back() + dir[ordering][i];
				if (board[p.y][p.x]==player)
					count++;
			}
			if (count>=2) {
				REP(i, 8) {
					point p = playerPos[playerId].back() + neighbour[i];
					if (board[p.y][p.x]=='.')
						checkFillBFS(p, player);
				}
			}
			return true;
		}
	}

	void checkFillBFS(point s, char player) {

		queue<point> q;
		bool check=true, visited[22][37];
		MS(visited, 0);

		q.push(s);
		visited[s.y][s.x] = 1;

		while (!q.empty()) {
			point p = q.front();
			q.pop();
			REP(i, 4) {
				point next = p + dir[ordering][i];
				if (!visited[next.y][next.x]) {
					if (board[next.y][next.x]=='.') {
						q.push(next);
						visited[next.y][next.x] = 1;
					}
					else if (board[next.y][next.x]!=player) {
						check = false;
						break;
					}
				}
			}
		}
		if (check) {
			REP(i, 22) {
				REP(j, 37) {
					if (visited[i][j]) {
						board[i][j] = player;
						playerScore[player-'0']++;
						cellsLeft--;
					}
				}
			}
		}
	}

	void debugGameState(int oppeonetCount) {
		DB("canGoBack   = %d\n", canGoBack);
		DB("playerVaild = %d\n", playerVaild);
		REP(i, playerCount) {
			DB("Player %d : ", i);
			REP(j, playerPos[i].size())
				DB("%2d,%2d  ", playerPos[i][j].x, playerPos[i][j].y);
			DB("\n");
		}
	}
};

GameState game;

bool noPlayerOn(GameState &game, point p) {

	REP(i, playerCount) {
		if (game.playerPos[i].back()==p)
			return true;
	}
	return false;
}

score negamax(GameState &game, int playerId, int depth) {

	if (depth == MAX_DEPTH) {
		return score(game.playerScore);
	}
	else {
		score maxVal;
		maxVal.playerScore[playerId] = MIN;
		int goodMoves = 0;

		REP(i, 4) {
			GameState child = game;
			if (child.doGoodMove(dir[ordering][i], playerId)) {
				goodMoves++;
				score cur = negamax(child, (playerId+1)%playerCount, depth+1);
				if (cur.getPlayerScore(playerId) > maxVal.getPlayerScore(playerId))
					maxVal = cur;
			}
		}

		if (!goodMoves) {
			REP(i, 4) {
				GameState child = game;
				if (child.doMove(dir[ordering][i], playerId)) {
					goodMoves++;
					score cur = negamax(child, (playerId+1)%playerCount, depth+1);
					if (cur.getPlayerScore(playerId) > maxVal.getPlayerScore(playerId))
						maxVal = cur;
				}
			}
		}


		return maxVal;
	}

}

GameMove getbestMove(GameState game, int playerId) {

	GameMove bestMove;
	score maxVal;
	maxVal.playerScore[playerId] = MIN;
	int goodMoves = 0;

	REP(i, 4) {
		GameState child = game;
		if (child.doGoodMove(dir[ordering][i], playerId)) {
			goodMoves++;
			score cur = negamax(child, (playerId+1)%playerCount, 1);
			if (cur.getPlayerScore(playerId) > maxVal.getPlayerScore(playerId)) {
				maxVal = cur;
				bestMove = GameMove(-1, child.playerPos[playerId].back());
			}
		}
	}

	if (!goodMoves) {
		REP(i, 4) {
			GameState child = game;
			if (child.doMove(dir[ordering][i], playerId)) {
				score cur = negamax(child, (playerId+1)%playerCount, 1);
				if (cur.getPlayerScore(playerId) > maxVal.getPlayerScore(playerId)) {
					maxVal = cur;
					bestMove = GameMove(-1, child.playerPos[playerId].back());
				}
			}
		}
	}
	DB("%d vs %d\n", maxVal.playerScore[playerId], game.playerScore[playerId]);
	if (maxVal.playerScore[playerId] == game.playerScore[playerId]) {
		int minDist = 10000;
		REP(i, 22) {
			REP(j, 37) {
				if(game.board[i][j]=='.' && game.playerPos[playerId].back().manhatanDistance(point(j, i))<minDist
				   && noPlayerOn(game, point(j, i)))
					bestMove = GameMove(-1, point(j, i));
			}
		}
	}
	return bestMove;

}

int main(){

	srand(time(NULL));
	scanf("%d", &playerCount); // DB("%d\n", playerCount);
	playerCount++;

	while(1){

		ordering = 0;
		clock_t t = clock();
		int round;
		game.canGoBack = 0;
		game.playerVaild = 0;

		scanf("%d", &round);  //DB("%d\n", round);
		REP(i, playerCount) {
			int px, py, back;
			scanf("%d %d %d", &px, &py, &back);  //DB("%d %d %d\n", px, py, back);
			if (px!=-1 || py!=-1) {
				game.playerPos[i].push_back(point(px, py)+offset);
				game.canGoBack ^= back<<i;
				game.playerVaild ^= 1<<i;
			}
		}
		char c;
		game.cellsLeft = 0;
		game.playerScore[0] = game.playerScore[1] = game.playerScore[2] = game.playerScore[3] = 0;
		REP(i, 22) {
			if(i>0 && i<21)
				c = getchar();
			REP(j, 37) {
				if (i==0 || i==21 || j==0 || j==36) {
					game.board[i][j] = '#';
				}
				else {
					scanf("%c", &game.board[i][j]);
					//DB("%c", game.board[i][j]);
					if (game.board[i][j]=='.')
						game.cellsLeft++;
					else
						game.playerScore[game.board[i][j]-'0']++;
				}
			}
			//DB("\n");
		}

		GameMove bestMove = getbestMove(game, 0);
		bestMove.print();
		t = clock() - t;
		DB("Time Taken = %lf sec\n", (double)t/CLOCKS_PER_SEC);
	}

	return 0;
}

//