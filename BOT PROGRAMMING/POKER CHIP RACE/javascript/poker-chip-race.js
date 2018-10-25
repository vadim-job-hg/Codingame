/**
 * It's the survival of the biggest!
 * Propel your chips across a frictionless table top to avoid getting eaten by bigger foes.
 * Aim for smaller oil droplets for an easy size boost.
 * Tip: merging your chips will give you a sizeable advantage.
 **/

var MAX_SPEED = 15;
var MAX_TARGET_SPEED = 100;
var MIN_TARGET_RADIUS = 8;
/** It doesn't make sense to try and predict positions dozens of rounds in advance */
var MAX_PREDICTION_HORIZON = 24;
var DEFAULT_PREDICTION_HORIZON = 3;
/** Percentage of the radius that we try to keep free around us (vital space) */
var DISTANCE_MARGIN = 0.01;

var debug = function() {
  var args = arguments;
  var message = Object.keys(args).map(function(arg) { return args[arg]; }).join(' ');
  printErr(message, '\n');
};

var getNorm = function(vector, p1, p2) {
  if(!p1) p1 = 'x';
  if(!p2) p2 = 'y';
  return Math.sqrt(Math.pow(vector[p1], 2) + Math.pow(vector[p2], 2));
};
var distance = function(from, to) {
  return getNorm({
    x: from.x - to.x,
    y: from.y - to.y
  });
};
var getSpeed = function(entity) {
  return getNorm(entity, 'vx', 'vy');
};
var normalized = function(vector) {
  var norm = getNorm(vector);
  return {
    x: vector.x / norm,
    y: vector.y / norm
  };
};

var isMine = function(entity) {
  return (entity.owner == playerId);
};
/**
 * Largest first
 */
var sortBySize = function(a, b) {
  return a.radius < b.radius;
};
var getMyEntities = function(allEntities) {
  return allEntities.filter(function(entity) {
    return isMine(entity);
  });
};

/**
 * @return {Object|null} The entity with this id or null if not found (e.g. has been eaten)
 */
var getEntityById = function(allEntities, id) {
  for(var i = allEntities.length - 1; i >= 0; i--) {
    if(allEntities[i].id == id) {
      return allEntities[i];
    }
  }
  return null;
};

var isEatable = function(mine, target) {
  // TODO: take into account the prospective size
  // (i.e. the size after using matter to reach the target)
  return (mine.radius * 0.87 > target.radius) || isMine(target);
};
var isWorthIt = function(mine, target) {
  return isEatable(mine, target) &&
         target.radius >= (mine.radius / 4) &&
         getSpeed(target) <= MAX_TARGET_SPEED;
};

/**
 * @return {Boolean} Whether or not the velocity is already high enough
 */
var canMove = function(mine) {
  // TODO: tweak max speed (should take target into account)
  var can = mine.allowRedirect || getSpeed(mine) <= MAX_SPEED;
  mine.allowRedirect = false;
  return can;
};

/**
 * @TODO Do not target an entity which is fleeing away
 * @TODO Do not target an entity which is "protected" by an uneatable entity
 *
 * @param {Function} criterion Sort function to apply to eatable entities to choose the best one
 * @warning Will return `null` if no entity is eatable
 */
var selectEatableEntity = function(entities, player, criterion) {
  var eatable = entities.filter(function(entity) {
    return isWorthIt(player, entity) && (entity.id != player.id);
  });

  var sorted = eatable.sort(criterion);
  return sorted[0];
};

var getNearestEatableEntity = function(entities, player) {
  var nearest = function(a, b) {
    return distance(a, player) > distance(b, player);
  };
  return selectEatableEntity(entities, player, nearest);
};
var getLargestEatableEntity = function(entities, player) {
  return selectEatableEntity(entities, player, sortBySize);
};
var getBestEntity = function(entities, player) {
  // Compromise size vs distance
  // TODO: tweak heuristic
  var heuristic = function(a, b) {
    as = (a.radius >= MIN_TARGET_RADIUS ? a.radius : 0);
    bs = (b.radius >= MIN_TARGET_RADIUS ? b.radius : 0);
    return distance(a, player) - a.radius > distance(b, player) - b.radius;
  };
  return selectEatableEntity(entities, player, heuristic);
};

/**
 * @param {Object} entity A moving entity. We assume it will stay on its current course.
 *   Properties `vx` and `vy` are expressed in units per round.
 * @param {Float} [n] Number of rounds to predict over. Defaults to 1
 */
var estimatePosition = function(entity, n) {
  if(!n) {
    n = 1;
  }

  return {
    x: entity.x + n * entity.vx,
    y: entity.y + n * entity.vy
  };
};

/**
 * @param {Object} entity The controlled entity
 * @param {Object} target The entity to reach
 * @param {Float} [speed] Average speed (units per round) to assume. Defaults to max(current speed, MAX_SPEED)
 * @return {Float} Number of rounds necessary to reach the target
 */
var estimateEta = function(entity, target, speed) {
  if(!speed) {
    speed = Math.max(getSpeed(entity), MAX_SPEED);
  }

  // TODO: take into account target displacement and compute
  // a real intersection point
  var distanceToTarget = distance(entity, target);
  return distanceToTarget / speed;
};


/**
 * @param {Object} myEntity
 * @param {Array} allEntities
 * @param {Integer} [n] Number of rounds to predict ahead
 * @return {Object} id of an entity endangering this entity, or null if it's safe
 */
var isEndangered = function(myEntity, allEntities, n) {
  if(!n) {
    n = DEFAULT_PREDICTION_HORIZON;
  }

  var myPosition = estimatePosition(myEntity, n);
  var dangereous = allEntities.filter(function(e) {
    if(isEatable(myEntity, e)) {
      return false;
    }

    // TODO: trajectory based detection (continuous movement)
    // TODO: take bouncing into account
    var d;
    var criticalDistance = myEntity.radius + e.radius;
    for(var i = 1; i <= n; ++i) {
      d = distance(estimatePosition(myEntity, i), estimatePosition(e, i));
      if(d <= (1 - DISTANCE_MARGIN) * criticalDistance) {
        return true;
      }
    }
    // This entity is not going to be near in the next n rounds
    return false;
  });

  if(!dangereous || dangereous.length < 1) {
    return null;
  }

  // Return the biggest dangereous entity
  dangereous.sort(sortBySize);
  return dangereous[0];
};

/**
 * @return {Object} The best possible position to escape this predator
 */
var chooseEscapeDestination = function(myEntity, predator, n) {
  // TODO: take current inertia into account
  // TODO: check that this works for still predators

  if(!n) {
    n = DEFAULT_PREDICTION_HORIZON;
  }

  // Determine crash position
  // TODO: refactor to avoid code duplication
  var position, d, predatorPosition;
  var criticalDistance = myEntity.radius + predator.radius;
  for(var i = 1; i <= n; i++) {
    predatorPosition = estimatePosition(predator, i);
    d = distance(estimatePosition(myEntity, i), predatorPosition);
    if(d <= (1 - DISTANCE_MARGIN) * criticalDistance) {
      position = predatorPosition;
      break;
    }
  }
  var toCrash = {
    x: position.x - myEntity.x,
    y: position.y - myEntity.y
  };

  // Go to the perpendicular to that direction
  // TODO: take environment into account (to choose left / right)
  var normal = {
    x: - toCrash.y,
    y: toCrash.x
  };
  normal = normalized(normal);
  // Compensate for current speed
  var currentDirection = normalized({ x: myEntity.vx, y: myEntity.vy });
  normal.x += -(currentDirection.x / 2);
  normal.y += -(currentDirection.y / 2);

  debug('Escaping towards', normal.x, normal.y);

  return {
    x: myEntity.x + normal.x,
    y: myEntity.y + normal.y
  };
};

var assignTarget = function(myEntity, allEntities) {
  target = getBestEntity(allEntities, myEntity);
  targets[myEntity.id] = (target ? target.id : null);
  // Allow to rectify course, even if we're already moving over target speed
  myEntity.allowRedirect = true;
};

/**
 * Assign a target to each controlled entity which is not already assigned.
 * If the current target is no longer eatable or no longer exists, reassign a new one.
 *
 * @TODO When assigning to one of my one entities, assign reciprocally
 */
var assignTargets = function(myEntities, allEntities) {
  myEntities.forEach(function(mine) {
    if(!targets[mine.id]) {
      assignTarget(mine, allEntities);
      return;
    }

    // Even if a target is already assigned, we must check that it exists
    // and is still eatable
    target = getEntityById(allEntities, targets[mine.id]);
    if(!target || !isEatable(mine, target)) {
      assignTarget(mine, allEntities);
      return;
    }
  });
};

// Player identifiers range from 0 to 4
var playerId = parseInt(readline());
/**
 * My entity id => its target entity's id
 * This cannot be a simple property of the entities because they're reloaded
 * at each game turn.
 */
var targets = {};

// Main game loop
while (true) {
  // The number of chips under your control
  var playerChipCount = parseInt(readline());
  // The total number of entities on the table, including your chips
  var entityCount = parseInt(readline());

  // ----- Input
  var entities = [];
  for (var i = 0; i < entityCount; i++) {
    var inputs = readline().split(' ');
    var entity = {
      // Unique identifier for this entity
      id: parseInt(inputs[0]),
      // The owner of this entity (-1 for neutral droplets)
      owner: parseInt(inputs[1]),
      // The current radius of this entity
      radius: parseFloat(inputs[2]),

      // Position (x from 0 to 799, y from 0 to 514)
      x: parseFloat(inputs[3]),
      y: parseFloat(inputs[4]),
      // Speed
      vx: parseFloat(inputs[5]),
      vy: parseFloat(inputs[6]),
    };
    entities.push(entity);
  }

  // ----- Game logic
  var myEntities = getMyEntities(entities);
  assignTargets(myEntities, entities);

  myEntities.forEach(function(mine) {
    // One instruction per chip: 2 real numbers (x y) for a propulsion, or 'WAIT' to stay still
    // You can append a message to your line, it will get displayed over the entity

    var predator = isEndangered(mine, entities);
    if(predator) {
      debug(mine.id, 'is in DANGER because of', predator.id);
      var escape = chooseEscapeDestination(mine, predator);
      print(escape.x, escape.y, 'FLY YOU FOOLS');
      return;
    }

    var target = getEntityById(entities, targets[mine.id]);
    if(target && canMove(mine)) {
      // TODO: move only if we're no longer on course and it's not too costly
      // TODO: fleeing: estimate the ETA to dangereous entities assuming no change in my trajectory, flee if the ETA is too small
      var eta = estimateEta(mine, target);
      debug('Moving', mine.id, 'to', target.id, 'will take', eta, 'rounds.');
      var estimatedPosition = estimatePosition(target, Math.min(eta, MAX_PREDICTION_HORIZON));

      // ----- Output
      print(estimatedPosition.x, estimatedPosition.y, target.id);
    }
    else {
      print('WAIT');
    }
  });
}