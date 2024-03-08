"""
$(TYPEDSIGNATURES)

Get the SimTree parameters in a `Dictionary{String, Vector{String}}`
SimTree must be installed.
Give the root simtree directory
"""
function getsimtreeparams(simtreedirectory::String=".")::Dict{String, Vector{String}}
    cmd = Cmd(`SimTree list`; dir=simtreedirectory)
    iobf = IOBuffer()
    @suppress begin
	run(pipeline(cmd, stdout=iobf))
    end
    seekstart(iobf)

    parvaldict = Dict{String, Vector{String}}()

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

