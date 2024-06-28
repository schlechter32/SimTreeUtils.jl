#!/bin/bash
arg1=${1:-default}
umask 007

if [ "${studyroot+set}" = "set" ]; then
    echo "Current StudyRoot is: $studyroot"
    retval=$("$ST_PATH/st.py" "$@" | tee /dev/tty | tail -n 1)    # | tail -n 1)
    if [ -d "$retval" ]; then
        cd $retval
    fi
else

    echo "Current StudyRoot is not set please set now"
    "$ST_PATH/st.py" "init"
    source .srenv
fi
