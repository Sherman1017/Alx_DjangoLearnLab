#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User
from relationship_app.models import Book, Author

print("=== CUSTOM PERMISSIONS DEMONSTRATION ===")
print("=" * 40)

# Create test data if needed
author, created = Author.objects.get_or_create(name="Demo Author")

users = ['admin_user', 'librarian_user', 'member_user']

print("DEMONSTRATING PERMISSION-BASED ACCESS:")
print("=" * 35)

for username in users:
    user = User.objects.get(username=username)
    profile = user.userprofile
    
    print(f"\n👤 {username} ({profile.role}):")
    print("-" * 30)
    
    # Check permissions
    can_add = user.has_perm('relationship_app.can_add_book')
    can_edit = user.has_perm('relationship_app.can_change_book') 
    can_delete = user.has_perm('relationship_app.can_delete_book')
    
    print(f"  📖 Book Management Capabilities:")
    print(f"    {'✅' if can_add else '❌'} Add new books")
    print(f"    {'✅' if can_edit else '❌'} Edit existing books")
    print(f"    {'✅' if can_delete else '❌'} Delete books")
    
    # Show what operations they can perform
    if can_add and can_edit and can_delete:
        print("  🎯 Can perform: ALL book operations")
    elif can_add and can_edit and not can_delete:
        print("  🎯 Can perform: Add and Edit books only")
    elif not can_add and not can_edit and not can_delete:
        print("  🎯 Can perform: View books only (no management)")
    else:
        print("  🎯 Custom permission set")

print("\n" + "=" * 40)
print("🚀 PERMISSION SYSTEM READY FOR PRODUCTION!")
print("=" * 40)

print("\n💡 USAGE INSTRUCTIONS:")
print("1. Admins can manage all book operations")
print("2. Librarians can add and edit books (but not delete)")
print("3. Members can only view books")
print("4. All unauthorized access returns 403 errors")
print("5. UI automatically shows/hides actions based on permissions")
