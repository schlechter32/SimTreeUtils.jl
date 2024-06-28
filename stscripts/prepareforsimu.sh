./scripts/washhands.sh
curr_date=$(date +"%y%m%d_%H%M%S")
# run julia to create a file with all simtree parameters
cd MetaData/Tool
git add .
git commit -m "run $curr_date"
cd ../..
julia --project=MetaData/Tool scripts/findsimtreeparams.jl

# activate correct python env
source venv_rlrsamdp/bin/activate

python3 scripts/create_hparam_config.py Results/
