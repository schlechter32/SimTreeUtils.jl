#!/bin/bash
arg1=$1
echo $arg1

if [ $arg1 = "cd" ];then
    cd $studyroot
fi
if [ "${studyroot+set}" = "set" ]; then
    echo "Current StudyRoot is: $studyroot"
    "$ST_PATH/st.py"
else

    "$ST_PATH/st.py"
    source .srenv
fi
