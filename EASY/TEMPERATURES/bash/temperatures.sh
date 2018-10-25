read n # n: the number of temperatures to analyse
read -a temps # temps: the n temperatures expressed as integers ranging from -273 to 5526

if [ $n == 0 ]
then
    echo 0
else
    tempsLength=${#temps[@]}
    closest=${temps[0]}
    pos=0

    if [[ $closest -lt 0 ]]
    then
        closest=$(( 0 - $closest ))
    fi

    for (( i=0;i<$tempsLength;i++))
    do
        tempInt=${temps[${i}]}
        if [ $tempInt -lt 0 ]
        then
            tempInt=$(( 0 - $tempInt ))
        fi

        if [ $tempInt -lt $closest ] # && [ $tempInt -ge 0 ]
        then
            closest=$tempInt
            pos=$i
        elif [ $tempInt -eq $closest ] && [ ${temps[${i}]} -ge 0 ]
        then
            closest=$tempInt
            pos=$i
        fi
    done

    echo ${temps[${pos}]}
fi