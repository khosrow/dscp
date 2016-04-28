#!/bin/bash

FAIL=0
PASS=0

DIR=`dirname $0`
$DIR/setup.sh || exit 1

mkdir -p ~/.dsh/group

LS=`ls -l ~/.dsh/group`
echo "$LS"

echo "Running test suite"
echo "------------------"

for TEST in `ls $DIR/test-*.sh`
do
	./$TEST
	if [ $? -ne 0 ]; then
		RET=1
		((FAIL++))
	else
		((PASS++))
	fi
done

echo "-----------------"
echo "Summary:"
echo "Tests passed: $PASS"
echo "Tests failed: $FAIL"

exit $RET