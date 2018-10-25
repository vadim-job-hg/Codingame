# from here https://github.com/Peekmo/CodinGame-Bash/blob/master/Horses.sh
read n
declare -a horses
declare -a sorted
lower=10000000; last=-1

for((i=0 ; i<n ; i++)); do
    read horse
    sorted[horse]=1
done

if [[ ${#sorted[@]} -ne n ]]; then lower=0;
else
    for i in ${!sorted[@]}; do
        if [[ $last -ne -1 && $(($i-$last)) -lt $lower ]]; then 
            lower=$(($i-$last)); fi
        last=$i
    done
fi
echo $lower