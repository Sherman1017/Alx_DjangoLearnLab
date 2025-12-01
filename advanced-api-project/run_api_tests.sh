#!/bin/bash

echo "========================================="
echo "Running Django REST Framework API Tests"
echo "========================================="
echo ""

echo "🔍 Checking Django setup..."
python3 manage.py check

echo ""
echo "🧪 Running tests..."
echo ""

python3 manage.py test api --verbosity=2

TEST_RESULT=$?

echo ""
echo "========================================="
if [ $TEST_RESULT -eq 0 ]; then
    echo "✅ All tests passed successfully!"
else
    echo "❌ Some tests failed."
fi
echo "========================================="

exit $TEST_RESULT
