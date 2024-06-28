#!/usr/bin/env bash

SimTree add --sp Topology string BA4_2 BA6_2 BA10_3 BA10_3b --sp PoissonProcess string AvaMax AvaMaxStd AvaMaxStdPlus --sp DemandValues string DV4_6_8 --sp PAR_K_CANDPATHS int 4 --sp PAR_SPECTRUMSLOTLENGTH int 30 50 80 --sp PAR_DEMANDNUMBER int 100 300 600 --sp PAR_TIMELIMIT int 50400

