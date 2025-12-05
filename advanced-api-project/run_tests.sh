#!/bin/bash

echo "Running Django REST Framework API Tests..."
echo "=========================================="
echo ""

# Run tests with detailed output using python3
python3 manage.py test api --verbosity=2 --keepdb

# Capture the exit code
TEST_RESULT=$?

echo ""
echo "=========================================="
if [ $TEST_RESULT -eq 0 ]; then
    echo "✅ All tests passed successfully!"
else
    echo "❌ Some tests failed. Please check the output above."
fi

exit $TEST_RESULT
