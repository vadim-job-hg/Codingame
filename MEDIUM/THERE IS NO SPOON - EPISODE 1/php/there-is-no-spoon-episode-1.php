<?php
/**
 * Don't let the machines win. You are humanity's last hope...
 **/

fscanf(STDIN, "%d",
    $width // the number of cells on the X axis
);
fscanf(STDIN, "%d",
    $height // the number of cells on the Y axis
);
$lines = [];
for ($i = 0; $i < $height; $i++)
{
    $lines[] = stream_get_line(STDIN, 31 + 1, "\n"); // width characters, each either 0 or .
}

for($y=0; $y<$height; $y++){
    for($x=0; $x<$width; $x++){
        if($lines[$y][$x]=="."){
            continue;
        }
        $rx = $ry = $bx = $by = -1;
        for($tx=$x+1; $tx<$width; $tx++){
            if(isset($lines[$y][$tx])&&$lines[$y][$tx]=='0'){
                $rx = $tx;
                $ry = $y;
                break;
            }
        }

        for($ty=$y+1; $ty<$height; $ty++){
            if(isset($lines[$ty][$x])&&$lines[$ty][$x]=='0'){
                $bx = $x;
                $by = $ty;
                break;
            }
        }
        echo "$x $y $rx $ry $bx $by\n";
    }
}
