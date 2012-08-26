#!/bin/bash
# This script will initialize the repository once the super -> submodules have been created.
# It will work whether or not the students have thus far committed, so the script can also
# be used to reinstantiate the professor repository, add a T.A. or review past courses

[ "$#" -lt 1 ] && echo "Course name (*existing) must be provided." && exit 1
COURSE="$1"

# TODO Use a Spring controller within Astrocyte to redirect students/professor to
# demo directory: e.g., /lessons/{login}/{commmand} - The model will determine
# security role of the user.
PUBLIC_PROF="public-prof"
PUBLIC_STUDENT="public-student"

URL="http://localhost/lessons"
#URL="http://www.myelinprice.com/lessons"

git clone $URL/$PUBLIC_PROF/$COURSE.git


# At this point, if you CD into a directory and type 'git status', you get:
# On branch master, nothing to commit.
# This gives the false impression that the submodules have been initialized.
# They have not.  These directories are NOT the .gitmodules entry repos yet.
# The message is inherited by the coures level git repo
cd $COURSE

# Note: This only checks out a revision, a detached HEAD.
git submodule update --init 

# The following is required before tracking comes into play.
git submodule foreach git checkout master


# TODO standardize client like server.  Directories resolved, environment set
exec ../$( dirname $0 )/checkout-student.sh $COURSE PROTOTYPE
