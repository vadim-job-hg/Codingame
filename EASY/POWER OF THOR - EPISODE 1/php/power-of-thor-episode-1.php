<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 * ---
 * Hint: You can use the debug stream to print initialTX and initialTY, if Thor seems not follow your orders.
 **/

fscanf(STDIN, "%d %d %d %d",
    $lightX, // the X position of the light of power
    $lightY, // the Y position of the light of power
    $initialTX, // Thor's starting X position
    $initialTY // Thor's starting Y position
);
while (TRUE)
{
    fscanf(STDIN, "%d", $remainingTurns);
    $move_string = "";
    // Write an action using echo(). DON'T FORGET THE TRAILING \n
    // To debug (equivalent to var_dump): error_log(var_export($var, true));
    if($initialTY<$lightY){
        $move_string = "S";
        $initialTY++;
    }
    elseif ($initialTY>$lightY){
        $move_string = "N";
        $initialTY--;
    }
    if ($initialTX<$lightX){
        $move_string .= "E";
        $initialTX++;
    }
    elseif ($initialTX>$lightX){
        $move_string .= "W";
        $initialTX--;
    }
    echo($move_string."\n");
}
?>