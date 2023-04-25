#!/bin/bash

echo Hello Wordl!

# ./matMul.exe 1024 256

for i in 2048 1024 512 256 128 64 32 16 8 6 4 2
do
    if [ $i != 2048 ] ; then
        k=$(expr $i / 2)
        while [ $k -gt 1 ]
        do
            ./matMul.exe $i $k
            k=$(expr $k / 2)
        done
    fi
done