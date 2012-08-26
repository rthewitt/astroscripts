#!/bin/bash

# === This is not complete
# Arguments
# 1. Prototype's file
# 2. Student file

NUM_SECTIONS=3

s_start[0]='--IMPORT-DECLARATION-START--'
s_start[1]='--INSTRUCTIONS-START--'
s_start[2]='--CLASS-BODY-START--'

# TODO Bugfix below, double dash in archetype
s_end[0]='--IMPORT-DECLARATION--END--'
s_end[1]='--INSTRUCTIONS-END--'
s_end[2]='--CLASS-BODY-END--'

PROTO_FILE=$1
STUDENT_FILE=$2

i=0

while [ "$i" -lt $NUM_SECTIONS ]
do
START=${s_start[$i]}
END=${s_end[$i]}

sed -n "
/${START}/,/${END}/ {
/^\/\/.*/ d
p
}" > blurb < $PROTO_FILE

sed '/'"$START"'/ {
	r blurb
	d
}' < $STUDENT_FILE > temp

sed '/'$END'/ d' < temp > $STUDENT_FILE

rm temp
rm blurb

let "i++"
done
