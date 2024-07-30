"""
$(TYPEDSIGNATURES)

Get the SimTree parameters in a `Dictionary{String, Vector{String}}`
SimTree must be installed.
Give the root simtree directory
"""
function getsimtreeparams(simtreedirectory::String=".")::Dict{String,Vector{String}}
    cmd = Cmd(`SimTree list`; dir=simtreedirectory)
    iobf = IOBuffer()
    @suppress begin
        run(pipeline(cmd, stdout=iobf))
    end
    seekstart(iobf)

    parvaldict = Dict{String,Vector{String}}()

    par_val_rgx = r"\[([^\] ]*) ([^\]]*)\]"

    for l in eachline(iobf)
        for m in eachmatch(par_val_rgx, l)
            if haskey(parvaldict, m.captures[1])
                vals = parvaldict[m.captures[1]]
                m.captures[2] ∈ vals && continue
                push!(vals, m.captures[2])
            else
                parvaldict[m.captures[1]] = String[m.captures[2]]
            end
        end
    end
    return parvaldict
end

"""
$(TYPEDSIGNATURES)

Wraps the function you want to run through SimTree simulate
"""
function stsimulate(simulatefunction)


    if haskey(ENV, "SIMTREE_RESULTS_PATH")
        SIMTREE_RESULTS_PATH = ENV["SIMTREE_RESULTS_PATH"]
    else
        @warn "Now resultspath set using cwd/results"
        SIMTREE_RESULTS_PATH = "$(pwd())/results"
    end
    if haskey(ENV, "ST_SEED")
        str_seed = ENV["ST_SEED"]
        println("Seed is:$(str_seed):")

        SEED = parse(Int, ENV["ST_SEED"])
    else
        @warn "Seed not set from ST using 0"
        SEED = 0
    end
    include("$SIMTREE_RESULTS_PATH/sim.par")
    if haskey(ENV, "DATA_PATH")
        datapath = ENV["DATA_PATH"]
    else
        @warn "Datapath not set using pwd/data"
        datapath = "$(pwd())/data"
    end
    results = simulatefunction(PARAMSDICT, SEED,datapath)
    @show results
    JLD2.save("$SIMTREE_RESULTS_PATH/study.jld2", results)


end
