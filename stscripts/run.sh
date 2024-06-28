#!/bin/bash    
umask 0007
    
STUDY_ROOT="$(dirname $(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null && pwd))"    
TOOL_PATH="$(realpath $STUDY_ROOT/MetaData/Tool)"
export SIMTREE_RESULTS_PATH="$(pwd)"
export JULIAUP_DEPOT_PATH="/u/bulk/home/wima/$USER/julia"
export JULIA_DEPOT_PATH="/u/bulk/home/wima/$USER/julia"

    
args="$@ --script"
echo $args > simtree_arguments.txt
git -C $TOOL_PATH rev-parse HEAD > commithash
# Create logging configuration for hyperparameters
# ./create_hparam_config.py  "$STUDY_ROOT/Results"
# start julia
$HOME/.juliaup/bin/julia --project=$TOOL_PATH -e "import Pkg; Pkg.instantiate()"
$HOME/.juliaup/bin/julia --project=$TOOL_PATH --threads 1 $TOOL_PATH/simu/rlsim.jl
    
# export something
if [ $? -eq 0 ]; then    
    if test -e "study.jld2"; then
        echo '<?xml version="1.0" encoding="ISO-8859-1"?>' > Export.log    
        echo '<SimulationResults version="2" seed_index="1" result_type="export" batch="1" number_of_batches="1">' >> Export.log
        echo '</SimulationResults>' >> Export.log    
    fi
fi

