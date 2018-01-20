var N = parseInt(readline()); // the number of temperatures to analyse
var TEMPS = readline(); // the N temperatures expressed as integers ranging from -273 to 5526

if (TEMPS) {
    printErr(TEMPS);
    var temperatures = TEMPS.split(' ');
    var minus = -9999;
    var plus = 9999;

    for (i in temperatures) {
        var t = temperatures[i];

        if (t < 0) {
            if (parseInt(minus) < parseInt(t)) minus = t;
        } else {
            if (parseInt(plus) > parseInt(t)) plus = t;
        }
    }

    if (-parseInt(minus) < parseInt(plus)) {
        print(minus);
    } else {
        print(plus);
    }
} else {
    print('0');
}