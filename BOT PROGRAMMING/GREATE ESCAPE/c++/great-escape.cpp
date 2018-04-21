// Rank: 208/1153

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cassert>
#include <stack>
#include <time.h>

using namespace std;

struct Wall
{
    enum Orientation
    {
        Horizontal,
        Vertical
    };

    int x;
    int y;
    Orientation orientation;
};

struct Player
{
    int x; // x-coordinate of the player
    int y; // y-coordinate of the player
    int wallsLeft; // number of walls available for the player
};


int w; // width of the board
int h; // height of the board
int playerCount; // number of players (2 or 3)
int myId; // id of my player (0 = 1st player, 1 = 2nd player, ...)

int turns;

vector<Wall> walls;
vector<Player> players;

vector<vector<pair<int, int>>> storedPaths;

int target;

vector<string> phrases = {
    "You shall not pass!",
    "Stop right there!",
    "The way is shut!",
    "HALT!",
    "STOP!",
    "Don't move!",
    "Don't go there!",
    "Path blocked."
};

bool isGoalNode(int id, int x, int y)
{
    assert(id >= 0 && id <= 2);

    switch (id)
    {
    case 0:
        if (x == w-1)
            return true;
        else
            return false;

    case 1:
        if (x == 0)
            return true;
        else
            return false;

    case 2:
        if (y == h-1)
            return true;
        else
            return false;
    }
}

bool hasVerticalWall(int x, int y)
{
    for (auto& wall : walls)
    {
        if ((wall.orientation == Wall::Orientation::Vertical) && (wall.x == x))
        {
            if (wall.y == y)
                return true;
        }
    }
    return false;
}

bool hasHorizontalWall(int x, int y)
{
    for (auto& wall : walls)
    {
        if ((wall.orientation == Wall::Orientation::Horizontal) && (wall.y == y))
        {
            if (wall.x == x)
                return true;
        }
    }
    return false;
}

vector<pair<int, int>> getNeighbors(pair<int, int> node)
{
    vector<pair<int, int>> neighbors;

    if ((node.first > 0)
     && (!hasVerticalWall(node.first, node.second - 1))
     && (!hasVerticalWall(node.first, node.second)))
    {
        neighbors.push_back({node.first - 1, node.second});
    }

    if ((node.second > 0)
     && (!hasHorizontalWall(node.first - 1, node.second))
     && (!hasHorizontalWall(node.first, node.second)))
    {
        neighbors.push_back({node.first, node.second - 1});
    }

    if ((node.first < w-1)
     && (!hasVerticalWall(node.first + 1, node.second - 1))
     && (!hasVerticalWall(node.first + 1, node.second)))
    {
        neighbors.push_back({node.first + 1, node.second});
    }

    if ((node.second < h-1)
     && (!hasHorizontalWall(node.first - 1, node.second + 1))
     && (!hasHorizontalWall(node.first, node.second + 1)))
    {
        neighbors.push_back({node.first, node.second + 1});
    }

    return neighbors;
}

vector<pair<int, int>> dijkstra(pair<int, int> source, int id)
{
    auto dist = vector<vector<int>>(h, vector<int>(w, numeric_limits<int>::max()));
    auto prev = vector<vector<pair<int, int>>>(h, vector<pair<int, int>>(w, {numeric_limits<int>::max(), numeric_limits<int>::max()}));

    vector<pair<int, int>> unvisited;

    // Initialization
    dist[source.second][source.first] = 0;
    for (int y = 0; y < h; ++y)
    {
        for (int x = 0; x < w; ++x)
            unvisited.push_back({x, y});
    }

    while (!unvisited.empty())
    {
        // Find node with smallest distance
        vector<pair<int, int>>::iterator minIt = unvisited.begin();
        int minDist = numeric_limits<int>::max();
        for (auto it = unvisited.begin(); it != unvisited.end(); ++it)
        {
            if (dist[it->second][it->first] < minDist)
            {
                minDist = dist[it->second][it->first];
                minIt = it;
            }
        }

        // Return an empty list when there is no way to get to the goal
        if (minDist == numeric_limits<int>::max())
            return {};

        // Remove and return best vertex
        pair<int, int> target = *minIt;
        unvisited.erase(minIt);

        // Check if goal node
        if (isGoalNode(id, target.first, target.second))
        {
            stack<pair<int, int>> pathStack;
            pair<int, int> node = target;
            while (prev[node.second][node.first] != pair<int, int>{numeric_limits<int>::max(), numeric_limits<int>::max()})
            {
                pathStack.push(node);
                node = prev[node.second][node.first];
            }

            vector<pair<int, int>> path;
            while (!pathStack.empty())
            {
                path.push_back(pathStack.top());
                pathStack.pop();
            }

            return path;
        }

        vector<pair<int, int>> neighbors = getNeighbors(target);
        for (pair<int, int>& neighbor : neighbors)
        {
            int alt = dist[target.second][target.first] + 1;
            if (alt < dist[neighbor.second][neighbor.first])
            {
                dist[neighbor.second][neighbor.first] = alt;
                prev[neighbor.second][neighbor.first] = target;
            }
        }
    }

    return {};
}

void move(int x, int y)
{
    assert(players[myId].x == x || players[myId].y == y);

    if (x > players[myId].x)
        cout << "RIGHT" << endl;
    else if (x < players[myId].x)
        cout << "LEFT" << endl;
    else
    {
        if (y > players[myId].y)
            cout << "DOWN" << endl;
        else if (y < players[myId].y)
            cout << "UP" << endl;
    }
}

int calculateMovesDiff()
{
    auto& paths = storedPaths;

    paths.clear();
    paths.resize(playerCount);

    for (int i = 0; i < playerCount; ++i)
    {
        if (players[i].x != -1)
        {
            paths[i] = dijkstra({players[i].x, players[i].y}, i);
            if (paths[i].empty())
                return -numeric_limits<int>::max();
        }
    }

    int movesDiff = numeric_limits<int>::max();
    for (int i = 0; i < playerCount; ++i)
    {
        if ((i != myId) && (players[i].x != -1))
            movesDiff = min((int)paths[i].size() - (int)paths[myId].size(), movesDiff);
    }

    return movesDiff;
}

bool checkValidWallPlacement(Wall wall)
{
    if ((wall.x == -1) || (wall.y == -1)
     || (wall.x == w) || (wall.y == h)
     || (wall.x == w-1 && wall.orientation == Wall::Orientation::Horizontal)
     || (wall.y == h-1 && wall.orientation == Wall::Orientation::Vertical)
     || (wall.x == 0 && wall.orientation == Wall::Orientation::Vertical)
     || (wall.y == 0 && wall.orientation == Wall::Orientation::Horizontal))
        return false;

    if (wall.orientation == Wall::Orientation::Vertical)
    {
        if (hasVerticalWall(wall.x, wall.y-1) || hasVerticalWall(wall.x, wall.y)
         || hasVerticalWall(wall.x, wall.y+1) || hasHorizontalWall(wall.x-1, wall.y+1))
        {
            return false;
        }
    }
    else
    {
        if (hasHorizontalWall(wall.x-1, wall.y) || hasHorizontalWall(wall.x, wall.y)
         || hasHorizontalWall(wall.x+1, wall.y) || hasVerticalWall(wall.x+1, wall.y-1))
        {
            return false;
        }
    }

    return true;
}

pair<Wall, int> findBestWall(int movesDiff, int turn = 1)
{
    Wall wall{-1, -1, Wall::Orientation::Horizontal};

    // Calculate the paths of the oponents
    int i;
    int smallestPath = myId;
    vector<vector<pair<int, int>>> paths(playerCount);
    for (i = 0; i < playerCount; ++i)
    {
        if ((i != myId) && (players[i].x != -1))
        {
            if (isGoalNode(i, players[i].x, players[i].y))
                return {Wall{-1, -1, Wall::Orientation::Horizontal}, movesDiff};

            paths[i] = dijkstra({players[i].x, players[i].y}, i);
            assert(!paths[i].empty());

            if (smallestPath == myId)
            {
                smallestPath = i;
            }
            else
            {
                if (paths[i].size() < paths[smallestPath].size())
                    smallestPath = i;
                else if (paths[i].size() == paths[smallestPath].size())
                {
                    if (rand() % 2)
                        smallestPath = i;
                }
            }

            paths[i].insert(paths[i].begin(), {players[i].x, players[i].y});
        }
    }

    // Pick a target
    if (target == myId)
    {
        // If there are 3 players and we are last, aim for second place
        if ((playerCount == 3) && (players[3 - myId - smallestPath].x != -1)
         && (players[smallestPath].x != -1)
         && (players[3 - myId - smallestPath].x != -1)
         && (storedPaths[myId].size() + 1 > paths[smallestPath].size())
         && (storedPaths[myId].size() + 1 > paths[3 - myId - smallestPath].size()))
        {
            i = 3 - myId - smallestPath;
        }
        else // attack the currently winning oponent
        {
            i = smallestPath;
        }
    }
    else // target already given in previous round
        i = target;

    auto attemptWall = [&](int x, int y, Wall::Orientation orientation)
        {
            if (!checkValidWallPlacement(Wall{x, y, orientation}))
                return;

            walls.push_back(Wall{x, y, orientation});

            if (calculateMovesDiff() == -numeric_limits<int>::max())
            {
                walls.pop_back();
                return;
            }

            int tentativeMovesDiff = storedPaths[i].size() - storedPaths[myId].size();
            if (turn < turns)
            {
                if (tentativeMovesDiff > movesDiff)
                {
                    wall = Wall{x, y, orientation};
                    movesDiff = tentativeMovesDiff;
                }

                pair<int, int> oldPositions[playerCount];

                // Move other players
                for (int j = 0; j < playerCount; ++j)
                {
                    if ((j != myId) && (players[j].x != -1))
                    {
                        oldPositions[j] = {players[j].x, players[j].y};

                        auto path = dijkstra({players[j].x, players[j].y}, j);
                        if (path.empty())
                        {
                            for (int k = 0; k < j; ++k)
                            {
                                if ((k != myId) && (players[k].x != -1))
                                {
                                    players[k].x = oldPositions[k].first;
                                    players[k].y = oldPositions[k].second;
                                }
                            }

                            walls.pop_back();
                            return;
                        }

                        players[j].x = path[0].first;
                        players[j].y = path[0].second;
                    }
                }

                int oldTarget = target;
                if (target == myId)
                    target = i;

                tentativeMovesDiff = findBestWall(movesDiff, turn+1).second;
                target = oldTarget;

                // Move players back to their old position
                for (int j = 0; j < playerCount; ++j)
                {
                    if ((j != myId) && (players[j].x != -1))
                    {
                        players[j].x = oldPositions[j].first;
                        players[j].y = oldPositions[j].second;
                    }
                }
            }

            walls.pop_back();

            if (tentativeMovesDiff > movesDiff)
            {
                wall = Wall{x, y, orientation};
                movesDiff = tentativeMovesDiff;
            }
        };

    // Only try to place walls on places that block this path
    for (int j = 0; j < min<int>(paths[i].size()-1, 5); ++j)
    {
        if (paths[i][j+1].first > paths[i][j].first)
        {
            if (paths[i][j].second != 1)
                attemptWall(paths[i][j].first+1, paths[i][j].second, Wall::Orientation::Vertical);

            if (paths[i][j].second != h-2)
                attemptWall(paths[i][j].first+1, paths[i][j].second-1, Wall::Orientation::Vertical);
        }
        else if (paths[i][j+1].first < paths[i][j].first)
        {
            if (paths[i][j].second != 1)
                attemptWall(paths[i][j].first, paths[i][j].second, Wall::Orientation::Vertical);

            if (paths[i][j].second != h-2)
                attemptWall(paths[i][j].first, paths[i][j].second-1, Wall::Orientation::Vertical);
        }
        else
        {
            if (paths[i][j+1].second > paths[i][j].second)
            {
                if (paths[i][j].first != 1)
                {
                    //cerr << "START " << paths[i][j].first << " " << paths[i][j].second+1 << endl;
                    attemptWall(paths[i][j].first, paths[i][j].second+1, Wall::Orientation::Horizontal);
                    //cerr << "STOP " << paths[i][j].first << " " << paths[i][j].second+1 << endl;
                }

                if (paths[i][j].first != w-2)
                {
                    //cerr << "START " << paths[i][j].first-1 << " " << paths[i][j].second+1 << endl;
                    attemptWall(paths[i][j].first-1, paths[i][j].second+1, Wall::Orientation::Horizontal);
                    //cerr << "STOP " << paths[i][j].first-1 << " " << paths[i][j].second+1 << endl;
                }
            }
            else if (paths[i][j+1].second < paths[i][j].second)
            {
                if (paths[i][j].first != 1)
                    attemptWall(paths[i][j].first, paths[i][j].second, Wall::Orientation::Horizontal);

                if (paths[i][j].first != w-2)
                    attemptWall(paths[i][j].first-1, paths[i][j].second, Wall::Orientation::Horizontal);
            }
        }
    }

    if (turn == 1)
    {
        // Only place the wall right next to the opponent (wait until he gets to the proposed location first)
        if (wall.x > -1)
        {
            if (wall.orientation == Wall::Orientation::Vertical)
            {
                if (paths[i][1].first > paths[i][0].first)
                {
                    if (((wall.x != paths[i][0].first+1) || (wall.y != paths[i][0].second))
                     && ((wall.x != paths[i][0].first+1) || (wall.y != paths[i][0].second-1)))
                    {
                        return {Wall{-1, -1, Wall::Orientation::Horizontal}, movesDiff};
                    }
                }
                else if (paths[i][1].first < paths[i][0].first)
                {
                    if (((wall.x != paths[i][0].first) || (wall.y != paths[i][0].second))
                     && ((wall.x != paths[i][0].first) || (wall.y != paths[i][0].second-1)))
                    {
                        return {Wall{-1, -1, Wall::Orientation::Horizontal}, movesDiff};
                    }
                }
                else
                    return {Wall{-1, -1, Wall::Orientation::Horizontal}, movesDiff};
            }
            else // horizontal wall
            {
                if (paths[i][1].second > paths[i][0].second)
                {
                    if (((wall.x != paths[i][0].first) || (wall.y != paths[i][0].second+1))
                     && ((wall.x != paths[i][0].first-1) || (wall.y != paths[i][0].second+1)))
                    {
                        return {Wall{-1, -1, Wall::Orientation::Horizontal}, movesDiff};
                    }
                }
                else if (paths[i][1].second < paths[i][0].second)
                {
                    if (((wall.x != paths[i][0].first) || (wall.y != paths[i][0].second))
                     && ((wall.x != paths[i][0].first-1) || (wall.y != paths[i][0].second)))
                    {
                        return {Wall{-1, -1, Wall::Orientation::Horizontal}, movesDiff};
                    }
                }
                else
                    return {Wall{-1, -1, Wall::Orientation::Horizontal}, movesDiff};
            }
        }
    }

    return {wall, movesDiff};
}

bool placeWall(int movesDiff)
{
    bool wallFound = false;
    Wall wallToPlace = findBestWall(movesDiff).first;

    if (wallToPlace.x > -1)
        wallFound = true;

    if (wallFound)
    {
        if (wallToPlace.orientation == Wall::Orientation::Vertical)
        {
            cout << wallToPlace.x << " " << wallToPlace.y << " V"
                 << " " << phrases[rand() % phrases.size()] << endl;
        }
        else
        {
            cout << wallToPlace.x << " " << wallToPlace.y << " H"
                 << " " << phrases[rand() % phrases.size()] << endl;
        }

        players[myId].wallsLeft--;
        return true;
    }
    else
    {
        cerr << "oh oh" << endl;
        return false;
    }
}


/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
int main()
{
    srand(time(NULL));

    cin >> w >> h >> playerCount >> myId; cin.ignore();

    // We can calculate more when there is only one opponent
    if (playerCount == 2)
        turns = 2;
    else
        turns = 2;

    // Choose a target to bother with walls
    if (playerCount == 2)
        target = 1 - myId;
    else
    {
        if (myId == 0)
            target = 2 - (rand() % 2);
        else if (myId == 1)
            target = 2 - ((rand() % 2) * 2);
        else
        target = rand() % 2;
    }

    // game loop
    int iteration = 0;
    while (1) {
        iteration++;

        vector<Wall> previousWalls;

        walls.clear();
        players.clear();

        for (int i = 0; i < playerCount; i++) {
            Player player;
            cin >> player.x >> player.y >> player.wallsLeft; cin.ignore();
            players.push_back(player);
        }

        int wallCount; // number of walls on the board
        cin >> wallCount; cin.ignore();
        for (int i = 0; i < wallCount; i++) {
            Wall wall;
            string wallOrientation; // wall orientation ('H' or 'V')
            cin >> wall.x >> wall.y >> wallOrientation; cin.ignore();

            if (wallOrientation == "H")
                wall.orientation = Wall::Orientation::Horizontal;
            else
                wall.orientation = Wall::Orientation::Vertical;

            walls.push_back(wall);
        }

        // If an opponent added a wall then stop with targetting a single player
        if (target != myId)
        {
            for (auto it = walls.begin(), prevIt = previousWalls.begin();
                 (it != walls.end()) && (prevIt != previousWalls.end());
                 ++it, ++prevIt)
            {
                if ((it->x != prevIt->x) || (it->y != prevIt->y) || (it->orientation != prevIt->orientation))
                {
                    target = myId;
                    break;
                }
            }
        }

        int movesDiff = calculateMovesDiff();

        // Check when to move
        if ((movesDiff >= 0) // when winning
         || (iteration <= 5) // in our first 6 turns
         || (players[myId].wallsLeft == 0) // when no more walls left
         || !placeWall(movesDiff)) // when failed to find a place to put a wall
        {
            auto path = dijkstra({players[myId].x, players[myId].y}, myId);
            assert(!path.empty());
            move(path[0].first, path[0].second);
        }
    }
}