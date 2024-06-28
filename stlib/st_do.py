from .st_utils import only_in_study_root,to_fs_path
import os
import subprocess
import toml
import shutil
join = os.path.join

@only_in_study_root
def do_remove(args):
    subprocess.call(['SimTree', 'remove', '--fav'])
def do_create(args,st_root):
    st_root.create_params_and_template()
    pass
@only_in_study_root
def do_run(args,st_root):

    stpath=os.getenv("ST_PATH")
    toolpath=join(stpath, "MetaData","Tool")
    # subprocess.Popen(['sh',stpath +"/stscripts/prepareforsimu.sh"])
    run_command=f"SimTree simulate --sb {stpath}/stscripts/run.sh --lps 1 --d 1" .split(" ")
    tt=subprocess.call(run_command)
# washhands.sh
# umask 007
# prepare for simu
# ./scripts/washhands.sh
# curr_date=$(date +"%y%m%d_%H%M%S")
# # run julia to create a file with all simtree parameters
# cd MetaData/Tool
# git add .
# git commit -m "run $curr_date"
# cd ../..
# julia --project=MetaData/Tool scripts/findsimtreeparams.jl

# activate correct python env
# source venv_rlrsamdp/bin/activate

# python3 scripts/create_hparam_config.py Results/
# simulate.sh
# SimTree simulate --sb MetaData/run.sh --gps --d 1 --pr mem=20G cores=1
    print("in run")

    if not os.path.exists("st_params.toml"):
        print("Can't run with out st_params.toml, please create")
        return
    st_params=toml.load('st_params.toml')
    print(st_root.study_root_dir)

@only_in_study_root
def do_unlockall(args):
    subprocess.call(['SimTree', 'unlock', '--fav'])

@only_in_study_root
def do_cleanall(args):
    subprocess.call(['SimTree', 'clean', '--fav', '--fdff'])
def do_uncompress(args):
    if os.path.isfile('Results') or os.path.isdir('Results'):
        raise Exception('"Results" already exists')
    ret = subprocess.call(['tar', '-xf', 'Results.tgz'])
    if ret != 0:
        raise Exception('Uncompressing failed')
    os.remove('Results.tgz')
@only_in_study_root
def do_compress(args):
    if os.path.isfile('Results.tgz') or os.path.isdir('Results.tgz'):
        raise Exception('"Results.tgz" already exists')
    ret = subprocess.call(['tar', '-czf', 'Results.tgz', 'Results/'])
    if ret != 0:
        raise Exception('Compressing failed')
    shutil.rmtree('Results')
def do_cd(args):
    if args.path[0] == ".":
        return os.getenv("studyroot") 
    par_set = " ".join(args.path)
    print(f"parset {par_set}")

    if to_fs_path(par_set):
        return
    os.chdir(os.getenv("studyroot"))
    if os.path.exists("results.toml"):
        print("loading results")
        results=toml.load("results.toml")
        results_selector_dict={}
        for idx,(elm,res) in enumerate(results.items()):
            clean_elem=elm.replace(" ","")
            print(f"{res}:{idx}={clean_elem}")
            results_selector_dict[str(idx)]=clean_elem
            results_selector_dict[clean_elem]=clean_elem
        user_in=input("Select number or path: \n")

        to_fs_path(results_selector_dict[user_in])


@only_in_study_root
def do_count(args):
    print("Calling count")
    subdirs = []
    for parent, dirs, _ in os.walk('Results'):
        subdirs += [join(parent, d) for d in dirs if d.startswith('Para')]
    if len(subdirs) > 0:
        subdirs = [d.split(os.sep) for d in subdirs]
        depth = max(len(d) for d in subdirs)
        num_leaves = sum(1 for d in subdirs if len(d) == depth)
        print(f'{num_leaves} parameter value sets')
    else:
        print('No parameter value sets')

@only_in_study_root
def test_sr_func(args):
    print(os.getcwd())

# TODO: Ask tobi what prune does
@only_in_study_root
def do_prune(args):
    deleted = 0
    while True:
        recently_deleted = 0
        subdirs = []
        for parent, dirs, _ in os.walk('Results'):
            subdirs += [join(parent, d) for d in dirs if d.startswith('Para')]
            print(dirs)
        if len(subdirs) > 0:
            depth = max(d.count(os.sep) for d in subdirs)
            non_leaves = (d for d in subdirs if d.count(os.sep) < depth)
            for d in non_leaves:
                with os.scandir(d) as it:
                    if not any(it):  # directory empty?
                        os.rmdir(d)
                        deleted += 1
                        recently_deleted += 1
        if recently_deleted == 0:
            break  # completely pruned
    print(f'Deleted {deleted} folders')

@only_in_study_root
def do_list(args, unknown_args):
    # %%spname%% 
    tt=subprocess.run(
        ['SimTree', 'list', '--print-format', '%%content%% %%value%%'] +
            unknown_args, capture_output=True, text=True
    )
    info_string="""
Meaning of symbols
    F - - - - - - -  Final results exists
    - E - - - - - -  Directory is empty
    - - L - - - - -  Directory is locked
    - - - B - - - -  Default batches exists
    - - - - S - - -  Seeded results exists
    - - - - - R - -  Export results exists
    - - - - - - X -  Seed directories are locked
    - - - - - - - W  Directory is not empty (may contain foreign files, see Option --force-delete-foreign-files)
                                             """
    # print(tt.stdout)
    par_result_list=tt.stdout.split("\n")
    # print("Results")
    # print(par_result_list)
    # print('Elems')
    line_splits=[par_res.split("  ") for par_res in par_result_list]
    # print(line_splits)
    print(f"{info_string}")
    results_dict={}
    for param_line in line_splits:
        # print(param_line)
        if len(param_line) >1:
            res = ''.join([elem for elem in param_line[0] if elem != '-']).strip(" ")
            results_dict[param_line[1]]=res
            print(f"    {res}:{param_line[1]}")
    with open("results.toml", "w") as toml_results:
        toml.dump(results_dict,toml_results)
        

    # [print(snip, end="\n") for snip in tt.stdout.split("\n")]
    # print(tt)
