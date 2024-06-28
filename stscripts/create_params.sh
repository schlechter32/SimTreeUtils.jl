#!/usr/bin/env bash

SimTree add --sp Topology string BA4_2 BA5_2 BA6_2 BA10_3 BA10_3b --sp PoissonProcess string AvaMax AvaMaxStd AvaMaxStdPlus --sp DemandValues string DV4_6_8 --sp PAR_K_CANDPATHS int 4 --sp PAR_J_FREQBLOCKS int 4 --sp PAR_SPECTRUMSLOTLENGTH int 30 50 80 --sp PAR_POMDP string RSAPOMDP1_1_1_1 RSAPOMDP1_1_1_2 --sp PAR_DISCOUNT float 0.9 --sp ExploreDecay string LDS_1_001_075 --sp PAR_MAX_STEPS int 10000 --sp PAR_LEARNING_RATE float 0.005 --sp NNHiddenLayers string HL_500_500_500

