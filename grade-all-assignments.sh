# This will grade all subprojects.  A few things to note:
#
# 1. Why would we ever want to grade more than one assignment at once?
# 2. We may still intend to move away from submodule projects
# 3. It may be good to have a single project, output for class cleaner
# 4. We'll probably use a partial submodule only for incremental project
#    But for regular, unconnected curriculum, we'll want separate.
# 5. We can and should specifiy individual test classes using -Dtest...
#

mvn -fn test | egrep 'SUCCESS|FAILED' | grep -v BUILD
