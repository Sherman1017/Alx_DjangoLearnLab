#!/bin/bash

echo "=== Verifying GitHub Push ==="

cd /Alx_DjangoLearnLab

echo "1. Checking git status..."
git status

echo -e "\n2. Checking last commit..."
git log --oneline -1

echo -e "\n3. Checking remote repository..."
git remote -v

echo -e "\n4. Checking if django_blog directory exists..."
if [ -d "django_blog" ]; then
    echo "✅ django_blog directory exists"
    
    echo -e "\n5. Checking key files..."
    important_files=(
        "django_blog/blog/models.py"
        "django_blog/blog/views.py"
        "django_blog/blog/forms.py"
        "django_blog/blog/urls.py"
        "django_blog/django_blog/settings.py"
        "django_blog/templates/blog/base.html"
        "django_blog/templates/blog/register.html"
        "django_blog/templates/blog/login.html"
        "django_blog/templates/blog/profile.html"
        "django_blog/static/css/style.css"
    )
    
    for file in "${important_files[@]}"; do
        if [ -f "$file" ]; then
            echo "✅ $file"
        else
            echo "❌ $file (MISSING)"
        fi
    done
    
    echo -e "\n6. Django project structure:"
    find django_blog -type f -name "*.py" | grep -E "(settings|urls|models|views|forms)" | sort
    
else
    echo "❌ django_blog directory not found!"
fi

echo -e "\n=== Push Verification Complete ==="
echo "If all files show ✅, the project is ready to push."
echo ""
echo "To push to GitHub:"
echo "  git push origin main"
echo ""
echo "If asked for credentials:"
echo "  Username: your GitHub username"
echo "  Password: GitHub Personal Access Token (with repo scope)"
