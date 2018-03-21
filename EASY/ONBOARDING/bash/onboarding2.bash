#!/bin/bash

read n
read temp
temps=(${temp// / })

closest=10000
for i in ${temps[@]}; do
    if [ $((${i#-})) -lt $((${closest#-})) ] || [[ $((${i#-})) -eq $((${closest#-})) && $((${closest})) -lt 0 ]]; then
        closest=$i
    fi
done

if [ $((n)) -eq 0 ]; then
    closest=0
fi

echo $closest