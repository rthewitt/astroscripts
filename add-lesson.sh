#!/bin/bash
# Once a course project has been set up locally by the professor
# running this script will add the lessons to all student modules
# and push them.  Students then simply update

# Precondition: Prototype project has already been set up with this
# lesson.  The lessons has been customized and instructions provided.


[ "$#" -lt 1 ] && echo "Lab number must be provided." && exit 1

source $( dirname $0 )/setenv-client.sh

git submodule foreach git pull

# No longer needed, kept for posterity
#git submodule foreach '$toplevel/../scripts/build-lesson.sh $name 7 `echo $toplevel | sed "s:.*/::g"`'

# Didn't work, using external script with same environment
#git submodule foreach buildMavenLesson $1
git submodule foreach $BIN_DIR/build-lesson.sh $1

pause "Press enter to view changes made to local student repositories."

# Tracking files, so that reset will be effective if needed
# The importance of this will change after prototype merge is implemented
git submodule foreach git add -A

git submodule foreach git status

# TODO change script, this comes into play after committing
#f_yesno "Do you want to review changes?" && git submodule summary HEAD && pause 'Press [enter] key to continue...'

safe_commit=0
f_yesno "Commit and push these changes?" && safe_commit=1
if [ $safe_commit -eq 1 ]
then
git submodule foreach 'git commit -m "lesson / project generated for student"' # more specific
git submodule foreach git push
echo "Updating super project now"
git add -A
git commit -m "Update all student projects with lesson" # add more specific information here
f_yesno "Do you want to push changes?" && git push || "You must push class project manually to maintain record."
else
f_yesno "Manually handling submodules is NOT recommended.  Do you want to abort and revert all changes to student repositories?" && git submodule foreach 'git reset --hard' && echo 'All changes reverted, exiting script' && exit 0
fi

