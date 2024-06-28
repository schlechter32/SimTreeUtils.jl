import SimTreeUtils
import TOML

stpd = SimTreeUtils.getsimtreeparams("/u/bulk/home/wima/fchrstou/workspace/RL_RSA_MDPs/exp2")
open("UserTemp/simtreeparams.toml", "w") do io
  TOML.print(io, stpd)
end

