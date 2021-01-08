#!/bin/bash
PYTHON3=`which python3`
PIP3=`which pip3`
export PYTHON3=$PYTHON3
#echo $PYTHON3
export PIP3=$PIP3
#echo $PIP3

$PYTHON3 $1
