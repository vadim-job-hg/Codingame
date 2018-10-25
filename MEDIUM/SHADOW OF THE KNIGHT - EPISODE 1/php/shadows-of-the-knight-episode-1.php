<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

fscanf(STDIN, "%d %d",
    $W, // width of the building.
    $H // height of the building.
);
fscanf(STDIN, "%d",
    $N // maximum number of turns before game over.
);
fscanf(STDIN, "%d %d",
    $X0,
    $Y0
);
$minx = $miny  = 0;
$maxx = $W - 1;
$maxy = $H - 1;
// game loop
while (TRUE)
{
    fscanf(STDIN, "%s",
        $bombDir // the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
    );

    if(strpos($bombDir, "U")!==false)
        $maxy = $Y0 - 1;
    elseif (strpos($bombDir, "D")!==false)
        $miny = $Y0 + 1;
    if(strpos($bombDir, "L")!==false)
        $maxx = $X0 - 1;
    elseif (strpos($bombDir, "R")!==false)
        $minx = $X0 + 1;
    $X0 = $minx + ceil(($maxx  - $minx)/2);
    $Y0 = $miny + ceil(($maxy  - $miny)/2);
    # the location of the next window Batman should jump to.
    echo("$X0 $Y0\n");
}