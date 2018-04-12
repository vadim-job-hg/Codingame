#pragma GCC optimize "O3,omit-frame-pointer,inline"
#include <iostream>
#include <vector>
#include <algorithm>
#include <array>
#include <set>
#include <map>
#include <random>
#include <memory>
#include <functional>
#include <chrono>
#include <sstream>
#include <cassert>
#define repeat(i,n) for (int i = 0; (i) < (n); ++(i))
#define repeat_from(i,m,n) for (int i = (m); (i) < (n); ++(i))
#define whole(f,x,...) ([&](decltype((x)) y) { return (f)(begin(y), end(y), ## __VA_ARGS__); })(x)
typedef long long ll;
using namespace std;
using namespace std::chrono;
template <typename T> vector<vector<T> > vectors(T a, size_t h, size_t w) { return vector<vector<T> >(h, vector<T>(w, a)); }
const int dy[] = { -1, 1, 0, 0, 0 };
const int dx[] = { 0, 0, 1, -1, 0 };
bool is_on_field(int y, int x, int h, int w) { return 0 <= y and y < h and 0 <= x and x < w; }
const int inf = 1e9+7;

struct point_t { int y, x; };
point_t point(int y, int x) { return (point_t) { y, x }; }
template <typename T>
point_t point(T const & p) { return (point_t) { p.y, p.x }; }
bool operator == (point_t a, point_t b) { return make_pair(a.y, a.x) == make_pair(b.y, b.x); }
bool operator != (point_t a, point_t b) { return make_pair(a.y, a.x) != make_pair(b.y, b.x); }
bool operator <  (point_t a, point_t b) { return make_pair(a.y, a.x) <  make_pair(b.y, b.x); }

namespace primitive {

    const int player_number = 4;
    enum class player_id_t : int {
        id0 = 0,
        id1 = 1,
        id2 = 2,
        id3 = 3,
    };
    struct config_t {
        int height, width;
        player_id_t self_id;
    };
    istream & operator >> (istream & in, config_t & a) {
        int self_id;
        in >> a.width >> a.height >> self_id;
        a.self_id = player_id_t(self_id);
        return in;
    }

    enum class item_kind_t : int {
        extra_range = 1,
        extra_bomb = 2,
    };
    enum class entity_type_t {
        player = 0,
        bomb = 1,
        item = 2,
    };
    struct player_t { entity_type_t type; player_id_t id;    int x, y; int bomb, range; };
    struct bomb_t   { entity_type_t type; player_id_t owner; int x, y; int time, range; };
    struct item_t   { entity_type_t type; int dummy1;        int x, y; item_kind_t kind; int dummy2; };
    union entity_t {
        struct { entity_type_t type; player_id_t owner; int x, y, param1, param2; };
        player_t player;
        bomb_t bomb;
        item_t item;
    };
    istream & operator >> (istream & in, entity_t & a) {
        return in >> (int &)(a.type) >> (int &)(a.owner) >> a.x >> a.y >> a.param1 >> a.param2;
    }
    bool operator < (entity_t const & a, entity_t const & b) {
        return make_tuple(a.type, a.owner, a.y, a.x, a.param1, a.param2) < make_tuple(b.type, b.owner, b.y, b.x, b.param1, b.param2);
    }
    entity_t entity_cast(player_t const & a) { entity_t b; b.player = a; return b; }
    entity_t entity_cast(bomb_t   const & a) { entity_t b; b.bomb   = a; return b; }
    entity_t entity_cast(item_t   const & a) { entity_t b; b.item   = a; return b; }
    const int bomb_time = 8;
    bomb_t place_bomb(player_t const & a) {
        bomb_t b = {};
        b.type = entity_type_t::bomb;
        b.owner = a.id;
        b.y = a.y;
        b.x = a.x;
        b.time = bomb_time;
        b.range = a.range;
        return b;
    }
    item_t drop_item(int y, int x, item_kind_t kind) {
        item_t a = {};
        a.type = entity_type_t::item;
        a.y = y;
        a.x = x;
        a.kind = kind;
        return a;
    }

    enum class cell_t {
        wall = -2,
        empty = -1,
        box = 0,
        box_extra_range = 1,
        box_extra_bomb = 2,
    };
    bool is_box(cell_t a) {
        return a != cell_t::wall and a != cell_t::empty;
    }
    struct turn_t {
        config_t config;
        vector<vector<cell_t> > field;
        vector<entity_t> entities;
    };
    istream & operator >> (istream & in, turn_t & a) {
        a.field = vectors(cell_t::empty, a.config.height, a.config.width);
        repeat (y, a.config.height) {
            repeat (x, a.config.width) {
                char c; in >> c;
                assert (c == '.' or c == 'X' or isdigit(c));
                a.field[y][x] =
                    c == '.' ? cell_t::empty :
                    c == 'X' ? cell_t::wall :
                    cell_t(c-'0');
            }
        }
        int n; in >> n;
        a.entities.resize(n);
        repeat (i,n) in >> a.entities[i];
        return in;
    }
    item_kind_t open_item_box(cell_t a) {
        switch (a) {
            case cell_t::box_extra_range: return item_kind_t::extra_range;
            case cell_t::box_extra_bomb:  return item_kind_t::extra_bomb;
            default: assert (false);
        }
    }

    enum class action_t {
        move = 0,
        bomb = 1,
    };
    struct command_t {
        action_t action;
        int y, x;
    };
    struct output_t {
        command_t command;
        string message;
    };
    ostream & operator << (ostream & out, command_t const & a) {
        const string table[] = { "MOVE", "BOMB" };
        return out << table[int(a.action)] << ' ' << a.x << ' ' << a.y;
    }
    ostream & operator << (ostream & out, output_t const & a) {
        return out << a.command << ' ' << a.message;
    }
    bool operator < (command_t const & a, command_t const & b) { return make_tuple(a.action, a.y, a.x) < make_tuple(b.action, b.y, b.x); }
    command_t default_command(player_t const & self) {
        command_t command = {};
        command.action = action_t::move;
        command.y = self.y;
        command.x = self.x;
        return command;
    }
    command_t create_command(player_t const & self, int dy, int dx, action_t action) {
        command_t command = {};
        command.action = action;
        command.y = self.y + dy;
        command.x = self.x + dx;
        return command;
    }

    const int time_limit = 100; // msec
}
using namespace primitive;

int total_bomb(player_id_t id, vector<entity_t> const & entities) {
    int placed = 0;
    int reserved = 0;
    for (auto & ent : entities) {
        if (ent.type == entity_type_t::player) {
            if (ent.player.id == id) {
                reserved += ent.player.bomb;
            }
        } else if (ent.type == entity_type_t::bomb) {
            if (ent.bomb.owner == id) {
                placed += 1;
            }
        }
    }
    return placed + reserved;
}

multimap<point_t,entity_t> entity_multimap(vector<entity_t> const & entities) {
    multimap<point_t,entity_t> ent_at;
    for (auto & ent : entities) {
        ent_at.emplace(point(ent), ent);
    }
    return ent_at;
}

struct exploded_time_info_t { int time; bool owner[player_number]; };
exploded_time_info_t default_explosion_info() { exploded_time_info_t a = { inf }; return a; }
vector<vector<exploded_time_info_t> > exploded_time(turn_t const & turn) {
    int h = turn.config.height;
    int w = turn.config.width;
    map<point_t,entity_t> obstructions; // modified dynamically
    array<vector<point_t>, bomb_time> explode_at = {};
    for (auto & ent : turn.entities) {
        if (ent.type == entity_type_t::bomb) {
            obstructions[point(ent)] = ent;
            explode_at[ent.bomb.time-1].push_back(point(ent));
        } else if (ent.type == entity_type_t::item) {
            obstructions[point(ent)] = ent;
        }
    }
    vector<vector<cell_t> > field = turn.field; // modified
    vector<vector<exploded_time_info_t> > result = vectors(default_explosion_info(), h, w);
    auto update = [&](int y, int x, int time, player_id_t owner) {
        if (result[y][x].time < time) return;
        result[y][x].time = time;
        result[y][x].owner[int(owner)] = true;
    };
    function<void (bomb_t const &, int, set<point_t> &)> explode = [&](bomb_t const & ent, int time, set<point_t> & used) {
        if (used.count(point(ent))) return;
        used.insert(point(ent));
        update(ent.y, ent.x, time, ent.owner);
        repeat (i,4) {
            repeat_from (l, 1, ent.range) {
                int ny = ent.y + l*dy[i];
                int nx = ent.x + l*dx[i];
                if (not is_on_field(ny, nx, h, w)) continue;
                if (field[ny][nx] == cell_t::wall) break;
                update(ny, nx, time, ent.owner);
                bool obstructed = false;
                if (obstructions.count(point(ny, nx))) {
                    obstructed = true;
                    auto & nent = obstructions[point(ny, nx)];
                    // > Any bomb caught in an explosion is treated as if it had exploded at the very same moment.
                    // > Explosions do not go through obstructions such as boxes, items or other bombs, but are included on the cells the obstruction occupies.
                    // > A single obstruction may block the explosions of several bombs that explode on the same turn.
                    if (nent.type == entity_type_t::bomb and nent.bomb.time > time) {
                        explode(nent.bomb, time, used);
                    } else if (nent.type == entity_type_t::item) {
                        used.insert(point(nent));
                    }
                }
                if (field[ny][nx] != cell_t::empty) obstructed = true;
                if (is_box(field[ny][nx])) used.insert(point(ny, nx));
                if (obstructed) {
                    break;
                }
            }
        }
    };
    repeat (t, bomb_time) {
        set<point_t> used;
        for (point_t p : explode_at[t]) {
            if (obstructions.count(p)) {
                auto & ent = obstructions[p];
                if (ent.type == entity_type_t::bomb) {
                    explode(ent.bomb, t+1, used);
                }
            }
        }
        for (point_t p : used) {
            obstructions.erase(p);
            field[p.y][p.x] = cell_t::empty;
        }
    }
    return result;
}

map<player_id_t,player_t> select_player(vector<entity_t> const & entities) {
    map<player_id_t,player_t> player;
    for (auto & ent : entities) {
        if (ent.type == entity_type_t::player) {
            player[ent.player.id] = ent.player;
        }
    }
    return player;
}
shared_ptr<player_t> find_player(vector<entity_t> const & entities, player_id_t id) {
    auto players = select_player(entities);
    return players.count(id) ? make_shared<player_t>(players[id]) : nullptr;
}
map<point_t,bomb_t> select_bomb(vector<entity_t> const & entities) {
    map<point_t,bomb_t> bombs;
    for (auto & ent : entities) {
        if (ent.type == entity_type_t::bomb) {
            bombs[point(ent)] = ent.bomb;
        }
    }
    return bombs;
}

bool is_valid_commands(turn_t const & turn, map<player_id_t,command_t> const & commands) {
    vector<player_t> players;
    set<point_t> bombs;
    for (entity_t ent : turn.entities) {
        switch (ent.type) {
            case entity_type_t::player:
                players.push_back(ent.player);
                break;
            case entity_type_t::bomb:
                bombs.insert(point(ent));
                break;
            case entity_type_t::item:
                // nop
                break;
        }
    }
    for (player_t & ent : players) {
        if (commands.count(ent.id)) {
            command_t command = commands.at(ent.id);
            if (point(command) != point(ent)) {
                if (not is_on_field(command.y, command.x, turn.config.height, turn.config.width)) return false;
                if (abs(command.y - ent.y) + abs(command.x - ent.x) >= 2) return false;
                if (turn.field[command.y][command.x] != cell_t::empty) return false;
                if (bombs.count(point(command))) return false;
            }
            if (command.action == action_t::bomb) {
                if (ent.bomb == 0) return false;
                if (bombs.count(point(ent))) return false;
            }
        }
    }
    return true;
}

struct next_turn_info_t {
    bool killed[player_number];
    int box[player_number];
    int range[player_number];
    int bomb[player_number];
};
shared_ptr<turn_t> next_turn(turn_t const & cur, vector<vector<exploded_time_info_t> > const & exptime, map<player_id_t,command_t> const & commands, next_turn_info_t & info) {
    if (not is_valid_commands(cur, commands)) return nullptr;
    info = {};
    shared_ptr<turn_t> nxt = make_shared<turn_t>();
    nxt->config = cur.config;
    nxt->field = cur.field;
    // bomb
    // > At the start of the round, all bombs have their countdown decreased by 1.
    // > Any bomb countdown that reaches 0 will cause the bomb to explode immediately, before players move.
    map<point_t,item_t> items; // after explosion
    repeat (y, cur.config.height) {
        repeat (x, cur.config.width) {
            if (exptime[y][x].time-1 == 0) {
                // > Once the explosions have been computed, any box hit is then removed. This means that the destruction of 1 box can count for 2 different players.
                if (is_box(cur.field[y][x])) {
                    nxt->field[y][x] = cell_t::empty;
                    // drop item
                    if (cur.field[y][x] != cell_t::box) {
                        item_kind_t kind = open_item_box(cur.field[y][x]);
                        items[point(y, x)] = drop_item(y, x, kind);
                    }
                    repeat (i,player_number) {
                        if (exptime[y][x].owner[i]) {
                            info.box[i] += 1;
                        }
                    }
                }
            }
        }
    }
    // split entities
    map<player_id_t,player_t> players; // after explosion
    map<point_t,bomb_t> bombs; // after explosion, before placing
    array<int,player_number> exploded_bombs = {};
    for (entity_t ent : cur.entities) {
        if (exptime[ent.y][ent.x].time-1 == 0) {
            switch (ent.type) {
                case entity_type_t::player:
                    info.killed[int(ent.player.id)] = true;
                    if (ent.player.id == cur.config.self_id) return nullptr;
                    break;
                case entity_type_t::bomb:
                    exploded_bombs[int(ent.bomb.owner)] += 1;
                    break;
                case entity_type_t::item:
                    // nop
                    break;
            }
        } else {
            switch (ent.type) {
                case entity_type_t::player:
                    players[ent.player.id] = ent.player;
                    break;
                case entity_type_t::bomb:
                    ent.bomb.time -= 1;
                    bombs[point(ent)] = ent.bomb;
                    nxt->entities.push_back(ent);
                    break;
                case entity_type_t::item:
                    items[point(ent)] = ent.item;
                    break;
            }
        }
    }
    // player
    // > Players then perform their actions simultaneously.
    // > Any bombs placed by a player appear at the end of the round.
    set<point_t> player_exists; // moved
    for (auto & it : players) {
        player_t ent = it.second;
        if (commands.count(ent.id)) {
            command_t command = commands.at(ent.id);
            // place bomb
            if (command.action == action_t::bomb) {
                ent.bomb -= 1;
                nxt->entities.push_back(entity_cast(place_bomb(ent))); // don't add to map<point_t,player_t> bombs
            }
            // move
            if (point(command) != point(ent)) {
                ent.y = command.y;
                ent.x = command.x;
                // get item
                if (items.count(point(ent))) {
                    switch (items[point(ent)].kind) {
                        case item_kind_t::extra_range:
                            ent.range += 1;
                            info.range[int(ent.id)] += 1;
                            break;
                        case item_kind_t::extra_bomb:
                            ent.bomb += 1;
                            info.bomb[int(ent.id)] += 1;
                            break;
                    }
                }
            }
        }
        ent.bomb += exploded_bombs[int(ent.id)]; // after placing a bomb
        player_exists.insert(point(ent));
        nxt->entities.push_back(entity_cast(ent));
    }
    // item
    for (auto & it : items) {
        item_t ent = it.second;
        if (player_exists.count(point(ent))) continue;
        nxt->entities.push_back(entity_cast(ent));
    }
    return nxt;
}

bool is_survivable(player_id_t self_id, turn_t const & turn, vector<vector<exploded_time_info_t> > const & exptime) {
    shared_ptr<player_t> self = find_player(turn.entities, self_id);
    if (not self) return false;
    if (exptime[self->y][self->x].time-1 == 0) return false;
    int h = turn.config.height;
    int w = turn.config.width;
    set<point_t> bombs;
    for (auto & ent : turn.entities) {
        if (ent.type == entity_type_t::bomb) {
            bombs.insert(point(ent));
        }
    }
    vector<vector<bool> > cur = vectors(false, h, w);
    cur[self->y][self->x] = true;
    repeat (t, bomb_time) {
        bool exists = false;
        vector<vector<bool> > prv = cur;
        cur = vectors(false, h, w);
        repeat (y, h) repeat (x, w) {
            if (not prv[y][x]) continue;
            if (exptime[y][x].time-1 == t) continue; // TODO: 同じ座標を異なる複数の時刻に爆風が通るのを漏らしてる
            repeat (i,5) {
                int ny = y + dy[i];
                int nx = x + dx[i];
                if (not is_on_field(ny, nx, h, w)) continue;
                if (turn.field[ny][nx] == cell_t::wall) continue;
                if (is_box(turn.field[ny][nx]) and exptime[ny][nx].time-1 >= t) continue;
                if (point(ny, nx) != point(y, x) and bombs.count(point(ny, nx)) and exptime[ny][nx].time-1 >= t) continue;
                cur[ny][nx] = true;
                exists = true;
            }
        }
        if (not exists) return false;
    }
    return true;
}

bool is_survivable_with_commands(player_id_t self_id, vector<map<player_id_t,command_t> > const & commands, turn_t const & a_turn, vector<vector<exploded_time_info_t> > const & a_exptime) {
    turn_t turn = a_turn;
    vector<vector<exploded_time_info_t> > exptime = a_exptime;
    repeat (t, int(commands.size())) {
        if (not find_player(turn.entities, self_id)) return false;
        next_turn_info_t info;
        shared_ptr<turn_t> nturn = next_turn(turn, exptime, commands[t], info);
        if (not nturn) return false;
        turn = *nturn;
        exptime = exploded_time(turn);
    }
    if (not find_player(turn.entities, self_id)) return false;
    return is_survivable(self_id, turn, exptime);
}

set<command_t> forbidden_commands(turn_t const & turn, vector<map<player_id_t,command_t> > const & commands_base) {
    vector<vector<exploded_time_info_t> > exptime = exploded_time(turn);
    player_t self = *find_player(turn.entities, turn.config.self_id);
    set<command_t> forbidden;
    const action_t actions[2] = { action_t::bomb, action_t::move }; // the first is bomb
    repeat (i,5) repeat (j,2) {
        vector<map<player_id_t,command_t> > commands = commands_base;
        if (commands.empty()) commands.emplace_back();
        commands[0][self.id] = create_command(self, dy[i], dx[i], actions[j]);
        if (is_survivable_with_commands(self.id, commands, turn, exptime)) {
            break; // if true with placing a bomb, then true without a bomb
        } else {
            forbidden.insert(commands[0][self.id]);
        }
    }
    return forbidden;
}

struct photon_t {
    turn_t turn;
    command_t initial_command;
    int age;
    int box, range, bomb; // difference
    vector<vector<exploded_time_info_t> > exptime;
    int box_acc;
    double bonus;
    double score; // cached
    uint64_t signature;
};
double evaluate_photon(photon_t const & pho) { // very magic
    int h = pho.turn.config.height;
    int w = pho.turn.config.width;
    map<player_id_t,player_t> players = select_player(pho.turn.entities);
    player_t self = players[pho.turn.config.self_id];
    double score = 0;
    const double box_base = 10;
    const double box_delta = 1;
    score += box_base  * pho.box;
    score += box_delta * pho.box_acc;
    repeat (y,h) {
        repeat (x,w) {
            if (is_box(pho.turn.field[y][x]) and pho.exptime[y][x].time != inf and pho.exptime[y][x].owner[int(self.id)]) {
                score += box_base - box_delta * pho.exptime[y][x].time;
            }
        }
    }
    score += 0.8 * min(5, pho.range) + 0.4 * pho.range;
    score += 3.0 * min(2, pho.bomb)  + 1.1 * min(4, pho.bomb)  + 0.5 * pho.bomb;
    score -= 0.2 * (pho.bomb - self.bomb);
    score -= 0.05 * abs(self.y - h/2.);
    score -= 0.05 * abs(self.x - w/2.);
    // score -= 2 * players.size(); // TODO: 実際には相手は回避するので、回避不能性を見なければ
    score += pho.bonus;
    return score;
}
uint64_t signature_photon(photon_t const & pho) {
    int h = pho.turn.config.height;
    int w = pho.turn.config.width;
    uint64_t p = 1e9+7;
    uint64_t acc = 0;
    auto f = [&](uint64_t x) { acc = acc * p + x; };
    f(pho.age);
    f(pho.box);
    f(pho.range);
    f(pho.bomb);
    f(pho.box_acc);
    repeat (y,h) repeat (x,w) {
        f(min(bomb_time+1, pho.exptime[y][x].time));
    }
    for (entity_t const & ent : pho.turn.entities) {
        f(int(ent.type));
        f(int(ent.owner));
        f(ent.y);
        f(ent.x);
        f(ent.param1);
        f(ent.param2);
    }
    return acc;
}
photon_t initial_photon(turn_t const & turn) {
    photon_t pho = {};
    pho.turn = turn;
    whole(sort, pho.turn.entities);
    pho.range = find_player(turn.entities, turn.config.self_id)->range;
    pho.bomb = total_bomb(turn.config.self_id, turn.entities);
    pho.exptime = exploded_time(turn);
    pho.score = evaluate_photon(pho);
    pho.signature = signature_photon(pho);
    return pho;
}
shared_ptr<photon_t> update_photon(photon_t const & pho, map<player_id_t,command_t> const & commands) {
    player_id_t self_id = pho.turn.config.self_id;
    shared_ptr<photon_t> npho = make_shared<photon_t>(pho);
    next_turn_info_t info;
    auto next_turn_ptr = next_turn(pho.turn, pho.exptime, commands, info);
    if (not next_turn_ptr) return nullptr;
    npho->turn = *next_turn_ptr;
    assert (commands.count(self_id));
    if (pho.age == 0) npho->initial_command = commands.at(self_id);
    whole(sort, npho->turn.entities);
    npho->age += 1;
    npho->box   += info.box[  int(self_id)];
    npho->range += info.range[int(self_id)];
    npho->bomb  += info.bomb[ int(self_id)];
    npho->exptime = exploded_time(npho->turn);
    npho->box_acc += pho.box;
    npho->score = evaluate_photon(*npho);
    npho->signature = signature_photon(*npho);
    return npho;
}

class AI {
private:
    config_t config;
    vector<turn_t> turns; // history
    vector<output_t> outputs;

private:
    default_random_engine engine;

public:
    AI(config_t const & a_config) {
        engine = default_random_engine(); // fixed seed
        config = a_config;
    }
    output_t think(turn_t const & turn) {
        // prepare
        high_resolution_clock::time_point clock_begin = high_resolution_clock::now();
        int height = config.height;
        int width  = config.width;
        map<player_id_t,player_t> players = select_player(turn.entities);
        player_t self = players[turn.config.self_id];
        multimap<point_t,entity_t> ent_at = entity_multimap(turn.entities);

        // to survive
        set<command_t> forbidden; {
            vector<vector<exploded_time_info_t> > exptime = exploded_time(turn);
            vector<map<player_id_t,command_t> > commands_base(1);
            map<point_t,bomb_t> bombs = select_bomb(turn.entities);
            for (auto & it : players) {
                player_t & ent = it.second;
                if (ent.id != self.id) {
                    if (ent.bomb == 0) continue;
                    if (bombs.count(point(ent))) continue;
                    commands_base[0][ent.id] = create_command(ent, 0, 0, action_t::bomb);
                }
            }
            forbidden = forbidden_commands(turn, commands_base);
            if (forbidden.size() == 10) {
                commands_base.clear();
                forbidden = forbidden_commands(turn, commands_base);
            }
            if (forbidden.size() == 10) {
                forbidden.clear(); // TODO: しかたないから無視する ひとつ前の時点で気付くべきだったということ
            }
        }

        // beam search
        string message = "";
        command_t command = default_command(self); {
            vector<shared_ptr<photon_t> > beam;
            beam.emplace_back(make_shared<photon_t>(initial_photon(turn)));
            const int beam_width = 100;
            const int point_beam_width = 6;
            const int simulation_time = 8;
            const int time_limit_margin = 5;
            auto clock_check = [&]() {
                high_resolution_clock::time_point clock_end = high_resolution_clock::now();
                ll clock_count = duration_cast<milliseconds>(clock_end - clock_begin).count();
                return clock_count < time_limit - time_limit_margin; // magic, randomness
            };
            repeat (age, simulation_time) {
                set<uint64_t> used;
                vector<vector<vector<shared_ptr<photon_t> > > > nbeam = vectors(vector<shared_ptr<photon_t> >(), height, width);
                for (auto const & pho : beam) {
                    repeat (i,5) repeat (j,2) {
                        map<player_id_t,command_t> commands; {
                            player_t curself = *find_player(pho->turn.entities, pho->turn.config.self_id);
                            action_t action = j == 0 ? action_t::move : action_t::bomb;
                            command_t command = create_command(curself, dy[i], dx[i], action);
                            if (age == 0 and forbidden.count(command)) continue;
                            commands[curself.id] = command;
                        }
                        shared_ptr<photon_t> npho = update_photon(*pho, commands);
                        if (not npho) continue;
                        npho->bonus = uniform_real_distribution<double>(- 0.2, 0.2)(engine);
                        if (used.count(npho->signature)) continue;
                        used.insert(npho->signature);
                        if (not is_survivable(self.id, npho->turn, npho->exptime)) continue;
                        point_t p = point(*find_player(npho->turn.entities, npho->turn.config.self_id));
                        nbeam[p.y][p.x].push_back(npho);
                    }
                    if (not clock_check()) break;
                }
                if (not clock_check()) break;
                beam.clear();
                repeat (y,height) repeat (x,width) {
                    whole(sort, nbeam[y][x], [&](shared_ptr<photon_t> const & a, shared_ptr<photon_t> const & b) { return a->score > b->score; }); // reversed
                    if (nbeam[y][x].size() > point_beam_width) nbeam[y][x].resize(point_beam_width);
                    whole(copy, nbeam[y][x], back_inserter(beam));
                }
                whole(sort, beam, [&](shared_ptr<photon_t> const & a, shared_ptr<photon_t> const & b) { return a->score > b->score; }); // reversed
                if (beam.size() > beam_width) beam.resize(beam_width);
                if (not beam.empty()) command = beam[0]->initial_command;
                if (message.empty() and beam.empty()) {
                    if (age == 0) {
                        message = "Sayonara!";
                    } else {
                        message = "Aieee";
                    }
                }
            }
        }

        // log
        high_resolution_clock::time_point clock_end = high_resolution_clock::now(); {
            ll clock_count = duration_cast<milliseconds>(clock_end - clock_begin).count();
            ostringstream oss;
            if (message.empty()) {
                oss << clock_count << "ms";
            } else {
                oss << message << " (" << clock_count << "ms)";
            }
            message = oss.str();
        }
        // update info
        turns.push_back(turn);
        // return
        output_t output;
        output.command = command;
        output.message = message;
        outputs.push_back(output);
        return output;
    }
};

int main() {
    config_t config; cin >> config;
    AI ai(config);
    while (true) {
        turn_t turn = { config }; cin >> turn;
        high_resolution_clock::time_point begin = high_resolution_clock::now();
        output_t output = ai.think(turn);
        cout << output << endl;
        high_resolution_clock::time_point end = high_resolution_clock::now();
        ll count = duration_cast<microseconds>(end - begin).count();
        cerr << "elapsed time: " << count/1000 << "." << count%1000 << "msec" << endl;
    }
}