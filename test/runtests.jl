using SimTreeUtils
using Test

include("testutils.jl")
@testset "SimTreeUtils.jl" begin
    # Write your tests here.
    @test typeof(SimTreeUtils.stsimulate(testmainfunction))== Dict{String,Any}
end
