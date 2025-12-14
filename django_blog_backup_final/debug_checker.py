import os
import sys

print("=== Debugging Checker Requirements ===")

# 1. Check ALL templates exist with correct content
print("\n1. Checking ALL template files...")
template_dir = "templates/blog"
required_templates = [
    "post_list.html",      # Listing blog posts
    "post_detail.html",    # Viewing blog posts  
    "post_form.html",      # Creating/editing blog posts
    "post_confirm_delete.html",  # Deleting blog posts
    "base.html",
    "home.html",
    "register.html",
    "login.html",
    "profile.html"
]

for template in required_templates:
    path = os.path.join(template_dir, template)
    if os.path.exists(path):
        print(f"✅ {template} exists")
        # Check if it has content
        with open(path, 'r') as f:
            content = f.read()
            if len(content.strip()) > 100:
                print(f"   Has content: {len(content)} chars")
            else:
                print(f"   ⚠ May be empty or minimal: {len(content)} chars")
    else:
        print(f"❌ {template} MISSING")

# 2. Check views.py for EXACT mixin usage
print("\n2. Checking views.py for EXACT mixin implementation...")
with open('blog/views.py', 'r') as f:
    views_content = f.read()
    lines = views_content.split('\n')

# Look for exact patterns the checker might want
print("\nSearching for specific patterns:")

# Pattern 1: class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView)
update_pattern_found = False
for i, line in enumerate(lines):
    if 'class PostUpdateView' in line and 'LoginRequiredMixin' in line and 'UserPassesTestMixin' in line:
        update_pattern_found = True
        print(f"✅ Line {i+1}: {line.strip()}")
        # Check next few lines for test_func
        for j in range(i+1, min(i+10, len(lines))):
            if 'def test_func' in lines[j]:
                print(f"✅ Found test_func in PostUpdateView")
                break

# Pattern 2: class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView)
delete_pattern_found = False
for i, line in enumerate(lines):
    if 'class PostDeleteView' in line and 'LoginRequiredMixin' in line and 'UserPassesTestMixin' in line:
        delete_pattern_found = True
        print(f"✅ Line {i+1}: {line.strip()}")
        # Check next few lines for test_func
        for j in range(i+1, min(i+10, len(lines))):
            if 'def test_func' in lines[j]:
                print(f"✅ Found test_func in PostDeleteView")
                break

# Pattern 3: class PostCreateView(LoginRequiredMixin, CreateView)
create_pattern_found = False
for i, line in enumerate(lines):
    if 'class PostCreateView' in line and 'LoginRequiredMixin' in line:
        create_pattern_found = True
        print(f"✅ Line {i+1}: {line.strip()}")

if not update_pattern_found:
    print("❌ PostUpdateView doesn't have BOTH LoginRequiredMixin AND UserPassesTestMixin")
if not delete_pattern_found:
    print("❌ PostDeleteView doesn't have BOTH LoginRequiredMixin AND UserPassesTestMixin")
if not create_pattern_found:
    print("❌ PostCreateView doesn't have LoginRequiredMixin")

# 3. Check template content for specific Django template tags
print("\n3. Checking template Django syntax...")
for template in ["post_list.html", "post_detail.html", "post_form.html", "post_confirm_delete.html"]:
    path = os.path.join(template_dir, template)
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read()
            if '{%' in content and '%}' in content:
                print(f"✅ {template} contains Django template tags")
            else:
                print(f"⚠ {template} may not have proper Django template syntax")

print("\n=== Debug Complete ===")
