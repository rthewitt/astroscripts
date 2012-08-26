#!/bin/bash

# To accomodate foreach workaround.
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
BIN_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

function f_yesno() {
   echo -n "$1 (y/n) "
   read ans
   # Consider accepting only yes/no answers
   # using a while loop
   case "$ans" in
      y|Y|yes|YES|Yes) return 0 ;;
      *) return 1 ;;
   esac
}

function pause() {
   read -p "$*"
}

# This function works for both create and add-existing.
function buildMavenLesson() {

   echo "$1" WAS PROVIDED AS THE ARGUMENT

   COURSE_NUMBER=
   STUDENT_NAME=
   STUDENT_NUMBER=

   LAB_NO=$1

   git pull

   . .info

   echo "$1" WAS PROVIDED AS THE ARGUMENT
   echo "C#: $COURSE_NUMBER"
   echo "SNA: $STUDENT_NAME"
   echo "S#: $STUDENT_NUMBER"

   # TODO make this conditional, new / existing / modular / rolling-dependencies
   if [ "$#" -lt 2 ]; then
      echo -n "Please enter the relevant Java class: "
      read CLASS_NAME
   else
      echo "USING ARGUMENT $2 as Class Name"
      CLASS_NAME="$2"
   fi

   # Centralize, once concrete
   mvn archetype:generate -B -DarchetypeCatalog=local -DarchetypeGroupId=com.myelin.lessons \
   -DarchetypeArtifactId=student-lesson-nair -DarchetypeVersion=1.0 -DartifactId=lab_$LAB_NO \
   -Djava-class-name=$CLASS_NAME -Dstudent-name=$STUDENT_NAME -Dstudent-number=$STUDENT_NUMBER \
   -Dlab-number=$LAB_NO -Dcourse-number=$COURSE_NUMBER
}
