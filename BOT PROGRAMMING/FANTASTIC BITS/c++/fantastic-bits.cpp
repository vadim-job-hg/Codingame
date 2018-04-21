#pragma GCC optimize("-O3")
#pragma GCC optimize("inline")
#pragma GCC optimize("omit-frame-pointer")
#pragma GCC optimize("unroll-loops")

#include <iostream>
#include <chrono>
#include <string>
#include <algorithm>
#include <math.h>

using namespace std;
using namespace std::chrono;

// #define PROFILE
// #define PROD
// #define DEBUG

#ifdef PROFILE
    const int DURATIONS_COUNT = 1;
    double durations[DURATIONS_COUNT];
    high_resolution_clock::time_point starts[DURATIONS_COUNT];

    #define PS(i)   starts[i] = NOW;
    #define PE(i)   durations[i] = durations[i] + duration_cast<duration<double>>(NOW - starts[i]).count();
#else
    #define PS(i)
    #define PE(i)
#endif

high_resolution_clock::time_point start;
#define NOW high_resolution_clock::now()
#define TIME duration_cast<duration<double>>(NOW - start).count()

// ***********************************************************
constexpr double WIDTH = 16000.0;
constexpr double HEIGHT = 7500.0;

constexpr int OBLIVIATE = 0;
constexpr int PETRIFICUS = 1;
constexpr int ACCIO = 2;
constexpr int FLIPENDO = 3;
constexpr int SPELL_DURATIONS[] = {3, 1, 6, 3};
constexpr int SPELL_COSTS[] = {5, 10, 20, 20};

constexpr double E = 0.00001;
constexpr int VERTICAL = 1;
constexpr int HORIZONTAL = 2;
constexpr double INF = 16000*16000 + 7500*7500;
constexpr int WIZARD = 1;
constexpr int SNAFFLE = 2;
constexpr int BLUDGER = 3;
constexpr int POLE = 4;
constexpr double TO_RAD = M_PI / 180.0;

constexpr double ANGLES[] = {0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0, 190.0, 200.0, 210.0, 220.0, 230.0, 240.0, 250.0, 260.0, 270.0, 280.0, 290.0, 300.0, 310.0, 320.0, 330.0, 340.0, 350.0};
constexpr int ANGLES_LENGTH = 36;

constexpr int DEPTH = 4;
constexpr int SPELL_DEPTH = 8;
constexpr int POOL = 50;
constexpr double MUTATION = 2;

// ***********************************************************

double cosAngles[ANGLES_LENGTH];
double sinAngles[ANGLES_LENGTH];

int myTeam;
int mana = 0;
int turn = 0;
int myScore = 0;
int hisScore = 0;
double energy = 0;
int depth = 0;

int smana;
int smyScore;
int shisScore;

class Point;
class Unit;
class Wizard;
class Snaffle;
class Bludger;
class Spell;
class Pole;

Wizard* myWizard1;
Wizard* myWizard2;
Wizard* hisWizard1;
Wizard* hisWizard2;
Point* myGoal;
Point* hisGoal;
Point* mid;

Unit* units[20];
int unitsFE = 0;

Unit* unitsById[24];

Snaffle* snaffles[20];
int snafflesFE = 0;

Wizard* wizards[4];
Bludger* bludgers[2];
Pole* poles[4];

Unit* spellTargets[4][20];
int spellTargetsFE[4];

bool doLog = false;

Spell* spells[16];

int victory;

// ***********************************************************

static unsigned int g_seed;
inline void fast_srand(int seed) {
  //Seed the generator
  g_seed = seed;
}
inline int fastrand() {
  //fastrand routine returns one integer, similar output value range as C lib.
  g_seed = (214013*g_seed+2531011);
  return (g_seed>>16)&0x7FFF;
}
inline int fastRandInt(int maxSize) {
  return fastrand() % maxSize;
}
inline int fastRandInt(int a, int b) {
  return(a + fastRandInt(b - a));
}
inline double fastRandDouble() {
  return static_cast<double>(fastrand()) / 0x7FFF;
}
inline double fastRandDouble(double a, double b) {
  return a + (static_cast<double>(fastrand()) / 0x7FFF)*(b-a);
}

// ****************************************************************************************

class Solution {
public:
    double energy;
    int moves1[DEPTH];
    int moves2[DEPTH];

    int spellTurn1;
    Unit* spellTarget1;
    int spell1;

    int spellTurn2;
    Unit* spellTarget2;
    int spell2;

    Solution* merge(Solution* solution) {
        Solution* child = new Solution();

        for (int i = 0; i < DEPTH; ++i) {
            if (fastRandInt(2)) {
                child->moves1[i] = solution->moves1[i];
                child->moves2[i] = solution->moves2[i];
            } else {
                child->moves1[i] = moves1[i];
                child->moves2[i] = moves2[i];
            }
        }

        if (fastRandInt(2)) {
            child->spellTurn1 = solution->spellTurn1;
            child->spellTarget1 = solution->spellTarget1;
            child->spell1 = solution->spell1;
        } else {
            child->spellTurn1 = spellTurn1;
            child->spellTarget1 = spellTarget1;
            child->spell1 = spell1;
        }

        if (fastRandInt(2)) {
            child->spellTurn2 = solution->spellTurn2;
            child->spellTarget2 = solution->spellTarget2;
            child->spell2 = solution->spell2;
        } else {
            child->spellTurn2 = spellTurn2;
            child->spellTarget2 = spellTarget2;
            child->spell2 = spell2;
        }


        return child;
    }

    void copy(Solution* solution) {
        for (int i = 0; i < DEPTH; ++i) {
            moves1[i] = solution->moves1[i];
            moves2[i] = solution->moves2[i];
        }

        spellTurn1 = solution->spellTurn1;
        spell1 = solution->spell1;
        spellTarget1 = solution->spellTarget1;
        spellTurn2 = solution->spellTurn2;
        spell2 = solution->spell2;
        spellTarget2 = solution->spellTarget2;

        this->energy = solution->energy;
    }

    void mutate();

    void randomize();
};



// ****************************************************************************************

class Point {
public:
    double x;
    double y;

    Point() {};

    Point(double x, double y) {
        this->x = x;
        this->y = y;
    }
};

inline double dist(double x1, double y1, double x2, double y2) {
    return sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2));
}

inline double dist2(double x1, double y1, double x2, double y2) {
    return (x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2);
}

inline double dist(Point* p, double x2, double y2) {
    return dist(p->x, p->y, x2, y2);
}

inline double dist2(Point* p, double x2, double y2) {
    return dist2(p->x, p->y, x2, y2);
}

inline double dist(Point* u1, Point* u2) {
    return dist(u1->x, u1->y, u2->x, u2->y);
}

inline double dist2(Point* u1, Point* u2) {
    return dist2(u1->x, u1->y, u2->x, u2->y);
}

// ****************************************************************************************

class Collision {
public:
    double t;
    int dir;
    Unit* a;
    Unit* b;

    Collision() {}

    Collision* update(double t, Unit* a, int dir) {
        b = NULL;
        this->t = t;
        this->a = a;
        this->dir = dir;

        return this;
    }

    Collision* update(double t, Unit* a, Unit* b) {
        dir = 0;
        this->t = t;
        this->a = a;
        this->b = b;

        return this;
    }
};

Collision** collisionsCache;
int collisionsCacheFE = 0;

// ****************************************************************************************

class Spell {
public:
    Wizard* caster;
    int duration;
    Unit* target;
    int type;

    int sduration;
    Unit* starget;

    void cast(Unit* target);

    void apply();

    void save();

    void reset() {
        duration = sduration;
        target = starget;
    }

    void reloadTarget();

    virtual void effect() {}

    virtual void print() {}
};

// ****************************************************************************************

class Obliviate : public Spell {
public:
    Obliviate(Wizard* caster, int type) {
        duration = 0;
        this->type = type;
        this->caster = caster;
    }

    virtual void print();

    virtual void effect();
};

// ****************************************************************************************

class Petrificus : public Spell {
public:
    Petrificus(Wizard* caster, int type) {
        duration = 0;
        this->type = type;
        this->caster = caster;
    }

    virtual void print();

    virtual void effect();
};

// ****************************************************************************************

class Accio : public Spell {
public:
    Accio(Wizard* caster, int type) {
        duration = 0;
        this->type = type;
        this->caster = caster;
    }

    virtual void print();

    virtual void effect();
};

// ****************************************************************************************

class Flipendo : public Spell {
public:
    Flipendo(Wizard* caster, int type) {
        duration = 0;
        this->type = type;
        this->caster = caster;
    }

    virtual void print();

    virtual void effect();
};

// ****************************************************************************************

class Unit : public Point {
public:
    int id;
    int type;
    int state;
    bool dead = false;
    double r;
    double m;
    double f;
    double vx;
    double vy;

    double sx;
    double sy;
    double svx;
    double svy;

    Wizard* carrier = NULL;
    Snaffle* snaffle = NULL;

    int grab = 0;

    #ifndef PROD
    double lx;
    double ly;
    double lvx;
    double lvy;
    Wizard* lcarrier;
    Snaffle* lsnaffle;
    bool ldead;

    void store() {
        lx = x;
        ly = y;
        lvx = vx;
        lvy = vy;
        lcarrier = carrier;
        lsnaffle = snaffle;
        ldead = dead;
    }

    void compare();
    #endif

    void update(int id, int x, int y, int vx, int vy, int state) {
        this->id = id;
        this->x = x;
        this->y = y;
        this->vx = vx;
        this->vy = vy;
        this->state = state;
    }

    double speedTo(Point* p) {
        double d = 1.0 / dist(this, x, y);

        // vitesse dans la direction du checkpoint - (vitesse orthogonale)^2/dist au cheeckpoint
        double dx = (p->x - this->x) * d;
        double dy = (p->y - this->y) * d;
        double nspeed = vx*dx + vy*dy;
        double ospeed = dy*vx - dx*vy;

        return nspeed - (5 * ospeed * ospeed * d);
    }

    double speed() {
        return sqrt(vx*vx + vy*vy);
    }

    inline void thrust(double thrust, Point* p, double distance) {
        double coef = (thrust/m) / distance;
        vx += (p->x - x) * coef;
        vy += (p->y - y) * coef;
    }

    inline void thrust(double thrust, double x, double y, double distance) {
        double coef = (thrust/m) / distance;
        vx += (x - this->x) * coef;
        vy += (y - this->y) * coef;
    }

    virtual void move(double t) {
        x += vx * t;
        y += vy * t;
    }

    virtual Collision* collision(double from) {
        double tx = 2.0;
        double ty = tx;

        if (x + vx < r) {
            tx = (r - x)/vx;
        } else if (x + vx > WIDTH - r) {
            tx = (WIDTH - r - x)/vx;
        }

        if (y + vy < r) {
            ty = (r - y)/vy;
        } else if (y + vy > HEIGHT - r) {
            ty = (HEIGHT - r - y)/vy;
        }

        int dir;
        double t;

        if (tx < ty) {
            dir = HORIZONTAL;
            t = tx + from;
        } else {
            dir = VERTICAL;
            t = ty + from;
        }

        if (t <= 0.0 || t > 1.0) {
            return NULL;
        }

        return collisionsCache[collisionsCacheFE++]->update(t, this, dir);
    }

    virtual Collision* collision(Unit* u, double from) {
        double x2 = x - u->x;
        double y2 = y - u->y;
        double r2 = r + u->r;
        double vx2 = vx - u->vx;
        double vy2 = vy - u->vy;
        double a = vx2*vx2 + vy2*vy2;

        if (a < E) {
            return NULL;
        }

        double b = -2.0*(x2*vx2 + y2*vy2);
        double delta = b*b - 4.0*a*(x2*x2 + y2*y2 - r2*r2);

        if (delta < 0.0) {
            return NULL;
        }

        // double sqrtDelta = sqrt(delta);
        // double d = 1.0/(2.0*a);
        // double t1 = (b + sqrtDelta)*d;
        // double t2 = (b - sqrtDelta)*d;
        // double t = t1 < t2 ? t1 : t2;

        double t = (b - sqrt(delta))*(1.0/(2.0*a));

        if (t <= 0.0) {
            return NULL;
        }

        t += from;

        if (t > 1.0) {
            return NULL;
        }

        return collisionsCache[collisionsCacheFE++]->update(t, this, u);
    }

    virtual void bounce(Unit* u) {
        double mcoeff = (m + u->m) / (m * u->m);
        double nx = x - u->x;
        double ny = y - u->y;
        double nxnydeux = nx*nx + ny*ny;
        double dvx = vx - u->vx;
        double dvy = vy - u->vy;
        double product = (nx*dvx + ny*dvy) / (nxnydeux * mcoeff);
        double fx = nx * product;
        double fy = ny * product;
        double m1c = 1.0 / m;
        double m2c = 1.0 / u->m;

        vx -= fx * m1c;
        vy -= fy * m1c;
        u->vx += fx * m2c;
        u->vy += fy * m2c;

        // Normalize vector at 100
        double impulse = sqrt(fx*fx + fy*fy);
        if (impulse < 100.0) {
            double min = 100.0 / impulse;
            fx = fx * min;
            fy = fy * min;
        }

        vx -= fx * m1c;
        vy -= fy * m1c;
        u->vx += fx * m2c;
        u->vy += fy * m2c;
    }

    virtual void bounce(int dir) {
        if (dir == HORIZONTAL) {
            vx = -vx;
        } else {
            vy = -vy;
        }
    }

    virtual void end() {
        x = round(x);
        y = round(y);
        vx = round(vx*f);
        vy = round(vy*f);
    }

    bool can(Unit* u) {
        if (type == SNAFFLE) {
            return !carrier && !dead && !u->snaffle && !u->grab;
        } else if (u->type == SNAFFLE) {
            return !u->carrier && !u->dead && !snaffle && !grab;
        }

        return true;
    }

    virtual void print() {}

    virtual void save() {
        sx = x;
        sy = y;
        svx = vx;
        svy = vy;
    }

    virtual void reset() {
        x = sx;
        y = sy;
        vx = svx;
        vy = svy;
    }
};

// ****************************************************************************************
class Pole : public Unit {
public:

    Pole(int id, double x, double y) {
        this->id = id;
        r = 300;
        m = INF;
        type = POLE;
        this->x = x;
        this->y = y;
        vx = 0;
        vy = 0;
        dead = false;
        f = 0.0;
    }

    virtual void move(double t) {}

    virtual void save() {}

    virtual void reset() {}

    virtual Collision* collision(double from) {
        return NULL;
    }
};

// ****************************************************************************************

class Wizard : public Unit {
public:
    int team;
    Spell* spells[4];

    int sgrab;
    Snaffle* ssnaffle;

    int spell;
    Unit* spellTarget;

    Wizard(int team) {
        this->team = team;
        this->r = 400.0;
        this->m = 1;
        this->f = 0.75;

        snaffle = NULL;
        grab = 0;
        type = WIZARD;

        spells[OBLIVIATE] = new Obliviate(this, OBLIVIATE);
        spells[PETRIFICUS] = new Petrificus(this, PETRIFICUS);
        spells[ACCIO] = new Accio(this, ACCIO);
        spells[FLIPENDO] = new Flipendo(this, FLIPENDO);

        spellTarget = NULL;
    }

    inline void grabSnaffle(Snaffle* snaffle);

    void apply(int move);

    void output(int move, int spellTurn, int spell, Unit* target) {
        if (!spellTurn && spells[spell]->duration == SPELL_DURATIONS[spell]) {
            if (spell == OBLIVIATE) {
                cout << "OBLIVIATE ";
            } else if (spell == PETRIFICUS) {
                cout << "PETRIFICUS ";
            } else if (spell == ACCIO) {
                cout << "ACCIO ";
            } else if (spell == FLIPENDO) {
                cout << "FLIPENDO ";
            }

            cout << target->id << endl;

            return;
        }

        // Adjust the targeted point for this angle
        // Find a point with the good angle
        double px = x + cosAngles[move] * 10000.0;
        double py = y + sinAngles[move] * 10000.0;

        if (snaffle) {
            cout << "THROW " << round(px) << " " << round(py) << " 500";
         } else {
            cout << "MOVE " << round(px) << " " << round(py) << " 150";
        }

        cout << endl;
    }

    bool cast(int spell, Unit* target) {
        int cost = SPELL_COSTS[spell];

        if (mana < cost || target->dead) {
            return false;
        }

        mana -= cost;

        this->spell = spell;
        spellTarget = target;

        return true;
    }

    virtual Collision* collision(Unit* u, double from) {
        if (u->type == SNAFFLE) {
            u->r = -1.0;
            Collision* result = Unit::collision(u, from);
            u->r = 150.0;

            return result;
        } else {
            return Unit::collision(u, from);
        }
    }

    virtual void bounce(Unit* u);

    void play();

    virtual void end();

    virtual void save() {
        Unit::save();

        sgrab = grab;
        ssnaffle = snaffle;
    }

    virtual void reset() {
        Unit::reset();

        grab = sgrab;
        snaffle = ssnaffle;
    }

    virtual void print();

    void updateSnaffle();

    void apply(Solution* solution, int turn, int index) {
        if (index == 1) {
            if (solution->spellTurn1 == turn) {
                if (!myWizard1->cast(solution->spell1, solution->spellTarget1)) {
                    myWizard1->apply(solution->moves1[turn]);
                }
            } else {
                myWizard1->apply(solution->moves1[turn]);
            }
        } else {
            if (solution->spellTurn2 == turn) {
                if (!myWizard2->cast(solution->spell2, solution->spellTarget2)) {
                    myWizard2->apply(solution->moves2[turn]);
                }
            } else {
                myWizard2->apply(solution->moves2[turn]);
            }
        }
    }
};

// ****************************************************************************************

class Snaffle : public Unit {
public:
    Wizard* scarrier;



    Snaffle() {
        this->r = 150.0;
        this->m = 0.5;
        this->f = 0.75;

        carrier = NULL;
        type = SNAFFLE;
    }

    virtual Collision* collision(double from) {
        if (carrier || dead) {
            return NULL;
        }

        double tx = 2.0;
        double ty = tx;

        if (x + vx < 0.0) {
            tx =  -x/vx;
        } else if (x + vx > WIDTH) {
            tx = (WIDTH - x)/vx;
        }

        if (y + vy < r) {
            ty = (r - y)/vy;
        } else if (y + vy > HEIGHT - r) {
            ty = (HEIGHT - r - y)/vy;
        }

        int dir;
        double t;

        if (tx < ty) {
            dir = HORIZONTAL;
            t = tx + from;
        } else {
            dir = VERTICAL;
            t = ty + from;
        }

        if (t <= 0.0 || t > 1.0) {
            return NULL;
        }

        return collisionsCache[collisionsCacheFE++]->update(t, this, dir);
    }

    virtual Collision* collision(Unit* u, double from) {
        if (u->type == WIZARD) {
            r = -1.0;
            Collision* result = Unit::collision(u, from);
            r = 150.0;

            return result;
        } else {
            return Unit::collision(u, from);
        }
    }

    virtual void bounce(Unit* u) {
        if (u->type == WIZARD) {
            Wizard* target = (Wizard*) u;
            if (!target->snaffle && !target->grab && !dead && !carrier) {
                target->grabSnaffle(this);
            }
        } else {
            Unit::bounce(u);
        }
    }

    virtual void bounce(int dir) {
        if (dir == HORIZONTAL && y >= 1899.0 && y <= 5599.0) {
            dead = true;

            if (!myTeam) {
                if (x > 8000) {
                    myScore += 1;
                } else {
                    hisScore += 1;
                }
            } else {
                if (x > 8000) {
                    hisScore += 1;
                } else {
                    myScore += 1;
                }
            }
        } else {
            Unit::bounce(dir);
        }
    }

    virtual void move(double t) {
        if (!dead && !carrier) {
            Unit::move(t);
        }
    }

    virtual void end() {
        if (!dead && !carrier) {
            Unit::end();
        }
    }

    virtual void save() {
        Unit::save();

        scarrier = carrier;
    }

    virtual void reset() {
        Unit::reset();

        carrier = scarrier;
        dead = false;
    }

    virtual void print() {
        if (dead) {
            cerr << "Snaffle " << id << " dead";
        } else {
            cerr << "Snaffle " << id << " " << x << " " << y << " " << vx << " " << vy << " " << speed() << " " << " | ";

            if (carrier) {
                cerr << "Carrier " << carrier->id << " | ";
            }
        }

        cerr << endl;
    }
};

// ****************************************************************************************

class Bludger : public Unit {
public:
    Wizard* last;
    int ignore[2];

    Wizard* slast;

    Bludger() {
        this->r = 200.0;
        this->m = 8;
        this->f = 0.9;

        last = NULL;
        ignore[0] = -1;
        ignore[1] = -1;
        type = BLUDGER;
    }

    virtual void print() {
        cerr << "Bludger " << id << " " << x << " " << y << " " << vx << " " << vy << " " << speed() << " " << ignore[0] << " " << ignore[1] << " | ";

        if (last) {
            cerr << "Last " << last->id << " | ";
        }

        cerr << endl;
    }

    virtual void save() {
        Unit::save();

        slast = last;
    }

    virtual void reset() {
        Unit::reset();

        last = slast;
        ignore[0] = -1;
        ignore[1] = -1;
    }

    virtual void bounce(Unit* u) {
        if (u->type == WIZARD) {
            last = (Wizard*) u;
        }

        Unit::bounce(u);
    }

    void play() {
        // Find our target
        Wizard* target = NULL;
        double d;

        for (int i = 0; i < 4; ++i) {
            Wizard* wizard = wizards[i];

            if ((last && last->id == wizard->id) || wizard->team == ignore[0] || wizard->team == ignore[1]) {
                continue;
            }

            double d2 = dist2(this, wizard);

            if (!target || d2 < d) {
                d = d2;
                target = wizard;
            }
        }

        if (target) {
            thrust(1000.0, target, sqrt(d));
        }

        ignore[0] = -1;
        ignore[1] = -1;
    }
};

// ****************************************************************************************

void Obliviate::print() {
    if (duration) {
        cerr << "Obliviate " << target->id << " " << duration << " | ";
    }
}

void Petrificus::print() {
    if (duration) {
        cerr << "Petrificus " << target->id << " " << duration << " | ";
    }
}

void Accio::print() {
    if (duration) {
        cerr << "Accio " << target->id << " " << duration << " | ";
    }
}

void Flipendo::print() {
    if (duration) {
        cerr << "Flipendo " << target->id << " " << duration << " | ";
    }
}

void Spell::cast(Unit* target) {
    this->target = target;
    duration = SPELL_DURATIONS[type];
}

void Spell::apply() {
    if (duration) {
        duration -= 1;

        if (!target->dead) {
            effect();
        }
    }
}

void Spell::reloadTarget() {
    if (!duration || target->dead) {
        // Cancel the spell
        target = NULL;
        duration = 0;
    }
}

void Spell::save() {
    sduration = duration;
    starget = target;
}

void Obliviate::effect() {
    ((Bludger*)target)->ignore[caster->team] = caster->team;
}

void Petrificus::effect() {
    target->vx = 0.0;
    target->vy = 0.0;
}

void Accio::effect() {
    double d = dist(caster, target);

    if (d < 10.0) {
        return;
    }

    double dcoef = d*0.001;
    double power = 3000.0 / (dcoef*dcoef);

    if (power > 1000.0) {
        power = 1000.0;
    }

    dcoef = 1.0 / d;
    power = power / target->m;
    target->vx -= dcoef * power * (target->x - caster->x);
    target->vy -= dcoef * power * (target->y - caster->y);
}

void Flipendo::effect() {
    double d = dist(caster, target);

    if (d < 10.0) {
        return;
    }

    double dcoef = d*0.001;
    double power = 6000.0 / (dcoef*dcoef);

    if (power > 1000.0) {
        power = 1000.0;
    }

    dcoef = 1.0 / d;
    power = power / target->m;
    target->vx += dcoef * power * (target->x - caster->x);
    target->vy += dcoef * power * (target->y - caster->y);
}

// ****************************************************************************************

#ifndef PROD
void Unit::compare() {
    if (lx != x || ly != y || lvx != vx || lvy != vy || lcarrier != carrier || lsnaffle != snaffle || ldead != dead) {
        cerr << "Diff " << id << " : "
        << (x - lx) << " "
        << (y - ly) << " "
        << dist(x, y, lx, ly) << " | "
        << (vx - lvx) << " "
        << (vy - lvy) << " "
        << (speed() - sqrt(lvx*lvx + lvy*lvy)) << " | "
        << carrier << " " << lcarrier << " | "
        << snaffle << " " << lsnaffle << " | ";

        if (ldead) {
            cerr << "dead";
        }

        cerr << endl;
    }
}
#endif

void Wizard::print() {
    cerr << "Wizard " << id << " " << x << " " << y << " " << vx << " " << vy << " " << speed() << " " << grab << " | ";

    if (snaffle) {
        cerr << "Snaffle " << snaffle->id << " | ";
    }

    for (int i = 0; i < 4; ++i) {
        spells[i]->print();
    }

    cerr << endl;
}

void Wizard::updateSnaffle() {
    if (state) {
        for (int i = 0; i < snafflesFE; ++i) {
            Snaffle* snaffle = snaffles[i];

            if (snaffle->x == x && snaffle->y == y && snaffle->vx == vx && snaffle->vy == vy) {
                this->snaffle = snaffle;
                snaffle->carrier = this;
            }
        }

        grab = 3;
    } else {
        if (grab) {
            grab -= 1;
        }
        snaffle = NULL;
    }
}

void Wizard::play() {
    // Relacher le snaffle qu'on porte dans tous les cas
    if (snaffle) {
        snaffle->carrier = NULL;
        snaffle = NULL;
    }
}

void Wizard::end() {
    Unit::end();

    if (grab) {
        grab -= 1;

        if (!grab) {
            // Check if we can grab a snaffle
            for (int i = 0; i < snafflesFE; ++i) {
                Snaffle* snaffle = snaffles[i];

                if (!snaffle->dead && !snaffle->carrier && dist2(this, snaffle) < 159201.0) {
                    grabSnaffle(snaffle);
                    break;
                }
            }
        }
    }

    if (snaffle) {
        snaffle->x = x;
        snaffle->y = y;
        snaffle->vx = vx;
        snaffle->vy = vy;
    }

    if (spellTarget) {
        spells[spell]->cast(spellTarget);
        spellTarget = NULL;
    }
}

void Wizard::bounce(Unit* u) {
    if (u->type == SNAFFLE) {
        Snaffle* target = (Snaffle*) u;
        if (!snaffle && !grab && !target->dead && !target->carrier) {
            grabSnaffle(target);
        }
    } else {
        if (u->type == BLUDGER) {
            ((Bludger*) u)->last = this;
        }

        Unit::bounce(u);
    }
}

inline void Wizard::grabSnaffle(Snaffle* snaffle) {
    grab = 4;
    snaffle->carrier = this;
    this->snaffle = snaffle;

    // Stop the accio spell if we have one
    Spell* accio = this->spells[ACCIO];
    if (accio->duration && accio->target->id == snaffle->id) {
        accio->duration = 0;
        accio->target = NULL;
    }
}

void Wizard::apply(int move) {
    if (snaffle) {
        double coef = 500.0 * (1.0 / snaffle->m);
        snaffle->vx += cosAngles[move] * coef;
        snaffle->vy += sinAngles[move] * coef;
    } else {
        vx += cosAngles[move] * 150.0;
        vy += sinAngles[move] * 150.0;
    }
}

void Solution::mutate() {
    int r = fastRandInt(4);

    if (!r) {
        // Change a moves1
        moves1[fastRandInt(DEPTH)] = fastRandInt(ANGLES_LENGTH);
    } else if (r == 1) {
        // Change a moves2
        moves2[fastRandInt(DEPTH)] = fastRandInt(ANGLES_LENGTH);
    } else if (r == 2) {
        // Change spell1
        spellTurn1 = fastRandInt(SPELL_DEPTH);
        spell1 = fastRandInt(4);
        spellTarget1 = spellTargets[spell1][fastRandInt(spellTargetsFE[spell1])];
    } else {
        // Change spell2
        spellTurn2 = fastRandInt(SPELL_DEPTH);
        spell2 = fastRandInt(4);
        spellTarget2 = spellTargets[spell2][fastRandInt(spellTargetsFE[spell2])];
        spellTarget2->speed();
    }

}

void Solution::randomize() {
    for (int i = 0; i < DEPTH; ++i) {
        moves1[i] = fastRandInt(ANGLES_LENGTH);
        moves2[i] = fastRandInt(ANGLES_LENGTH);
    }

    spellTurn1 = fastRandInt(SPELL_DEPTH);
    spell1 = fastRandInt(4);
    spellTarget1 = spellTargets[spell1][fastRandInt(spellTargetsFE[spell1])];
    spellTurn2 = fastRandInt(SPELL_DEPTH);
    spell2 = fastRandInt(4);
    spellTarget2 = spellTargets[spell2][fastRandInt(spellTargetsFE[spell2])];

}

// ****************************************************************************************

bool mustErase(Collision* col, Unit* a, Unit* b) {
    if (a->id == col->a->id) {
        return true;
    }

    if (b != NULL && col->b != NULL) {
        if (a->id == col->b->id
            || b->id == col->a->id
            || b->id == col->b->id) {
            return true;
        }
    } else if (b != NULL) {
        if (b->id == col->a->id) {
            return true;
        }
    } else if (col->b != NULL) {
        if (a->id == col->b->id) {
            return true;
        }
    }

    return false;
}

Collision** collisions;
int collisionsFE = 0;

Collision** tempCollisions;
int tempCollisionsFE = 0;

Collision* fake;

void move() {
    double t = 0.0;
    double delta;

    Collision* next = fake;
    collisionsCacheFE = 0;
    collisionsFE = 0;
    tempCollisionsFE = 0;

    Collision* col;
    Unit* a;
    Unit* b;
    Unit* u;
    int i, j;

    // Get first collisions
    for (i = 0; i < unitsFE; ++i) {
        a = units[i];

        col = a->collision(t);

        if (col) {
            collisions[collisionsFE++] = col;

            if (col->t < next->t) {
                next = col;
            }
        }

        for (j = i + 1; j < unitsFE; ++j) {
            b = units[j];

            if (a->can(b)) {
                col = a->collision(b, t);

                if (col) {
                    collisions[collisionsFE++] = col;

                    if (col->t < next->t) {
                        next = col;
                    }
                }
            }
        }
    }

    while (t < 1.0) {
        if (next == fake) {
            for (i = 0; i < unitsFE; ++i) {
                units[i]->move(1.0 - t);
            }

            break;
        } else {
            // Move to the collision time
            delta = next->t - t;
            for (i = 0; i < unitsFE; ++i) {
                units[i]->move(delta);
            }

            t = next->t;

            if (next->dir) {
                /*if (doLog) {
                    cerr << next->a->id << " bounce with wall at " << t << endl;
                }*/
                next->a->bounce(next->dir);
            } else {
                /*if (doLog) {
                    cerr << next->a->id << " bounce with " << next->b->id << " at " << t << endl;
                }*/
                next->a->bounce(next->b);
            }

            a = next->a;
            b = next->b;

            // Invalid previous collisions for the concerned units and get new ones
            next = fake;

            for (i = 0; i < collisionsFE; ++i) {
                col = collisions[i];

                if (!mustErase(col, a, b)) {
                    if (col->t < next->t) {
                        next = col;
                    }

                    tempCollisions[tempCollisionsFE++] = col;
                }
            }

            Collision** temp = tempCollisions;
            tempCollisions = collisions;
            collisions = temp;

            collisionsFE = tempCollisionsFE;
            tempCollisionsFE = 0;

            // Find new collisions for a
            col = a->collision(t);
            if (col) {
                collisions[collisionsFE++] = col;

                if (col->t < next->t) {
                    next = col;
                }
            }

            for (i = 0; i < unitsFE; ++i) {
                u = units[i];

                if (a->id != u->id && a->can(u)) {
                    col = a->collision(u, t);

                    if (col) {
                        collisions[collisionsFE++] = col;

                        if (col->t < next->t) {
                            next = col;
                        }
                    }
                }
            }

            // Find new collisions for b
            if (b) {
                col = b->collision(t);

                if (col) {
                    collisions[collisionsFE++] = col;

                    if (col->t < next->t) {
                        next = col;
                    }
                }

                for (i = 0; i < unitsFE; ++i) {
                    u = units[i];

                    if (b->id != u->id && b->can(u)) {
                        col = b->collision(u, t);

                        if (col) {
                            collisions[collisionsFE++] = col;

                            if (col->t < next->t) {
                                next = col;
                            }
                        }
                    }
                }
            }
        }
    }
}

void play() {
    for (int i = 0; i < 4; ++i) {
        spells[i]->apply();
    }

    bludgers[0]->play();
    bludgers[1]->play();
    wizards[0]->play();
    wizards[1]->play();
    wizards[2]->play();
    wizards[3]->play();

    for (int i = 5; i < 16; ++i) {
        spells[i]->apply();
    }

    move();

    for (int i = 0; i < unitsFE; ++i) {
        units[i]->end();
    }

    if (mana != 100) {
        mana += 1;
    }
}

double eval() {
    // Hidden ;)
    return 0;
}

void reset() {
    for (int i = 0; i < unitsFE; ++i) {
        units[i]->reset();
    }

    for (int i = 0; i < 16; ++i) {
        spells[i]->reset();
    }

    mana = smana;
    myScore = smyScore;
    hisScore = shisScore;
}

void dummies() {
    if (hisWizard1->snaffle) {
        hisWizard1->snaffle->thrust(500.0, hisGoal, dist(hisWizard1, hisGoal));
    } else {
        Snaffle* target = NULL;
        double targetD = INF;
        double d;

        for (int i = 0; i < snafflesFE; ++i) {
            Snaffle* snaffle = snaffles[i];

            if (!snaffle->dead) {
                d = dist2(hisWizard1, snaffle);

                if (d < targetD) {
                    targetD = d;
                    target = snaffle;
                }
            }
        }

        if (target) {
            hisWizard1->thrust(150.0, target, sqrt(targetD));
        }
    }

    if (hisWizard2->snaffle) {
        hisWizard2->snaffle->thrust(500.0, hisGoal, dist(hisWizard2, hisGoal));
    } else {
        Snaffle* target = NULL;
        double targetD = INF;
        double d;

        for (int i = 0; i < snafflesFE; ++i) {
            Snaffle* snaffle = snaffles[i];

            if (!snaffle->dead) {
                d = dist2(hisWizard2, snaffle);

                if (d < targetD) {
                    targetD = d;
                    target = snaffle;
                }
            }
        }

        if (target) {
            hisWizard2->thrust(150.0, target, sqrt(targetD));
        }
    }
}

void simulate(Solution* solution) {
    energy = 0;
    depth = 0;

    myWizard1->apply(solution, 0, 1);
    myWizard2->apply(solution, 0, 2);
    dummies();

    play();
    depth = 1;

    solution->energy = eval() * 0.1;

    for (int i = 1; i < DEPTH; ++i) {
        myWizard1->apply(solution, i, 1);
        myWizard2->apply(solution, i, 2);
        dummies();

        play();
        depth += 1;
    }

    solution->energy += energy + eval();

    reset();
}

void simulate2(Solution* solution) {
    doLog = true;

    cerr << "Solution: " << endl;
    for (int i = 0; i < DEPTH; ++i) {
        cerr << ANGLES[solution->moves1[i]] << " " << ANGLES[solution->moves2[i]] << endl;
    }
    cerr << "Spell 1: " << solution->spellTurn1 << " " << solution->spell1 << " " << solution->spellTarget1->id << endl;
    cerr << "Spell 2: " << solution->spellTurn2 << " " << solution->spell2 << " " << solution->spellTarget2->id << endl;

    energy = 0;
    depth = 0;

    myWizard1->apply(solution, 0, 1);
    myWizard2->apply(solution, 0, 2);
    dummies();

    play();

    cerr << "******* State at turn " << depth + 1 << endl;
    for (int i = 0; i < unitsFE; ++i) {
        units[i]->print();
    }
    depth = 1;

    solution->energy = eval() * 0.1;

    for (int i = 1; i < DEPTH; ++i) {
        myWizard1->apply(solution, i, 1);
        myWizard2->apply(solution, i, 2);
        dummies();

        play();

        cerr << "******* State at turn " << depth + 1 << endl;
        for (int i = 0; i < unitsFE; ++i) {
            units[i]->print();
        }
        depth += 1;
    }

    solution->energy += energy + eval();

    cerr << "Sanity check : " << solution->energy << endl;
    cerr << "Mana: " << mana << endl;
    cerr << "My score: " << myScore << endl;
    cerr << "His score: " << hisScore << endl;

    reset();

    doLog = false;
}

// ****************************************************************************************

int main() {
    fast_srand(42);

    fake = new Collision();
    fake->t = 1000.0;

    for (int i = 0; i < ANGLES_LENGTH; ++i) {
        cosAngles[i] = cos(ANGLES[i] * TO_RAD);
        sinAngles[i] = sin(ANGLES[i] * TO_RAD);
    }

    cin >> myTeam; cin.ignore();

    collisionsCache = new Collision*[100];
    collisions = new Collision*[100];
    tempCollisions = new Collision*[100];

    for (int i = 0; i < 100; ++i) {
        collisionsCache[i] = new Collision();
    }

    wizards[0] = new Wizard(0);
    wizards[1] = new Wizard(0);
    wizards[2] = new Wizard(1);
    wizards[3] = new Wizard(1);

    units[0] = wizards[0];
    units[1] = wizards[1];
    units[2] = wizards[2];
    units[3] = wizards[3];

    if (!myTeam) {
        myWizard1 = wizards[0];
        myWizard2 = wizards[1];
        hisWizard1 = wizards[2];
        hisWizard2 = wizards[3];
        myGoal = new Point(16000, 3750);
        hisGoal = new Point(0, 3750);
    } else {
        myWizard1 = wizards[2];
        myWizard2 = wizards[3];
        hisWizard1 = wizards[0];
        hisWizard2 = wizards[1];
        myGoal = new Point(0, 3750);
        hisGoal = new Point(16000, 3750);
    }

    mid = new Point(8000, 3750);

    bludgers[0] = new Bludger();
    bludgers[1] = new Bludger();

    units[4] = bludgers[0];
    units[5] = bludgers[1];

    poles[0] = new Pole(20, 0, 1750);
    poles[1] = new Pole(21, 0, 5750);
    poles[2] = new Pole(22, 16000, 1750);
    poles[3] = new Pole(23, 16000, 5750);

    units[6] = poles[0];
    units[7] = poles[1];
    units[8] = poles[2];
    units[9] = poles[3];

    unitsFE = 10;

    int spellsFE = 0;
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            spells[spellsFE++] = wizards[j]->spells[i];
        }
    }

    Solution* best = new Solution();

    int oldSnafflesFE;

    while (1) {
        int entities;
        cin >> entities; cin.ignore();
        start = NOW;

        int bludgersFE = 0;

        if (turn) {
            for (int i = 0; i < 24; ++i) {
                Unit* u = unitsById[i];

                if (u && u->type == SNAFFLE) {
                    u->dead = true;
                    u->carrier = NULL;
                }
            }
        }

        for (int i = 0; i < entities; i++) {
            int id; // entity identifier
            string entityType; // "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
            int x; // position
            int y; // position
            int vx; // velocity
            int vy; // velocity
            int state; // 1 if the wizard is holding a Snaffle, 0 otherwise
            cin >> id >> entityType >> x >> y >> vx >> vy >> state; cin.ignore();

            Unit* unit;

            if (entityType == "WIZARD" || entityType == "OPPONENT_WIZARD") {
                unit = wizards[id];
            } else if (entityType == "SNAFFLE") {
                if (!turn) {
                    unit = new Snaffle();
                } else {
                    unit = unitsById[id];
                }

                unit->dead = false;
                units[unitsFE++] = unit;
                snaffles[snafflesFE++] = (Snaffle*)unit;
            } else if (entityType == "BLUDGER") {
                unit = bludgers[bludgersFE++];
            }

            unit->update(id, x, y, vx, vy, state);
        }

        if (turn == 0) {
            victory = (snafflesFE / 2) + 1;

            for (int i = 0; i < unitsFE; ++i) {
                unitsById[units[i]->id] = units[i];
            }
        }

        // Mise à jour des carriers et des snaffles
        for (int i = 0; i < 4; ++i) {
            wizards[i]->updateSnaffle();
        }

        // Mise à jour du score
        if (turn && oldSnafflesFE != snafflesFE) {
            for (int i = 0; i < 24; ++i) {
                Unit* u = unitsById[i];

                if (u && u->type == SNAFFLE && u->dead) {
                    if (!myTeam) {
                        if (u->x > 8000) {
                            myScore += 1;
                        } else {
                            hisScore += 1;
                        }
                    } else {
                        if (u->x > 8000) {
                            hisScore += 1;
                        } else {
                            myScore += 1;
                        }
                    }

                    delete u;
                    unitsById[i] = NULL;
                }
            }
        }

        // Cibles pour les sorts

        // Bludgers pour tous les sorts
        for (int i = 0; i < 4; ++i) {
            spellTargets[i][0] = bludgers[0];
            spellTargets[i][1] = bludgers[1];
            spellTargetsFE[i] = 2;
        }

        // Wizards ennemis pour petrificus et flipendo
        if (!myTeam) {
            spellTargets[PETRIFICUS][spellTargetsFE[PETRIFICUS]++] = wizards[2];
            spellTargets[PETRIFICUS][spellTargetsFE[PETRIFICUS]++] = wizards[3];
            spellTargets[FLIPENDO][spellTargetsFE[FLIPENDO]++] = wizards[2];
            spellTargets[FLIPENDO][spellTargetsFE[FLIPENDO]++] = wizards[3];
        } else {
            spellTargets[PETRIFICUS][spellTargetsFE[PETRIFICUS]++] = wizards[0];
            spellTargets[PETRIFICUS][spellTargetsFE[PETRIFICUS]++] = wizards[1];
            spellTargets[FLIPENDO][spellTargetsFE[FLIPENDO]++] = wizards[0];
            spellTargets[FLIPENDO][spellTargetsFE[FLIPENDO]++] = wizards[1];
        }

        // Snaffles pour tous les sorts sauf obliviate
        for (int i = 1; i < 4; ++i) {
            for (int j = 0; j < snafflesFE; ++j) {
                spellTargets[i][spellTargetsFE[i]++] = snaffles[j];
            }
        }

        for (int i = 0; i < unitsFE; ++i) {
            units[i]->save();

            smana = mana;
            smyScore = myScore;
            shisScore = hisScore;
        }

        for (int i = 0; i < 16; ++i) {
            spells[i]->reloadTarget();
            spells[i]->save();
        }

        #ifndef PROD
        if (turn) {
            for (int i = 0; i < unitsFE; ++i) {
                units[i]->compare();
            }
        }
        #endif

        #ifndef PROD
        cerr << "hisScore : " << hisScore << endl;
        cerr << "victory : " << victory << endl;
        #endif

        /*cerr << "***** State for this turn " << endl;
        cerr << "Mana: " << mana << endl;
        cerr << "My score: " << myScore << endl;
        cerr << "His score: " << hisScore << endl;
        for (int i = 0; i < unitsFE; ++i) {
            units[i]->print();
        }*/

        // Evolution

        Solution* base;
        if (turn) {
            base = new Solution();

            for (int j = 1; j < DEPTH; ++j) {
                base->moves1[j - 1] = best->moves1[j];
                base->moves2[j - 1] = best->moves2[j];
            }

            base->spellTurn1 = best->spellTurn1;
            base->spell1 = best->spell1;
            base->spellTarget1 = best->spellTarget1;
            base->spellTurn2 = best->spellTurn2;
            base->spell2 = best->spell2;
            base->spellTarget2 = best->spellTarget2;

            if (!base->spellTurn1) {
                base->spellTurn1 = SPELL_DEPTH - 1;
            } else {
                base->spellTurn1 -= 1;
            }

            if (!base->spellTurn2) {
                base->spellTurn2 = SPELL_DEPTH - 1;
            } else {
                base->spellTurn2 -= 1;
            }

            if (base->spellTarget1->dead) {
                base->spellTurn1 = SPELL_DEPTH - 1;
                base->spellTarget1 = spellTargets[base->spell1][fastRandInt(spellTargetsFE[base->spell1])];
            }

            if (base->spellTarget2->dead) {
                base->spellTurn2 = SPELL_DEPTH - 1;
                base->spellTarget2 = spellTargets[base->spell2][fastRandInt(spellTargetsFE[base->spell2])];
            }

            delete best;
        }

        Solution** pool = new Solution*[POOL];
        Solution** newPool = new Solution*[POOL];
        Solution** temp;
        int counter = POOL;

        best = new Solution();
        Solution* sol = new Solution();
        sol->randomize();

        simulate(sol);
        pool[0] = sol;

        best->copy(sol);

        Solution* tempBest = sol;

        // First generation
        int startI = 1;

        if (turn) {
            // Populate the POOL with some copy of the previous best one
            for (int i = startI; i < POOL / 5; ++i) {
                Solution* solution = new Solution();
                solution->copy(base);

                // Add a last one random
                solution->moves1[DEPTH - 1] = fastRandInt(ANGLES_LENGTH);
                solution->moves2[DEPTH - 1] = fastRandInt(ANGLES_LENGTH);

                simulate(solution);

                if (solution->energy > tempBest->energy) {
                    tempBest = solution;
                }

                pool[i] = solution;
            }

            delete base;

            startI = POOL / 5;
        }

        for (int i = startI; i < POOL; ++i) {
            Solution* solution = new Solution();
            solution->randomize();

            simulate(solution);

            if (solution->energy > tempBest->energy) {
                tempBest = solution;
            }

            pool[i] = solution;
        }

        if (tempBest->energy > best->energy) {
            best->copy(tempBest);
        }
        tempBest = best;

        double limit = turn ? 0.085 : 0.800;

        #ifdef DEBUG
            #define LIMIT counter <= 1000
        #else
            #define LIMIT TIME < limit
        #endif

        int generation = 1;
        int bestGeneration = 1;

        int poolFE;
        while (LIMIT) {
            // New generation

            // Force the actual best with a mutation to be in the pool
            Solution* solution = new Solution();
            solution->copy(tempBest);
            solution->mutate();
            simulate(solution);

            if (solution->energy > tempBest->energy) {
                tempBest = solution;
            }

            newPool[0] = solution;

            counter += 1;

            poolFE = 1;
            while (poolFE < POOL && LIMIT) {
                int aIndex = fastRandInt(POOL);
                int bIndex;

                do {
                    bIndex = fastRandInt(POOL);
                } while (bIndex == aIndex);

                int firstIndex = pool[aIndex]->energy > pool[bIndex]->energy ? aIndex : bIndex;

                do {
                    aIndex = fastRandInt(POOL);
                } while (aIndex == firstIndex);

                do {
                    bIndex = fastRandInt(POOL);
                } while (bIndex == aIndex || bIndex == firstIndex);

                int secondIndex = pool[aIndex]->energy > pool[bIndex]->energy ? aIndex : bIndex;

                Solution* child = pool[firstIndex]->merge(pool[secondIndex]);

                if (!fastRandInt(MUTATION)) {
                    child->mutate();
                }

                simulate(child);

                if (child->energy > tempBest->energy) {
                    tempBest = child;
                }

                newPool[poolFE++] = child;

                counter += 1;
            }

            // Burn previous generation !!
            for (int i = 0; i < POOL; ++i) {
                delete pool[i];
            }

            temp = pool;
            pool = newPool;
            newPool = temp;

            if (tempBest->energy > best->energy) {
                best->copy(tempBest);
                bestGeneration = generation;
            }
            tempBest = best;

            generation += 1;
        }

        #ifndef PROD
        cerr << "Counter: " << counter << endl;
        cerr << "Energy: " << best->energy << endl;
        cerr << "Generation: " << generation << endl;
        #endif

        #ifdef DEBUG
        // Play a last time for debug
        simulate2(best);
        #endif

        // Play a last time to check some infos
        myWizard1->apply(best, 0, 1);
        myWizard2->apply(best, 0, 2);
        dummies();

        play();

/*        cerr << "***** State for next turn " << endl;
        cerr << "Mana: " << mana << endl;
        cerr << "My score: " << myScore << endl;
        cerr << "His score: " << hisScore << endl;
        for (int i = 0; i < unitsFE; ++i) {
            units[i]->print();
        }*/

        smana = mana;
        bludgers[0]->slast = bludgers[0]->last;
        bludgers[1]->slast = bludgers[1]->last;

        for (int i = 0; i < 16; ++i) {
            spells[i]->save();
        }

        #ifndef PROD
        for (int i = 0; i < unitsFE; ++i) {
            units[i]->store();
        }
        #endif

        reset();

        #ifdef PROFILE
            double totalSpent = 0;
            for (int i = 0; i < DURATIONS_COUNT; i++) {
                totalSpent += durations[i];
            }
            for (int i = 0; i < DURATIONS_COUNT; i++) {
                fprintf(stderr, "Time %3d: %.6fms (%.2f%%)\n", i, durations[i] * 1000.0, durations[i] * 100.0/totalSpent);
            }
            fprintf(stderr, "Total: %.6fms (%.6fms per turn)\n", totalSpent * 1000.0, totalSpent * 1000.0/(double)(turn + 1));
        #endif

        myWizard1->output(best->moves1[0], best->spellTurn1, best->spell1, best->spellTarget1);
        myWizard2->output(best->moves2[0], best->spellTurn2, best->spell2, best->spellTarget2);

        // Burn last generation !!
        for (int i = 0; i < poolFE; ++i) {
            delete pool[i];
        }

        delete [] pool;
        delete [] newPool;

        turn += 1;
        unitsFE = 10;

        oldSnafflesFE = snafflesFE;
        snafflesFE = 0;
    }
}