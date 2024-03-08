module SimTreeUtils

using Parameters
using Printf
using DocStringExtensions
using Suppressor

export copyresults, findrelpaths, getparameters, simsnum, getsims, getsimspath

include("simulation.jl")
include("metaanalysis.jl")

end
