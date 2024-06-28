#!/usr/bin/env python3

import toml
import os
import glob
import readline
join = os.path.join
def load_toml():
    to=toml.load("test/test.toml")
    print(to)

def is_study_root(folder):
    return os.path.isdir(join(folder, 'MetaData')) and \
            os.path.isdir(join(folder, 'Results')) and \
            os.path.isdir(join(folder, 'Temp'))

def has_study_root_env():
    return os.getenv("studyroot") is not None

def only_in_study_root(func):
    def wrapper(*args, **kwargs):
        cur_dir =os.getcwd()
        if not has_study_root_env() and not is_study_root('.'):

            raise Exception('Studyroot not set and not in studyroot')
        if not is_study_root('.'):
            os.chdir(os.getenv("studyroot"))
            
        func(*args, **kwargs)
        os.chdir(cur_dir)
    return wrapper
def write_env(sr_dir):
    os.chdir(sr_dir)
    with open("", "w") as file:
            file.write(f"export studyroot={sr_dir}\n")

def to_st_type_string(val):
    type_map={
        "str": "string",
        "float":"float",
            "int":"int"
    }
    return type_map[type(val).__name__]

class Studyroot:
    study_root_dir=""
    def set_study_root(self):
        shell_root=os.getenv("studyroot")
        print(f"shellroot {shell_root}")
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
        print(self.study_root_dir)
    @only_in_study_root
    def create_params_and_template(self):

        if os.path.exists("st_params.toml"):
            toml_content=toml.load("st_params.toml")
        else:
            print("ERROR: No st_params.tomls found in Studyroot")

            return
            
        print(toml_content)
        simtree_params=toml_content["SimTreeParams"]
        sp_string="SimTree add "
        for par,vals in simtree_params.items():
            sp_string+="--sp " + par
            if isinstance(vals,list):
                sp_string += f" {to_st_type_string(vals[1])}"
                for val in vals:
                    sp_string += f" {val}"
            else:
                sp_string+=f" {to_st_type_string(vals)} {vals}"
            sp_string+=" "
        os.system(sp_string)


    @only_in_study_root
    def test_sr_func(self):
        print(os.getcwd())






if __name__=="__main__":
    str=Studyroot()
    str.set_study_root()
    # str.create_params_and_template()
    # str.test_sr_func()

