#!/bin/bash

DIR=`dirname $0`

echo -n "Running test on 'dscp -a' ... "

# Create test file
echo "test" > /tmp/source.txt

# Create group file
echo "localhost \
localhost \
localhost" > ~/.dsh/machines.list
python $DIR/../dscp/dscp.py -a /tmp/source.txt /tmp/dest.txt
diff /tmp/source.txt /tmp/dest.txt
RET=$?

rm ~/.dsh/machines.list

if [ $RET -eq 0 ]; then
	echo "PASSED"
	exit 0
else
	echo "FAILED"
	exit 1
fi
