<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

fscanf(STDIN, "%d",
    $surfaceN // the number of points used to draw the surface of Mars.
);
$landing_height = 0;
$lastY = 0;
for ($i = 0; $i < $surfaceN; $i++)
{
    fscanf(STDIN, "%d %d",
        $landX, // X coordinate of a surface point. (0 to 6999)
        $landY // Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
    );
    if($lastY==$landY){
        $landing_height = $lastY;
    }
    $lastY = $landY;
}

// game loop
while (TRUE)
{
    fscanf(STDIN, "%d %d %d %d %d %d %d",
        $X,
        $Y,
        $hSpeed, // the horizontal speed (in m/s), can be negative.
        $vSpeed, // the vertical speed (in m/s), can be negative.
        $fuel, // the quantity of remaining fuel in liters.
        $rotate, // the rotation angle in degrees (-90 to 90).
        $power // the thrust power (0 to 4).
    );

    // Write an action using echo(). DON'T FORGET THE TRAILING \n
    // To debug (equivalent to var_dump): error_log(var_export($var, true));
    $dist = $Y-$landing_height;
    if ($vSpeed<-35)
        $power = 4;
    else
        $power = 3;
    if($dist>1200 and $v_speed>-45)
        $power = (int)($power*(1-$dist/3000));

    // 2 integers: rotate power. rotate is the desired rotation angle (should be 0 for level 1), power is the desired thrust power (0 to 4).
    echo "0 ".$power."\n";
}
?>