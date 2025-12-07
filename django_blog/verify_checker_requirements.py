import os
import sys

print("=== Verifying Checker Requirements ===")

# 1. Check URLs in blog/urls.py
print("\n1. Checking URL patterns in blog/urls.py...")
with open('blog/urls.py', 'r') as f:
    urls_content = f.read()

required_urls = [
    'post/new/',
    'post/<int:pk>/update/',
    'post/<int:pk>/delete/'
]

all_urls_found = True
for url in required_urls:
    if url in urls_content:
        print(f"✅ Found URL: {url}")
    else:
        print(f"❌ Missing URL: {url}")
        all_urls_found = False

# 2. Check views.py for mixins
print("\n2. Checking views.py for required mixins...")
with open('blog/views.py', 'r') as f:
    views_content = f.read()

if 'LoginRequiredMixin' in views_content:
    print("✅ LoginRequiredMixin is used")
else:
    print("❌ LoginRequiredMixin is NOT used")

if 'UserPassesTestMixin' in views_content:
    print("✅ UserPassesTestMixin is used")
else:
    print("❌ UserPassesTestMixin is NOT used")

# Check specific view classes
view_classes = ['PostCreateView', 'PostUpdateView', 'PostDeleteView']
for view_class in view_classes:
    if f'class {view_class}' in views_content:
        print(f"✅ {view_class} exists")
    else:
        print(f"❌ {view_class} missing")

# 3. Check templates
print("\n3. Checking required templates...")
required_templates = [
    'templates/blog/post_list.html',
    'templates/blog/post_detail.html',
    'templates/blog/post_form.html',
    'templates/blog/post_confirm_delete.html',
]

all_templates_exist = True
for template in required_templates:
    if os.path.exists(template):
        print(f"✅ Template exists: {template}")
    else:
        print(f"❌ Template missing: {template}")
        all_templates_exist = False

# 4. Check Post model
print("\n4. Checking Post model...")
with open('blog/models.py', 'r') as f:
    models_content = f.read()

if 'class Post' in models_content:
    print("✅ Post model exists")
    
    # Check fields
    required_fields = ['title', 'content', 'published_date', 'author']
    for field in required_fields:
        if field in models_content:
            print(f"✅ Field '{field}' found")
        else:
            print(f"❌ Field '{field}' missing")
else:
    print("❌ Post model not found")

print("\n=== Summary ===")
if all_urls_found and all_templates_exist:
    print("✅ All checker requirements should be met!")
else:
    print("❌ Some requirements are missing.")
    
print("\nRequired fixes:")
print("1. URLs must contain: post/new/, post/<int:pk>/update/, post/<int:pk>/delete/")
print("2. Views must use LoginRequiredMixin and UserPassesTestMixin")
print("3. All templates must exist")
