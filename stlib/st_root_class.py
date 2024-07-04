from .st_utils import *
class Studyroot:
    study_root_dir=""
    toml_content={}
    stparams={}
    runparams={}
    partparams={}
    gps=0
    lps=1
    mem="10G"
    batches=1
    cores=1
    def __init__(self):
       self.set_study_root=self.set_study_root(0) 
    def safe_set(self,key,dict):
        if key in dict:
            if hasattr(self,key):
                setattr(self,key,dict[key])


    def set_study_root(self,args):
        # print("Setting sr root")
        shell_root=os.getenv("studyroot")
        # print(f"shellroot {shell_root}")
        pwd=os.getcwd()

        if shell_root is not None:
            self.study_root_dir=shell_root
        elif is_study_root(pwd):
            self.study_root_dir=pwd
        else:
            # TODO: Path completion
            self.study_root_dir=input("Set fullpath to studyroot: ")
        # os.system(f"export studyroot={self.study_root_dir}")
        write_env(self.study_root_dir)
        print(f"set sroot as {self.study_root_dir}")

    @only_in_study_root
    def load_toml(self):

        if os.path.exists("st_params.toml"):
            toml_content=toml.load("st_params.toml")
            print(toml_content)
            self.toml_content=toml_content
            self.stparams=toml_content["SimTreeParams"]
            self.runparams=toml_content["SimulateAllRunParams"]
            if "PartialSim" in toml_content:
                self.partparams=toml_content["PartialSim"]

        else:
            print("ERROR: No st_params.tomls found in Studyroot")

            return

    @only_in_study_root
    def create_params_and_template(self):

            
        print(toml_content)
        simtree_params=toml_content["SimTreeParams"]
        sp_string="SimTree add "
        template_string=""
        for par,vals in simtree_params.items():
            sp_string+="--sp " + par
            template_string+=f"PARAMSDICT[{par}]=%%{par}%% \n"
            if isinstance(vals,list):
                sp_string += f" {to_st_type_string(vals[1])}"
                for val in vals:
                    sp_string += f" {val}"
            else:
                sp_string+=f" {to_st_type_string(vals)} {vals}"
            sp_string+=" "
        with open('paramsdict.jl', "w") as template:
            template.write(template_string)
        # os.system(sp_string)
