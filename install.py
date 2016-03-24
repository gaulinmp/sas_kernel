# -*- coding: utf-8 -*-
import os
import sys

from jupyter_client.kernelspec import install_kernel_spec
from jupyter_core import paths

def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False # assume not an admin on non-Unix platforms

def main(argv=[]):
    here = os.path.realpath(__file__)
    heredir = os.path.dirname(here)
    user = '--user' in argv or not _is_root()
    install_kernel_spec(heredir, 'sas', user=user, replace=True)

    # Because this isn't a package, we have to tell the kernel where kernel.py is
    # The below is a terrible, terrible, shameful hack. But it seems to work.
    # Only tested on linux with anaconda that is.
    for i_path in paths.jupyter_path():
        saskpath = os.path.join(i_path, 'kernels', 'sas', 'kernel.json')
        if os.path.exists(saskpath):
            # Found where it put the sas kernel.
            break
    else:
        print("Couldn't find kernel.json in any paths: ", paths.jupyter_path())
        return
    str_to_replace = 'TODO:FIXASAP/kernel.py'
    with open(saskpath) as fh:
        json_txt = fh.read()
    new_json_txt = json_txt.replace(str_to_replace, saskpath[:-4]+'py')
    with open(saskpath, 'w') as fh:
        fh.write(new_json_txt)
    print("wrote to {}: {}".format(saskpath, new_json_txt))

if __name__ == '__main__':
    main(argv=sys.argv)
