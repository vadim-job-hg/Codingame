/**
Codingame kutulu
https://github.com/TidyMaze/code_of_kutulu/blob/master/main.go
*/

package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"math"
	"os"
	"sort"
)

// 1.0 => 6
// 1.1 => 70
const FactDistExplorers = 0.9

// TraversableDist how far we search available cells
// 3 => 168
// 4 => 63
const TraversableDist = 7

// RangeWanderers guard
// 5 => 191
// 6 => 58
// 7  => 14
const RangeWanderers = 7

// RangeSlashers guard
// 5 => 117
// 6 => 14
// 7 => 87
const RangeSlashers = 6

// RangeSpawnings guard
// 6 => 178
// 7 => 150
// 8 => 175
const RangeSpawnings = 7

// MinSanityYell below : allow yell
// 200 => 150
// 220 => 135
// 240 => 170
const MinSanityYell = 220

// LightDistance below : allow light
// 10 => 39
// 12 => 34
// 14 => 29
const LightDistance = 16

// 190 => 63
const RequiredHealMe = 190

// 215 => 126
// 225 => 60
// 236 => 63
const RequiredHealOther = 225

// 180 => 5
const PlanForceUse = 180

type grid [][]cell
type cell int

const (
	inputWall    = "#"
	inputSpawn   = "w"
	inputShelter = "U"
	inputEmpty   = "."
)

const (
	cellWall    = iota
	cellSpawn   = iota
	cellShelter = iota
	cellEmpty   = iota
)

type coord struct {
	x, y int
}

type minionState int

const (
	stateSpawning  minionState = 0
	stateWandering minionState = 1
	stateStalking  minionState = 2
	stateRushing   minionState = 3
	stateStunned   minionState = 4
)

type explorer struct {
	id              int
	coord           coord
	sanity          int
	plansRemaining  int
	lightsRemaining int
}

type minion interface {
	getCoord() coord
}

type wanderer struct {
	id         int
	coord      coord
	state      minionState
	target     int
	recallTime int
}

type slasher struct {
	id              int
	coord           coord
	state           minionState
	target          int
	changeStateTime int
}

type spawningMinion struct {
	id        int
	coord     coord
	state     minionState
	target    int
	spawnTime int
}

type yell struct {
	by, on int
}

type light struct {
	by int
}

type plan struct {
	by int
}

func (w wanderer) getCoord() coord {
	return w.coord
}

func (s slasher) getCoord() coord {
	return s.coord
}

func (s spawningMinion) getCoord() coord {
	return s.coord
}

type loggable interface {
	String() string
}

const (
	entityTypeExplorer      = "EXPLORER"
	entityTypeWanderer      = "WANDERER"
	entityTypeEffectPlan    = "EFFECT_PLAN"
	entityTypeEffectLight   = "EFFECT_LIGHT"
	entityTypeSlasher       = "SLASHER"
	entityTypeEffectShelter = "EFFECT_SHELTER"
	entityTypeEffectYell    = "EFFECT_YELL"
)

func buildGridOfWalls(width int, height int) grid {
	res := make(grid, height)
	for i := 0; i < height; i++ {
		res[i] = make([]cell, width)
	}
	return res
}

func printGrid(g grid) {
	res := ""
	for _, line := range g {
		for _, cell := range line {
			res += cellToString(cell)
		}
		res += "\n"
	}
	log(res)
}

func log(mes ...interface{}) {
	fmt.Fprintln(os.Stderr, mes...)
}

func cellToString(c cell) string {
	switch c {
	case cellWall:
		return "#"
	case cellSpawn:
		return "w"
	case cellShelter:
		return "U"
	case cellEmpty:
		return "."
	default:
		panic("unrecognized cell " + string(c))
	}
}

func parseCell(c string) cell {
	switch c {
	case inputWall:
		return cellWall
	case inputSpawn:
		return cellSpawn
	case inputShelter:
		return cellShelter
	case inputEmpty:
		return cellEmpty
	default:
		panic("unrecognized string " + c)
	}
}

func parseGrid(scanner *bufio.Scanner, width int, height int) grid {
	res := buildGridOfWalls(width, height)
	for i := 0; i < height; i++ {
		scanner.Scan()
		line := scanner.Text()
		for j, c := range line {
			res[i][j] = parseCell(string(c))
		}
	}
	return res
}

func send(command string) {
	fmt.Println(command)
}

func sendMove(x, y int, message string) {
	send(fmt.Sprintf("MOVE %d %d %s", x, y, message))
}

func sendWait(message string) {
	send(fmt.Sprintf("WAIT %s", message))
}

func sendPlan(message string) {
	send(fmt.Sprintf("PLAN %s", message))
}

func sendLight(message string) {
	send(fmt.Sprintf("LIGHT %s", message))
}

func sendYell(message string) {
	send(fmt.Sprintf("YELL %s", message))
}

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func manhattanDist(from coord, to coord) int {
	return abs(to.x-from.x) + abs(to.y-from.y)
}

func getEmptyCells(g grid) []coord {
	res := make([]coord, 0)
	for i, line := range g {
		for j, cell := range line {
			if cell == cellEmpty {
				res = append(res, coord{j, i})
			}
		}
	}
	return res
}

func minionInCoord(minions []minion, coord coord) bool {
	for _, m := range minions {
		if m.getCoord() == coord {
			return true
		}
	}
	return false
}

func getCloseTraversableCells(g grid, from coord, distFromMe map[coord]int, minions []minion) []coord {
	res := make([]coord, 0)
	for i, line := range g {
		for j, cell := range line {
			c := coord{j, i}
			d, prs := distFromMe[c]
			if (isTraversable(cell)) && prs && d <= TraversableDist && !minionInCoord(minions, c) {
				res = append(res, c)
			}
		}
	}

	if len(res) == 0 {
		log("WOOPS NOTHING")
		for i, line := range g {
			for j, cell := range line {
				c := coord{j, i}
				d, prs := distFromMe[c]
				if (isTraversable(cell)) && prs && d <= TraversableDist {
					res = append(res, c)
				}
			}
		}
	}

	return res
}

func getFarestCoord(g grid, minions []minion, explorers []explorer, myExplorer explorer, candidates []coord) coord {
	if len(candidates) == 0 {
		panic("no candidates for farest coord")
	}
	bestIndex := -1
	bestDistance := -1.0
	for i, c := range candidates {

		dist, _ := dijkstraRaw(g, c)

		sum := 0.0
		count := 0
		for _, m := range minions {
			thisDist, prs := dist[m.getCoord()]
			if prs {
				checkDst(thisDist)
				sum += float64(thisDist)
				count++
			}
		}

		score := sum / float64(count)

		sumEx := 0.0
		countEx := 0
		for _, e := range explorers {
			thisDist, prs := dist[e.coord]
			if prs && e.id != myExplorer.id {
				checkDst(thisDist)
				sumEx += float64(thisDist)
				countEx++
			}
		}

		scoreEx := sumEx / float64(countEx)

		scoreTot := score - FactDistExplorers*scoreEx

		if bestDistance == -1 || scoreTot > bestDistance {
			bestIndex = i
			bestDistance = scoreTot
			log("Farest : ", candidates[bestIndex], " with distance ", bestDistance)
		}
	}
	return candidates[bestIndex]
}

func getAwayFromMinions(g grid, me explorer, minions []minion, explorers []explorer, distFromMe map[coord]int, prevFromMe map[coord]coord, distFromMeRaw map[coord]int, prevFromMeRaw map[coord]coord) coord {
	empties := getCloseTraversableCells(g, me.coord, distFromMe, minions)
	log(fmt.Sprintf("empties: %v", empties))
	return getFarestCoord(g, minions, explorers, me, empties)
}

func getBestExplorer(me explorer, explorers []explorer) coord {
	bestIndex := -1
	bestScore := -1
	for i, e := range explorers {
		if e.id != me.id && (bestScore == -1 || e.sanity > bestScore) {
			bestIndex = i
			bestScore = e.sanity
		}
	}
	return explorers[bestIndex].coord
}

type Scored struct {
	item  minion
	score int
}

type ByDist []Scored

func (a ByDist) Len() int           { return len(a) }
func (a ByDist) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByDist) Less(i, j int) bool { return a[i].score < a[j].score }

func getFrighteningMinions(me explorer, wanderers []wanderer, slashers []slasher, spawningMinions []spawningMinion, distFromMe map[coord]int) []minion {
	MaxTake := 3

	minions := make([]minion, 0)
	allScored := make([]Scored, 0)

	for _, w := range wanderers {
		if d, p := distFromMe[w.coord]; p {
			new := Scored{w, d}
			allScored = append(allScored, new)
		}
	}

	for _, s := range slashers {
		if d, p := distFromMe[s.coord]; p {
			new := Scored{s, d}
			allScored = append(allScored, new)
		}
	}

	// for _, s := range spawningMinions {
	// 	if d, p := distFromMe[s.coord]; p && d <= RangeSpawnings {
	// 		minions = append(minions, s)
	// 	}
	// }

	sort.Sort(ByDist(allScored))
	log(fmt.Sprintf("all scored: %v", allScored))

	for _, m := range allScored {
		if len(minions) < MaxTake {
			minions = append(minions, m.item)
		}
	}

	return minions
}

// Item : heap item
type Item struct {
	value    interface{}
	priority int
	index    int
}

// A PriorityQueue implements heap.Interface and holds Items.
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// We want Pop to give us the highest, not lowest, priority so we use greater than here.
	return pq[i].priority < pq[j].priority
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

// Push add item to heap
func (pq *PriorityQueue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*Item)
	item.index = n
	*pq = append(*pq, item)
}

// Pop get first item by priority
func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	item.index = -1 // for safety
	*pq = old[0 : n-1]
	return item
}

func (pq *PriorityQueue) update(value coord, priority int) {
	for _, item := range *pq {
		if item.value == value {
			item.priority = priority
			heap.Fix(pq, item.index)
			return
		}
	}
}

func logQueue(pq PriorityQueue) {
	for i, item := range pq {
		if i >= 5 {
			return
		}
		log(fmt.Sprintf("%.2d:%v", item.priority, item.value.(coord)))
	}
}

func isTraversable(cell cell) bool {
	return cell == cellEmpty || cell == cellSpawn || cell == cellShelter
}

func getTraversableCells(grid grid) []coord {
	coords := make([]coord, 0)
	for i, line := range grid {
		for j, cell := range line {
			if isTraversable(cell) {
				coords = append(coords, coord{j, i})
			}
		}
	}
	return coords
}

func neighbors(grid grid, from coord) []coord {
	offsets := [4]coord{
		{0, -1},
		{0, 1},
		{-1, 0},
		{1, 0},
	}

	res := make([]coord, 4)
	for _, o := range offsets {
		targetCoord := coord{from.x + o.x, from.y + o.y}

		if insideGrid(grid, targetCoord) && isTraversable(grid.getCell(targetCoord)) {
			res = append(res, targetCoord)
		}
	}
	return res
}

func insideGrid(g grid, c coord) bool {
	return c.x >= 0 && c.x < len(g[0]) && c.y >= 0 && c.y < len(g)
}

func (g grid) getCell(at coord) cell {
	if !insideGrid(g, at) {
		panic(fmt.Sprintf("Coord %v outside grid", at))
	}
	return g[at.y][at.x]
}

func checkDst(d int) {
	if d < 0 || d > 1000 {
		panic(fmt.Sprintf("distance was %d", d))
	}
}

func dijkstra(grid grid, source coord, wanderers []wanderer) (map[coord]int, map[coord]coord) {
	dist := make(map[coord]int)
	dist[source] = 0
	prev := make(map[coord]coord)
	q := make(PriorityQueue, 0)
	heap.Init(&q)
	for _, v := range getTraversableCells(grid) {
		dv, prsDv := dist[v]
		checkDst(dv)
		priority := math.MaxInt64
		if prsDv {
			priority = dv
		}
		heap.Push(&q, &Item{
			value:    v,
			priority: priority,
		})
	}
	for len(q) > 0 {
		u := heap.Pop(&q).(*Item).value.(coord)
		for _, v := range neighbors(grid, u) {
			dU, prsU := dist[u]
			if prsU {
				countWanderers := 0
				for _, w := range wanderers {
					if w.coord == v {
						countWanderers++
					}
				}

				alt := dU + 1
				checkDst(alt)
				dV, prsV := dist[v]
				if countWanderers == 0 && (!prsV || alt < dV) {
					dist[v] = alt
					prev[v] = u
					q.update(v, alt)
				}
			}
		}
	}
	return dist, prev
}

func dijkstraRaw(grid grid, source coord) (map[coord]int, map[coord]coord) {
	dist := make(map[coord]int)
	dist[source] = 0
	prev := make(map[coord]coord)
	q := make(PriorityQueue, 0)
	heap.Init(&q)
	for _, v := range getTraversableCells(grid) {
		dv, prsDv := dist[v]
		checkDst(dv)
		priority := math.MaxInt64
		if prsDv {
			priority = dv
		}
		heap.Push(&q, &Item{
			value:    v,
			priority: priority,
		})
	}
	for len(q) > 0 {
		u := heap.Pop(&q).(*Item).value.(coord)
		for _, v := range neighbors(grid, u) {
			dU, prsU := dist[u]
			if prsU {
				alt := dU + 1
				checkDst(alt)
				dV, prsV := dist[v]
				if !prsV || alt < dV {
					dist[v] = alt
					prev[v] = u
					q.update(v, alt)
				}
			}
		}
	}
	return dist, prev
}

func canUseLight(explorer explorer, onGoingYell bool, onGoingPlan bool, onGoingLight bool) bool {
	return explorer.lightsRemaining > 0 && !onGoingYell && !onGoingPlan && !onGoingLight
}
func canUsePlan(explorer explorer, onGoingYell bool, onGoingPlan bool, onGoingLight bool) bool {
	return explorer.plansRemaining > 0 && !onGoingYell && !onGoingPlan && !onGoingLight
}
func canUseYell(onGoingYell bool, onGoingPlan bool, onGoingLight bool) bool {
	return !onGoingYell && !onGoingPlan && !onGoingLight
}

func existsLightTarget(distFromMe map[coord]int, wanderers []wanderer) bool {
	for _, w := range wanderers {
		if d, prs := distFromMe[w.coord]; prs && d <= LightDistance {
			return true
		}
	}
	return false
}

func wanderersVeryClose(distFromMe map[coord]int, wanderers []wanderer) bool {
	for _, w := range wanderers {
		if d, prs := distFromMe[w.coord]; prs && d <= 2 {
			return true
		}
	}
	return false
}

func existsOtherExplorersToHeal(myExplorer explorer, distFromMe map[coord]int, explorers []explorer) bool {
	if myExplorer.sanity > RequiredHealMe {
		return false
	}
	for _, e := range explorers {
		if d, prs := distFromMe[e.coord]; e.id != myExplorer.id && prs && d <= 2 && e.sanity <= RequiredHealOther {
			return true
		}
	}
	return false
}

var yelled = make([]int, 0)

func alreadyYelled(explorer explorer) bool {
	return contains(yelled, explorer.id)
}

func contains(s []int, e int) bool {
	for _, a := range s {
		if a == e {
			return true
		}
	}
	return false
}

func existsOtherExplorersInRangeYell(myExplorer explorer, distFromMe map[coord]int, explorers []explorer) bool {
	for _, e := range explorers {
		if d, prs := distFromMe[e.coord]; e.id != myExplorer.id && prs && d <= 1 && !alreadyYelled(e) && e.sanity < MinSanityYell {
			return true
		}
	}
	return false
}

func main() {

	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 1000000), 1000000)

	var width int
	scanner.Scan()
	fmt.Sscan(scanner.Text(), &width)

	var height int
	scanner.Scan()
	fmt.Sscan(scanner.Text(), &height)

	currentGrid := parseGrid(scanner, width, height)
	printGrid(currentGrid)

	var sanityLossLonely, sanityLossGroup, wandererSpawnTime, wandererLifeTime int
	scanner.Scan()
	fmt.Sscan(scanner.Text(), &sanityLossLonely, &sanityLossGroup, &wandererSpawnTime, &wandererLifeTime)

	for {
		var entityCount int
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &entityCount)

		explorers := make([]explorer, 0)
		wanderers := make([]wanderer, 0)
		slashers := make([]slasher, 0)
		spawningMinions := make([]spawningMinion, 0)
		yells := make([]yell, 0)
		lights := make([]light, 0)
		plans := make([]plan, 0)

		for i := 0; i < entityCount; i++ {
			var entityType string
			var id, x, y, param0, param1, param2 int
			scanner.Scan()
			fmt.Sscan(scanner.Text(), &entityType, &id, &x, &y, &param0, &param1, &param2)

			switch entityType {
			case entityTypeExplorer:
				explorers = append(explorers, explorer{id, coord{x, y}, param0, param1, param2})
			case entityTypeWanderer:
				state := minionState(param1)
				switch state {
				case stateSpawning:
					spawningMinions = append(spawningMinions, spawningMinion{id, coord{x, y}, stateSpawning, param2, param0})
				case stateWandering:
					wanderers = append(wanderers, wanderer{id, coord{x, y}, stateWandering, param2, param0})
				default:
					panic("unrecognized state " + string(state))
				}
			case entityTypeEffectPlan:
				plans = append(plans, plan{param1})
			case entityTypeEffectLight:
				lights = append(lights, light{param1})
			case entityTypeSlasher:
				state := minionState(param1)
				switch state {
				case stateSpawning:
					spawningMinions = append(spawningMinions, spawningMinion{id, coord{x, y}, stateSpawning, param2, param0})
				case stateWandering:
					fallthrough
				case stateStalking:
					fallthrough
				case stateRushing:
					fallthrough
				case stateStunned:
					slashers = append(slashers, slasher{id, coord{x, y}, state, param2, param0})
				default:
					panic("unrecognized state " + string(state))
				}
			case entityTypeEffectShelter:
			case entityTypeEffectYell:
				yells = append(yells, yell{param1, param2})
			default:
				panic("unrecognized entityType " + string(entityType))
			}
		}

		log(fmt.Sprintf("explorers %v", explorers))
		log(fmt.Sprintf("wanderers %v", wanderers))
		log(fmt.Sprintf("spawning %v", spawningMinions))
		log(fmt.Sprintf("slashers %v", slashers))

		myExplorer := explorers[0]

		log(fmt.Sprintf("Me: %v", myExplorer))

		// update yelled
		for _, y := range yells {
			if y.by == myExplorer.id && !contains(yelled, y.on) {
				yelled = append(yelled, y.on)
			}
		}

		onGoingYell := false
		for _, e := range yells {
			if e.by == myExplorer.id {
				onGoingYell = true
			}
		}

		onGoingLight := false
		for _, e := range lights {
			if e.by == myExplorer.id {
				onGoingLight = true
			}
		}
		onGoingPlan := false
		for _, e := range plans {
			if e.by == myExplorer.id {
				onGoingPlan = true
			}
		}

		distFromMe, prevFromMe := dijkstra(currentGrid, myExplorer.coord, wanderers)
		distFromMeRaw, prevFromMeRaw := dijkstraRaw(currentGrid, myExplorer.coord)
		// log("distances: ", distFromMe)
		// log("previous: ", prevFromMe)
		//
		// log("distances raw: ", distFromMeRaw)
		// log("previous raw: ", prevFromMeRaw)

		if canUseLight(myExplorer, onGoingYell, onGoingPlan, onGoingLight) && !wanderersVeryClose(distFromMeRaw, wanderers) && existsLightTarget(distFromMeRaw, wanderers) {
			sendLight("LIGTH IT BABY!")
		} else if canUsePlan(myExplorer, onGoingYell, onGoingPlan, onGoingLight) && !wanderersVeryClose(distFromMeRaw, wanderers) && (existsOtherExplorersToHeal(myExplorer, distFromMeRaw, explorers) || myExplorer.sanity < PlanForceUse) {
			sendPlan("PLAN IT BABY!")
		} else if canUseYell(onGoingYell, onGoingPlan, onGoingLight) && !wanderersVeryClose(distFromMeRaw, wanderers) && existsOtherExplorersInRangeYell(myExplorer, distFromMeRaw, explorers) {
			sendYell("YELL IT BABY!")
		} else {
			frighteningMinions := getFrighteningMinions(myExplorer, wanderers, slashers, spawningMinions, distFromMeRaw)
			if len(frighteningMinions) > 0 {
				log(fmt.Sprintf("Danger: %v", frighteningMinions))
				awayMinionCoord := getAwayFromMinions(currentGrid, myExplorer, frighteningMinions, explorers, distFromMe, prevFromMe, distFromMeRaw, prevFromMeRaw)

				log(fmt.Sprintf("target is %v", awayMinionCoord))

				firstOne := awayMinionCoord

				path := make([]coord, 0)

				prev, isPrev := prevFromMe[awayMinionCoord]
				for currentStep := awayMinionCoord; isPrev && prev != myExplorer.coord; {
					path = append(path, currentStep)
					firstOne = currentStep
					prev, isPrev = prevFromMe[currentStep]
					currentStep = prev
				}

				log(fmt.Sprintf("Path (from last to first): %v", path))

				nextMove := firstOne
				log(fmt.Sprintf("immediate move: %v", nextMove))
				sendMove(nextMove.x, nextMove.y, "Avoiding minion")
			} else if len(explorers) > 1 {
				best := getBestExplorer(myExplorer, explorers)
				sendMove(best.x, best.y, "Following leader")
			} else {
				sendWait("Nothing to do")
			}
		}
		// if myExplorer.sanity <= 30 && myExplorer.lightsRemaining > 0 {
		// 	panic(fmt.Sprintf("Still have so much lights! (%d)", myExplorer.lightsRemaining))
		// }
		// if myExplorer.sanity <= 30 && myExplorer.plansRemaining > 0 {
		// 	panic(fmt.Sprintf("Still have so much plans! (%d)", myExplorer.plansRemaining))
		// }
	}
}