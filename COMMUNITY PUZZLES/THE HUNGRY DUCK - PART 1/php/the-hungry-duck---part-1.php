<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
function get($x= 0, $y = 0){
    GLOBAL $food;
    GLOBAL $W;
    GLOBAL $H;

    $current = $food[$y][$x];
    if($x+1>=$W)
        $right = 0;
    else
        $right = get($x+1, $y);
    if($y+1>=$H)
        $down = 0;
    else
        $down = get($x, $y+1);
    $current+=$down>$right?$down:$right;
    return $current;
}

fscanf(STDIN, "%d %d",
    $W,
    $H
);
$food = [];
for ($i = 0; $i < $H; $i++)
{
    $inputs = fgets(STDIN);
    $inputs = explode(" ",$inputs);
    $food[$i] = [];
    for ($j = 0; $j < $W; $j++)
    {
        $food[$i][$j] = intval($inputs[$j]);
    }
}

// Write an action using echo(). DON'T FORGET THE TRAILING \n
// To debug (equivalent to var_dump): error_log(var_export($var, true));

echo(get()."\n");