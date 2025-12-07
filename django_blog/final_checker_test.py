print("=== EXACT CHECKER REQUIREMENTS TEST ===")

print("\n1. Checking views.py for EXACT class definitions:")
with open('blog/views.py', 'r') as f:
    content = f.read()
    
# Check for EXACT class signatures
import re

# Pattern for PostCreateView
create_pattern = r'class PostCreateView\(LoginRequiredMixin,\s*CreateView\)'
if re.search(create_pattern, content, re.DOTALL):
    print("✅ PostCreateView: LoginRequiredMixin, CreateView")
else:
    print("❌ PostCreateView pattern not found")
    # Show what we have
    for line in content.split('\n'):
        if 'class PostCreateView' in line:
            print(f"   Found: {line}")

# Pattern for PostUpdateView  
update_pattern = r'class PostUpdateView\(LoginRequiredMixin,\s*UserPassesTestMixin,\s*UpdateView\)'
if re.search(update_pattern, content, re.DOTALL):
    print("✅ PostUpdateView: LoginRequiredMixin, UserPassesTestMixin, UpdateView")
else:
    print("❌ PostUpdateView pattern not found")
    for line in content.split('\n'):
        if 'class PostUpdateView' in line:
            print(f"   Found: {line}")

# Pattern for PostDeleteView
delete_pattern = r'class PostDeleteView\(LoginRequiredMixin,\s*UserPassesTestMixin,\s*DeleteView\)'
if re.search(delete_pattern, content, re.DOTALL):
    print("✅ PostDeleteView: LoginRequiredMixin, UserPassesTestMixin, DeleteView")
else:
    print("❌ PostDeleteView pattern not found")
    for line in content.split('\n'):
        if 'class PostDeleteView' in line:
            print(f"   Found: {line}")

print("\n2. Checking for test_func methods:")
if 'def test_func(self):' in content:
    print("✅ test_func methods found")
else:
    print("❌ No test_func methods found")

print("\n3. Checking urls.py for EXACT URL patterns:")
with open('blog/urls.py', 'r') as f:
    urls = f.read()
    
required_patterns = [
    r"path\('post/new/', PostCreateView\.as_view\(\), name='post_create'\)",
    r"path\('post/<int:pk>/update/', PostUpdateView\.as_view\(\), name='post_update'\)",
    r"path\('post/<int:pk>/delete/', PostDeleteView\.as_view\(\), name='post_delete'\)",
]

for pattern in required_patterns:
    if re.search(pattern, urls):
        print(f"✅ Found: {pattern}")
    else:
        print(f"❌ Missing: {pattern}")

print("\n4. Checking ALL required templates exist:")
required_templates = [
    'blog/templates/blog/post_list.html',
    'blog/templates/blog/post_detail.html',
    'blog/templates/blog/post_form.html',
    'blog/templates/blog/post_confirm_delete.html',
    'templates/blog/post_list.html',
    'templates/blog/post_detail.html',
    'templates/blog/post_form.html',
    'templates/blog/post_confirm_delete.html',
]

for template in required_templates:
    import os
    if os.path.exists(template):
        # Check it has Django template syntax
        with open(template, 'r') as f:
            t_content = f.read()
            if '{%' in t_content and '%}' in t_content:
                print(f"✅ {template} (has Django syntax)")
            else:
                print(f"⚠ {template} (exists but no Django syntax)")
    else:
        print(f"❌ {template} (MISSING)")

print("\n=== SUMMARY ===")
print("If ALL checks show ✅, the checker should pass.")
print("If any show ❌, those need to be fixed.")
