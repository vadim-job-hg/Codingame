# https://www.codingame.com/ide/puzzle/the-bridge-episode-2
# https://github.com/e1r0nd/codingame/blob/097966d46d6857eedb19bb9e2592f4d600b99703/(hard)%20The%20Bridge.js
/**
 * The Bridge
 * https://www.codingame.com/training/hard/the-bridge-episode-2
 * Statement:
 * The goal of the puzzle is to drive a group of motorbikes along a road,
 * avoiding holes and regulating your speed. This puzzle requires to predict
 * all the situations the motorbikes can perform along the time and chose
 * the most optimized choice.
 * Story:
 * Take the control of the resistance against the machines. You have
 * injected a virus in a Moto-Terminator and you have to send it onto a
 * platform to capture it.
 */
// M - the amount of motorbikes to control
// V -  the minimum amount of motorbikes that must survive
const [M, V] = [+readline(), +readline()];
const roads = Array(4).fill().map(_ => readline().split``.map(c => c === '.'));
const roadLength = roads[0].length;
const copy = (bikes) => bikes.map(b => ({x: b.x, y: b.y, speed: b.speed}));

const findPath = (original, V) => {
    const results = [];
    const applyMove = (bikes, move) => bikes.map(bike => {
        const next = bike.x + bike.speed;
        let nextLane = bike.y;
        let checked = roads[bike.y].slice(bike.x, next);

        if (move === 'UP' || move === 'DOWN') {
            if (move === 'UP' && bike.y === 0 || move === 'DOWN' && bike.y === 3) {
                checked = [];
                bikes = [];
            } else {
                nextLane = bike.y + (move === 'UP' ? -1 : 1);
                checked.push(...roads[nextLane].slice(bike.x, next));
            }
        }
        if (checked.some(x => !x) && move !== 'JUMP' || next < roadLength && !roads[nextLane][next]) {
            return null;
        }
        [bike.x, bike.y] = [next, nextLane];

        return bike;
    }).filter(b => b);

    for (let move of ['SPEED', 'WAIT', 'JUMP', 'DOWN', 'UP', 'SLOW']) {
        let bikes = copy(original);

        if (move === 'SPEED') {
            bikes.forEach(b => b.speed++);
        } else if (move === 'SLOW') {
            bikes.forEach(b => b.speed--);
            if (bikes[0].speed === 0) {
                bikes = [];
            }
        }

        bikes = applyMove(bikes, move);
        bikes.length >= V && results.push({move: move, bikes: bikes});
    }

    return results;
};

const backtrack = (bikes, V) => {
    const [stack, moves] = [[bikes], []];

    while(stack.length) {
        bikes = stack[0];
        !bikes.next && (bikes.next = findPath(bikes, V), bikes.id = 0);

        if (bikes[0].x >= roadLength) {
          return moves.reverse();
        }

        if (bikes.id < bikes.next.length) {
            let next = bikes.next[bikes.id++];
            stack.unshift(next.bikes);
            moves.unshift(next.move);
        } else {
            stack.shift();
            moves.shift();
        }
    }
    return null;
};

let move = null;

// game loop
while (true) {
    const [speed, bikes] = [+readline(), []];

    for (let i = 0; i < M; i++) {
        let [x, y, active] = readline().split` `.map(n => +n);
        active && bikes.push({x, y, speed});
    }

    for (let expected = bikes.length; !move && expected >= V; expected--) {
        move = backtrack(copy(bikes), expected);
    }

    print(move.shift() || 'WAIT');
}