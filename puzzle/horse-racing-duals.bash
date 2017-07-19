# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
read N
var_pi=()
for (( i=0; i<N; i++ )); do
    read Pi
    var_pi+=(Pi)
done
sorted=($(printf '%s\n' "${var_pi[@]}"|sort))
min =10000000
var_abs = 0
# Write an action using echo
# To debug: echo "Debug messages..." >&2
for (( i=0; i<N; i++ )); do
    var_abs = sorted[i]
done
echo "answer"