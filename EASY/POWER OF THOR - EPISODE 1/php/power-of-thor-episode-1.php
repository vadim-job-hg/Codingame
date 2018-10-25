<?php
fscanf(STDIN, "%d %d %d %d", $lightX, $lightY, $initialTX, $initialTY);
while (TRUE){
    fscanf(STDIN, "%d", $remainingTurns);
    $move_string = "";
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
