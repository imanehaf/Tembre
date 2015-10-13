#!/bin/sh

arch=$1
dist="mainResults/$arch"
mkdir $dist
cp -r results/* $dist
