#!/bin/bash

echo "=== Final Push to GitHub ==="
echo ""

cd /Alx_DjangoLearnLab

# Check if we have changes to commit
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to commit."
else
    echo "Staging changes..."
    git add .
    
    echo "Committing changes..."
    git commit -m "Update Django blog project with authentication system"
fi

# Check remote
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
if [ -z "$REMOTE_URL" ]; then
    echo "❌ No remote repository configured."
    echo ""
    echo "To configure remote:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/Alx_DjangoLearnLab.git"
    echo "  git branch -M main"
    exit 1
fi

echo "Remote URL: $REMOTE_URL"
echo ""

# Push to GitHub
echo "Pushing to GitHub..."
if [[ $REMOTE_URL == https://* ]]; then
    echo "Using HTTPS. You may be prompted for credentials."
    echo "Username: your GitHub username"
    echo "Password: GitHub Personal Access Token"
    echo ""
fi

git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "Project URL: https://github.com/$(echo $REMOTE_URL | sed 's|https://github.com/||' | sed 's|.git$||')"
    echo "Django blog directory: /django_blog/"
else
    echo ""
    echo "❌ Push failed. Possible reasons:"
    echo "  1. Authentication failed (use PAT instead of password)"
    echo "  2. Network issues"
    echo "  3. Permission denied"
    echo ""
    echo "To use Personal Access Token:"
    echo "  git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/Alx_DjangoLearnLab.git"
    echo "  git push origin main"
fi
