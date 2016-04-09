#!/bin/bash

echo -n "Running test on 'dscp -a' ... "

# Create test file
echo "test" > /tmp/source.txt

# Create group file
echo "localhost
localhost
localhost" > ~/.dsh/machines.list
python ../dscp/dscp.py /tmp/source.txt local:/tmp/dest.txt
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
