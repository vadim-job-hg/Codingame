<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
function get_distance($lat_a, $lat_b, $long_a, $long_b){
    $x = ($long_b - $long_a)*cos(($lat_b + $lat_a)/2);
    $y = $lat_b - $lat_a;
    return sqrt($x*$x +$y*$y)*6371;
}

fscanf(STDIN, "%s",
    $lon
);
fscanf(STDIN, "%s",
    $lat
);
fscanf(STDIN, "%d",
    $n
);
$current = [];
$closest = 3.402823e+38;
for ($i = 0; $i < $n; $i++)
{
    $DEFIB_TEMP = explode(';', stream_get_line(STDIN, 256 + 1, "\n"));
    $defib = [
        'id'=>$DEFIB_TEMP[0],
        'name'=>$DEFIB_TEMP[1],
        'address'=>$DEFIB_TEMP[2],
        'phone'=>$DEFIB_TEMP[3],
        'long'=>$DEFIB_TEMP[4],
        'lat'=>$DEFIB_TEMP[5],
    ];
    $distance = get_distance(floatval(str_replace(',', '.', $lat)), floatval(str_replace(',', '.', $defib['lat'])), floatval(str_replace(',', '.', $lon)), floatval(str_replace(',', '.', $defib['long'])));
    if($distance<$closest){
        $current = $defib;
        $closest = $distance;
    }
}

// Write an action using echo(). DON'T FORGET THE TRAILING \n
// To debug (equivalent to var_dump): error_log(var_export($var, true));

echo("{$current['name']}\n");
?>