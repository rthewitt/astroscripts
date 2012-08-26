#!/bin/bash

# This is a temporary workaround, because I'm trying to call a sourced bash function
# from git foreach.  I'll have to figure out how to access internal functions of the
# script, instead of executing external commands.  If not possible, I will simply
# maintain this separation.  The logic is still maintained only once, in setenv-client.sh

[ "$#" -lt 1 ] && echo "Lab number must be provided." && exit 1

source $( dirname $0 )/setenv-client.sh

WORKAROUND_LAB_NO=$1

buildMavenLesson $1 "DemoLesson"
