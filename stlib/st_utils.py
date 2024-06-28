import toml
import os
import re
join=os.path.join

def to_fs_path(pars):
    values = re.split(' |:', pars)
    path = join(os.getenv("studyroot"),"Results")
    for v in values:
        dirs = next(os.walk(path))[1]
        try:
            c = next(d for d in dirs if d.endswith(f'__{v}'))
        except StopIteration:
            # raise Exception(f'Invalid parameter value "{v}"')
            return False
        path = join(path, c)
    print(path)
    return True

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
    with open(".srenv", "w") as file:
            file.write(f"export studyroot={sr_dir}\n")

def to_st_type_string(val):
    type_map={
        "str": "string",
        "float":"float",
            "int":"int"
    }
    return type_map[type(val).__name__]

def is_bulk_location(path):
    return path.startswith(bulk_user)


def get_ghost_folder(folder):
    assert is_bulk_location(folder)
    return folder.replace(bulk_root, user_root)
