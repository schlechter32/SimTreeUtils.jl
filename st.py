#!/usr/bin/env python3

# import toml
# import os
# import glob
# import readline
import sys
import argparse
from stlib.st_do import *
from stlib.st_root_class import Studyroot









if __name__=="__main__":
    st_root=Studyroot()
    # print("Arguments passed to st.py (before parsing):", sys.argv[1:])
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    
    # Print all arguments
    # subparsers = parser.add_subparsers(dest='command')
    cd_parser = subparsers.add_parser('cd', help='Go to roota: .; Results dir i for interactive pars from list for direct')
    cd_parser.add_argument("path", nargs="+", help="To Resultspath")
    cd_parser.set_defaults(func=do_cd)
    p = subparsers.add_parser('test', help='Test param')
    p.set_defaults(func=test_sr_func)
    p.set_defaults(func=st_root.set_study_root)
    p = subparsers.add_parser('init', help='Set studyroot for current shell session')
    p.set_defaults(func=st_root.set_study_root)
    p = subparsers.add_parser('count', help='counts the parameter value sets')
    p.set_defaults(func=do_count)
    p = subparsers.add_parser('list', help='lists the parameter value sets')
    p.set_defaults(func=do_list, accept_unknown_args=True)

    p = subparsers.add_parser('compress', help='compresses the Results folder of a study root')
    p.set_defaults(func=do_compress)
    p = subparsers.add_parser('uncompress', help='uncompresses the Results folder of a study root')
    p.set_defaults(func=do_uncompress)

    p = subparsers.add_parser('unlockall', help='unlocks all parameter sets')
    p.set_defaults(func=do_unlockall)
    p = subparsers.add_parser('cleanall', help='cleans all parameter sets and all foreign files')
    p.set_defaults(func=do_cleanall)

    p = subparsers.add_parser('run', help='cleans all parameter sets and all foreign files')
    p.set_defaults(func=lambda args: do_run(args,st_root))

    p = subparsers.add_parser('create', help='cleans all parameter sets and all foreign files')
    p.set_defaults(func=lambda args: do_create(args,st_root))
    p = subparsers.add_parser('remove', help='removes the study root')
    p.set_defaults(func=do_remove)
    # do_count(args=0)
    # str.set_study_root()
    # str.create_params_and_template()
    # str.test_sr_func()

    args, unknown_args = parser.parse_known_args()
    accept_unknown_args = True
    if not 'accept_unknown_args' in args or not args.accept_unknown_args:
        accept_unknown_args = False
        args = parser.parse_args()
    if 'func' in args:
        try:
            if accept_unknown_args:
                args.func(args, unknown_args)
            else:
                args.func(args)
        except Exception as e:
            exit('ERROR: {}'.format(e))
