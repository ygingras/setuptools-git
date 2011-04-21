#!/usr/bin/env python

"""
A hook into setuptools for Git.
"""

from subprocess import CalledProcessError
from subprocess import PIPE

try:
    from subprocess import check_output
except ImportError:
    # BBB for python <2.7
    def check_output(*popenargs, **kwargs):
        from subprocess import Popen
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = Popen(stdout=PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise CalledProcessError(retcode, cmd, output=output)
        return output


def gitlsfiles(dirname=""):
    try:
        output = check_output(['git', 'ls-files', dirname], stderr=PIPE)
    except CalledProcessError:
        # Something went terribly wrong but the setuptools doc says we
        # must be strong in the face of danger.  We shall not run away
        # in panic.
        return []

    return output.splitlines()


if __name__ == "__main__":
    import sys
    from pprint import pprint

    if len(sys.argv) != 2:
        print("USAGE: %s DIRNAME" % sys.argv[0])
        sys.exit(1)

    pprint(gitlsfiles(sys.argv[1]))
