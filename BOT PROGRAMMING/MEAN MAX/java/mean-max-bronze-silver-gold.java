import java.util.*;
import java.util.stream.Collectors;

class Player {
  public static void main(String args[]) {
    MeanMax meanMax = new MeanMax();
    meanMax.gameLoop();
  }
}

class MeanMax {
  final int LOOTER_COUNT = 3;

  final double MAP_RADIUS = 6000.0;

  final double WATERTOWN_RADIUS = 3000.0;

  final int TANKER_THRUST = 500;
  final double TANKER_EMPTY_MASS = 2.5;
  final double TANKER_MASS_BY_WATER = 0.5;
  final double TANKER_FRICTION = 0.40;
  final double TANKER_RADIUS_BASE = 400.0;
  final double TANKER_RADIUS_BY_SIZE = 50.0;
  final int TANKER_EMPTY_WATER = 1;

  final int MAX_THRUST = 300;

  final double REAPER_MASS = 0.5;
  final double REAPER_FRICTION = 0.20;
  final int REAPER_SKILL_DURATION = 3;
  final int REAPER_SKILL_COST = 30;
  final int REAPER_SKILL_ORDER = 0;
  final double REAPER_SKILL_RANGE = 2000.0;
  final double REAPER_SKILL_RADIUS = 1000.0;
  final double REAPER_SKILL_MASS_BONUS = 10.0;

  final double DESTROYER_MASS = 1.5;
  final double DESTROYER_FRICTION = 0.30;
  final int DESTROYER_SKILL_DURATION = 1;
  final int DESTROYER_SKILL_COST = 60;
  final int DESTROYER_SKILL_ORDER = 2;
  final double DESTROYER_SKILL_RANGE = 2000.0;
  final double DESTROYER_SKILL_RADIUS = 1000.0;
  final int DESTROYER_NITRO_GRENADE_POWER = 1000;

  final double DOOF_MASS = 1.0;
  final double DOOF_FRICTION = 0.25;
  final double DOOF_RAGE_COEF = 1.0 / 100.0;
  final int DOOF_SKILL_DURATION = 3;
  final int DOOF_SKILL_COST = 30;
  final int DOOF_SKILL_ORDER = 1;
  final double DOOF_SKILL_RANGE = 2000.0;
  final double DOOF_SKILL_RADIUS = 1000.0;

  final double LOOTER_RADIUS = 400.0;
  final int LOOTER_REAPER = 0;
  final int LOOTER_DESTROYER = 1;
  final int LOOTER_DOOF = 2;

  final int TYPE_TANKER = 3;
  final int TYPE_WRECK = 4;
  final int TYPE_REAPER_SKILL_EFFECT = 5;
  final int TYPE_DOOF_SKILL_EFFECT = 6;
  final int TYPE_DESTROYER_SKILL_EFFECT = 7;

  final double EPSILON = 0.00001;
  final double MIN_IMPULSE = 30.0;
  final double IMPULSE_COEFF = 0.5;

  // Center of the map
  final Point WATERTOWN = new Point(0, 0);

  // The null collision
  final Collision NULL_COLLISION = new Collision(1.0 + EPSILON);

  final int MY_PLAYER_ID = 0;
  final int PLAYER1_ID = 1;
  final int PLAYER2_ID = 2;

  Referee referee = new Referee();

  public int round(double d) {
    int s = d < 0 ? -1 : 1;
    return s * (int) Math.round(s * d);
  }

  void gameLoop() {
    while (true) {
      referee.reset();
      referee.readGameInput();
      referee.play();
    }
  }

  class Point {
    double x;
    double y;

    Point(double x, double y) {
      this.x = x;
      this.y = y;
    }

    double distance(Point p) {
      return Math.sqrt((this.x - p.x) * (this.x - p.x) + (this.y - p.y) * (this.y - p.y));
    }

    // Move the point to an other point for a given distance
    void moveTo(Point p, double distance) {
      double d = distance(p);

      if (d < EPSILON) {
        return;
      }

      double dx = p.x - x;
      double dy = p.y - y;
      double coef = distance / d;

      this.x += dx * coef;
      this.y += dy * coef;
    }

    boolean isInRange(Point p, double range) {
      return p != this && distance(p) <= range;
    }
  }

  abstract class Circle extends Point {
    double radius;

    Circle(double x, double y) {
      super(x, y);
    }

    public boolean isInDoofSkill(Set<SkillEffect> skillEffects) {
      return skillEffects.stream().anyMatch(s -> s instanceof DoofSkillEffect && isInRange(s, s.radius + radius));
    }
  }

  class Wreck extends Circle {
    int id;
    int water;

    Wreck(int id, double radius, double x, double y, int water) {
      super(x, y);
      this.id = id;
      this.radius = radius;
      this.water = water;
    }
  }

  abstract class Unit extends Circle {
    int id;
    int type;
    double vx;
    double vy;
    double mass = -1d;
    double friction;

    Unit(int id, int type, double x, double y, double vx, double vy) {
      super(x, y);
      this.id = id;
      this.type = type;
      this.vx = vx;
      this.vy = vy;
    }

    void move(double t) {
      x += vx * t;
      y += vy * t;
    }

    double speed() {
      return Math.sqrt(vx * vx + vy * vy);
    }

    void thrust(Point p, int power) {
      double distance = distance(p);

      // Avoid a division by zero
      if (Math.abs(distance) <= EPSILON) {
        return;
      }

      double coef = (((double) power) / mass) / distance;
      vx += (p.x - this.x) * coef;
      vy += (p.y - this.y) * coef;
    }

    void adjust(Set<SkillEffect> skillEffects) {
      x = round(x);
      y = round(y);

      if (isInDoofSkill(skillEffects)) {
        // No friction if we are in a doof skill effect
        vx = round(vx);
        vy = round(vy);
      } else {
        vx = round(vx * (1.0 - friction));
        vy = round(vy * (1.0 - friction));
      }
    }

    // Search the next collision with the map border
    Collision getCollision() {
      // Check instant collision
      if (distance(WATERTOWN) + radius >= MAP_RADIUS) {
        return new Collision(0.0, this);
      }

      // We are not moving, we can't reach the map border
      if (vx == 0.0 && vy == 0.0) {
        return NULL_COLLISION;
      }

      // Search collision with map border
      // Resolving: sqrt((x + t*vx)^2 + (y + t*vy)^2) = MAP_RADIUS - radius <=> t^2*(vx^2 + vy^2) + t*2*(x*vx + y*vy) + x^2 + y^2 - (MAP_RADIUS - radius)^2 = 0
      // at^2 + bt + c = 0;
      // a = vx^2 + vy^2
      // b = 2*(x*vx + y*vy)
      // c = x^2 + y^2 - (MAP_RADIUS - radius)^2

      double a = vx * vx + vy * vy;

      if (a <= 0.0) {
        return NULL_COLLISION;
      }

      double b = 2.0 * (x * vx + y * vy);
      double c = x * x + y * y - (MAP_RADIUS - radius) * (MAP_RADIUS - radius);
      double delta = b * b - 4.0 * a * c;

      if (delta <= 0.0) {
        return NULL_COLLISION;
      }

      double t = (-b + Math.sqrt(delta)) / (2.0 * a);

      if (t <= 0.0) {
        return NULL_COLLISION;
      }

      return new Collision(t, this);
    }

    // Search the next collision with an other unit
    Collision getCollision(Unit u) {
      // Check instant collision
      if (distance(u) <= radius + u.radius) {
        return new Collision(0.0, this, u);
      }

      // Both units are motionless
      if (vx == 0.0 && vy == 0.0 && u.vx == 0.0 && u.vy == 0.0) {
        return NULL_COLLISION;
      }

      // Change referencial
      // Unit u is not at point (0, 0) with a speed vector of (0, 0)
      double x2 = x - u.x;
      double y2 = y - u.y;
      double r2 = radius + u.radius;
      double vx2 = vx - u.vx;
      double vy2 = vy - u.vy;

      // Resolving: sqrt((x + t*vx)^2 + (y + t*vy)^2) = radius <=> t^2*(vx^2 + vy^2) + t*2*(x*vx + y*vy) + x^2 + y^2 - radius^2 = 0
      // at^2 + bt + c = 0;
      // a = vx^2 + vy^2
      // b = 2*(x*vx + y*vy)
      // c = x^2 + y^2 - radius^2

      double a = vx2 * vx2 + vy2 * vy2;

      if (a <= 0.0) {
        return NULL_COLLISION;
      }

      double b = 2.0 * (x2 * vx2 + y2 * vy2);
      double c = x2 * x2 + y2 * y2 - r2 * r2;
      double delta = b * b - 4.0 * a * c;

      if (delta < 0.0) {
        return NULL_COLLISION;
      }

      double t = (-b - Math.sqrt(delta)) / (2.0 * a);

      if (t <= 0.0) {
        return NULL_COLLISION;
      }

      return new Collision(t, this, u);
    }

    // Bounce between 2 units
    void bounce(Unit u) {
      double mcoeff = (mass + u.mass) / (mass * u.mass);
      double nx = x - u.x;
      double ny = y - u.y;
      double nxnysquare = nx * nx + ny * ny;
      double dvx = vx - u.vx;
      double dvy = vy - u.vy;
      double product = (nx * dvx + ny * dvy) / (nxnysquare * mcoeff);
      double fx = nx * product;
      double fy = ny * product;
      double m1c = 1.0 / mass;
      double m2c = 1.0 / u.mass;

      vx -= fx * m1c;
      vy -= fy * m1c;
      u.vx += fx * m2c;
      u.vy += fy * m2c;

      fx = fx * IMPULSE_COEFF;
      fy = fy * IMPULSE_COEFF;

      // Normalize vector at min or max impulse
      double impulse = Math.sqrt(fx * fx + fy * fy);
      double coeff = 1.0;
      if (impulse > EPSILON && impulse < MIN_IMPULSE) {
        coeff = MIN_IMPULSE / impulse;
      }

      fx = fx * coeff;
      fy = fy * coeff;

      vx -= fx * m1c;
      vy -= fy * m1c;
      u.vx += fx * m2c;
      u.vy += fy * m2c;

      double diff = (distance(u) - radius - u.radius) / 2.0;
      if (diff <= 0.0) {
        // Unit overlapping. Fix positions.
        moveTo(u, diff - EPSILON);
        u.moveTo(this, diff - EPSILON);
      }
    }

    // Bounce with the map border
    void bounce() {
      double mcoeff = 1.0 / mass;
      double nxnysquare = x * x + y * y;
      double product = (x * vx + y * vy) / (nxnysquare * mcoeff);
      double fx = x * product;
      double fy = y * product;

      vx -= fx * mcoeff;
      vy -= fy * mcoeff;

      fx = fx * IMPULSE_COEFF;
      fy = fy * IMPULSE_COEFF;

      // Normalize vector at min or max impulse
      double impulse = Math.sqrt(fx * fx + fy * fy);
      double coeff = 1.0;
      if (impulse > EPSILON && impulse < MIN_IMPULSE) {
        coeff = MIN_IMPULSE / impulse;
      }

      fx = fx * coeff;
      fy = fy * coeff;
      vx -= fx * mcoeff;
      vy -= fy * mcoeff;

      double diff = distance(WATERTOWN) + radius - MAP_RADIUS;
      if (diff >= 0.0) {
        // Unit still outside of the map, reposition it
        moveTo(WATERTOWN, diff + EPSILON);
      }
    }
  }

  class Tanker extends Unit {
    int water;
    int size;

    Tanker(int id, double x, double y, double vx, double vy, int water, int size) {
      super(id, TYPE_TANKER, x, y, vx, vy);
      this.water = water;
      this.size = size;
      init();
    }

    void init() {
      water = TANKER_EMPTY_WATER;
      mass = TANKER_EMPTY_MASS + TANKER_MASS_BY_WATER * water;
      friction = TANKER_FRICTION;
      radius = TANKER_RADIUS_BASE + TANKER_RADIUS_BY_SIZE * size;
    }

    boolean isFull() {
      return water >= size;
    }

    boolean isInMap() {
      return isInRange(WATERTOWN, MAP_RADIUS);
    }

    void play() {
      if (isFull()) {
        // Try to leave the map
        thrust(WATERTOWN, -TANKER_THRUST);
      } else if (distance(WATERTOWN) > WATERTOWN_RADIUS) {
        // Try to reach watertown
        thrust(WATERTOWN, TANKER_THRUST);
      }
    }

    Collision getCollision() {
      // Tankers can go outside of the map
      return NULL_COLLISION;
    }
  }

  abstract class Looter extends Unit {
    int skillCost;
    double skillRange;
    int driverId;

    Action action = null;

    Looter(int id, int unitType, double x, double y, double vx, double vy, int driverId) {
      super(id, unitType, x, y, vx, vy);
      this.driverId = driverId;
      radius = LOOTER_RADIUS;
    }

    SkillEffect skill(Point p, Driver driver) throws TooFarException, NoRageException {
      if (driver.rage < skillCost)
        throw new NoRageException();
      if (distance(p) > skillRange)
        throw new TooFarException();

      driver.rage -= skillCost;
      return skillImpl(p);
    }

    abstract SkillEffect skillImpl(Point p);

    public void setAction(Action action) {
      if (action instanceof MoveAction) {
        if (action.power < 0) {
          action.power = 0;
        }
        action.power = Math.min(action.power, MAX_THRUST);

        // Apply Steering Strategy
        action.target.x -= vx;
        action.target.y -= vy;
      }
      this.action = action;
    }

    void thrust() {
      thrust(action.target, action.power);
    }
  }

  class Reaper extends Looter {
    Reaper(int id, double x, double y, double vx, double vy, int driverId) {
      super(id, LOOTER_REAPER, x, y, vx, vy, driverId);
      init();
    }

    void init() {
      mass = REAPER_MASS;
      friction = REAPER_FRICTION;
      skillCost = REAPER_SKILL_COST;
      skillRange = REAPER_SKILL_RANGE;
    }

    SkillEffect skillImpl(Point p) {
      return new ReaperSkillEffect(TYPE_REAPER_SKILL_EFFECT, p.x, p.y, REAPER_SKILL_DURATION, REAPER_SKILL_ORDER);
    }
  }

  class Destroyer extends Looter {
    Destroyer(int id, double x, double y, double vx, double vy, int driverId) {
      super(id, LOOTER_DESTROYER, x, y, vx, vy, driverId);
      init();
    }

    void init() {
      mass = DESTROYER_MASS;
      friction = DESTROYER_FRICTION;
      skillCost = DESTROYER_SKILL_COST;
      skillRange = DESTROYER_SKILL_RANGE;
    }

    SkillEffect skillImpl(Point p) {
      return new DestroyerSkillEffect(TYPE_DESTROYER_SKILL_EFFECT, p.x, p.y, DESTROYER_SKILL_DURATION, DESTROYER_SKILL_ORDER);
    }
  }

  class Doof extends Looter {
    Doof(int id, double x, double y, double vx, double vy, int driverId) {
      super(id, LOOTER_DOOF, x, y, vx, vy, driverId);
      init();
    }

    void init() {
      mass = DOOF_MASS;
      friction = DOOF_FRICTION;
      skillCost = DOOF_SKILL_COST;
      skillRange = DOOF_SKILL_RANGE;
    }

    SkillEffect skillImpl(Point p) {
      return new DoofSkillEffect(TYPE_DOOF_SKILL_EFFECT, p.x, p.y, DOOF_SKILL_DURATION, DOOF_SKILL_ORDER);
    }
  }

  class Driver {
    Integer score;
    int id;
    int rage;
    Map<Integer, Looter> looters = new HashMap<>();

    Driver(int id, int score, int rage) {
      this.id = id;
      this.score = score;
      this.rage = rage;
    }

    void setLooter(Looter looter) {
      looters.put(looter.type, looter);
    }
  }

  class Collision {
    double t;
    Unit a;
    Unit b;

    Collision(double t) {
      this(t, null, null);
    }

    Collision(double t, Unit a) {
      this(t, a, null);
    }

    Collision(double t, Unit a, Unit b) {
      this.t = t;
      this.a = a;
      this.b = b;
    }

    Tanker dead() {
      if (a instanceof Destroyer && b instanceof Tanker && b.mass < REAPER_SKILL_MASS_BONUS) {
        return (Tanker) b;
      }

      if (b instanceof Destroyer && a instanceof Tanker && a.mass < REAPER_SKILL_MASS_BONUS) {
        return (Tanker) a;
      }

      return null;
    }
  }

  abstract class SkillEffect extends Point {
    int type;
    double radius;
    int duration;
    int order;

    SkillEffect(int type, double x, double y, double radius, int duration, int order) {
      super(x, y);
      this.type = type;
      this.radius = radius;
      this.duration = duration;
      this.order = order;
    }

    void apply(List<Unit> units) {
      duration -= 1;
      applyImpl(units.stream().filter(u -> isInRange(u, radius + u.radius)).collect(Collectors.toList()));
    }

    abstract void applyImpl(List<Unit> units);
  }

  class ReaperSkillEffect extends SkillEffect {
    ReaperSkillEffect(int type, double x, double y, int duration, int order) {
      super(type, x, y, REAPER_SKILL_RADIUS, duration, order);
    }

    void applyImpl(List<Unit> units) {
      // Increase mass
      units.forEach(u -> u.mass += REAPER_SKILL_MASS_BONUS);
    }
  }

  class DestroyerSkillEffect extends SkillEffect {

    DestroyerSkillEffect(int type, double x, double y, int duration, int order) {
      super(type, x, y, DESTROYER_SKILL_RADIUS, duration, order);
    }

    void applyImpl(List<Unit> units) {
      // Push units
      units.forEach(u -> u.thrust(this, -DESTROYER_NITRO_GRENADE_POWER));
    }
  }

  class DoofSkillEffect extends SkillEffect {

    DoofSkillEffect(int type, double x, double y, int duration, int order) {
      super(type, x, y, DOOF_SKILL_RADIUS, duration, order);
    }

    void applyImpl(List<Unit> units) {
      // Nothing to do now
    }
  }

  @SuppressWarnings("serial")
  class NoRageException extends Exception {
  }

  @SuppressWarnings("serial")
  class TooFarException extends Exception {
  }

  abstract class Action {
    Point target = null;
    int power = 0;
    String message = "MESSAGE";
  }

  class WaitAction extends Action {
    public WaitAction() {
      this.message = "WAIT";
    }

    @Override
    public String toString() {
      return "WAIT " + message;
    }
  }

  abstract class TargetAction extends Action {
    public TargetAction(Point target) {
      this.target = target;
    }

    public TargetAction(Point target, String message) {
      this(target);
      this.message = message;
    }
  }

  class MoveAction extends TargetAction {
    public MoveAction(Point target, int power) {
      super(target);
      this.power = power;
    }

    public MoveAction(Point target, int power, String message) {
      super(target, message);
      this.power = power;
    }

    @Override
    public String toString() {
      int targetX = round(target.x);
      int targetY = round(target.y);
      return targetX + " " + targetY + " " + power + " " + message;
    }
  }

  class SkillAction extends TargetAction {
    public SkillAction(Point target, String message) {
      super(target, message);
    }

    @Override
    public String toString() {
      int targetX = round(target.x);
      int targetY = round(target.y);
      return "SKILL " + targetX + " " + targetY + " " + message;
    }
  }

  class Referee {
    Scanner in = new Scanner(System.in);

    List<Unit> units = new ArrayList<>();
    List<Tanker> tankers = new ArrayList<>();
    List<Wreck> wrecks = new ArrayList<>();
    List<Driver> drivers = new ArrayList<>();
    List<Looter> enemyLooters = new ArrayList<>();

    Set<SkillEffect> skillEffects = new TreeSet<>(Comparator.comparingInt(a -> a.order));

    Driver myDriver;
    Reaper myReaper;
    Destroyer myDestroyer;
    Doof myDoof;

    Driver enemyDriver1;
    Reaper enemyReaper1;
    Doof enemyDoof1;

    Driver enemyDriver2;
    Reaper enemyReaper2;
    Doof enemyDoof2;

    void initReferee() {
      adjust();
    }

    void reset() {
      units.clear();
      wrecks.clear();
      tankers.clear();
      skillEffects.clear();
      drivers.clear();
      enemyLooters.clear();
    }

    void readGameInput() {
      readDriverInfo();
      readUnitInfo();
    }

    private void readDriverInfo() {
      int myScore = in.nextInt();
      int enemyScore1 = in.nextInt();
      int enemyScore2 = in.nextInt();
      int myRage = in.nextInt();
      int enemyRage1 = in.nextInt();
      int enemyRage2 = in.nextInt();

      myDriver = new Driver(MY_PLAYER_ID, myScore, myRage);
      enemyDriver1 = new Driver(PLAYER1_ID, enemyScore1, enemyRage1);
      enemyDriver2 = new Driver(PLAYER2_ID, enemyScore2, enemyRage2);
      drivers.add(myDriver);
      drivers.add(enemyDriver1);
      drivers.add(enemyDriver2);
    }

    private void readUnitInfo() {
      int unitCount = in.nextInt();
      for (int i = 0; i < unitCount; i++) {
        int unitId = in.nextInt();
        int unitType = in.nextInt();
        int driverId = in.nextInt();
        float mass = in.nextFloat();
        int radius = in.nextInt();
        int x = in.nextInt();
        int y = in.nextInt();
        int vx = in.nextInt();
        int vy = in.nextInt();
        int extra = in.nextInt();
        int extra2 = in.nextInt();

        switch (unitType) {
          case LOOTER_REAPER:
            Reaper reaper = new Reaper(unitId, x, y, vx, vy, driverId);
            units.add(reaper);
            addLooter(reaper, driverId);
            if (driverId == MY_PLAYER_ID) {
              myReaper = reaper;
            } else if (driverId == PLAYER1_ID) {
              enemyReaper1 = reaper;
              enemyLooters.add(reaper);
            } else {
              enemyReaper2 = reaper;
              enemyLooters.add(reaper);
            }
            break;

          case LOOTER_DESTROYER:
            Destroyer destroyer = new Destroyer(unitId, x, y, vx, vy, driverId);
            units.add(destroyer);
            addLooter(destroyer, driverId);
            if (driverId == MY_PLAYER_ID) {
              myDestroyer = destroyer;
            } else {
              enemyLooters.add(destroyer);
            }
            break;

          case LOOTER_DOOF:
            Doof doof = new Doof(unitId, x, y, vx, vy, driverId);
            units.add(doof);
            addLooter(doof, driverId);
            if (driverId == MY_PLAYER_ID) {
              myDoof = doof;
            } else if (driverId == PLAYER1_ID) {
              enemyDoof1 = doof;
              enemyLooters.add(doof);
            } else {
              enemyDoof2 = doof;
              enemyLooters.add(doof);
            }
            break;

          case TYPE_TANKER:
            Tanker tanker = new Tanker(unitId, x, y, vx, vy, extra, extra2);
            units.add(tanker);
            tankers.add(tanker);
            break;

          case TYPE_WRECK:
            Wreck wreck = new Wreck(unitId, radius, x, y, extra);
            wrecks.add(wreck);
            break;

          case TYPE_REAPER_SKILL_EFFECT:
            ReaperSkillEffect reaperSkillEffect = new ReaperSkillEffect(unitType, x, y, extra, REAPER_SKILL_ORDER);
            skillEffects.add(reaperSkillEffect);
            break;

          case TYPE_DOOF_SKILL_EFFECT:
            DoofSkillEffect doofSkillEffect = new DoofSkillEffect(unitType, x, y, extra, DOOF_SKILL_ORDER);
            skillEffects.add(doofSkillEffect);
            break;
        }
      }
    }

    void addLooter(Looter looter, int playerId) {
      drivers.get(playerId).setLooter(looter);
    }

    void play() {
      Action[] myActions = pickMyActions();

      assignActions(MY_PLAYER_ID, myActions);

      System.out.println(myReaper.action);
      System.out.println(myDestroyer.action);
      System.out.println(myDoof.action);
    }

    Action pickDummyReaperAction(Reaper reaper) {
      Point target = pickWreckMinDist(reaper);
      if (target == null) {
        return new WaitAction();
      } else {
        return new MoveAction(target, MAX_THRUST);
      }
    }

    Action pickMyReaperAction() {
      String message = "REAPER";
      Point target = pickMyWreck();
      if (target == null) {
        target = myDestroyer;
        message = "DEST";
      }
      return new MoveAction(target, MAX_THRUST, message);
    }

    Action pickMyDestroyerAction(Reaper targetEnemyReaper) {
      String message = "NADE";
      Point target = pickMyDestroyerSkillTarget();
      if (target == null) {
        target = pickMyTanker();
        message = "DEST";
        if (target == null) {
          target = targetEnemyReaper;
          message = "PLAYER" + targetEnemyReaper.driverId;
        }
        return new MoveAction(target, MAX_THRUST, message);
      } else {
        return new SkillAction(target, message);
      }
    }

    Action pickMyDoofAction(Reaper targetEnemyReaper) {
      Point target = pickMyDoofSkillTarget(targetEnemyReaper);
      String message = "OIL";
      if (target == null) {
        target = targetEnemyReaper;
        message = "PLAYER" + targetEnemyReaper.driverId;
        return new MoveAction(target, MAX_THRUST, message);
      } else {
        return new SkillAction(target, message);
      }
    }

    Action[] pickDummyEnemyActions(Reaper reaper) {
      Action reaperAction = pickDummyReaperAction(reaper);
      Action destroyerAction = new WaitAction();
      Action doofAction = new WaitAction();
      return new Action[]{reaperAction, destroyerAction, doofAction};
    }

    Action[] pickMyActions() {
      Reaper targetEnemyReaper = pickMyTargetEnemyReaper();
      Action reaperAction = pickMyReaperAction();
      Action destroyerAction = pickMyDestroyerAction(targetEnemyReaper);
      Action doofAction = pickMyDoofAction(targetEnemyReaper);
      return new Action[]{reaperAction, destroyerAction, doofAction};
    }

    Point pickWreckMinDist(Reaper reaper) {
      Point target = null;
      double minScore = Double.POSITIVE_INFINITY;

      for (Wreck wreck : wrecks) {
        double score = reaper.distance(wreck);
        if (score < minScore) {
          target = wreck;
          minScore = score;
        }
      }
      return target;
    }

    Reaper pickMyTargetEnemyReaper() {
      List<Driver> driversCopy = new ArrayList<>(drivers);
      driversCopy.sort((d1, d2) -> d2.score.compareTo(d1.score));

      int myRank = driversCopy.indexOf(myDriver) + 1;
      int targetEnemyId;

      if (myRank == 2) {
        targetEnemyId = driversCopy.get(0).id; // rank #1
      } else {
        targetEnemyId = driversCopy.get(1).id; // rank #2
      }

      if (targetEnemyId == PLAYER1_ID) {
        return enemyReaper1;
      } else {
        return enemyReaper2;
      }
    }

    double score(Point target, int water) {
      double allyDist = myReaper.distance(target) + myDestroyer.distance(target);
      double enemyReaperDist = enemyReaper1.distance(target) + enemyReaper2.distance(target);
      double enemyDoofDist = enemyDoof1.distance(target) + enemyDoof2.distance(target);
      double distance = allyDist * 2 / (enemyReaperDist + enemyDoofDist);
      return water / distance;
    }

    Point pickMyWreck() {
      Point target = null;
      double maxScore = Double.NEGATIVE_INFINITY;

      for (Wreck wreck : wrecks) {
        if (!wreck.isInDoofSkill(skillEffects)) {
          double score = score(wreck, wreck.water);
          if (score > maxScore) {
            target = wreck;
            maxScore = score;
          }
        }
      }
      return target;
    }

    Point pickMyDestroyerSkillTarget() {
      boolean enoughRage = myDriver.rage >= (DESTROYER_SKILL_COST + DOOF_SKILL_COST);
      if (enoughRage && myDestroyer.isInRange(myReaper, DESTROYER_SKILL_RANGE)) {
        // check if there is enemy looters around
        for (Unit enemyLooter : enemyLooters) {
          if (enemyLooter.isInRange(myReaper, DESTROYER_SKILL_RADIUS)) {
            return myReaper;
          }
        }
      }
      return null;
    }

    Point pickMyTanker() {
      Point target = null;
      double maxScore = 0;

      for (Tanker tanker : tankers) {
        if (tanker.isInMap()) {
          double score = score(tanker, tanker.water);
          if (score > maxScore) {
            target = tanker;
            maxScore = score;
          }
        }
      }
      return target;
    }

    Point pickMyDoofSkillTarget(Reaper targetEnemyReaper) {
      Point target = null;
      if (myDriver.rage >= DOOF_SKILL_COST) {
        Unit otherReaper = targetEnemyReaper.equals(enemyReaper1) ? enemyReaper2 : enemyReaper1;
        target = pickMyDoofSkillTarget2(targetEnemyReaper);
        if (target == null) {
          target = pickMyDoofSkillTarget2(otherReaper);
        }
      }
      return target;
    }

    Point pickMyDoofSkillTarget2(Unit enemyReaper) {
      Point target = null;
      for (Wreck wreck : wrecks) {
        boolean enemyInRange = enemyReaper.isInRange(wreck, wreck.radius);
        boolean myDoofInRange = myDoof.isInRange(wreck, DOOF_SKILL_RANGE);
        boolean myReaperNotInRange = !myReaper.isInRange(wreck, wreck.radius);
        if (enemyInRange && myDoofInRange && myReaperNotInRange && !wreck.isInDoofSkill(skillEffects)) {
          target = wreck;
        }
      }
      return target;
    }

    void assignActions(int playerId, Action actions[]) {
      for (int i = 0; i < LOOTER_COUNT; ++i) {
        Driver driver = drivers.get(playerId);
        Looter looter = driver.looters.get(i);
        Action action = actions[i];
        looter.setAction(action);

        if (action instanceof SkillAction) {
          try {
            SkillEffect effect = looter.skill(action.target, driver);
            skillEffects.add(effect);
          } catch (NoRageException | TooFarException e) {
            System.err.println(e.getMessage());
          }
        }
      }
    }

    // Get the next collision for the current round
    // All units are tested
    Collision getNextCollision() {
      Collision result = NULL_COLLISION;

      for (int i = 0; i < units.size(); ++i) {
        Unit unit = units.get(i);

        // Test collision with map border first
        Collision collision = unit.getCollision();

        if (collision.t < result.t) {
          result = collision;
        }

        for (int j = i + 1; j < units.size(); ++j) {
          collision = unit.getCollision(units.get(j));

          if (collision.t < result.t) {
            result = collision;
          }
        }
      }

      return result;
    }

    // Play a collision
    void playCollision(Collision collision) {
      if (collision.b == null) {
        // Bounce with border
        collision.a.bounce();
      } else {
        Tanker dead = collision.dead();

        if (dead != null) {
          // A destroyer killed a tanker
          tankers.remove(dead);
          units.remove(dead);
          // (potential new wreck)
        } else {
          // Bounce between two units
          collision.a.bounce(collision.b);
        }
      }
    }

    void updateGame() {
      // Apply skill effects
      for (SkillEffect effect : skillEffects) {
        effect.apply(units);
      }

      // Apply thrust for tankers
      for (Tanker t : tankers) {
        t.play();
      }

      // Apply wanted thrust for looters
      for (Driver driver : drivers) {
        for (Looter looter : driver.looters.values()) {
          if (looter.action instanceof MoveAction && looter.action.target != null) {
            looter.thrust();
          }
        }
      }

      double t = 0.0;

      // Play the round. Stop at each collisions and play it. Repeat until t > 1.0

      Collision collision = getNextCollision();

      while (collision.t + t <= 1.0) {
        double delta = collision.t;
        units.forEach(u -> u.move(delta));
        t += collision.t;

        playCollision(collision);

        collision = getNextCollision();
      }
    }

    void adjust() {
      units.forEach(u -> u.adjust(skillEffects));
    }

    // pseudo code
    /*
    void simulateTurn() {
      for (int playerId = 0; playerId < 3; ++playerId) {
        assignActions(playerId, actions);
      }
      updateGame();
    }
    */
  }
}