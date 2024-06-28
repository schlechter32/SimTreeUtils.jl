#!/usr/bin/env bash
./scripts/prepareforsimu.sh

# global
SimTree simulate --sb MetaData/run.sh --gps --d 1 --pr mem=20G cores=1
# local
#SimTree simulate --sb MetaData/run.sh --lps 1 --d 2
