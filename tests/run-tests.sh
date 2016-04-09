#!/bin/bash

FAIL=0
PASS=0

./setup.sh || exit 1

echo "Running test suite"
echo "------------------"

for TEST in `ls test-*.sh`
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