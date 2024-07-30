module SimTreeUtils

using Parameters
using Printf
using DocStringExtensions
using Suppressor
using JLD2

export copyresults, findrelpaths, getparameters, simsnum, getsims, getsimspath

include("simulation.jl")
include("metaanalysis.jl")

end
