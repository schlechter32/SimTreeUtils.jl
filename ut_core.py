#!/usr/bin/env python3

import os
import stat
import sys
import re
import subprocess
import argparse
from distutils.dir_util import copy_tree
import tempfile
import shutil
import glob
from itertools import product

join = os.path.join


bulk_root = '/u/bulk/home/wima/'
bulk_user = join(bulk_root, 'tenderle/')
user_root = '/u/home/wima/tenderle/bulk/'


def is_bulk_location(path):
    return path.startswith(bulk_user)

def get_ghost_folder(folder):
    assert is_bulk_location(folder)
    return folder.replace(bulk_root, user_root)

def is_study_root(folder):
    return os.path.isdir(join(folder, 'MetaData')) and \
            os.path.isdir(join(folder, 'Results')) and \
            os.path.isdir(join(folder, 'Temp'))


class StudyRoot:
    @classmethod
    def existing_from_folder(cls, folder):
        if not is_study_root(folder):
            raise Exception('Folder {} is not a study root'.format(folder))
        ghost = get_ghost_folder(folder)
        return cls(folder, ghost)

    def __init__(self, root, ghost_root):
        self.root = root
        self.ghost_root = ghost_root

    @property
    def has_ghost(self):
        return os.path.isdir(self.ghost_root)

    def move(self, dst):
        if not is_bulk_location(dst):
            raise Exception('Cannot move study root outside of bulk')

        if self.has_ghost:
            self._unlink()

        shutil.move(self.root, dst)
        self.root = dst

        if self.has_ghost:
            new_ghost = get_ghost_folder(dst)
            shutil.move(self.ghost_root, new_ghost)
            self.ghost_root = new_ghost
            self._link()

    def _unlink(self):
        if self.has_ghost:
            os.unlink(join(self.root, 'MetaData'))
            os.unlink(join(self.ghost_root, 'Results'))

    def _link(self):
        os.symlink(join(self.ghost_root, 'MetaData'), join(self.root, 'MetaData'))
        os.symlink(join(self.root, 'Results'), join(self.ghost_root, 'Results'))


def only_in_study_root(func):
    def wrapper(*args, **kwargs):
        if not is_study_root('.'):
            raise Exception('Current working directory is not a study root')
        return func(*args, **kwargs)
    return wrapper

def do_run(args):
    #GSProgramStarter --exec $(pwd)/run.sh --pr cores=1 mem=15G
    with tempfile.NamedTemporaryFile(mode='w', dir=os.getcwd(), suffix='.sh', delete=False) as file:
        run_file = file.name
        file.write('#!/bin/bash\n')
        file.write('cd ' + os.getcwd() + '\n')
        file.write(args.command + '\n')
        if args.mail:
            file.write('/u/home/wima/tenderle/scripts/jobDoneMail.sh\n')
    os.chmod(run_file, 0o750)
    cmd = ['GSProgramStarter', '--exec', run_file]
    if args.memory is not None:
        cmd += ['--pr', 'cores=1', 'mem=' + args.memory]
    subprocess.call(cmd)
    os.remove(run_file)

def do_prepare(args):
    folder = os.getcwd()
    if is_study_root(folder):
        raise Exception('Current directory is already a study root')

    ghost = False
    if is_bulk_location(folder):
        ghost_folder = get_ghost_folder(folder)
        ghost_metadata = join(ghost_folder, 'MetaData')
        choice = input('Create ghost folders at {} (y/[n])? '.format(ghost_folder)) or 'n'
        if choice in ('y', 'Y'):
            ghost = True
            try:
                os.makedirs(ghost_metadata)
            except OSError:
                raise Exception('Folder {} already exists'.format(ghost_metadata))
            os.symlink(ghost_metadata, join(folder, 'MetaData'))

    copy_tree('/u/home/wima/tenderle/scripts/study_root_template', '.')

    if ghost:
        os.symlink(join(folder, 'Results'), join(ghost_folder, 'Results'))

@only_in_study_root
def do_prune(args):
    deleted = 0
    while True:
        recently_deleted = 0
        subdirs = []
        for parent, dirs, _ in os.walk('Results'):
            subdirs += [join(parent, d) for d in dirs if d.startswith('Para')]
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
def do_add(args):
    if any(len(p) < 2 for p in args.simulation_parameter):
        raise Exception('Invalid parameter specification')

    regex = re.compile(r'Para([IFS])__(.+)__(.+)')

    types = {}
    params = {}

    subdirs = []
    for parent, dirs, _ in os.walk('Results'):
        subdirs += [join(parent, d) for d in dirs if d.startswith('Para')]
    if len(subdirs) > 0:
        subdirs = [d.split(os.sep) for d in subdirs]
        depth = max(len(d) for d in subdirs)
        leaves = (d for d in subdirs if len(d) == depth)

        for leaf in leaves:
            for p in leaf[1:]:
                t, name, val = regex.match(p).groups()
                types[name] = t
                if name in params:
                    params[name].add(val)
                else:
                    params[name] = {val}

    type_map = {'string': 'S', 'int': 'I', 'float': 'F'}

    for p in args.simulation_parameter:
        n = p[0]
        try:
            t = type_map[p[1]]
            vals = set(p[2:])
        except KeyError:
            if n in types:
                t = types[n]
            else:
                raise Exception('Invalid type for parameter ' + n)
            vals = set(p[1:])

        if n in types and t != types[n]:
            raise Exception('Wrong type for parameter ' + n)

        if t == 'I':
            try:
                [int(x) for x in vals]
            except ValueError:
                raise Exception('Non-integer value provided for parameter ' + n)
        elif t == 'F':
            try:
                [float(x) for x in vals]
            except ValueError:
                raise Exception('Non-float value provided for parameter ' + n)

        types[n] = t
        params[n] = vals

    prefixes = [f'Para{types[n]}__{n}__' for n in params.keys()]
    proto = 'Results/' + '{}/'.join(prefixes) + '{}'
    count = 0
    for vals in product(*params.values()):
        path = proto.format(*vals)
        if not os.path.isdir(path):
            os.makedirs(path)
            count += 1
    print(f'Added {count} parameter value sets')

@only_in_study_root
def do_list(args, unknown_args):
    # %%spname%% 
    subprocess.call(
        ['SimTree', 'list', '--print-format', '%%content%% %%value%%'] +
            unknown_args
    )

@only_in_study_root
def do_count(args):
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
def do_unlockall(args):
    subprocess.call(['SimTree', 'unlock', '--fav'])

@only_in_study_root
def do_cleanall(args):
    subprocess.call(['SimTree', 'clean', '--fav', '--fdff'])

def do_move(args):
    sr = StudyRoot.existing_from_folder(os.path.abspath(args.current_path))
    sr.move(os.path.abspath(args.new_path))

def do_remove(args):
    folder = os.path.abspath(args.path)
    if not os.path.isdir(join(folder, 'MetaData')):
        print('No MetaData folder found. Not removing anything.')
        return
    ghost = get_ghost_folder(folder)
    if os.path.isdir(ghost):
        shutil.rmtree(ghost)
    shutil.rmtree(folder)

@only_in_study_root
def do_compress(args):
    if os.path.isfile('Results.tgz') or os.path.isdir('Results.tgz'):
        raise Exception('"Results.tgz" already exists')
    ret = subprocess.call(['tar', '-czf', 'Results.tgz', 'Results/'])
    if ret != 0:
        raise Exception('Compressing failed')
    shutil.rmtree('Results')

def do_uncompress(args):
    if os.path.isfile('Results') or os.path.isdir('Results'):
        raise Exception('"Results" already exists')
    ret = subprocess.call(['tar', '-xf', 'Results.tgz'])
    if ret != 0:
        raise Exception('Uncompressing failed')
    os.remove('Results.tgz')

def do_find_stale_ghosts(args):
    def is_stale(metadata_folder):
        return os.path.islink(join(os.path.dirname(metadata_folder), 'Results')) and \
            not os.path.islink(metadata_folder.replace(user_root, bulk_root))

    folders = glob.iglob(user_root + '**/MetaData', recursive=True)
    stale = [os.path.dirname(f) for f in folders if is_stale(f)]
    if len(stale) > 0:
        print('The following folders might be stale ghost folders. Double check before removing!')
        print('\n'.join(stale))

@only_in_study_root
def do_to_fs_path(args):
    values = re.split(' |:', args.spp)
    path = 'Results'
    for v in values:
        dirs = next(os.walk(path))[1]
        try:
            c = next(d for d in dirs if d.endswith(f'__{v}'))
        except StopIteration:
            raise Exception(f'Invalid parameter value "{v}"')
        path = join(path, c)
    print(path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    p = subparsers.add_parser('run', help='runs a task using the global scheduler')
    p.set_defaults(func=do_run)
    p.add_argument('--memory', '-m', type=str, help='e.g. -m 15G')
    p.add_argument('--mail', action='store_true', help='sends a notification mail after the job has finished')
    p.add_argument('command')
    p = subparsers.add_parser('prepare', help='prepares a folder as study root')
    p.set_defaults(func=do_prepare)
    p = subparsers.add_parser('prune', help='prunes folders without leaves')
    p.set_defaults(func=do_prune)
    p = subparsers.add_parser('add', help='adds parameters')
    p.set_defaults(func=do_add)
    p.add_argument('--simulation-parameter', '--sp', action='append', nargs='+', help='--sp Parameter [type] val1 val2 ...')
    p = subparsers.add_parser('list', help='lists the parameter value sets')
    p.set_defaults(func=do_list, accept_unknown_args=True)
    p = subparsers.add_parser('count', help='counts the parameter value sets')
    p.set_defaults(func=do_count)
    p = subparsers.add_parser('unlockall', help='unlocks all parameter sets')
    p.set_defaults(func=do_unlockall)
    p = subparsers.add_parser('cleanall', help='cleans all parameter sets and all foreign files')
    p.set_defaults(func=do_cleanall)
    p = subparsers.add_parser('move', help='moves a study root')
    p.set_defaults(func=do_move)
    p.add_argument('current_path')
    p.add_argument('new_path')
    p = subparsers.add_parser('compress', help='compresses the Results folder of a study root')
    p.set_defaults(func=do_compress)
    p = subparsers.add_parser('uncompress', help='uncompresses the Results folder of a study root')
    p.set_defaults(func=do_uncompress)
    p = subparsers.add_parser('show-stale-ghosts', help='show stale ghost folders in user home')
    p.set_defaults(func=do_find_stale_ghosts)
    p = subparsers.add_parser('to-fs-path', help='translates a simulation parameter path to a file system path')
    p.set_defaults(func=do_to_fs_path)
    p.add_argument('spp', help='e.g. A:0:x:10')
    p = subparsers.add_parser('remove', help='removes the study root')
    p.set_defaults(func=do_remove)
    p.add_argument('path')

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
