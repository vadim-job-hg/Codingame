#include <iostream>

using namespace std;

int main()
{
    while (1) {
        string enemy1; // name of enemy 1
        cin >> enemy1; cin.ignore();
        int dist1; // distance to enemy 1
        cin >> dist1; cin.ignore();
        string enemy2; // name of enemy 2
        cin >> enemy2; cin.ignore();
        int dist2; // distance to enemy 2
        cin >> dist2; cin.ignore();

        if (dist1 < dist2)
            cout << enemy1 << endl;
        else
            cout << enemy2 << endl;
    }
}