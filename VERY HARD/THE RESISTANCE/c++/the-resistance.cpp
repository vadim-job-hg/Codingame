/*~~~~~~~~~~~~~~~~~~*
*                  *
* $Dollar Akshay$  *
*                  *
*~~~~~~~~~~~~~~~~~~*/

//https://www.codingame.com/ide/28851516be94dd1da9c26c054ed61ccdfcde661

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
#define mp(a,b) make_pair(a,b)
#define DB(s,x) fprintf(stderr,s,x);
#define MS(x,n) memset(x,n,sizeof(x))
#define SORT(a,n) sort(begin(a),begin(a)+n)
#define REV(a,n) reverse(begin(a),begin(a)+n)
#define ll long long
#define pii pair<int,int>
#define MOD 1000000007


int len, n;

char code[100000];
bool calc[10001];
ll int DP[10001];
vector<int> words;

char alphabet[26][10] = {
".-","-...","-.-.","-..",".","..-.",	// a-f
"--.","....","..",".---","-.-",".-..",	// g-l
"--","-.","---",".--.","--.-",".-.",	// m-r
"...","-","..-","...-",".--","-..-",	// s-x
"-.--","--.." };						// y-z

char original[10000][100],dict[10000][100];

void wordToMorse(char original[100], char dict[100]) {

	char morse[100] = "";
	int len = strlen(original);
	REP(i, len)
		strcat(morse, alphabet[original[i] - 'A']);
	strcpy(dict, morse);

}

ll int DFS(int k) {

	if (k==len) {
		return 1;
	}

	if (calc[k])
		return DP[k];

	REP(i, n) {
		if (strncmp(code+k, dict[i], strlen(dict[i]))==0) {
			words.push_back(i);
			DP[k] += DFS(k+strlen(dict[i]));
			words.pop_back();
		}
	}
	calc[k] = true;
	return DP[k];
}

int main() {

	scanf("%s", code);
	len = strlen(code);
	scanf("%d", &n);
	REP(i, n) {
		scanf("%s", original[i]);
		wordToMorse(original[i], dict[i]);
	}
	printf("%lld\n", DFS(0));
	sp;
	return 0;
}

//Solved