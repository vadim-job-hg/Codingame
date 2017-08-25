<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
fscanf(STDIN, "%d",
    $N // Number of elements which make up the association table.
);
fscanf(STDIN, "%d",
    $Q // Number Q of file names to be analyzed.
);
$dictionary =[];
for ($i = 0; $i < $N; $i++)
{
    fscanf(STDIN, "%s %s",
        $EXT, // file extension
        $MT // MIME type.
    );
    $dictionary[strtolower($EXT)] = $MT;
}
error_log(var_export($dictionary, true));
for ($i = 0; $i < $Q; $i++)
{
    $FNAME = stream_get_line(STDIN, 500 + 1, "\n"); // One file name per line.
    $farr = explode('.', $FNAME);
    error_log(var_export($FNAME, true));
    if(count($farr)>1){
        $e = strtolower(end($farr));
        if(isset($dictionary[$e])){
            echo("{$dictionary[$e]}\n");
        }
        else echo("UNKNOWN\n");

    } else echo("UNKNOWN\n");
}

// Write an action using echo(). DON'T FORGET THE TRAILING \n
// To debug (equivalent to var_dump): error_log(var_export($var, true));

?>