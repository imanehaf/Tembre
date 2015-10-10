#!/bin/sh

di="results"
root="/home/imanies/extPkgs/testExe/Tembre"
./../../zsim/build/opt/zsim modif.cfg
cd $di
mkdir $2
cd $2
mkdir $1
mv ../../zsim-ev.h5 $1/$1.h5
cp ../../modif.cfg $1/$1.cfg
cd $root
rm *.h5 modif.cfg 
