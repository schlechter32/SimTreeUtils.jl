
#!/usr/bin/env bash
#
# SimTree add \
# --sp Topology string BA4_2 BA6_2 BA10_3 BA10_3b \
# --sp PoissonProcess string AvaMax AvaMaxStd AvaMaxStdPlus \
# --sp DemandValues string DV4_6_8 \
# --sp PAR_K_CANDPATHS int 4 \
# --sp PAR_J_FREQBLOCKS int 1 \
# --sp PAR_SPECTRUMSLOTLENGTH int30 50 80 \
# --sp PAR_DEMANDNUMBER int 1000  \
# --sp PAR_TIMELIMIT int 50400 \
# --sp PAR_RESET_SEED string true \
# --sp PAR_EARLY_STOPPING_ROUNDS int 500 \
# --sp PAR_TOTAL_TIMESTEPS int 10000000 \
# --sp PAR_NUM_STEPS int 100 \
# --sp PAR_NUM_ENVS int 1 \
# --sp PAR_NUM_MINIBATCHES int 1 \
# --sp PAR_UPDATE_EPOCHS int 1 \
# --sp PAR_EPISODES int 1 \
# --sp PAR_LOG_INTERVAL int 10 \
# --sp PAR_LEARNING_RATE float 0.00005 \
# --sp PAR_EPSILON float 1.0 \
# --sp PAR_GAMMA float 0.995 \
# --sp PAR_GAE_LAMBDA float 0.9 \
# --sp PAR_CLIP_COEF float 0.1 \
# --sp PAR_ENT_COEF float 1.0 \
# --sp PAR_V_COEF float 1.0 \
# --sp PAR_NORM_ADVANTAGES string true \
# --sp PAR_CLIP_VALUE string false \
# --sp PAR_ANNEAL_LR string true \
# --sp PAR_POMDP string RSAPOMDP1_1_1_1 RSAPOMDP1_1_1_2

  # --sp PoissonProcess string  AvaMaxStdPlus \

 SimTree add \
--sp Topology string BA4_2 BA5_2 BA6_2 BA10_3 BA10_3b cost239 nsfnetchen  \
--sp PAR_DEMAND_LIST string loaded \
--sp PAR_POMDP string RSAPOMDP1_1_1_2

# SimTree  add \
# --sp Topology string BA4_2 BA5_2 BA6_2 BA10_3 BA10_3b cost239 nsfnetchen  \
# --sp PAR_DEMAND_LIST string loaded \
# --sp PoissonProcess string  Fixed \
# --sp DemandValues string DV4_6_8 \
# --sp PAR_K_CANDPATHS int 4 \
# --sp PAR_J_FREQBLOCKS int 4 \
# --sp PAR_SPECTRUMSLOTLENGTH int 100 \
# --sp PAR_DEMANDNUMBER int 100000  \
# --sp PAR_TIMELIMIT int 50400 \
# --sp PAR_RESET_SEED string true false \
# --sp PAR_EARLY_STOPPING_ROUNDS int 500 \
# --sp PAR_TOTAL_TIMESTEPS int 10000000 \
# --sp PAR_NUM_STEPS int 100 \
# --sp PAR_NUM_ENVS int 1 \
# --sp PAR_NUM_MINIBATCHES int 1 \
# --sp PAR_UPDATE_EPOCHS int 1 \
# --sp PAR_EPISODES int 1000000 1000 10000 15000 100 \
# --sp PAR_LOG_INTERVAL int 1 \
# --sp PAR_LEARNING_RATE float 0.00005 \
# --sp PAR_EPSILON float 1.0 \
# --sp PAR_GAMMA float 0.995 \
# --sp PAR_GAE_LAMBDA float 0.9 \
# --sp PAR_CLIP_COEF float 0.1 \
# --sp PAR_ENT_COEF float 1.0 \
# --sp PAR_V_COEF float 1.0 \
# --sp PAR_NORM_ADVANTAGES string true \
# --sp PAR_CLIP_VALUE string false \
# --sp PAR_ANNEAL_LR string true \
# --sp PAR_NN_WIDTH_FACTOR int 3 \
# --sp PAR_POMDP string RSAPOMDP1_1_1_2



# Topologies
# nsfnet fc
# cost239 ho
# generate demands kspff *3 
# put topologies on ikr base
#
# bw/slots arrival time service time process 
# [4,6,8]
# amount 320 kspff * 3
# avamaxstdplus

