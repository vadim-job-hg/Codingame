<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

fscanf(STDIN, "%d",
    $R
);
fscanf(STDIN, "%d",
    $L
);
$array = [$R];
for($i=1; $i<$L; $i++){
    $new_array = [];
    $num =   0;
    $last = -1;
    foreach($array as $v){
        if($v !=$last){
            if($num != 0){
                $new_array[] = $num;
                $new_array[] = $last;
            }
            $num = 1;
        }
        else
            $num +=1;
        $last = $v;
    }
    $new_array[] = $num;
    $new_array[] = $last;
    $array = $new_array;
}
echo implode(' ', $array);