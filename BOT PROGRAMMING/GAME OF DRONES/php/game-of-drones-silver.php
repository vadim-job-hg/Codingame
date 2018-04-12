<?php
namespace GameOfDrones;
define('DEBUG', true);
function debug() {if (!DEBUG) return; foreach (func_get_args() as $sArgDebug) error_log(var_export($sArgDebug, true));}
/**
 * Class GameSet
 * Represent all components of the current game. Players, Zones and Drones are defined also are the size of the map.
 *
 * @package GameOfDrones
 * @author Nicolas (niconoe) Giraud <nicolas.giraud.dev@gmail.com>
 * @copyright Copyright © 2015, Nicolas Giraud
 */
class GameSet
{
    const SET_WIDTH = 4000;
    const SET_HEIGHT = 1800;
    //Pythagoras' formula on max width and max height to find the longest distance, to ceil (=√(4000*4000 + 1800*1800))
    const SET_MAX_DISTANCE = 4387;
    /**
     * @var Player[]
     */
    public static $aPlayers;
    /**
     * @var int Number of players in the game (2 to 4 players)
     */
    public static $nbPlayers;
    /**
     * @var Zone[]
     */
    public static $aZones;
    /**
     * @var int Number of zones on the map (4 to 8)
     */
    public static $nbZones;
    /**
     * @var int Number of drones in each team (3 to 11)
     */
    public static $nbDrones;
    /**
     * @var int ID of your player (0, 1, 2, or 3)
     */
    public static $idMe;
    /**
     * @var Coordinate[] Array of all coordinates that are goals to reach (points on the circle in a zone)
     */
    public static $aGoalsPoints;
    public static function initialization()
    {
        fscanf(STDIN, '%d %d %d %d', self::$nbPlayers, self::$idMe, self::$nbDrones, self::$nbZones);
        self::initPlayers();
        self::initZones();
    }
    public static function initPlayers()
    {
        for ($i=0; $i<self::$nbPlayers; ++$i) {
            self::$aPlayers[$i] = new Player();
        }
    }
    public static function initZones()
    {
        for ($i=0; $i<self::$nbZones; ++$i) {
            list($x, $y) = explode(' ', trim(fgets(STDIN)), 2);
            self::$aZones[$i] = new Zone($x, $y);
            self::$aZones[$i]->setIdZone($i);
        }
        //After they're all init, calculate the closest distances
        for ($i=0; $i<self::$nbZones; ++$i) {
            self::$aZones[$i]->calculateNearestCoordinateZones();
        }
        foreach (self::$aZones as $oZone) {
            foreach ($oZone->aClosestCoordinatesZones as $oCoordinates) {
                self::$aGoalsPoints[] = $oCoordinates;
            }
        }
    }
    public static function prepareRun()
    {
        //The zones are given in the same order as in the initialization.
        for ($i=0; $i<self::$nbZones; ++$i) {
            self::$aZones[$i]->setControllingPlayer(trim(fgets(STDIN)));
        }
        //For each players, write the position of the drones
        for ($i=0; $i<self::$nbPlayers; ++$i) {
            $oPlayer = self::$aPlayers[$i];
            $oPlayer->resetDrones();
            for ($j=0; $j<self::$nbDrones; ++$j) {
                list($x, $y) = explode(' ', trim(fgets(STDIN)), 2);
                $oPlayer->addDrone(new Drone($x, $y));
            }
        }
    }
    public static function playRun()
    {
        $oMe = self::getMe();
        $aMyDrones = $oMe->aDrones;
        ///////// PART 1 //////
        // All this part is for the start. Active this part when exists at least one zone unvisited
        $aZones = [];
        $aOkZones = array_fill(0, self::$nbZones, false);
        $aLockedDrones = [];
        $aDistances = self::_getDronesDistances(self::getMe());
        do {
            //Get the closest drones for each zones
            for ($idZone = 0; $idZone < self::$nbZones; ++$idZone) {
                if (true === $aOkZones[$idZone]) {
                    continue;
                }
                $fMinDistance = self::SET_MAX_DISTANCE;
                foreach ($aDistances[$idZone] as $idZonePoint => $aDroneDistances) {
                    foreach ($aDroneDistances as $idDrone => $fDistance) {
                        if (!empty($aLockedDrones[$idDrone])) {
                            continue;
                        }
                        if ($fDistance < $fMinDistance) {
                            $aZones[$idZone] = [
                                'distance' => $fDistance,
                                'idDrone' => $idDrone,
                                'idZonePoint' => $idZonePoint,
                            ];
                            $fMinDistance = $fDistance;
                        }
                    }
                }
            }
            //Define a destination for each closest drones.
            foreach ($aZones as $idZone => $aInformation) {
                //If the drone is not locked to a destination, add it.
                //or if the drone already have a destination, check if this new destination is near.
                if (
                    empty($aLockedDrones[$aInformation['idDrone']]) ||
                    $aInformation['distance'] < $aLockedDrones[$aInformation['idDrone']]['distance']
                ) {
                    $aLockedDrones[$aInformation['idDrone']] = [
                        'distance' => $aInformation['distance'],
                        'idZone' => $idZone,
                        'idZonePoint' => $aInformation['idZonePoint'],
                    ];
                }
            }
            //For each zone a same drone must access, only keep the closest zone in game. All others have to be
            //calculated again with unused drones.
            foreach ($aLockedDrones as $aLockedDrone) {
                $aOkZones[$aLockedDrone['idZone']] = true;
            }
        } while (count($aLockedDrones) !== self::$nbDrones && count(array_filter($aOkZones)) !== self::$nbZones);
        //If more zones than drones, amount of zones the player will conquer is full and some drones left.
        //Make them reach the closest zone.
        for ($i=0;$i<self::$nbDrones; ++$i) {
            if (isset($aLockedDrones[$i])) {
                continue;
            }
            $fMinDistance = self::SET_MAX_DISTANCE;
            for ($j=0; $j<self::$nbZones; ++$j) {
                $fDistance = $aMyDrones[$i]->getDistance(self::$aZones[$j]);
                if ($fDistance < $fMinDistance) {
                    $fMinDistance = $fDistance;
                    $aLockedDrones[$i] = [
                        'distance' => $fDistance,
                        'idZone' => $j,
                        'idZonePoint' => null,
                    ];
                }
            }
        }
        //If more drones than zones, all drones have destinations zone to reach. Nothing to do more here.
        //Fix the trajectory to focus on the center of the focused zone to get in the fastest as possible.
        foreach ($aLockedDrones as $idDrone => $aDroneInformation) {
            //If distance is smaller than the speed of the drone, go to the idZonePoint to be closer. Otherwise, focus
            //the center of the circle of the zone.
            if ($aDroneInformation['distance'] < Drone::SPEED) {
                $aMyDrones[$idDrone]->moveToZone($aDroneInformation['idZone'], $aDroneInformation['idZonePoint']);
            } else {
                $aMyDrones[$idDrone]->moveToZone($aDroneInformation['idZone']);
            }
        }
        /////// END PART 1 ////
        //TODO Do functions for parts.
        // TODO do analyze on zones
        // - If exists 1 zone that owns to -1 and no drones in : PART 1
        // - If all zones under control or in battle, if still exists zone that -1 owns, maybe try to help.
        // - Try to find the group of minimum amount of zones in the smallest area and focus all drones on them.
        // - The focus must be with drones that do not make lose any zones until all zones on that group are mine.
        //For each drone, echo the coordinates to each drone must go.
        for ($i=0; $i<self::$nbDrones; ++$i) {
            echo $aMyDrones[$i];
        }
    }
    /**
     * Return all distances for each drones of all goal points of each zones, for a given player.
     * @param Player $oPlayer The player who owns the drones to check distances.
     * @return array Distances for each drones of all goal points of each zones.
     */
    private static function _getDronesDistances(Player $oPlayer)
    {
        $aDist = [];
        for ($i=0; $i<self::$nbZones; ++$i) {
            $oZone = self::$aZones[$i];
            $aDist[$i] = [];
            for ($j=0; $j<self::$nbZones; ++$j) {
                //Don't take the distance of the closest point for the same zone (X => X)
                if ($i === $j) {
                    continue;
                }
                $aDist[$i][$j] = [];
                for ($k=0; $k<self::$nbDrones; ++$k) {
                    $aDist[$i][$j][$k] = $oZone->aClosestCoordinatesZones[$j]->getDistance($oPlayer->aDrones[$k]);
                }
            }
        }
        return $aDist;
    }
    /**
     * Return the "human" player
     * @return \GameOfDrones\Player
     */
    public static function getMe()
    {
        return self::$aPlayers[self::$idMe];
    }
}
/**
 * Class Player
 * Define a player with his array of Drones.
 *
 * @package GameOfDrones
 * @author Nicolas (niconoe) Giraud <nicolas.giraud.dev@gmail.com>
 * @copyright Copyright © 2015, Nicolas Giraud
 */
class Player
{
    /**
     * @var Drone[]
     */
    public $aDrones = [];
    /**
     * Reset all drones owning
     * @return $this
     */
    public function resetDrones()
    {
        $this->aDrones = [];
        return $this;
    }
    /**
     * Add a drone to a player.
     * @param \GameOfDrones\Drone $drone
     * @return $this
     */
    public function addDrone(Drone $drone)
    {
        $this->aDrones[] = $drone;
        return $this;
    }
}
/**
 * Class Coordinate
 * Define a coordinate in 2 dimensions. The coordinate is so (X;Y) format. Based on the width of the map, a coordinate
 * also have an index.
 *
 * @package GameOfDrones
 * @author Nicolas (niconoe) Giraud <nicolas.giraud.dev@gmail.com>
 * @copyright Copyright © 2015, Nicolas Giraud
 */
class Coordinate
{
    /**
     * @var int The X component of the coordinate
     */
    public $x;
    /**
     * @var int The Y component of the coordinate
     */
    public $y;
    /**
     * @var int The index of the coordinate, based on the (x;y) coordinate
     */
    public $i;
    /**
     * Define a coordinate and its index.
     * @param $x
     * @param $y
     */
    public function __construct($x, $y)
    {
        $this->x = $x;
        $this->y = $y;
        $this->i = ($y * GameSet::SET_WIDTH) + $x;
    }
    /**
     * Return the coordinate in X Y format.
     * @return string
     */
    public function __toString()
    {
        return $this->x . ' ' . $this->y . "\n";
    }
    /**
     * Return the distance between this point and the given one in parameter
     * @param \GameOfDrones\Coordinate $oGoal The goal to reach. Distance calculated to this point.
     * @return float The distance between the two points.
     */
    public function getDistance(Coordinate $oGoal)
    {
        return sqrt(pow($oGoal->x - $this->x, 2) + pow($oGoal->y - $this->y, 2));
    }
}
/**
 * Class Zone
 * Extends the coordinate so a Zone is a center point on the map with a 100 point radius all around the center.
 * A Zone can also be owned by a player.
 *
 * @package GameOfDrones
 * @author Nicolas (niconoe) Giraud <nicolas.giraud.dev@gmail.com>
 * @copyright Copyright © 2015, Nicolas Giraud
 */
class Zone extends Coordinate
{
    const RADIUS = 100;
    /**
     * @var int ID of the team controlling the zone (0, 1, 2, or 3) or -1 if it is not controlled.
     */
    public $iControllingPlayer = -1;
    /**
     * @var Coordinate[] List of coordinates that are the closest to other zones.
     */
    public $aClosestCoordinatesZones = [];
    /**
     * @var int Id of the current zone
     */
    public $idZone;
    /**
     * Set the id of the team that control the Zone.
     * @param int $idTeam
     * @return $this
     */
    public function setControllingPlayer($idTeam)
    {
        $this->iControllingPlayer = $idTeam;
        return $this;
    }
    /**
     * Set the id of the zone itself.
     * @param int $idZone The ID to set.
     * @return $this
     */
    public function setIdZone($idZone)
    {
        $this->idZone = $idZone;
        return $this;
    }
    /**
     * For each other zone than self, find the point on the circle radius center of self closest to other zone.
     */
    public function calculateNearestCoordinateZones()
    {
        for ($i=0; $i<GameSet::$nbZones; ++$i) {
            if ($this->idZone >= $i) { //Avoid managing already managed zones.
                continue;
            }
            $this->_calculateNearestCoordinateZone(GameSet::$aZones[$i]);
        }
    }
    /**
     * Find the point on the circle radius center of self closest to other zone.
     * @param \GameOfDrones\Zone $oZone
     * @return $this
     */
    protected function _calculateNearestCoordinateZone(Zone $oZone)
    {
        //Here is the formula:
        //Zone 1 is coordinate (XA;YA), Zone 2 is coordinate (XB;YB), r is the radius (self::RADIUS)
        //If XA = XB then
        //  If YA < YB then A'=(XA;YA+r) and B'=(XB;YB-r)
        //  Else A'=(XA;YA-r) and B'=(XB;YB+r)
        //Else
        //  If YA < YB then A'=(XA+r*cos(tan⁻¹(a));YA+r*sin(tan⁻¹(a)) and
        //                  B'=(XB+r*cos(tan⁻¹(a)-PI);YB+r*sin(tan⁻¹(a)-PI)
        //  Else A'=(XA+r*cos(tan⁻¹(a)-PI);YA+r*sin(tan⁻¹(a)-PI) and
        //       B'=(XB+r*cos(tan⁻¹(a);YB+r*sin(tan⁻¹(a))
        // With a, the first coefficient of the equation y=ax+b of the straight passing through both zones.
        if ($this->x === $oZone->x) {
            if ($this->y < $oZone->y) {
                $xA = $this->x;
                $yA = $this->y + self::RADIUS;
                $xB = $oZone->x;
                $yB = $oZone->y - self::RADIUS;
            } else {
                $xA = $this->x;
                $yA = $this->y - self::RADIUS;
                $xB = $oZone->x;
                $yB = $oZone->y + self::RADIUS;
            }
        } else {
            // a = (YA - YB) / (XA - XB) (with XA != XB)
            $a = ($this->y - $oZone->y) / ($this->x - $oZone->x);
            if ($this->y < $oZone->y) {
                if ($a < 0) {
                    $xA = $this->x + self::RADIUS * cos(atan($a) - M_PI);
                    $yA = $this->y + self::RADIUS * sin(atan($a) - M_PI);
                    $xB = $oZone->x + self::RADIUS * cos(atan($a));
                    $yB = $oZone->y + self::RADIUS * sin(atan($a));
                } else {
                    $xA = $this->x + self::RADIUS * cos(atan($a));
                    $yA = $this->y + self::RADIUS * sin(atan($a));
                    $xB = $oZone->x + self::RADIUS * cos(atan($a) - M_PI);
                    $yB = $oZone->y + self::RADIUS * sin(atan($a) - M_PI);
                }
            } else {
                if ($a < 0) {
                    $xA = $this->x + self::RADIUS * cos(atan($a));
                    $yA = $this->y + self::RADIUS * sin(atan($a));
                    $xB = $oZone->x + self::RADIUS * cos(atan($a) - M_PI);
                    $yB = $oZone->y + self::RADIUS * sin(atan($a) - M_PI);
                } else {
                    $xA = $this->x + self::RADIUS * cos(atan($a) - M_PI);
                    $yA = $this->y + self::RADIUS * sin(atan($a) - M_PI);
                    $xB = $oZone->x + self::RADIUS * cos(atan($a));
                    $yB = $oZone->y + self::RADIUS * sin(atan($a));
                }
            }
        }
        //Round to the center of the circle.
        $xA = $this->_roundToCenter($xA, $this->x);
        $yA = $this->_roundToCenter($yA, $this->y);
        $xB = $this->_roundToCenter($xB, $oZone->x);
        $yB = $this->_roundToCenter($yB, $oZone->y);
        $this->aClosestCoordinatesZones[$oZone->idZone] = new Coordinate($xA, $yA);
        $oZone->aClosestCoordinatesZones[$this->idZone] = new Coordinate($xB, $yB);
        return $this;
    }
    /**
     * Use the floor or ceil function to find the coordinate closest to the center of the circle.
     * @param float $fCoordinateFrom One component of the coordinate on the circle
     * @param float $fCoordinateTo The same component but of the coordinate of the center of the circle.
     * @return int The rounded component of the coordinate depending of its position and the center's one.
     */
    private function _roundToCenter($fCoordinateFrom, $fCoordinateTo)
    {
        if ($fCoordinateFrom < $fCoordinateTo) { //Coordinate is too left or too up from center
            return ceil($fCoordinateFrom); //Get next coordinate at right or bottom.
        }
        if ($fCoordinateFrom > $fCoordinateTo) { //Coordinate is too right or too bottom from center
            return floor($fCoordinateFrom); //Get next coordinate at left or up
        }
        //Coordinate are same: Round it
        return round($fCoordinateFrom);
    }
}
/**
 * Class Drone
 * Extends the coordinate so a Drone is on a specific coordinate.
 *
 * @package GameOfDrones
 * @author Nicolas (niconoe) Giraud <nicolas.giraud.dev@gmail.com>
 * @copyright Copyright © 2015, Nicolas Giraud
 */
class Drone extends Coordinate
{
    /** The speed of a drone. A drone, for each step, can move to maximum 100 */
    const SPEED = 100;
    /**
     * @var Coordinate Destination to reach
     */
    public $oDestination;
    /**
     * Set the destination the drone have to go
     * @param \GameOfDrones\Coordinate $oDestination
     * @return $this
     */
    public function setDestination(Coordinate $oDestination)
    {
        $this->oDestination = $oDestination;
        return $this;
    }
    /**
     * Use this method to know if the drone has reached its destination.
     * @return bool True if the drone reaches its destination. False otherwise.
     */
    public function isArrived()
    {
        return ($this->i === $this->oDestination->i);
    }
    /**
     * Set the destination to the center of a zone or to a closest point on that zone.
     * @param int $idZone The ID of the zone to move to.
     * @param int|null $idZonePoint The ID of the point on the zone circle to move to.
     * @return $this
     */
    public function moveToZone($idZone, $idZonePoint = null)
    {
        $oZone = GameSet::$aZones[$idZone];
        //If no Zone Point given, set the center of the zone as destination.
        if ($idZonePoint === null) {
            $this->setDestination($oZone);
        } else {
            $this->setDestination($oZone->aClosestCoordinatesZones[$idZonePoint]);
        }
        return $this;
    }
    /**
     * Display the coordinates of the destination to move to this point.
     * @return string
     */
    public function __toString()
    {
        return $this->oDestination->__toString();
    }
}
GameSet::initialization();
while(1) {
    GameSet::prepareRun();
    GameSet::playRun();
}