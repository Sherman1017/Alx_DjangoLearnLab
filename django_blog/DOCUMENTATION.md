# Django Blog with Comment System

## Overview
This Django blog application features a complete comment system that allows users to:
- Read comments on blog posts
- Post comments (authenticated users only)
- Edit their own comments
- Delete their own comments

## Features Implemented

### 1. Comment Model
- **post**: ForeignKey to Post model (many-to-one relationship)
- **author**: ForeignKey to Django's User model
- **content**: TextField for comment text
- **created_at**: DateTimeField for creation timestamp
- **updated_at**: DateTimeField for last update timestamp

### 2. Comment Forms
- `CommentForm` using Django's ModelForm
- Validation: Comments must be at least 3 characters long
- Bootstrap-styled form widgets

### 3. Comment Views
- **post_detail_with_comments**: Display post with all comments
- **add_comment**: Create new comment (authenticated users only)
- **edit_comment**: Edit existing comment (author only)
- **delete_comment**: Delete comment (author only)

### 4. URL Patterns
- `/posts/<post_id>/` - View post with comments
- `/posts/<post_id>/comments/new/` - Add new comment
- `/comments/<comment_id>/edit/` - Edit comment
- `/comments/<comment_id>/delete/` - Delete comment

### 5. Templates
- `post_detail.html` - Main template showing post and comments
- `add_comment.html` - Form to add new comment
- `edit_comment.html` - Form to edit existing comment
- `delete_comment.html` - Confirmation for deleting comment

## User Permissions

### Unauthenticated Users:
- Can view blog posts
- Can read comments
- Cannot post, edit, or delete comments

### Authenticated Users:
- Can post new comments
- Can edit their own comments
- Can delete their own comments
- Cannot edit or delete other users' comments

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
