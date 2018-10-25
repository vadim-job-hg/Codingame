<?php
fscanf(STDIN, "%d",
    $n // the number of temperatures to analyse
);
$temps = stream_get_line(STDIN, 256 + 1, "\n"); // the n temperatures expressed as integers ranging from -273 to 5526
if($n !=0){
    $array = explode(' ', $temps);
    $min = (int)$array[0];
    foreach($array as $item){
        $item = (int)$item;
        if (abs($min)>abs($item) or (abs($min)==abs($item) and $item>$min))
            $min = $item;
    }
}
else
    $min = 0;
echo("$min\n");
