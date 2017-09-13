<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
$string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ?";
fscanf(STDIN, "%d",
    $L
);
fscanf(STDIN, "%d",
    $H
);
$T = stream_get_line(STDIN, 256 + 1, "\n");
$ROW = [];
for ($i = 0; $i < $H; $i++)
{
    $ROW[] = stream_get_line(STDIN, 1024 + 1, "\n");
}
for($i=0; $i<$H; $i++){
    $word = "";
    foreach(str_split($T) as $let){
        $index = strpos( $string, strtoupper($let));
        if($index===false){
            $index = strpos($string, strtoupper("?"));
        }
        $word .= substr($ROW[$i], ($index) * $L, $L);
    }
    echo $word.PHP_EOL;
}