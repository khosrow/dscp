#!/bin/sh

set -e
ssh-keygen -q -t rsa -f ~/.ssh/id_rsa -N ''
if [ -f ~/.ssh/id_rsa.pub ]; then
	cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
	ssh-keyscan localhost >> ~/.ssh/known_hosts
	LS=`ls -l ~/.ssh`
	echo $LS
	exit 0
else
	echo "Unable to setup SSH keys to perform tests!"
	exit 1
fi
