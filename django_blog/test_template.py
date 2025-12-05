import os
import sys
import django

# Setup Django
sys.path.append('/Alx_DjangoLearnLab/django_blog')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()

from django.template.loader import get_template

try:
    template = get_template('blog/home.html')
    print("✅ Template 'blog/home.html' found!")
    
    # Test other templates
    templates_to_test = [
        'blog/base.html',
        'blog/register.html',
        'blog/login.html',
        'blog/profile.html',
        'blog/post_list.html',
        'blog/post_detail.html',
        'blog/post_form.html',
        'blog/post_confirm_delete.html',
    ]
    
    for template_name in templates_to_test:
        try:
            get_template(template_name)
            print(f"✅ Template '{template_name}' found!")
        except:
            print(f"❌ Template '{template_name}' NOT found!")
            
except Exception as e:
    print(f"❌ Error: {e}")
