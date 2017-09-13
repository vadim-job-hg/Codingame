<?php
while (TRUE)
{
    $mountain_max = 0;
    $index_max = 0;
    for ($i = 0; $i < 8; $i++)
    {
        fscanf(STDIN, "%d",
            $mountainH // represents the height of one mountain.
        );
        if ($mountain_max<$mountainH){
            $mountain_max = $mountainH;
            $index_max = $i;
        }
    }
    echo $index_max."\n";
}
?>