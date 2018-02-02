#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <limits>
#include <sstream>

using namespace std;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
int main()
{
    int N; // the number of temperatures to analyse
    cin >> N; cin.ignore();
    string TEMPS; // the N temperatures expressed as integers ranging from -273 to 5526
    getline(cin, TEMPS);

    istringstream iss(TEMPS);

    int min = numeric_limits<int>::max();
    for (int i = 0; i < N; ++i)
    {
        int nr;
        iss >> nr;

        if (abs(nr) < abs(min) or (abs(nr) == abs(min) and nr>min))
            min = nr;
    }

    if (N > 0)
        cout << min << endl;
    else
        cout << 0 << endl;
}