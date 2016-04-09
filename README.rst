==========
dscp 
==========

.. image:: https://secure.travis-ci.org/khosrow/dscp.png
   :target: https://travis-ci.org/#!/khosrow/dscp

------------------------
Distributed secure copy
------------------------

:Author: Khosrow E.
:Manual section: 1
:Date: October 23, 2013

Synopsis
=========

**dscp** [options] file destination

Description
============

**dscp** is a tool for copying a file from one system to many systems simultaneously. It essentially performs a **for a in $(seq 1 10); do scp file $a:destination; done** in bourne shell. 

The tool assumes that dsh groups are setup either in **/etc/dsh/group** or **$HOME/.dsh/group** and that the **scp** command is available. All options are made to closely match those of dsh(1) and scp(1) as much as possible.

Options
========

  -h, --help            Show this help message and exit.
  -v, --verbose         Verbose output. Does not increase verbosity of **scp** .
  -q, --quiet           Make scp output quieter.
  -V, --version         Display version information and quit.
  -M, --show-machine-names
                        Prepends machine names on the standard output.
  -g groupname, --group groupname
                        Add  all  machines found in **/etc/dsh/group/groupname** to the list of machines that the specified file is copied to. 
  -a, --all             Add all machines found in **/etc/dsh/machines.list** to the list of machines that the specified file is copied to.
  -c, --concurrent      Copy files concurrently.
  -i identity_file, --identity-file identity_file
                        Selects the file from which the identity (private key) for public key authentication is read. This option is directly passed to ssh(1).
  -p, --preserve        Preserves modification times, access times, and modes from the original file.
  -r, --recursive       Recursively copy entire directories. Note that **scp** follows symbolic links encountered in the tree traversal.

License
========

This software is released under the MIT license.

See Also
=========
ssh(1), scp(1), dsh(1)