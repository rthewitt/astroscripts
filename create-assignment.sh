#!/bin/bash

# This script will allow the professor to interactively create an assignment on the fly.
# While the preferred strategy is to have a preconfigured, self-contained course, the
# ability to create an additional or intermediary lesson is crucial.  Note that a maven
# archetype will likely be created to facilitate this, which may or may not use core
# dependencies.

[ "$#" -lt 1 ] && echo "Lab number must be provided." && exit 1

source $( dirname $0 )/setenv-client.sh

PROTOTYPE=PROTOTYPE

cd $PROTOTYPE

buildMavenLesson $1
