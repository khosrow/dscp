#!/bin/bash
DIR=`dirname $0`

echo "DEBUG:"
LS=`ls -l ~/.dsh/group`
echo "$LS"

echo -n "Running test on 'dscp -g' using $HOME/.dsh/group ... "

# Create test file
echo "test" > /tmp/source.txt

# Create group file
set -e
touch ~/.dsh/group/local
echo "localhost
localhost
localhost" > ~/.dsh/group/local
set +e
python $DIR/../dscp/dscp.py -g local /tmp/source.txt /tmp/dest.txt
diff /tmp/source.txt /tmp/dest.txt
RET=$?

rm ~/.dsh/group/local

if [ $RET -eq 0 ]; then
	echo "PASSED"
	exit 0
else
	echo "FAILED"
	exit 1
fi
