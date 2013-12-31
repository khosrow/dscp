"""
dscp - distributed scure copy.
Copy a file to nodes in a cluster of systems.
"""

from __future__ import print_function
import __init__ as appinfo
import argparse
import sys
import subprocess
import logging
import os


def main():
    try:
        groupdirs = ['/etc/dsh/group', os.path.expanduser('~') + "/.dsh/group"]
    except IOError:
        groupdirs = ['/etc/dsh/group']

    try:
        machinelist = ['/etc/dsh/machines.list', os.path.expanduser('~') + "/.dsh/machines.list"]
    except IOError:
        machinelist = ['/etc/dsh/machines.list']

    parser = argparse.ArgumentParser(description=__doc__, usage="%(prog)s [options] file destination")

    # General options
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("-V", "--version", action="version", version="%(prog)s " + appinfo.__version__ )
    parser.add_argument("-q", "--quiet", help="Make scp output quieter", action="store_true")

    # dsh options
    parser.add_argument("-M", "--show-machine-names", help="Prepend the hostname on output", action="store_true")
    parser.add_argument("-g", "--group", metavar='groupname', help="Copy to group members")
    parser.add_argument("-a", "--all", help="Exectue on all machines", action="store_true")
    parser.add_argument("-c", "--concurrent", help="Copy files concurrently", action="store_true")

    # scp options
    parser.add_argument("-i", "--identity-file", metavar="identity_file", help="File containing the private key")
    parser.add_argument("-p", "--preserve", help="Preserve modification times", action="store_true")
    parser.add_argument("-r", "--recursive", help="Recursively copy entire directories", action="store_true")

    # file arguments
    parser.add_argument("file", nargs='+')
    parser.add_argument("destination")

    args = parser.parse_args()

    logging.basicConfig(format='[%(levelname)s]: %(message)s')
    logger = logging.getLogger('dscp')
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if not args.all and not args.group:
        errormsg = "One of -g or -a is required!"
        logger.error(errormsg)
        sys.exit(1)

    if args.all:
        if os.path.exists(machinelist[0]):
            filename = machinelist[0]
        elif len(machinelist) == 2 and os.path.exists(machinelist[1]):
            filename = machinelist[1]
        else:
            errormsg = "Unable to find %s" % " or ".join(machinelist)
            logger.error(errormsg)
            sys.exit(1)
    elif args.group:
        if os.path.exists(groupdirs[0] + "/" + args.group):
            filename = groupdirs[0] + "/" + args.group
        elif len(groupdirs) == 2 and os.path.exists(groupdirs[1] + "/" + args.group):
            filename = groupdirs[1] + "/" + args.group
        else:
            errormsg = "Unable to find %s in %s" % (args.group, " or ".join(groupdirs))
            logger.error(errormsg)
            sys.exit(1)

    if args.verbose:
        logger.debug("Opening file " + filename)
    try:
        nodes = open(filename)
    except IOError as e:
        logger.error(e)
        sys.exit(1)

    # Child process are kept track with a list
    children = list()

    # Wrap the execution in try/except to catch a ctrl-c
    try:
        for node in nodes:
            remote = node.rstrip()
            r, sep, comment = node.partition('#')
            remote = r.strip()
            if remote == '' or remote is None:
                continue
            
            for f in args.file:
                # prepare the scp commandline
                commands = ['scp']
                if args.quiet:
                    commands.append('-q')
                if args.preserve:
                    commands.append('-p')
                if args.identity_file:
                    commands.append('-i')
                    commands.append(args.identity_file)
                if args.recursive:
                    commands.append('-r')
                commands.append(f)
                commands.append(node.rstrip() + ":" + args.destination)
                logger.debug(" ".join(commands))

                if args.show_machine_names:
                    print("Copying %s -> %s:%s" % (f, remote, args.destination))
                    sys.stdout.flush()

                try:
                    if args.concurrent:
                        # popen will spawn a child process
                        p = subprocess.Popen(commands)
                        children.append(p)
                    else:
                        ret = subprocess.call(commands)
                        if ret:
                            logger.error("%s: scp exited with error!" % remote)
                except subprocess.CalledProcessError as e:
                    logger.error(e.output)
                except OSError as e:
                    logger.error(e)
                except ValueError as e:
                    logger.error(e)

        # now wait for all children to finish
        for p in children:
            p.wait()
    except KeyboardInterrupt:
        # kill any children forcefully then quit
        print("killing all child processes...")
        for p in children:
            p.kill()
        print("leaving abruptly!", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("leaving abruptly!", file=sys.stderr)
        sys.exit(1)
