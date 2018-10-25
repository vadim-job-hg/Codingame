#include <bits/stdc++.h>

using namespace std;

class Action;
class Unit;

const string MNB = "MOVE&BUILD";
const string PNB = "PUSH&BUILD";

vector<string> grid;
vector<Unit> my_units;
vector<Unit> enemy_units;
int unitsPerPlayer;

pair<int, int> dir_to_diff(string dir) {
    if (dir == "N") {
        return {0, -1};
    } else if (dir == "NE") {
        return {1, -1};
    } else if (dir == "E") {
        return {1, 0};
    } else if (dir == "SE") {
        return {1, 1};
    } else if (dir == "S") {
        return {0, 1};
    } else if (dir == "SW") {
        return {-1, 1};
    } else if (dir == "W") {
        return {-1, 0};
    } else if (dir == "NW") {
        return {-1, -1};
    } else {
        cout << "ERROR" << endl;
    }
}

struct Action {
    int index;
    int x1;
    int y1;
    int x2;
    int y2;
    string dir1;
    string dir2;
    string type;

    void print() {
        cout << type << " " << index << " " << dir1 << " " << dir2 << endl;
    }
};

class Unit {
public:
    int index;
    int x;
    int y;
    vector<Action> actions;

    Unit() {}

    int action(int action_ind) {
        int value = 0;
        Action act = actions[action_ind];
        if (act.type == MNB) {
            value = grid[y][x];
            x += act.x1;
            y += act.y1;
            value = grid[y][x] - value;
            value*=2;
            int t = grid[y + act.y2][x + act.x2] - '0';
            if (t == 3)
                t = -1;
            grid[y + act.y2][x + act.x2]++;
            value += t;
        } else {
            value = grid[y][x] - '0' + 1;
            int en_ind = -1;
            for (int i = 0; i < unitsPerPlayer; i++) {
                if ((enemy_units[i].x == x + act.x1) &&
                    (enemy_units[i].y == y + act.y1)) {
                    en_ind = i;
                    break;
                }
            }
            enemy_units[en_ind].x += act.x2;
            enemy_units[en_ind].y += act.y2;
            int t = grid[y + act.y1][x + act.x1] - '0';
            if (t == 3)
                t = -1;
            grid[y + act.y1][x + act.x1]++;
            value += t;
        }
        return value;
    }

    void revert_action(int action_ind) {
        Action act = actions[action_ind];
        if (act.type == MNB) {
            grid[y + act.y2][x + act.x2]--;
            x -= act.x1;
            y -= act.y1;
        } else {
            grid[y + act.y1][x + act.x1]--;
            int en_ind = -1;
            for (int i = 0; i < unitsPerPlayer; i++) {
                if ((enemy_units[i].x == x + act.x1 + act.x2) &&
                    (enemy_units[i].y == y + act.y1 + act.y2)) {
                    en_ind = i;
                    break;
                }
            }
            enemy_units[en_ind].x -= act.x2;
            enemy_units[en_ind].y -= act.y2;
        }
    }
};

int check_pos() {
    // Voronoi here
    return 0;
}

int main()
{
    int size;
    cin >> size;
    grid.resize(size);
    cin >> unitsPerPlayer;
    my_units.resize(unitsPerPlayer);
    my_units[0].index = 0;
    my_units[1].index = 1;
    enemy_units.resize(unitsPerPlayer);
    enemy_units[0].index = 0;
    enemy_units[1].index = 1;

    while (1) {
        for (int i = 0; i < size; i++) {
            string row;
            cin >> grid[i]; cin.ignore();
        }
        for (int i = 0; i < unitsPerPlayer; i++) {
            cin >> my_units[i].x >> my_units[i].y;
            my_units[i].actions.clear();
        }
        for (int i = 0; i < unitsPerPlayer; i++) {
            cin >> enemy_units[i].x >> enemy_units[i].y;
            enemy_units[i].actions.clear();
        }
        int legalActions;
        cin >> legalActions; cin.ignore();
        for (int i = 0; i < legalActions; i++) {
            string atype;
            int index;
            string dir1;
            string dir2;
            int dx, dy, dx2, dy2;
            cin >> atype >> index >> dir1 >> dir2; cin.ignore();
            tie(dx, dy) = dir_to_diff(dir1);
            tie(dx2, dy2) = dir_to_diff(dir2);
            my_units[index].actions.push_back({index, dx, dy, dx2, dy2, dir1, dir2, atype});
        }
        cerr << my_units[0].actions[0].x1 << endl;
        Action *act;
        int max_val = -100;
        for (int i = 0; i < unitsPerPlayer; i++) {
            for (int j = 0; j < my_units[i].actions.size(); ++j) {
                int t = my_units[i].action(j);
                t += check_pos();
                my_units[i].revert_action(j);
                if (t > max_val) {
                    act = &my_units[i].actions[j];
                    max_val = t;
                }
            }
        }
        act->print();
    }
}