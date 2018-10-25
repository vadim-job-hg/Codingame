<?php
define('MAX_VALUE', 10000000);
$N = (int)fgets(STDIN);
$pi = [];
for ($i = 0; $i < $N; $i++) $pi[] =(int)fgets(STDIN);
sort($pi); $min = MAX_VALUE;
for($i=0;$i<$N-1;$i++) if ($min>$pi[$i+1]-$pi[$i]) $min = $pi[$i+1]-$pi[$i];
echo($min);
?>