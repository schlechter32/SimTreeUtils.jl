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


if haskey(ENV,"SIMTREE_RESULTS_PATH")
    SIMTREE_RESULTS_PATH = ENV["SIMTREE_RESULTS_PATH"]
else
    @warn "Now resultspath set using cwd"
    SIMTREE_RESULTS_PATH="."
    str_seed=ENV["ST_SEED"]
    println("Seed is:$(str_seed):")
    SEED=parse(Int,ENV["ST_SEED"])
    include("$SIMTREE_RESULTS_PATH/sim.par")
    results = simulatefunction(PARAMSDICT,SEED,ENV["DATA_PATH"])
    @show results
    JLD2.save("$SIMTREE_RESULTS_PATH/study.jld2", results)


end
