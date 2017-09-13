<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

fscanf(STDIN, "%d",
    $n
);
$inputs = fgets(STDIN);
$inputs = explode(" ",$inputs);
for ($i = 0; $i < $n; $i++)
{
    $v = intval($inputs[$i]);
}

// Write an action using echo(). DON'T FORGET THE TRAILING \n
// To debug (equivalent to var_dump): error_log(var_export($var, true));

echo("answer\n");