#!/bin/bash
# Merges a specific prototype commit into the student branches in the internal course directory, pushes 
# all branches. Eventual behavior = specific student (self-paced), possibly merge from external prototype

# Revisit getops for --all and -s <student-id>, etc
[ "$#" -lt 2 ] && echo "Course name and commit hash must be provided" && exit 1

#TODO post-receive hook on student repos should force merge on internal working trees
# and send pull requests to professor

#TODO do any necessary testing before merge using fetch.  Consider no-ff for revert compared to reset.

echo "INSIDE BASH SCRIPT"

source $( dirname $0 )/setenv.sh

COURSE="$1"
COMMIT="$2"

problem=false
folder=""
[ -d "$PRIV_DIR" ] || problem=true && folder="$PRIV_DIR"
[ -d "$PUBLIC_DIR" ] || problem=true && folder="$PUBLIC_DIR"
[ -d "$PROF_DIR" ] || problem=true && folder="$PROF_DIR"
[ -d "$PUBLIC_DIR/$COURSE" ] || problem=true && folder="$COURSE in $PUBLIC_DIR"

# TODO read up on process redirection.  logging may not be best practice
if $problem; then fail "folder $folder not found"; fi;


cd $PROF_DIR/$COURSE


# If we don't do this, filtering branch list with grep
# returns all items in the current branch
# MUST UNDERSTAND THIS BEHAVIOR, MAKES NO SENSE
git checkout $PROTO_BRANCH

# What is the purpose of the prototype branch?
#git fetch --tags proto

# TODO move this into shared function.  Change echo to log.  Move test to start of prog
bstr=""; for b in `git branch | grep "$NAMESPACE_ST"`; do bstr="$bstr $b"; done
declare -a student_branches=($bstr)
[ "${#student_branches[@]}" -gt 0 ] || fail "No student branches found..."


# We could just use bstr, leave arrays out of this
for branch in ${student_branches[@]}; do
   git checkout $branch
   echo "updating local: $branch"
   git pull
   # consider sqash / no-ff, if we want different commit messages
   # Can students modify/revert/ammend this commit and affect PROTO?
   echo "merging: $COMMIT int $branch"
   # Did I really just pull from the PROTO branch?!
   git merge $COMMIT
   echo "pushing, may not always want to."
   git push
done

git checkout $PROTO_BRANCH
