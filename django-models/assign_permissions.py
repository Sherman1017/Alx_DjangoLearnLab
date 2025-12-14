#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book, UserProfile

def assign_permissions():
    print("Assigning permissions to roles...")
    
    # Get the Book content type
    book_content_type = ContentType.objects.get_for_model(Book)
    
    # Get the permissions
    can_add_book = Permission.objects.get(codename='can_add_book', content_type=book_content_type)
    can_change_book = Permission.objects.get(codename='can_change_book', content_type=book_content_type)
    can_delete_book = Permission.objects.get(codename='can_delete_book', content_type=book_content_type)
    
    # Assign permissions to users based on their roles
    users = User.objects.all()
    
    for user in users:
        try:
            profile = user.userprofile
            user.user_permissions.clear()  # Clear existing permissions
            
            if profile.role == 'Admin':
                # Admins get all permissions
                user.user_permissions.add(can_add_book, can_change_book, can_delete_book)
                print(f"✅ {user.username} (Admin) - All book permissions granted")
                
            elif profile.role == 'Librarian':
                # Librarians can add and change books, but not delete
                user.user_permissions.add(can_add_book, can_change_book)
                print(f"✅ {user.username} (Librarian) - Add and Change permissions granted")
                
            elif profile.role == 'Member':
                # Members get no book management permissions
                print(f"✅ {user.username} (Member) - No book management permissions")
                
            user.save()
            
        except UserProfile.DoesNotExist:
            print(f"❌ {user.username} - No profile found")
    
    print("\nPermission assignment complete!")

if __name__ == "__main__":
    assign_permissions()
